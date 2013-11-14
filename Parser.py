import string
import urllib2

from Registrar import Course
from ModifiedHTMLParser import HTMLParser
from collections import OrderedDict



class RegistrarUrlBuilder:
    """builds urls to the registrar course listing to feed to the parser"""
    
    def __init__(self):
        self.year_options = ("05", "06", "07", "08", "09", "10", "11", "12", "13")
        self.semester_options = ('A', 'B', 'F', 'S', 'W')
    
        self.root_url = "http://www.stevens.edu/sit/registrar/course-search?schedule-query="
        self.search_year = "&year=20" # + 05, 06, 07, 08, 09, 10, 11, 12, 13
        self.search_semester = "&sessionname="    # + A,B,F,S,W

    def _build_url(self, year, semester):
        return ([self.root_url + self.search_year + year + self.search_semester + semester, year, semester])

    def get_urls_all_semesters(self):
        urls = list()
        for year in self.year_options:
            for semester in self.semester_options:
                urls.append(self._build_url(year, semester))
        return urls
    
    def get_url_current_semester(self):
        return self._build_url("13", 'F')
    
    def get_urls_current_year(self):
        urls = list()
        for semester in self.semester_options:
            urls.append(self._build_url("13", semester))
        return urls
        
#    def get_url_next_semester(self):
#        return self._build_url("14", 'S')

def build_dict(identifier_list, data_list):
    dict = OrderedDict()
    for i in range(0, min(len(data_list),len(identifier_list))):
        dict.update( {str(identifier_list[i]).lower() : data_list[i]} )
    return dict

class RegistrarParser(HTMLParser):
    """ feed() the parser a string
    get_course_list() to receive the resulting course list"""

    def __init__(self):
        self.reset()
        self.year = None
        self.semester = None 
        self.Semester_Courses = list()
        self.identifiers = list()
        self.course_data = list()
        self.tag_depth = 0   
        self.is_parsing_data_identifiers = False

    def feedUrl(self, url):
        webpage = urllib2.urlopen(url)
        self.feed(webpage.read())
        
    def feed_tuple(self, url_tup):
        url, year, semester = url_tup
        self.year = year
        self.semester = semester
        self.feedUrl(url)

    def _strip_formatting(self, s):
        s = string.strip(s, '\n')
        s = string.strip(s, '\t')
        s =  string.strip(s, '\r')
        return s
    
    def handle_starttag(self, tag, attrs):
        
        def check_tag_attrs(attrs, id, value):
            if len(attrs) == 1 and len(attrs[0]) == 2:
                if attrs[0][0] == id and attrs[0][1] == value:
                    return True
            return False
        
        # doesn't detect <tbody> tags
        if tag == "tr" and not self.Semester_Courses:
            self.is_parsing_data_identifiers = True
        if tag == "tr" and check_tag_attrs(attrs, "class", "course"):
            self.is_parsing_data_identifiers = False
            self.tag_depth += 1
            
    #end tags ends data collection and builds the class, adding it to the list
    def handle_endtag(self, tag):
        if tag == "tr" and self.tag_depth > 0:
            self.tag_depth -= 1
            if tag == "tr" and self.tag_depth == 0:
                dict = build_dict(self.identifiers, self.course_data)
                dict.update({"year" : self.year})
                dict.update({"semester" : self.semester})
                
                try:
                    self.Semester_Courses.append(Course(dict))
                except Exception as inst:
                    print "Error:\n"
                    print type(inst)
                    print '\n'
                    print self.course_data
                    
                self.course_data = list()
                
    def handle_data(self, data):
        if self.tag_depth > 0:
            data = self._strip_formatting(data)
            if data:
                self.course_data.append(self._strip_formatting(data))
        if self.is_parsing_data_identifiers:
            data = self._strip_formatting(data)
            if data:
                self.identifiers.append(data)
                
    def get_course_list(self):
        return self.Semester_Courses