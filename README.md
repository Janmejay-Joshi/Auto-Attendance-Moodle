# **Auto-Attendance-Moodle**

  A Simple Script for marking attendance on Moodle automatically

## Prerequisite
* [python 3.6+](https://www.python.org/downloads/)
* [lxml](https://lxml.de/installation.html)
* [beautifullSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* [requests](https://requests.readthedocs.io/en/master/user/install/#install)

## Installation
Clone the project

```git
  git clone https://github.com/Janmejay-Joshi/Auto-Attendance-Moodle.git
```

Go to the project directory

```bash
  cd Auto-Attendance-Moodle
```

Install dependencies

```python3
pip install -r requirements.txt
```

## Usage
```python3
python AutoAtendance.py [ARGUMENTS]...
```

### Script Arguments
```
  -n, --no-persist          : Run only once 
      --remove-credentials  : Remove cached credentials
  -h, --help                : Print this Help section
```


## Disclaimer

I do not condone skipping of classes or using it to unfairly raise attendance.
The Script was just made as a fun little project.

## Known Issues

* Script breaks when server goes down
* Dosen't work Perfectly on termux

### For non-AIR Branch Students:

Edit MetaData.csv and Schedule.csv according to your own Schedule, Class Links and Static Class Passwords
