import Parser
import Datastore
import webapp2

def update_current_semester(): 
    url_builder = Parser.RegistrarUrlBuilder()
    url =  url_builder.get_url_current_semester()  

    parser = Parser.RegistrarParser()
    parser.feedUrl(url)

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

class DatastoreUpdate(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('starting parse')
        
        #Datastore.delete_all()
        #update_current_semester()
        update_all_semesters()
        

        
application = webapp2.WSGIApplication([
    ('/scripts/update', DatastoreUpdate),
], debug=True)
        




