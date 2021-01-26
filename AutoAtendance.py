
# load Required libraries and method

import AtendanceMethod
import requests
from datetime import datetime,timedelta
from csv import reader
from lxml import html
from bs4 import BeautifulSoup
from os import path

# Check if credentials exists if not create them else load them

if not path.exists("./credentials"):
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


def main():
   
        #Aporach Schedule
        with open('Schedule.csv', encoding = "utf-8") as csvfile:
            spamreader = reader(csvfile)
            now = datetime.now()

            for Schedule in spamreader:
                if Schedule[0] == now.strftime("%A")[:3]: 

                    schedule_time = datetime.strptime(Schedule[1],"%H:%M").replace(year=int(now.strftime("%Y")),month=int(now.strftime("%m")),day=int(now.strftime("%d"))) 
                    if schedule_time < now and schedule_time+ timedelta(hours=1) > now:
                        Lecture = Schedule[2]
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
        session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
        print("Logged in...")

        
        # Mark Atendance

        AtendanceMethod.Attendance(Lecture, session_requests)

if __name__ == '__main__':
    main()
