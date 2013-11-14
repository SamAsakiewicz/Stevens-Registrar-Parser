


class Course:
    """ A Single Aggregate Course
    
    Feed it registrar courses and it will pull relevent fields, 
        and calculate statistics automatically.
        
    It rejects any Registar Courses which do not have the correct name,
        and it will reject duplicates by looking at the year, semester,
        and section(/recitation/websection) of the input course"""
    
    def __init__(self, name):
        self.name = name
        self.semesters = list()
        self.teachers = list()
        self.enrolled = list()
        self.capacity = list()
        self.classrooms = list()
        self.times = list()
        
        self.avg_class_sections = list()
        self.avg_enrolled = 0
        self.avg_capacity = 0
        self.avg_fill_ratio = 0
        
        self.offered_online = False
        self.has_lab = False
        self.has_recitation = False
        
    def getTitle(self):
        return self.name
    
    def process(self, course):
        if self.name == course.name:
            if (course.year, course.semester, course.class_section) not in self.semesters:             
                self.semesters.append((course.year, course.semester, course.class_section))                
                self.teachers.append(course.instructor_1)
                self.enrolled.append(course.current)
                self.capacity.append(course.max)
                #self.classrooms.append(object)
                #self.times.append(object)
                
                # Calculate average statistics
                self.avg_enrolled = reduce(lambda x, y: x + y, self.enrolled)/len(self.enrolled)
                self.avg_capacity = reduce(lambda x, y: x + y, self.capacity)/len(self.capacity)
                
                if self.avg_capacity != 0: #don't divide by 0
                    self.avg_fill_ratio = float(self.avg_enrolled/self.avg_capacity)
                    
                if course.online is True:
                    self.offered_online = True
                    
                if course.recitation is True:
                    self.has_recitation= True
                    
                if course.lab is True:
                    self.has_lab= True
        
    def __str__(self):
        info =                                             \
            ("name:",           str(self.name)),           \
            ("semesters:",      str(self.semesters)),      \
            ("teachers:",       str(self.teachers)),       \
            ("enrolled:",       str(self.enrolled)),       \
            ("capacity:",       str(self.capacity)),       \
            ("classrooms:",     str(self.classrooms)),     \
            ("times:",          str(self.times)),          \
            ("teachers:",       str(self.teachers)),       \
            ("avg enrolled:",   str(self.avg_enrolled)),   \
            ("avg capacity:",   str(self.avg_capacity)),   \
            ("avg fill ratio:", str(self.avg_fill_ratio)), \
            ("has_recitation:", str(self.has_recitation)), \
            ("has_lab:",        str(self.has_lab)),        \
            ("offered_online:", str(self.offered_online))  

        s=str()
        for i in range(0,len(info)):
            s+='{0:<20}{1}'.format(info[i][0], info[i][1]) + '\n'
        return s
            
            
class Builder:
    """ Aggregate Course Builder
    
    Default constructer will initialize the dictionary/hashmap it uses
         to store the Aggregates it builds. The course name is the 
         unique idetifier/key.
    
    Call process_courses  to process a list of registrar courses. it will
        make a new aggregate class for every new course name, otherwise it
        will just have the aggregate of the corresponding name process the course"""
        
    def __init__(self):
        self.aggregates = dict()

    def process_course(self, course):
        #if if there is no aggregate for the course create one, then have the aggregate process the course
        if course.name not in self.aggregates:
            self.aggregates[course.name] = Course(course.name)           
        (self.aggregates.get(course.name)).process(course)
            
    def process_courses(self, courses):
        for course in courses:
            self.process_course(course) 
            
    def get_aggregates(self):
        return  list(self.aggregates.values())