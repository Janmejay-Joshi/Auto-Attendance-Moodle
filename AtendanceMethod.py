
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
            "OOP": ("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=5809",2), 
            "DS": ("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=6004",2), 
            "DSL": ("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=6195",2), 
            "TL": ("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=6145",2),
            "TLL":("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=6146",2),
            "STL":("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=5962",2),
            "ST":("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=6267",2),
            "DLD":("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=6268",2),
            "PHY":("http://op2020.mitsgwalior.in/mod/attendance/view.php?id=6268",2)
        } 

        return switcher.get(Lecture, 0) 

    def Assign_Attender(self):

        attendance_link = self.Find_Link()
        if attendance_link == None:
            return 

        attendance_type = self.Attendance_Type
        atender = Attender(attendance_link, self.lecture_link, self.session,self.persist)

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

    def __init__(self, Attendance_Link, Lecture_Link, session,persist):

        self.attendance_link = Attendance_Link
        self.lecture_link = Lecture_Link
        self.session = session
        self.persist = persist 

    def direct_link(self):

        attendance_page = self.session.get(self.attendance_link, headers = dict(referer = self.lecture_link), allow_redirects = True)

        print("Attendance Marked... [^_^]")
        if not self.persist:
            exit(0)
        else:
            return


    def present_button(self):

        attendance_page = self.session.get(self.attendance_link, headers = dict(referer = self.lecture_link), allow_redirects = True)
        sesskey = attendance_page.url.split("&")[1].split("=")[1] 
        sessid = attendance_page.url.split("?")[1].split("&")[0].split("=")[1] 
        
        soup = BeautifulSoup(attendance_page.content,'lxml')
        lables = soup.find("div",attrs={"class":"d-flex flex-wrap align-items-center"})
        status = lables.find_all("input")[0]['value']

        


        payload ={
                "sessid":sessid,
                "sesskey":sesskey,
                "sesskey":sesskey,
                "_qf__mod_attendance_form_studentattendance":1,
                "mform_isexpanded_id_session":1,
                "status":status,
                "submitbutton":"Save+changes" 
        }        


        result = self.session.post(self.attendance_link, data=payload, headers = dict(referer = self.attendance_link),allow_redirects=True)
                
        if result.url != attendance_page.url:
            print("Attendance Marked... [^_^]")
            if not self.persist:
                exit(0)
            else:
                return
        else:
            print("Unsuccessful")
        

    def password_button(self):

        attendance_page = self.session.get(self.attendance_link, headers = dict(referer = self.lecture_link), allow_redirects = True)
        sesskey = attendance_page.url.split("&")[1].split("=")[1] 
        sessid = attendance_page.url.split("?")[1].split("&")[0].split("=")[1] 
        
        soup = BeautifulSoup(attendance_page.content,'lxml')
        lables = soup.find("div",attrs={"class":"d-flex flex-wrap align-items-center"})
        status = lables.find_all("input")[0]['value']

        


        payload ={
                "sessid":sessid,
                "sesskey":sesskey,
                "sesskey":sesskey,
                "_qf__mod_attendance_form_studentattendance":1,
                "mform_isexpanded_id_session":1,
                "status":status,
                "submitbutton":"Save+changes" 
        }        


        result = self.session.post(self.attendance_link, data=payload, headers = dict(referer = self.attendance_link),allow_redirects=True)
                
        if result.url != attendance_page.url:
            print("Attendance Marked... [^_^]")
            if not self.persist:
                exit(0)
            else:
                return
        else:
            print("Unsuccessful")
