from google.appengine.ext import db



class DatastoreCourse(db.Model):

    year = db.StringProperty()
    semester = db.StringProperty()
    call_number = db.IntegerProperty() 
    name = db.StringProperty()
    identifier = db.StringProperty() 
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
    database_course.digest = course.digest().encode('utf-8');

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
        
        
        
class DatastoreAggregate(db.Model):

    name = db.StringProperty()
    identifier = db.StringProperty()
    
    department = db.StringProperty()
    recent_teacher = db.StringProperty()
    num_times_offered = db.IntegerProperty()
    
    most_common_teacher = db.StringProperty()
    most_recent_teacher = db.StringProperty()
    most_common_semester = db.StringProperty()
    
    avg_enrolled = db.IntegerProperty()
    avg_capacity = db.IntegerProperty()
    avg_fill_ratio = db.FloatProperty()
    
    offered_online = db.BooleanProperty()
    has_lab = db.BooleanProperty()
    has_recitation = db.BooleanProperty()

def add_aggregate(aggregate):
    
    aggregate_course = DatastoreAggregate()   

    aggregate_course.name = aggregate.name
    aggregate_course.identifier = aggregate.identifier
    aggregate_course.department = aggregate.department
    aggregate_course.recent_teacher = aggregate.recent_teacher

    aggregate_course.num_times_offered = int(aggregate.num_times_offered)
    aggregate_course.most_common_teacher = aggregate.most_common_teacher
    aggregate_course.most_recent_teacher = aggregate.most_recent_teacher
    aggregate_course.most_common_semester = aggregate.most_common_semester

    aggregate_course.avg_enrolled = int(aggregate.avg_enrolled)
    aggregate_course.avg_capacity = int(aggregate.avg_capacity)
    aggregate_course.avg_fill_ratio= float(aggregate.avg_fill_ratio)

    aggregate_course.offered_online = aggregate.offered_online
    aggregate_course.has_lab = aggregate.has_lab
    aggregate_course.has_recitation = aggregate.has_recitation

    aggregate_course.put()      


def add_aggregates(aggregates):
    for aggregate in aggregates:
        add_aggregate(aggregate)

def update_aggregate(aggregate):
    ds_aggregate = DatastoreAggregate.all()      \
    .filter('name =', aggregate.name).get()
    
    if not ds_aggregate:
        add_aggregate(aggregate)
        
def update_aggregates(aggregates):
    for aggregate in aggregates:
        update_aggregate(aggregate)
 
        
def delete_aggr():
    for aggregate_course in DatastoreAggregate.all():
        aggregate_course.delete()    
 
def delete_courses():
    for database_course in DatastoreCourse.all():
        database_course.delete() 
        
def delete_all():
    delete_courses()
    delete_aggr()
