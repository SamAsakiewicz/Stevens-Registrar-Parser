#!/usr/bin/env python 
import Parser
import Datastore
import Registrar
import Aggregate

################## Parse Courses ####################

def get_current_courses():
    url_builder = Parser.RegistrarUrlBuilder()
    url_tup =  url_builder.get_url_current_semester()  
    
    parser = Parser.RegistrarParser()
    parser.feed_tuple(url_tup)
    
    return parser.get_course_list()

def get_year_courses():
    url_builder = Parser.RegistrarUrlBuilder()
    urls_tup =  url_builder.get_urls_current_year() 
    
    courses = list()
    
    for url_tup in urls_tup:
        parser = Parser.RegistrarParser()
        parser.feed_tuple(url_tup)
        
        for course in parser.get_course_list():
            courses.append(course)
            
    return courses


def get_all_courses():
    url_builder = Parser.RegistrarUrlBuilder()
    urls_tup =  url_builder.get_urls_all_semesters() 
    
    courses = list()
    
    for url_tup in urls_tup:
        parser = Parser.RegistrarParser()
        parser.feed_tuple(url_tup)
        
        for course in parser.get_course_list():
            courses.append(course)
            
    return courses

################## Datastore Scripts ####################

#def update_current_semester(): 
#    courses = get_current_courses()
#    Datastore.update_courses(courses)
#
#def update_current_year(): 
#    courses = get_current_courses()
#    Datastore.update_courses(courses)

def update_current_semester(): 
    url_builder = Parser.RegistrarUrlBuilder()
    url_tup =  url_builder.get_url_current_semester()  

    url, year, semester = url_tup
    parser = Parser.RegistrarParser()
    parser.year = year
    parser.semester = semester
    parser.feedUrl(url)

    courses = parser.get_course_list()
    Datastore.update_courses(courses)
    
    
def update_current_year(): 
    url_builder = Parser.RegistrarUrlBuilder()
    url_tups =  url_builder.get_urls_current_year()

    for url_tup in url_tups:
        parser = Parser.RegistrarParser()
        parser.feed_tuple(url_tup)
    
        courses = parser.get_course_list()
        Datastore.update_courses(courses)

    
def update_all_semesters(): 
    url_builder = Parser.RegistrarUrlBuilder()
    urls_tupple =  url_builder.get_urls_all_semesters()  

    for url, year, semester in urls_tupple:
        parser = Parser.RegistrarParser()
        parser.year = year
        parser.semester = semester
        parser.feedUrl(url)
    
        courses = parser.get_course_list()
        Datastore.update_courses(courses)
        
def update_aggregates(portion):
    
    aggrbuilder = Aggregate.Builder()
    url_builder = Parser.RegistrarUrlBuilder()

    urls_tup =  url_builder.get_urls_all_semesters()
     
    for url_tup in urls_tup:
        parser = Parser.RegistrarParser()
        parser.feed_tuple(url_tup)
        
        for course in parser.get_course_list():
            aggrbuilder.process_course(course)
            
    if portion == 1:
        aggrs = aggrbuilder.get_aggregates()
        aggrs = aggrs[:len(aggrs)/2]
    else:
        aggrs = aggrbuilder.get_aggregates()
        aggrs = aggrs[len(aggrs)/2:]
        
    Datastore.add_aggregates(aggrs)

################## Print Debug Tests ####################

def print_current_semester():
    for course in get_current_courses():
        print str(course)

#def print_aggregates():
#    aggrbuilder = Aggregate.Builder()
#    #courses = get_current_courses()
#    courses = get_all_courses()
#    aggrbuilder.process_courses(courses)
#    
#    aggregates = aggrbuilder.get_aggregates()
#    print str(len(aggregates)) + " of aggregates"
#
##    for aggregate in aggregates:
##        print str(aggregate)      
