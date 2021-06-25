# **Auto-Attendance-Moodle**

  A Simple Script for marking attendance on Moodle automatically

## Prerequisite
* [python 3.6+](https://www.python.org/downloads/)
* [lxml](https://lxml.de/installation.html)
* [beautifullSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* [requests](https://requests.readthedocs.io/en/master/user/install/#install)

## Installation
Clone the project

```bash
  git clone https://github.com/Janmejay-Joshi/Auto-Attendance-Moodle.git
```

Go to the project directory

```bash
  cd Auto-Attendance-Moodle
```

Install dependencies

```pip
pip install -r requirements.txt
```

## Usage
```bash
python AutoAtendance.py [ARGUMENTS]...
```

### Script Arguments
```
  -n, --no-persist          : Run only once 
      --remove-credentials  : Remove cached credentials
  -h, --help                : Print this Help section
```

## Known Issues

* Script breaks when server goes down

### For non-AIR Branch Students:

Edit MetaData.csv and Schedule.csv according to your own Schedule, Class Links and Static Class Passwords
