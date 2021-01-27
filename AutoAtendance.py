
# load Required libraries and method

import getopt, sys
import AtendanceMethod
import requests
from datetime import datetime,timedelta
from csv import reader
from lxml import html
from bs4 import BeautifulSoup
from os import path,remove
from time import sleep


def PreProcess():
    
    persist = True

    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]
    
    # Options
    options = "nh"
    
    # Long options
    long_options = ["help", "no-persist", "remove-credentials"]
    
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # checking each argument
        for currentArgument, currentValue in arguments:
    
            if currentArgument in ("-h", "--Help"):
                print ("""
Usage:
    -n, --no-persist            : Run only once
        --remove-credentials    : Remove cached credentials
    -h, --help                  : Print this Help section
                        """)
                exit(0)
                
            elif currentArgument in ("-n", "--no-persist"):
                persist = False
    
            elif currentArgument in ("--remove-credentials"):
                print("Removing credentials...")
                remove("./credentials")
                exit(0)
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

# Check if credentials exists if not create them else load them

    if not path.exists("./credentials"):
        print("Credentials:\n")
        with open("./credentials",'w') as cred_file:
            USERNAME = input("Enter Moodle Username: ")
            PASSWORD = input("Enter Moodle Password: ")
            
            cred_file.write(f"{USERNAME}\n{PASSWORD}")
    else:
        with open("./credentials",'r') as cred_file:
            
            cred = cred_file.readlines()
            USERNAME = cred[0] 
            PASSWORD = cred[1] 

        LOGIN_URL = "http://op2020.mitsgwalior.in/login/index.php" 

    cred0 = [persist,LOGIN_URL,USERNAME,PASSWORD]
    return cred0

def main(cred0):
        
        persist,LOGIN_URL,USERNAME,PASSWORD = cred0 
        print("    Auto-Atendance running...",end = '\r')
        Lecture = None
        #Aporach Schedule
        with open('Schedule.csv', encoding = "utf-8") as csvfile:
            spamreader = reader(csvfile)
            now = datetime.now()

            for Schedule in spamreader:
                if Schedule[0] == now.strftime("%A")[:3]: 

                    schedule_time = datetime.strptime(Schedule[1],"%H:%M").replace(year=int(now.strftime("%Y")),month=int(now.strftime("%m")),day=int(now.strftime("%d"))) 
                    if schedule_time < now and schedule_time+ timedelta(hours=1) > now:
                        Lecture = Schedule[2]

            if not persist and Lecture == None:
                print("\nNo Class Right now [<.>_<.>]\n")
                exit(0)
            elif persist and Lecture == None:
                return 


        print(f"\nLecture now is : {Lecture}")
        print("Loging in...", end = "\r")

        
        # Setup session and cookies
        session_requests = requests.session()

        # Get login csrf token
        result = session_requests.get(LOGIN_URL)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='logintoken']/@value")))[0]

        # Create payload
        payload = {
            "username": USERNAME, 
            "password": PASSWORD, 
            "logintoken": authenticity_token
        }

        # Perform login
        result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

        if result.url == LOGIN_URL:
            print("Invalid Credentials")
            remove("./credentials") 
            exit(0)
        else:
            print("Logged in...")

        
        
        # Mark Atendance

        AtendanceMethod.Attendance(Lecture, session_requests, persist)

if __name__ == '__main__':

    cred = PreProcess()
    now = datetime.now()
    start_time = datetime.strptime("10:00","%H:%M").replace(year=int(now.strftime("%Y")),month=int(now.strftime("%m")),day=int(now.strftime("%d"))) 
    end_time = datetime.strptime("14:00","%H:%M").replace(year=int(now.strftime("%Y")),month=int(now.strftime("%m")),day=int(now.strftime("%d"))) 
    
    while start_time < datetime.now() < end_time:
        main(cred)
        sleep(300)        
