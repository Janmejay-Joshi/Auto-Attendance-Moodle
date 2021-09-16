from pwinput import pwinput
from shutil import copyfile
from lxml import html
import requests


def credentials() -> None:
    """TODO: Docstring for credentials.

    :arg1: None
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
        "logintoken": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))

    if result.url == LOGIN_URL:
        print("Invalid Credentials...")
        exit(0)
    else:
        print("Credentials Verified...")
        with open("./credentials", 'w') as cred_file:
            cred_file.write(f"{USERNAME}\n{PASSWORD}")


def main() -> None:
    """TODO: Docstring for main.
    :returns: TODO

    """
    credentials()


if __name__ == "__main__":
    main()
