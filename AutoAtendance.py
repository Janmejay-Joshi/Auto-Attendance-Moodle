# load Required libraries and method

import getopt, sys
import AtendanceMethod
import requests
from datetime import datetime,timedelta
from csv import reader
from lxml import html
from os import path,remove
from time import sleep
from shutil import copyfile


def PreProcess():

    """
    Initalizes login variables and checks for command line arguments

    Parameters: None

    Returns:
    cred0 : Array =

    [
        persist   : boolean
        LOGIN_URL : String
        USERNAME  : String
        PASSWORD  : String
    ]

    """

    persist = True
    argumentList = sys.argv[1:]

    options = "nh"

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
        print (str(err))

    # Check if credentials exists if not create them else load them

    if not path.exists("./credentials"):
        print("Credentials:\n")
        with open("./credentials",'w') as cred_file:
            USERNAME = input("Enter Moodle Username: ")
            PASSWORD = input("Enter Moodle Password: ")

            cred_file.write(f"{USERNAME}\n{PASSWORD}")
            BranchBool = input("Do you belong to AIR Branch [Y/N]: ")
            if BranchBool == 'y' or BranchBool == 'Y':
                GROUP = input("Enter Group for AIR branch [A/B]: ")
                if GROUP == 'a' or GROUP == 'A':
                    copyfile('./Schedule_A.csv','./Schedule.csv')
                elif GROUP == 'b' or GROUP == 'B':
                    copyfile('./Schedule_B.csv','./Schedule.csv')
                else:
                    print("\nEnter a valid Group" )
                    sys.exit(1)
            else:
                print("\nRewrite Schedule.csv and Metadata.csv according to your Schedule To make the Script work")
                exit(0)
    else:
        with open("./credentials",'r') as cred_file:

            cred = cred_file.readlines()
            USERNAME = cred[0]
            PASSWORD = cred[1]

    LOGIN_URL = "http://op2020.mitsgwalior.in/login/index.php"

    cred0 = [persist,LOGIN_URL,USERNAME,PASSWORD]
    return cred0

def main(cred0):
    """
    Logins to Moodle and Checks for Active Class then calls AttendanceMethod

    Parameters:
    cred0 : Array =

    [
        persist   : boolean
        LOGIN_URL : String
        USERNAME  : String
        PASSWORD  : String
    ]

    Returns: None

    """

    persist,LOGIN_URL,USERNAME,PASSWORD = cred0
    print("    Auto-Atendance running...",end = '\r')
    Lecture = None
    #Aporach Schedule
    with open('Schedule.csv', encoding = "utf-8") as csvfile:
        spamreader = reader(csvfile)
        now = datetime.now()
        Skip = True

        for Schedule in spamreader:
            if Skip:
                Skip = False
            else:
                if Schedule[0] == now.strftime("%A")[:3]:
                    schedule_time = datetime.strptime(Schedule[1],"%H:%M").replace(year=int(now.strftime("%Y")),month=int(now.strftime("%m")),day=int(now.strftime("%d")))
                    if schedule_time < now and schedule_time + timedelta(hours=1) > now:
                        Lecture = Schedule[2]

        if Lecture == None:
            if persist:
                return
            else:
                print("\nNo Class Right now [<.>_<.>]\n")
                exit(0)


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

    """
    Initalizes Credentials and then
    Checks if its time for classes then calls main function
    """

    cred = PreProcess()
    now = datetime.now()
   # start_time = datetime.strptime("10:00","%H:%M").replace(year=int(now.strftime("%Y")),month=int(now.strftime("%m")),day=int(now.strftime("%d"))) 
   # end_time = datetime.strptime("19:00","%H:%M").replace(year=int(now.strftime("%Y")),month=int(now.strftime("%m")),day=int(now.strftime("%d"))) 

   # while datetime.now() < end_time:
    while (1):
        main(cred)
        sleep(300)

