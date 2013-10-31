class Aggregate_Course:
    def __init__(self, title):
        self.title = title
        self.years = list()
        self.semesters = list()
        self.teachers = list()
        self.avg_class_sections = list()
        self.enrolled = list()
        self.capacity = list()
        self.classrooms = list()
        self.times = list()
        
        self.avg_enrolled = 0
        self.avg_capacity = 0
        self.avg_fill_percent = 0

        self.previously_processed = list()
        
    def getTitle(self):
        return self.title
    def process(self, course):
        if self.title != course.title:
            return
        if {course.year, course.semester} in self.previously_processed:
            return
        #process
                
        
class AggregateBuilder:
    def __init__(self):
        self.aggregate_courses = dict()
        
        