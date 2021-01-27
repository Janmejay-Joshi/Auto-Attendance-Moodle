
# Import WebScraping and Form Filling Libraries

from bs4 import BeautifulSoup
import requests
from lxml import html

"""
    Attendance class defing and allocating prerequisits which are required before marking attendance
"""

class Attendance():
    
    def __init__(self, Lecture, Session, persist):

        self.lecture_link, self.Attendance_Type = self.Attendance_Link_Type(Lecture)
        self.session = Session
        self.Lecture = Lecture
        self.persist = persist

        self.Assign_Attender()

    def Find_Link(self):
        result = self.session.get(self.lecture_link, headers = dict(referer = self.lecture_link))
        soup = BeautifulSoup(result.content, 'lxml')
        Table = soup.find('table', attrs = {"class":"generaltable attwidth boxaligncenter"})
        Columns = Table.find_all('tr')
        Submit = None

        for Column in Columns:
            Submit = Column.find('a')
            if Submit != None:
                break

        if(Submit != None):
            Attendance_Mark_link = Submit['href'];
        else:
            print("No Attendance Link Found...")
            if not self.persist:
                exit(0)
            else:
                return None

        return Attendance_Mark_link

    def Attendance_Link_Type(self, Lecture): 
        switcher = { 
            "EEES": ("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=1194",2), 
            "LA": ("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=789",1), 
            "AI": ("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=823",2),
            "ICP":("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=816",2),
            "ICPL":("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=1454",2),
            "BEEE":("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=1088",2),
            "BEEEL":("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=2077",2)
        } 

        return switcher.get(Lecture, 0) 

    def Assign_Attender(self):

        attendance_link = self.Find_Link()
        if attendance_link == None:
            return 

        attendance_type = self.Attendance_Type
        atender = Attender(attendance_link, self.lecture_link, self.session)

        if attendance_type == 1:
            print("Type1: Direct Link")
            atender.direct_link()

        elif attendance_type == 2:
            print("Type2: Present Button")
            atender.present_button()
        else:
            exit(0)

"""
    Attender class marks the actual atendance on basis of which type of Lecture it is
"""

class Attender():

    def __init__(self, Attendance_Link, Lecture_Link, session):

        self.attendance_link = Attendance_Link
        self.lecture_link = Lecture_Link
        self.session = session
    
    def direct_link(self):

        attendance_page = self.session.get(self.attendance_link, headers = dict(referer = self.lecture_link), allow_redirects = True)

        print(attendance_page) 
        if str(attendance_page) == "<Response [200]>":
            print("Attendance Marked... [^_^]")
            if not persist:
                exit(0)
            else:
                return
        else:
            print("Unsuccessful")

# currentlly not working present_button(self)

    def present_button(self):

        attendance_page = self.session.get(self.attendance_link, headers = dict(referer = self.lecture_link), allow_redirects = True)
        print (self.attendance_link)
        print(attendance_page) 
        
        payload = {
                    "status":"625",
                    "submitbutton":"Save changes"
                }

        result = self.session.post(self.attendance_link, data=payload, headers = dict(referer = self.attendance_link),allow_redirects=True)

        print(result.content)
                
        

