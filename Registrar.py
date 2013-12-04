import re
import hashlib



class Course:
    """ A Stevens Registrar Course
    
    Default constructor takes the generic Registrar supplied course information
    
    It will automatically process and create any other relevent statitics
    
    digest() will return an md5 hash of the class, to easily check if the course
        has been updated by the registrar"""
    
    def __init__(self, dict):
        self.dict = dict
        self.year = self.dict.get("year")
        self.semester = self.dict.get("semester")    
        self.call_number = int(self.dict.get("call#"))
        self.identifier = self.dict.get("section")
        self.course_ident = ""
        self.name = self.dict.get("title")
        self.max = int(self.dict.get("max"))
        self.current = int(self.dict.get("curr"))
        self.available = int(self.dict.get("available"))
        self.status = self.dict.get("status")
        self.instructor_1 = self.dict.get("instructor")
        self.instructor_2 = self.dict.get("instructor2")
        self.dept = None
        self.class_section = None
        self.online = False
        self.lab = False
        self.recitation = False
        self.process_section()
        
    def process_section(self):
        s = re.findall("[A-Za-z]+", self.identifier)
        self.course_ident = re.findall("[A-Za-z]+\s[0-9]+", self.identifier)[0]

        if len(s) >= 1:
            self.dept = s[0]
            
        if len(s) == 2:
            self.class_section = s[1]
            if len(s[1]) == 2:
                if s[1] == "WS":
                    self.online = True
                if s[1][0] == "R":
                    self.recitation = True
                if s[1][0] == "L":
                    self.lab = True
                    
    def get_dict(self):
        return self.dict
    
    def digest(self):
        m = hashlib.md5()
        m.update(str(self.year))
        m.update(str(self.semester))
        m.update(str(self.call_number))
        m.update(str(self.name))
        m.update(str(self.identifier))
        m.update(str(self.max))
        m.update(str(self.current))
        m.update(str(self.available))
        m.update(str(self.status))
        m.update(str(self.instructor_1))
        m.update(str(self.instructor_2))
        return m.hexdigest()
    
    def __str__(self):
        return str(self.dict)