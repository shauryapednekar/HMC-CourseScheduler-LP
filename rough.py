import json
import numpy as np
import pandas as pd
import time
import re
import time
from rough_data import all_prev_courses
import csv

"""
SKELETAL:

1. Get all courses offered next sem.

2. Remove courses taken previously.

3. Remove courses that I cannot take due to prereqs. 

4. (TODO - easy) Possibly add next sem courses that I have already permed into that arent already in courses.

5. (TODO - easy) Possibly remove next sem courses that I absolutely do not want to take/won't get in to.
    (TODO - easy) Possibly factor in preplacement here.

--- Have all the courses that I am willing and able to take. 

6. Make a dictionary of of course name to variable name (and its index in "all_courses" string).
    - "all_courses" contains "next_sem_possible_courses" + "all_prev_courses" + "prereq_courses" (all unique)
    
--- By this time, we will have:
    - "data" [dict]
    - "next_sem_possible_courses" [list]
    - "course_to_variable_name" [dict]
    - "course_to_number" [dict]

--- Constraints ---

7. Complete min enrollment constraint matrix:
    Ax >= 4 ;   A is just one row with all 1s

8. Complete max enrollment constraint matrix:
    Ax <= 6;    A is just one row with all 1s

9. Complete time conflict constraint matrix.
    Ax <= 1;     each row of A represents a discrete point in time

10. Complete no two same courses constraint matrix:
    Ax <= 1;     each row of A has a 1 for variables that are the same course (but different sections)

11. Complete electives constraint matrix. 

"""

#########################
# 1. GET ALL COURSES OFFERED NEXT SEM

with open("course_data.json", encoding="utf-8") as f:
    data = json.load(f)


def next_sem_possible_courses(data=data):
    """
    List of all courses with their complete course code
    """
    return list(data['data']["courses"].keys())


next_sem_possible_courses = next_sem_possible_courses()

######################
# 2.5 Only Keep 3 credit courses

def only_keep_full_classes(data=data, next_sem_possible_courses=next_sem_possible_courses):
    possible=[]
    
    for course in next_sem_possible_courses:
        if data['data']["courses"][course]["courseCredits"] == "3.0":
            possible.append(course)
        # else:
            # print(course)
    
    return possible

next_sem_possible_courses = only_keep_full_classes()

#######################
# 2. REMOVE PREVIOUSLY TAKEN COURSES

# print(all_prev_courses)
def remove_prev_courses(all_prev_courses=all_prev_courses, next_sem_possible_courses=next_sem_possible_courses):
    repeated = []
    output = []
    for course in next_sem_possible_courses:
        for prev_course in all_prev_courses:
            if prev_course in course:
                repeated.append(course)
                # next_sem_possible_courses.remove(course)
    
    # print(repeated)
    for course in next_sem_possible_courses:
        if course not in repeated:
            output.append(course)         
    # for prev_course in all_prev_courses:
    #     for course in next_sem_possible_courses:
    #         if prev_course in course:
    #             # print(course)
    #             next_sem_possible_courses.remove(course)
                
    return output

next_sem_possible_courses = remove_prev_courses()

for course in next_sem_possible_courses:
    if  "MATH 055" in course:
        print(course)



    
######################
# 3. REMOVE COURSES I CANNOT TAKE DUE TO PREREQS


def subject_codes(next_sem_possible_courses=next_sem_possible_courses):
    subject_codes = set()
    for course in next_sem_possible_courses:
        currCode = re.search(r"[^\s]+", course)
        if currCode:
            currCode = currCode.group(0)
            if currCode not in subject_codes:
                subject_codes.add(currCode)

    return subject_codes


subject_codes = subject_codes()
# print(subject_codes)

# Prereqs Function that only needs to be run once:
    # def prereqs(next_sem_possible_courses=next_sem_possible_courses, data=data, subject_codes=subject_codes):
    #     """
    #     Function to get the prereqs for each course
    #     """
    #     course_to_prereqs = {}
    #     for course in next_sem_possible_courses:
    #         description = data['data']["courses"][course]['courseDescription']
    #         if not description:
    #             prereqs = ""
    #         elif 'Prerequisite: ' not in description:
    #             prereqs = ""
    #         else:
    #             prereqs = description.partition('Prerequisite: ')[2]
    #             replacement_dict = {
    #                 "Arabic": "ARBC",
    #                 "Mathematics": "MATH",
    #                 "Math": "MATH",
    #                 "Korean": "KORE",
    #                 "Writing 1": "WRIT 001",
    #                 "Anthropology": "ANTH",
    #                 "Art": "ART",
    #                 "Physics": "PHYS",
    #                 "Biology": "BIOL",
    #                 "Chemistry": "CHEM",
    #                 "Computer Science": "CSCI",
    #                 "Economics": "ECON",
    #                 "Engineering": "ENGR",
    #                 "French": "FREN",
    #                 "Government": "GOVT",
    #                 "Psychology": "PSYC",
    #                 "Spanish": "SPAN"
    #             }

    #             for key in replacement_dict:
    #                 prereqs = prereqs.replace(key, replacement_dict[key])

    #             lis = []
    #             for course_code in subject_codes:
    #                 currCode = course_code + "\s?[0-9]*"

    #                 if re.findall(currCode, prereqs):
    #                     lis += re.findall(currCode, prereqs)

    #             newLis = []
    #             for l in lis:
    #                 check = True
    #                 for course_code in subject_codes:
    #                     if re.match(course_code + '\s[0-9]{3}', l):
    #                         pass
                        
    #                     elif re.match(course_code + '[0-9]{3}', l):
    #                         # print(l)
    #                         n = len(course_code)
    #                         l = l[0:n] + " " + l[n:]
    #                         # print(l)
    #                         check = False
    #                         newLis.append(l)
    #                     elif re.match(course_code + '[0-9]{2}', l):
    #                         n = len(course_code)
    #                         l = l[0:n] + " 0" + l[n:]
    #                         check = False
    #                         newLis.append(l)
    #                     elif re.match(course_code + '[0-9]{1}', l):
    #                         n = len(course_code)
    #                         l = l[0:n] + " 00" + l[n:]
    #                         check = False
    #                         newLis.append(l)

    #                     elif re.match(course_code + '\s[0-9]{2}', l):
    #                         n = len(course_code)+1
    #                         l = l[0:n] + "0" + l[n:]
    #                         check = False
    #                         newLis.append(l)

    #                     elif re.match(course_code + '\s[0-9]{1}', l):
    #                         n = len(course_code)+1
    #                         l = l[0:n] + "00" + l[n:]
    #                         check = False
    #                         newLis.append(l)

    #                 if check:
    #                     newLis.append(l)

    #             if "permission of the instructor" in prereqs or "permission of instructor" in prereqs:
    #                 # Contains only courses that have prereqs
    #                 course_to_prereqs[course] = [[prereqs], newLis, ["POI"]]
    #             else:
    #                 # Contains only courses that have prereqs
    #                 course_to_prereqs[course] = [[prereqs], newLis]

    #     return course_to_prereqs


    # course_to_prereqs = prereqs()

    # with open('prereqs.json', 'w') as fp:
    #     json.dump(prereqs(), fp, indent=4)

with open("prereqs_edited_by_hand.json", encoding="utf-8") as f:
    prereqs_edited = json.load(f)


def helper_next_sem_possible_courses_due_to_prereqs(lis, all_prev_courses=all_prev_courses):

    for elem in lis:
        if elem not in all_prev_courses:
            return False

    return True


def next_sem_possible_courses_due_to_prereqs(next_sem_possible_courses=next_sem_possible_courses, all_prev_courses=all_prev_courses, prereqs_edited=prereqs_edited):
    """
    Returns list of possible courses according to previously taken courses and prerequisites 
    (includes previously taken courses too)
    """
    possible_courses = []
    for course in next_sem_possible_courses:
        if course in prereqs_edited:
            currPrereqs = prereqs_edited[course][1:]
            if ["POI"] in currPrereqs:
                currPrereqs.remove(["POI"])
            temp = [helper_next_sem_possible_courses_due_to_prereqs(
                prereq, all_prev_courses) for prereq in currPrereqs]
            if True in temp:
                possible_courses.append(course)
            # else:
                # print(course)

        else:
            possible_courses.append(course)
    return possible_courses


next_sem_possible_courses = next_sem_possible_courses_due_to_prereqs()

######################
# 4. POSSIBLY ADD NEXT SEM COURSES I HAVE GOT POI

# -TODO:


def addPOIcourses():
    pass

#####################
# 5. POSSIBLY REMOVE COURSES I ABSOLUTELY DO NOT WANT TO TAKE

# -TODO:


def removeBadCourses():
    pass

######################
# 6. DICTIONARY OF COURSE_NAME TO VAR_NAME AND INDEX


def course_code_to_variable_and_index(next_sem_possible_courses=next_sem_possible_courses):
    """
    Dictionary that maps complete course code to a variable of the format "xi" where "i" is the variable number

    Takes in the list of all courses and returns two dictionaries:

        - course_to_variable_name: dict that maps complete course code to a variable of the format "xi" where "i" is the variable number
        - course_to_number: dict that maps complete_course_code to int i, where i equals corresponding variable name in course_to_variable_name

    Input: courses - List
    Output: (course_to_variable_name,courseToNumber) - Tuple of Two Dictionaries 
    """
    course_to_variable_name = {}
    course_to_number = {}
    i = 0

    for course in next_sem_possible_courses:
        course_to_number[course] = i
        course_to_variable_name[course] = "x" + str(i)
        i += 1

    return course_to_variable_name, course_to_number


course_to_variable_name, course_to_number = course_code_to_variable_and_index()

variable_name_to_course = {value:key for key, value in course_to_variable_name.items()}


#####################
# 7. MIN ENROLLMENT CONSTRAINT


def min_enrollment_matrix(next_sem_possible_courses=next_sem_possible_courses):
    """
    2. Minimum Enrollment Constraint
    """
    return np.ones(len(next_sem_possible_courses), dtype=int)

min_enrollment_matrix_np = min_enrollment_matrix()

min_enrollment_matrix = list(map(lambda x: x, min_enrollment_matrix_np))

with open(r'data\min_enrollment_matrix.txt', 'w') as f:
    for item in min_enrollment_matrix:
        f.write(str(item) + " ")

########################
# 8. MAX ENROLLMENT CONSTRAINT

def max_enrollment_matrix(next_sem_possible_courses=next_sem_possible_courses):
    """
    3. Maximum Enrollment Contraint
    """
    return np.ones(len(next_sem_possible_courses), dtype=int)


max_enrollment_matrix_np = max_enrollment_matrix()

max_enrollment_matrix = list(map(lambda x: x, max_enrollment_matrix_np))

with open(r'data\max_enrollment_matrix.txt', 'w') as f:
    for item in max_enrollment_matrix:
        f.write(str(item) + " ")

##########################
# 9. TIME CONFLICT CONSTRAINT

def time_conflict_matrix(course_to_variable_name=course_to_variable_name, course_to_number=course_to_number, data=data, next_sem_possible_courses=next_sem_possible_courses):
    """
    4. No Course (Timings) Conflict Constraint
    """
    # c4_matrix = np.array([])

    # [0800, 0810, 0820, 0830, 0840, 0850, 0900, 0910, ...]
    # Produces a list of all the possible reasonable times in ten minute intervals
    discrete_times = []

    for i in range(7, 10):
        for j in range(0, 6):
            currTime = "0" + str(i) + str(j) + "0"
            currTime = int(currTime)
            discrete_times.append(currTime)

    for i in range(10, 24):
        for j in range(0, 6):
            currTime = "0" + str(i) + str(j) + "0"
            currTime = int(currTime)
            discrete_times.append(currTime)

    c4 = []
    for currTime in discrete_times:
        currRow = [0]*len(next_sem_possible_courses)
        for currCourse in next_sem_possible_courses:
            course = data['data']['courses'][currCourse]
            start_time = course["courseSchedule"][0]["scheduleStartTime"]
            end_time = course["courseSchedule"][0]["scheduleEndTime"]

            # Removing the semicolon from "hh:mm" and then converting it to an int
            start_time = int(start_time[0:2] + start_time[3:])
            end_time = int(end_time[0:2] + end_time[3:])

            if currTime > start_time and currTime < end_time:
                # print(currCourse)
                # print(currTime)
                currRow[course_to_number[currCourse]] = 1

        # print(currTime)
        # print(currRow)
        c4.append(currRow)
        # time.sleep(3)
        # c4_matrix = np.append(c4_matrix, [currRow], axis=0)

    # print(c4)
    return c4
    # print(c4_matrix[0])
    # return c4_matrix

time_conflict_matrix = time_conflict_matrix()

with open(r'data\timeSlots.txt', 'w') as f:
    i=0
    for time in time_conflict_matrix:
        f.write('t' + str(i) + " ")
        i+=1
        

with open(r'data\time_conflict_matrix.txt', 'w') as f:
    i=0
    for time in time_conflict_matrix:
        f.write('t' + str(i) + " ")
        i+=1
        for course in time:
            f.write(str(course) + " ")
        f.write("\n")
            

def time_conflict_matrix_np(course_to_variable_name=course_to_variable_name, course_to_number=course_to_number, data=data, next_sem_possible_courses=next_sem_possible_courses):
    """
    4. No Course (Timings) Conflict Constraint
    """

    
    discrete_times = []

    # [0700, 0710, 0720, 0730, 0740, 0750, 0800, 0810, ...]
    # Produces a list of all the possible reasonable times in ten minute intervals
    for i in range(7, 10):
        for j in range(0, 6):
            currTime = "0" + str(i) + str(j) + "0"
            currTime = int(currTime)
            discrete_times.append(currTime)

    for i in range(10, 24):
        for j in range(0, 6):
            currTime = "0" + str(i) + str(j) + "0"
            currTime = int(currTime)
            discrete_times.append(currTime)

    c4_matrix = np.zeros(shape=(len(discrete_times), 2031))
    i = 0

    for currTime in discrete_times:
        # currRow = [0]*len(next_sem_possible_courses)
        for currCourse in next_sem_possible_courses:
            course = data['data']['courses'][currCourse]
            start_time = course["courseSchedule"][0]["scheduleStartTime"]
            end_time = course["courseSchedule"][0]["scheduleEndTime"]

            # Removing the semicolon from "hh:mm" and then converting it to an int
            start_time = int(start_time[0:2] + start_time[3:])
            end_time = int(end_time[0:2] + end_time[3:])

            if currTime >= start_time and currTime <= end_time:
                # print(currCourse)
                # print(currTime)
                c4_matrix[i][course_to_number[currCourse]] = 1
        i += 1

    # temp = im.fromarray(c4_matrix, 'L')
    # temp.save('np.png')
    return c4_matrix

time_conflict_matrix_np = time_conflict_matrix_np()

################################
# 10. NO TWO SAME COURSES CONTRAINT

# Groups courses that are the same (but different sections/campuses together)
def dict_w_same_codes(next_sem_possible_courses=next_sem_possible_courses):
    """
    Returns a dict which groups courses that are the same, but have different sections/campuses, together

    Input: courses; list
    Output: dict_w_same_codes; dictionary

    Returns dict of the format:
    {'AFRI 010': ['AFRI 010AC AF-01', 'AFRI 010B AF-01'], 'AFRI 121': ['AFRI 121 AF-01'], 'AFRI 191': ['AFRI 191 SC-01'], 'AMST 103': ['AMST 103 SC-01'],...}  
    """
    dict_w_same_codes = {}
    for course in next_sem_possible_courses:
        if course[0:8] in dict_w_same_codes:
            dict_w_same_codes[course[0:8]].append(course)
        else:
            dict_w_same_codes[course[0:8]] = [course]

    return dict_w_same_codes


dict_w_same_codes = dict_w_same_codes()


def no_same_courses_matrix(dict_w_same_codes=dict_w_same_codes, course_to_number=course_to_number, next_sem_possible_courses=next_sem_possible_courses):
    """
    Gets constraint matrix that ensures that two courses with the same basic course code can't be taken in the same sem
    """
    num_of_courses = len(next_sem_possible_courses)
    c7_matrix = []  # c2_matrix * X <= 1
    for key in dict_w_same_codes.keys():
        currRow = [0]*num_of_courses
        for course in next_sem_possible_courses:
            if key in course:
                currRow[course_to_number[course]] = 1

        c7_matrix.append(currRow)

    return c7_matrix

no_same_courses_matrix = no_same_courses_matrix()
with open(r'data\set_uniqueCourses.txt', 'w') as f:
    i=0
    for unique in dict_w_same_codes.keys():
        f.write("c" + str(i) + " ")
        i+=1

with open(r'data\no_same_courses_matrix.txt', 'w') as f:
    i=0
    for mainCourse in no_same_courses_matrix:
        f.write("c" + str(i) + " ")
        i+=1
        for course in mainCourse:
            f.write(str(course) + " ")
        f.write("\n")

####################################
# 11. ELECTIVES CONSTRAINT MATRIX


hsaCodes = {'DANC', 'WRIT', 'ORST', 'PPA', 'DS', 'ARBT', 'JAPN', 'CHNT', 'MSL', 'CASA', 'ASIA', 'ART', 'GWS', 'GREK', 'GLAS', 'LATN', 'SPEC', 'GOVT', 'RUST', 'HMSC', 'SPCH', 'CHST', 'CREA', 'PORT', 'LEAD', 'ARCN', 'SPAN', 'ITAL', 'MLLC', 'MES', 'MS', 'PPE', 'RLIT', 'LGST', 'POST', 'LAST', 'FREN', 'RUSS', 'STS', 'GEOG', 'GRMT', 'ARBC', 'FHS', 'AMST', 'POLI', 'ARHI', 'MUS', 'MENA', 'LGCS', 'CLAS', 'KRNT', 'LIT', 'JPNT', 'ENGL', 'MCBI', 'CGS', 'FS', 'HIST', 'CHLT', 'CHIN', 'SOC', 'MOBI', 'FLAN',  'ECON', 'CSMT', 'MCSI', 'EA', 'ANTH', 'FIN', 'EDUC', 'PHIL', 'GEOL', 'RLST', 'FWS', 'THEA', 'IR', 'GERM', 'ID', 'ASAM', 'HSA', 'KORE', 'HUM', 'AFRI', 'PSYC', }

hsaConcentration = "ECON"


def requirements_matrix(dict_w_same_codes=dict_w_same_codes, course_to_number=course_to_number, next_sem_possible_courses=next_sem_possible_courses, hsaCodes = hsaCodes, hsaConcentration=hsaConcentration, all_prev_courses = all_prev_courses):
    """
    1. Requirements
    (This will be based on what the student chooses for the next semester.)
    [
        1. Four Kernel Courses in Computer Science and Mathematics
        2. Two Computer Science Courses
        3. Two Mathematics Courses
        4. Clinic
        5. Math Electives
        6. CS Electives
        7. HSA Breadth 
        8. HSA Concentration
        9. HSA Mudd Humms
        10. HSA General
    ]
    
    Not adding Colloquia Row :--> because its not really a constraint since it doesnt have a fixed time nor does it count towards an overload  
    """
    prev_course_codes = set()
    for course in all_prev_courses:
        currCode = re.search(r"[^\s]+", course)
        if currCode:
            currCode = currCode.group(0)
            if currCode not in prev_course_codes:
                prev_course_codes.add(currCode)        
    
    
    num_of_courses = len(next_sem_possible_courses)
    A_matrix = []  # This will be very specific, I need to think about how I'll manage to do it in general.
    
    
    # First Row: Four Kernel Courses in Computer Science and Mathematics
    firstRow = [0]*num_of_courses
    secondRow = [0]*num_of_courses
    thirdRow = [0]*num_of_courses
    fourthRow = [0]*num_of_courses
    fifthRow = [0]*num_of_courses
    sixthRow = [0]*num_of_courses
    seventhRow = [0]*num_of_courses
    eigthRow = [0]*num_of_courses
    ninthRow = [0]*num_of_courses
    tenthRow = [0]*num_of_courses
    
    for course in next_sem_possible_courses:
        currCode = re.search(r"[^\s]+", course)
        if currCode:
            currCode = currCode.group(0)
        
        # First Row: Four Kernel Courses in Computer Science and Mathematics
        if (course[0:8]=="MATH 055") or (course[0:8]=="CSCI 060") or (course[0:8]=="CSCI081") or (course[0:8]=="CSCI 140"):
            firstRow[course_to_number[course]] = 1
        
        # Second Row: Two Computer Science Courses
        elif (course[0:8]=="CSCI 070") or (course[0:8]=="CSCI 131"):
            secondRow[course_to_number[course]] = 1
        
        # Third Row: Two Mathematics Courses   
        elif (course[0:8]== "MATH 131") or (course[0:8]=="MATH 171"):
            thirdRow[course_to_number[course]] = 1
        
        # Fourth Row: Clinic    
        elif (course[0:8]== "CSMT 183") or (course[0:8]=="CSMT 184"):
            fourthRow[course_to_number[course]] = 1
        
        # Fifth Row: Math courses above 100 (TODO: need to remove "strange" courses)    
        elif course[0:6]== "MATH 1":
            fifthRow[course_to_number[course]] = 1
        
        # Sixth Row: CS courses above 100 (TODO: need to remove "strange" courses):
        elif course[0:6]=="CSCI 1":
            sixthRow[course_to_number[course]] = 1
        
        # HSA Requirements:
        if currCode in hsaCodes:
            # Seventh Row: HSA Breadth Requirement
            if currCode != hsaConcentration:
                if currCode not in prev_course_codes:
                    # print("entered")
                    seventhRow[course_to_number[course]] = 1
            # Eight Row: HSA Concentration Requirement
            else:
                # print("entered")
                eigthRow[course_to_number[course]] = 1
            
            # Ninth Row: HSA Mudd Hum Requirement
            t = course.split(' ') 
            if t[2][0:2] == "HM":
                ninthRow[course_to_number[course]] = 1

            # Tenth Row: HSA General Requirement
            tenthRow[course_to_number[course]] = 1
            
            
    A_matrix.append(firstRow)
    A_matrix.append(secondRow)
    A_matrix.append(thirdRow)
    A_matrix.append(fourthRow)
    A_matrix.append(fifthRow)
    A_matrix.append(sixthRow)
    A_matrix.append(seventhRow)
    A_matrix.append(eigthRow)
    A_matrix.append(ninthRow)
    A_matrix.append(tenthRow)
    
      

    return A_matrix
    
requirements_matrix = requirements_matrix()

with open(r'data\requirements_matrix.txt', 'w') as f:
    i=1
    for requirement in requirements_matrix:
        f.write("r" + str(i) + " ")
        i+=1
        for course in requirement:
            f.write(str(course) + " ")
        f.write("\n")

######################################
# 12. COSTS

# -TODO 

def getPreferences():
    """
    Should ideally return something of the form:
    
    {
        "MATH 055 HM 01": 9,
        ...
    }
    
    that is based on the individual users preference of courses.
    """
    return {}

preferences = getPreferences()

def costs(next_sem_possible_courses=next_sem_possible_courses, course_to_number=course_to_number, preferences=preferences):
    num_of_courses = len(next_sem_possible_courses)
    
    costs = [0]*num_of_courses
    
    for course in next_sem_possible_courses:
        
        if course in preferences:
            costs[course_to_number[course]] = preferences[course]      
        
        else:
            # CS Courses = Cost of 5
            if (course[0:4]=="CSCI"):
                costs[course_to_number[course]] = 5
            
            # Math Courses = Cost of 4
            elif (course[0:4]=="MATH"):
                costs[course_to_number[course]] = 4
            
            elif (course[0:4]=="PHIL"):
                costs[course_to_number[course]] = 3
            
            else:
                costs[course_to_number[course]] = 2

    return costs
 
 
costs = costs()


#####################################
with open(r'data\course_names.txt', 'w') as f:
    i=0
    for course in next_sem_possible_courses:
        course = course.replace(" ", "_")
        f.write(course + " ")
        
with open(r'data\courses.txt', 'w') as f:
    i=0
    for course in next_sem_possible_courses:
        f.write(str(course_to_variable_name[course]) + " ")
        
with open(r'data\costs_names.txt', 'w') as f:
    i=0
    for cost in costs:
        course = next_sem_possible_courses[i]
        course = course.replace(" ", "_")
        f.write(course + " " + str(cost) + " ")
        i+=1

with open(r'data\costs.txt', 'w') as f:
    i=0
    for cost in costs:
        f.write("x" + str(i) + " " + str(cost) + " ")
        i+=1
######################################
# ROUGH/NOT NEEDED ANYMORE12

    # def updated_course_to_number(course_to_number=course_to_number, courses=courses, course_to_prereqs=course_to_prereqs, all_prev_courses=all_prev_courses):
    #     updated_course_to_number = course_to_number
    #     currCount = 2031
    #     seen = set()
    #     for course in course_to_prereqs:
    #         for prereqs in course_to_prereqs[course][1:]:
    #             for prereq in prereqs:
    #                 # print(prereq)
    #                 if prereq != "POI" and prereq not in seen:
    #                     # print(prereq)
    #                     seen.add(prereq)
    #                     courses.append(prereq)
    #                     updated_course_to_number[prereq] = "x" + str(currCount)
    #                     currCount+=1

    #     for course in all_prev_courses:
    #         if course not in seen:
    #             seen.add(course)
    #             courses.append(course)
    #             updated_course_to_number[course] = "x" + str(currCount)
    #             currCount+=1

    #     return updated_course_to_number, courses

    # # updated_course_to_number()
    # updated_course_to_number, courses = updated_course_to_number()
    # # print(updated_course_to_number)
    # """
    # Constraints:
    # 1. Electives Constraint
    # 2. Minimum Enrollment Constraint (done)
    # 3. Maximum Enrollment Contraint (done)
    # 4. No Course (Timings) Conflict Constraint (done)
    # 7. Can't take the same course twice during the same sem (done)

    # 5. Course Pre-Reqs Constraint [Doing with Python Function]
    # 6. Can't take a course taken previously [Doing with Python Function]

    # """

    # # possible_courses_due_to_prereqs = possible_courses_due_to_prereqs()

    # # print(len(possible_courses_due_to_prereqs))
