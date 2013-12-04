from collections import Counter


class Course:
    """ A Single Aggregate Course
    
    Feed it registrar courses and it will pull relevent fields, 
        and calculate statistics automatically.
        
    It rejects any Registar Courses which do not have the correct name,
        and it will reject duplicates by looking at the year, semester,
        and section(/recitation/websection) of the input course"""
    
    def __init__(self, name):
        self.name = name
        self.identifier = ""
        self.semesters = list()
        self.semesters_offered = list()
        self.teachers = list()
        self.enrolled = list()
        self.capacity = list()
        self.classrooms = list()
        self.times = list()
        
        self.department = ""
        self.recent_teacher = ""
        self.num_times_offered = 0
        
        self.most_common_teacher = ""
        self.most_recent_teacher = ""
        self.most_common_semester = ""
        
        self.avg_class_sections = list()
        self.avg_enrolled = 0
        self.avg_capacity = 0
        self.avg_fill_ratio = float()
        
        self.offered_online = False
        self.has_lab = False
        self.has_recitation = False
        
    def getTitle(self):
        return self.name
    
    def is_most_recent(self, course_tup):
        pass
    
    def process(self, course):
        if self.name == course.name:
            if (course.year, course.semester, course.class_section) not in self.semesters: 
                #add it to the unquie class identifier list, so we don't ever process duplicates            
                self.semesters.append((course.year, course.semester, course.class_section)) 
                
                if course.online is True:
                    self.offered_online = True
                    
                if course.recitation is True:
                    self.has_recitation= True
                    
                if course.lab is True:
                    self.has_lab= True
                
                #if it's a lab or recitation, we are done, it will just mess up the statistics
                if course.recitation or course.lab:
                    return
                
                if course.course_ident:
                    self.identifier = course.course_ident
                    
                self.semesters_offered.append(course.semester)      
                       
                self.teachers.append(course.instructor_1)
                self.most_recent_teacher = course.instructor_1
                
                
                self.enrolled.append(course.current)
                if course.max < 900:
                    self.capacity.append(course.max)
                #self.classrooms.append(object)
                #self.times.append(object)
                
                self.num_times_offered = len(self.semesters)

                # get the mode of the list of teachers, for most common teacher
                self.most_common_teacher = Counter(self.teachers).most_common(1)[0][0]
                
                # get the mode of the list of teachers, for most common teacher
                self.most_common_semester = Counter(self.semesters_offered).most_common(1)[0][0];
                
                self.department = course.dept
                
#                self.semesters.sort
#                self.
#                    self.recent_teacher
#                
                
                # Calculate average statistics
                self.avg_enrolled = reduce(lambda x, y: x + y, self.enrolled)/len(self.enrolled)
                if len(self.capacity):
                    self.avg_capacity = reduce(lambda x, y: x + y, self.capacity)/len(self.capacity)
                else:
                    self.avg_capacity = 999
                
                if self.avg_capacity != float(0): #don't divide by 0
                    self.avg_fill_ratio = float(float(self.avg_enrolled)/float(self.avg_capacity))
                    
                self.num_times_offered = len(self.semesters)
                
                
                
    def __str__(self):
        info =                                             \
            ("name:",           str(self.name)),           \
            ("identifier:",     str(self.identifier)),     \
            ("semesters:",      str(self.semesters)),      \
            ("common_semester:",str(self.most_common_semester)),   \
            ("times offered:",  str(self.num_times_offered)),   \
            ("department:",     str(self.department)),     \
            ("teachers:",       str(self.teachers)),       \
            ("common_teacher:", str(self.most_common_teacher)),       \
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