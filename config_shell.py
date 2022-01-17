from os import listdir
from sys import exit
from pwinput import pwinput
from shutil import copyfile
from configparser import ConfigParser
from lxml import html
import requests

Config = ConfigParser()


def set_credentials() -> None:
    """
    Gets User Input for credentials and Verifies the credentials

    :returns: None

    """

    LOGIN_URL = "http://op2020.mitsgwalior.in/login/index.php"

    print("Credentials:\n")
    USERNAME = input("Enter Moodle Username: ")
    PASSWORD = pwinput(prompt="Enter Moodle Password: ")

    print("\nVerifing Credentials...", end="\r")

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
        print("Invalid Credentials...")
        exit(0)
    else:
        print("Credentials Verified...")

        Config.add_section("credentials")
        Config.set("credentials", "username", USERNAME)
        Config.set("credentials", "password", PASSWORD)

        with open("./config.ini", "w") as cfgfile:
            Config.write(cfgfile)


def set_metadata() -> None:
    """
    Set Metadata.csv and Schedule.csv Files

    :returns: None

    """
    print("\nMetadata Configuration : \n")

    i = 0
    branches = {0: "NA"}

    for branch in listdir("./metadata"):
        i += 1
        print(f"[{i}] {branch}")
        branches[i] = branch

    print("[0] None")

    BRANCH = branches[int(input("\nEnter Branch Index : "))]
    print()

    if BRANCH == "NA":
        print("Write MetaData.csv and Schedule.csv according to your Lecture Schedule ")
        exit(1)

    i = 0
    groups = {0: "NA"}

    if len(listdir(f"./metadata/{BRANCH}")) > 2:
        for group in listdir(f"./metadata/{BRANCH}"):
            if group[0] != "S":
                i += 1
                print(f"[{i}] {group[-5]}")
                groups[i] = group[-5]

        print("[0] None")
        GROUP = groups[int(input("\nEnter Branch Index : "))]

    GROUP = groups[0]

    Config.add_section("metadata")
    Config.set("metadata", "branch", BRANCH)
    Config.set("metadata", "group", GROUP)

    if GROUP != "NA":
        copyfile(
            f"./metadata/{BRANCH}/MetaData_{BRANCH}_{GROUP}.csv",
            "./metadata/MetaData.csv",
        )

        copyfile(
            f"./metadata/{BRANCH}/Schedule_{BRANCH}_{GROUP}.csv",
            "./metadata/Schedule.csv",
        )

    else:
        copyfile(
            f"./metadata/{BRANCH}/MetaData_{BRANCH}.csv", "./metadata/MetaData.csv"
        )

        copyfile(
            f"./metadata/{BRANCH}/Schedule_{BRANCH}.csv", "./metadata/Schedule.csv"
        )

    with open("./config.ini", "w") as cfgfile:
        Config.write(cfgfile)


def configure() -> None:
    """
    Starts Configuration Wizard
    :returns: None

    """
    set_credentials()
    set_metadata()


if __name__ == "__main__":
    configure()
