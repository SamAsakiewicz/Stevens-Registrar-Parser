from google.appengine.ext import db



class DatastoreCourse(db.Model):

    year = db.StringProperty()
    semester = db.StringProperty()
    call_number = db.IntegerProperty() 
    name = db.StringProperty()
    identifier = db.StringProperty() 
#    department = db.StringProperty()
#    section = db.StringProperty()
    max = db.IntegerProperty() 
    current = db.IntegerProperty() 
    available = db.IntegerProperty() 
    status = db.StringProperty()
    instructor_1 = db.StringProperty()
    instructor_2 = db.StringProperty()

    dept = db.StringProperty()
    class_section = db.StringProperty()
    online = db.BooleanProperty()
    digest = db.StringProperty()
    
def delete_all():
    for database_course in DatastoreCourse.all():
        database_course.delete()

def add_course(course):
    database_course = DatastoreCourse(
                                      )   
    database_course.year = course.year
    database_course.semester = course.semester                                                                                
    database_course.call_number = course.call_number
    database_course.name = course.name
    database_course.identifier = course.identifier
    database_course.max = course.max
    database_course.current = course.current
    database_course.available = course.available
    database_course.status = course.status
    database_course.instructor_1 = course.instructor_1
    database_course.instructor_2 = course.instructor_2
    database_course.dept = course.dept
    database_course.class_section = course.class_section
    database_course.online = course.online
    database_course.digest = course.digest();

    database_course.put()      

def add_courses(courses):
    for course in courses:
        add_course(course)
        
def process_changes(ds_course, rs_course):
    pass

def update_course(rs_course):
    ds_course = DatastoreCourse.all()\
    .filter('name =', rs_course.name)\
    .filter('year =', rs_course.year)\
    .filter('semester =', rs_course.semester).get()
    
    if not ds_course:
        add_course(rs_course)

    elif rs_course.digest() != ds_course.digest:
        process_changes(ds_course, rs_course)
        
def update_courses(rs_courses):
    for rs_course in rs_courses:
        update_course(rs_course)