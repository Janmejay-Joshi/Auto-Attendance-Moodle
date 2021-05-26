# **Auto-Attendance-Moodle**

  A Simple Script for marking attendance on Moodle automatically

## Prerequisite
* [python 3.6+](https://www.python.org/downloads/)
* [lxml](https://lxml.de/installation.html)
* [beautifullSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* [requests](https://requests.readthedocs.io/en/master/user/install/#install)

## Installation
git clone the repository and in the root folder run to install dependencies
```
pip install -r requirements.txt
```

## Usage
Run AutoAtendance.py in a python environment.

### Script Arguments
```
  -n, --no-persist          : Run only once 
      --remove-credentials  : Remove cached credentials
  -h, --help                : Print this Help section
```
## Known Issues

* Script breaks when server goes down
