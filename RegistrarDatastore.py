from google.appengine.ext import db
from RegistrarParser import RegistrarCourse, RegistrarParser
from locale import currency

class DatastoreCourse(db.Model):
    call_number = db.IntegerProperty() 
    section = db.StringProperty()
    title = db.StringProperty() 
#    department = db.StringProperty()
#    section = db.StringProperty()
    max = db.IntegerProperty() 
    current = db.IntegerProperty() 
    available = db.IntegerProperty() 
    status = db.StringProperty()
    instructor_1 = db.StringProperty()
    instructor_2 = db.stringProperty()
#    days = db.StringProperty()
#    time = db.Time
#    location = db.StringProperty()
#    
#    statistics_started = db.DateTimeProperty()
#    statistics_last_modified = db.DateTimeProperty()
    
    def __eq__(self, other):
        if isinstance(other, RegistrarCourse):
            dict  = other.get_dict()
            
            DatastoreCourse.call_number = int(dict.get("Call#"))
            DatastoreCourse.section = dict.get("Section")
            DatastoreCourse.title = dict.get("Title")
            DatastoreCourse.max = int(dict.get("Max"))
            DatastoreCourse.current = int(dict.get("Curr"))
            DatastoreCourse.availabe = int(dict.get("Available"))
            DatastoreCourse.status = dict.get("Status")
            DatastoreCourse.instructor_1 = dict.get("Instructor")
            return self
        return NotImplemented

    def from_parsed_course(self, other):
        if isinstance(other, RegistrarCourse):
            dict  = other.get_dict()
            
            DatastoreCourse.call_number = int(dict.get("Call#"))
            DatastoreCourse.section = dict.get("Section")
            DatastoreCourse.title = dict.get("Title")
            DatastoreCourse.max = int(dict.get("Max"))
            DatastoreCourse.current = int(dict.get("Curr"))
            DatastoreCourse.availabe = int(dict.get("Available"))
            DatastoreCourse.status = dict.get("Status")
            DatastoreCourse.instructor_1 = dict.get("Instructor")
            return self
        return NotImplemented