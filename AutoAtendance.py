# load Required libraries and method

from configparser import ConfigParser
from getopt import getopt, error
from sys import argv
import AtendanceMethod
from config_shell import configure
import requests
from requests import RequestException
from datetime import datetime, timedelta
from csv import reader
from lxml import html
from os import path
from time import sleep


def PreProcess() -> list:

    """
    Initalizes login variables and checks for command line arguments

    :returns:
    cred0 : Array =

    [
        persist   : boolean
        LOGIN_URL : String
        USERNAME  : String
        PASSWORD  : String
    ]

    """

    persist = True
    argumentList = argv[1:]

    options = "nh"

    long_options = ["help", "no-persist", "configure"]

    try:
        # Parsing argument
        arguments, values = getopt(argumentList, options, long_options)

        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--Help"):
                print(
                    """
Usage:
    -n, --no-persist         : Run only once
        --configure          : Start configuration wizard
    -h, --help               : Print this Help section
                        """
                )
                exit(0)

            elif currentArgument in ("-n", "--no-persist"):
                persist = False

            elif currentArgument in ("--configure"):
                print("Removing config...")
                configure()
                exit(0)
    except error as err:
        print(str(err))

    # Check if credentials exists if not create them else load them

    if not path.exists("./config.ini"):
        configure()

    Config = ConfigParser()
    Config.read("./config.ini")

    USERNAME = Config["credentials"]["username"]
    PASSWORD = Config["credentials"]["password"]

    LOGIN_URL = "http://op2020.mitsgwalior.in/login/index.php"

    cred0 = [persist, LOGIN_URL, USERNAME, PASSWORD]
    return cred0


def main(cred0: list) -> None:
    """
    Logins to Moodle and Checks for Active Class then calls AttendanceMethod

    "arg0 : Array =

    [
        persist   : boolean
        LOGIN_URL : String
        USERNAME  : String
        PASSWORD  : String
    ]

    :returns: None

    """

    persist, LOGIN_URL, USERNAME, PASSWORD = cred0
    print("Auto-Atendance running...", end="\r")
    Lecture = None

    # Getting the CSV Schedule

    with open("./metadata/Schedule.csv", encoding="utf-8") as csvfile:
        spamreader = reader(csvfile)
        now = datetime.now()

        # Getting the Current Lecture by comparing current Time

        for Schedule in spamreader:
            if Schedule[0] == now.strftime("%A")[:3]:
                schedule_time = datetime.strptime(Schedule[1], "%H:%M").replace(
                    year=int(now.strftime("%Y")),
                    month=int(now.strftime("%m")),
                    day=int(now.strftime("%d")),
                )
                if schedule_time < now and schedule_time + timedelta(hours=1) > now:
                    Lecture = Schedule[2]

        if Lecture is None:
            if persist:
                return
            else:
                print("\nNo Class Right now [<.>_<.>]\n")
                exit(0)

    print(f"\nLecture now is : {Lecture}")
    print("Loging in...", end="\r")

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
        "logintoken": authenticity_token,
    }

    # Perform login
    result = session_requests.post(
        LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL)
    )

    if result.url == LOGIN_URL:
        print("Invalid Credentials")
        configure()
        exit(1)
    else:
        print("Logged in...")

    # Mark Atendance

    AtendanceMethod.Attendance(Lecture, session_requests, persist)


if __name__ == "__main__":

    """
    Initalizes Credentials and then
    Checks if its time for classes then calls main function
    """

    cred = PreProcess()
    now = datetime.now()

    # Uncoment Lines Below to Enable Time Limit For Auto-Attendance

    #    start_time = datetime.strptime("10:00", "%H:%M").replace(
    #        year=int(now.strftime("%Y")),
    #        month=int(now.strftime("%m")),
    #        day=int(now.strftime("%d")),
    #    )

    #    end_time = datetime.strptime("19:00", "%H:%M").replace(
    #        year=int(now.strftime("%Y")),
    #        month=int(now.strftime("%m")),
    #        day=int(now.strftime("%d")),
    #    )

    #    while datetime.now() < end_time:

    while 1:
        try:
            main(cred)
        except RequestException:
            print("\n\nNetwork / Server Error ! ( Retrying in 5 min )")
        except FileNotFoundError:
            print("\n\nMissing Schedule.csv \n Running Configuration Wizard.")
            configure()
        except Exception as e:
            print(e)
            print(
                """
        Tis is New :
            Report it as an issue on Github if you feel this is a reouccouring error
                """
            )

        sleep(300)
