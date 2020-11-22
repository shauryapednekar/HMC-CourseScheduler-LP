import json
import numpy as np
import pandas as pd
import time
import re
import time


# User Inputs Needed
from user.userInputs.previousCourses import all_prev_courses
from user.userInputs.preferences import myPreferences

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
        - "all_courses" contains "possible_courses" + "all_prev_courses" + "prereq_courses" (all unique)
        
    --- By this time, we will have:
        - "rawData" [dict]
        - "possible_courses" [list]
        - "course_to_variable_name" [dict]
        - "course_to_index" [dict]

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
 
##################################################
# 1 - Getting all courses that are going to be offered:

with open(r"rawData/course_data.json", encoding="utf-8") as f:
    rawData = json.load(f)

def possible_courses():
    """Nothing

    Returns:
        list: all courses (complete course code) being offered
    """  
    
    return list(rawData['data']["courses"].keys())

possible_courses = possible_courses()

###############################################
# 2 - Only Keep 3 Credit Courses:

def only_keep_three_credit_classes():
    """Removes all half credit/PE courses.

    Global Variables Needed:
        rawData (dict, optional): Defaults to rawData.
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        list: possible three credit courses
    """    
    possible=[]
    
    for course in possible_courses:
        if rawData['data']["courses"][course]["courseCredits"] == "3.0":
            possible.append(course)
    
    return possible

possible_courses = only_keep_three_credit_classes()

#######################
# 3 - Remove Previously Taken Courses:

def remove_prev_courses():
    """Removes previously taken courses.

    Global Variables Needed:
        all_prev_courses (dict, optional): user's previously taken courses. Defaults to all_prev_courses.
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        list: removes previously taken courses (all sections) from list of possible courses 
    """  
    # All sections of previously taken courses that are currently being offered
    repeated = []
    
    for course in possible_courses:
        for prev_course in all_prev_courses:
            # To find all sections of the prev_course
            if prev_course in course:
                repeated.append(course)
    
    # possible_courses minus repeated
    output = []
    for course in possible_courses:
        if course not in repeated:
            output.append(course)
                
    return output

possible_courses = remove_prev_courses()
    
######################
# 4 - Remove courses that cannot be taken due to prereqs:


def subject_codes():
    """Finds all possible subject codes (such as 'MATH' and 'RLST' etc.).

    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        set: All unique subject codes
    """
        
    subject_codes = set()
    for course in possible_courses:
        # Gets first word of course (until the first space) - which is the subject code:
        currCode = re.search(r"[^\s]+", course)
        if currCode:
            currCode = currCode.group(0)
            if currCode not in subject_codes:
                subject_codes.add(currCode)

    return subject_codes

subject_codes = subject_codes()

# Prereqs Function that only needs to be run once ('untab' the following block):
    # def prereqs(possible_courses=possible_courses, rawData=rawData, subject_codes=subject_codes):
    #     """Collects prereqs for each course

    #     Global Variables Needed:
    #         possible_courses (list, optional): Defaults to possible_courses.
    #         rawData (dict, optional): Defaults to rawData.
    #         subject_codes (set, optional): Defaults to subject_codes.

    #     Returns:
    #         dict: Dictionary where the keys are the courses that contain prerequisites and its values are a list of the prerequisites.
    #     """
        
    #     # Contains only the courses that have prereqs    
    #     course_to_prereqs = {}
        
    #     for course in possible_courses:
    #         description = rawData['data']["courses"][course]['courseDescription']
    #         if not description:
    #             prereqs = ""
    #         elif 'Prerequisite: ' not in description:
    #             prereqs = ""
                
    #         # Only finding prereqs for courses that have "Prerequisite:" in their description
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
    #             # Replaces subject names to corresponding subject codes
    #             for key in replacement_dict:
    #                 prereqs = prereqs.replace(key, replacement_dict[key])

    #             lis = []
    #             # Finds all prereqs of the form {subject code}{x*} where x* is one or more numbers
    #             for course_code in subject_codes:
    #                 currCode = course_code + "\s?[0-9]*"
                    
    #                 if re.findall(currCode, prereqs):
    #                     lis += re.findall(currCode, prereqs)

    #             newLis = []
    #             # Normalizes prereqs format (eg. 'CSCI5' --> 'CSCI 005')
    #             for l in lis:
    #                 check = True
    #                 for course_code in subject_codes:
    #                     if re.match(course_code + '\s[0-9]{3}', l): # eg. 'CSCI 005'
    #                         pass
                        
    #                     # eg. 'CSCI005' --> 'CSCI 005'
    #                     elif re.match(course_code + '[0-9]{3}', l): 
    #                         n = len(course_code)
    #                         l = l[0:n] + " " + l[n:]
    #                         check = False
    #                         newLis.append(l)
                        
    #                     # eg. 'CSCI05' --> 'CSCI 005'
    #                     elif re.match(course_code + '[0-9]{2}', l):
    #                         n = len(course_code)
    #                         l = l[0:n] + " 0" + l[n:]
    #                         check = False
    #                         newLis.append(l)
                            
    #                     # eg. 'CSCI5' --> 'CSCI 005'
    #                     elif re.match(course_code + '[0-9]{1}', l):
    #                         n = len(course_code)
    #                         l = l[0:n] + " 00" + l[n:]
    #                         check = False
    #                         newLis.append(l)

    #                     # eg. 'CSCI 05' --> 'CSCI 005'
    #                     elif re.match(course_code + '\s[0-9]{2}', l):
    #                         n = len(course_code)+1
    #                         l = l[0:n] + "0" + l[n:]
    #                         check = False
    #                         newLis.append(l)
                        
    #                     # eg. 'CSCI 5' --> 'CSCI 005'
    #                     elif re.match(course_code + '\s[0-9]{1}', l):
    #                         n = len(course_code)+1
    #                         l = l[0:n] + "00" + l[n:]
    #                         check = False
    #                         newLis.append(l)
                    
    #                 # Makes sure prereq is a specific course ("... MATH60", not "...MATH is recommended" for example)
    #                 if check:
    #                     newLis.append(l)

    #             # Adds ["POI"] to list of prereqs for appropriate courses
    #             if "permission of the instructor" in prereqs or "permission of instructor" in prereqs:
    #                 course_to_prereqs[course] = [[prereqs], newLis, ["POI"]]
    #             else:
    #                 course_to_prereqs[course] = [[prereqs], newLis]

    #     return course_to_prereqs


    # course_to_prereqs = prereqs()

    # with open(r'preReqs/prereqs.json', 'w') as fp:
    #     json.dump(prereqs(), fp, indent=4)

with open(r"preReqs/prereqs_edited_by_hand.json", encoding="utf-8") as f:
    prereqs_edited = json.load(f)


def helper_next_sem_possible_courses_due_to_prereqs(lis):
    """Helper function that checks whether the prereqs for a course have been fulfilled
    
    Global Variables Needed:
        all_prev_courses (set, optional): Defaults to all_prev_courses.

    Args:
        lis (list): list of prereqs  

    Returns:
        bool: True if prereqs have been fulfilled and false otherwise
    """    
    for elem in lis:
        if elem not in all_prev_courses:
            return False

    return True


def next_sem_possible_courses_due_to_prereqs():
    """
    Returns list of possible courses according to previously taken courses and prerequisites 
    (includes previously taken courses too)
    """
    possible_courses = []
    
    for course in possible_courses:
        
        # If the course has prereqs
        if course in prereqs_edited:
            currPrereqs = prereqs_edited[course][1:]
            if ["POI"] in currPrereqs:
                currPrereqs.remove(["POI"])
            
            # If prereqs are fulfilled, True will be present in temp
            # Otherwise, it will be only False values
             
            temp = [helper_next_sem_possible_courses_due_to_prereqs(prereq, all_prev_courses) for prereq in currPrereqs]
            if True in temp:
                possible_courses.append(course)
                
        # If the course does not have prereqs
        else:
            possible_courses.append(course)
        
    return possible_courses


possible_courses = next_sem_possible_courses_due_to_prereqs()

######################
# 5 - Add Courses for Which Permission of Instructor is Obtained (Regardless of Prereqs):

# -TODO:


def addPOIcourses():
    pass

#####################
# 6 - Remove Courses Which Should Never Be Included in the Solution:

# -TODO:

def removeBadCourses():
    pass

######################
# 7 - Dictionary of course_name -> var_name and course_name -> var_index

def course_code_to_variable_and_index():
    """Dictionary that maps complate course code to a variable of the format "xi" where "i" is the variable number
    
    

    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        tuple: tuple of two dictionaries:
                - course_to_variable_name: dict that maps complete course code to a variable of the format "xi" where "i" is the variable number
                - course_to_index: dict that maps complete_course_code to int i, where i equals corresponding variable name in course_to_variable_name
    """    
    
    course_to_variable_name = {}
    course_to_index = {}
    i = 0

    for course in possible_courses:
        course_to_index[course] = i
        course_to_variable_name[course] = "x" + str(i)
        i += 1

    return course_to_variable_name, course_to_index

course_to_variable_name, course_to_index = course_code_to_variable_and_index()

variable_name_to_course = {value:key for key, value in course_to_variable_name.items()}

##########################
# 8 - Time Conflict Constraint

def time_conflict_matrix():
    """Creates a matrix that where each row represents the classes that are occuring
       during the time corresponding to that row.

    Global Variables Needed:
        course_to_variable_name (dict, optional): Defaults to course_to_variable_name.
        course_to_index (dict, optional): Defaults to course_to_index.
        rawData (dict, optional): Defaults to rawData.
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        list of lists: 2-D Matrix where each element of each row is a zero or one 
                       where 1 correspondings to the class occuring during the time corresponding to its row and 0 otherwise.
    """
    
    # Produces a list of all the possible reasonable times in ten minute intervals
    # in the following format: [0800, 0810, 0820, 0830, 0840, 0850, 0900, 0910, ...]
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


    A_matrix = []
    for currTime in discrete_times:
        currRow = [0]*len(possible_courses)
        for currCourse in possible_courses:
            course = rawData['data']['courses'][currCourse]
            start_time = course["courseSchedule"][0]["scheduleStartTime"]
            end_time = course["courseSchedule"][0]["scheduleEndTime"]

            # Removing the colon from "hh:mm" and then converting it to an int
            start_time = int(start_time[0:2] + start_time[3:])
            end_time = int(end_time[0:2] + end_time[3:])

            # Not strictly greater than or less than because courses can take place
            # back to back.
            if currTime > start_time and currTime < end_time:
                currRow[course_to_index[currCourse]] = 1

        A_matrix.append(currRow)

    return A_matrix

time_conflict_matrix = time_conflict_matrix()

with open(r'amplData\timeSlots.txt', 'w') as f:
    i=0
    for time in time_conflict_matrix:
        f.write('t' + str(i) + " ")
        i+=1
        

with open(r'amplData\time_conflict_matrix.txt', 'w') as f:
    i=0
    for time in time_conflict_matrix:
        f.write('t' + str(i) + " ")
        i+=1
        for course in time:
            f.write(str(course) + " ")
        f.write("\n")
            
# Same as above function except using numpy for speed ("tab below block unless needed"): 
    # def time_conflict_matrix_np(course_to_variable_name=course_to_variable_name, course_to_index=course_to_index, rawData=rawData, possible_courses=possible_courses):
    #     """Same as time_conflict_matrix() except using numpy arrays for speed.

    #     Global Variables Needed:
    #         course_to_variable_name (dict, optional): Defaults to course_to_variable_name.
    #         course_to_index (dict, optional): Defaults to course_to_index.
    #         rawData (dict, optional): Defaults to rawData.
    #         possible_courses (list, optional): Defaults to possible_courses.

    #     Returns:
    #         list of lists: 2-D Matrix where each element of each row is a zero or one 
    #                        where 1 correspondings to the class occuring during the time corresponding to its row and 0 otherwise.
    #     """
        
    #     discrete_times = []

    #     # [0700, 0710, 0720, 0730, 0740, 0750, 0800, 0810, ...]
    #     # Produces a list of all the possible reasonable times in ten minute intervals
    #     for i in range(7, 10):
    #         for j in range(0, 6):
    #             currTime = "0" + str(i) + str(j) + "0"
    #             currTime = int(currTime)
    #             discrete_times.append(currTime)

    #     for i in range(10, 24):
    #         for j in range(0, 6):
    #             currTime = "0" + str(i) + str(j) + "0"
    #             currTime = int(currTime)
    #             discrete_times.append(currTime)

    #     A_matrix = np.zeros(shape=(len(discrete_times), 2031))
    #     i = 0

    #     for currTime in discrete_times:
    #         for currCourse in possible_courses:
    #             course = rawData['data']['courses'][currCourse]
    #             start_time = course["courseSchedule"][0]["scheduleStartTime"]
    #             end_time = course["courseSchedule"][0]["scheduleEndTime"]

    #             # Removing the semicolon from "hh:mm" and then converting it to an int
    #             start_time = int(start_time[0:2] + start_time[3:])
    #             end_time = int(end_time[0:2] + end_time[3:])

    #             if currTime >= start_time and currTime <= end_time:
    #                 A_matrix[i][course_to_index[currCourse]] = 1
    #         i += 1
            
    #     return A_matrix

    # time_conflict_matrix_np = time_conflict_matrix_np()

################################
# 10 - No Two Same Courses Constraint:

def dict_w_same_codes():
    """Groups courses that are the same (but different sections/campuses) together

    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        dict: Format of dictionary returned is {Course Code : [all courses that have the same course code]}
    """    
    
    dict_w_same_codes = {}
    for course in possible_courses:
        # Possible error for courses such as "CSCI 181Y" isnt the same as "CSCI 181B"
        if course[0:8] in dict_w_same_codes:
            dict_w_same_codes[course[0:8]].append(course)
        else:
            dict_w_same_codes[course[0:8]] = [course]

    return dict_w_same_codes

dict_w_same_codes = dict_w_same_codes()

def no_same_courses_matrix():
    """Creates constraint matrix that ensures that the solution provided doesn't include two courses that are essentially
       the same but at different campuses or different timings. 
       In the mod file, the following condition ensures it: Ax <= 1

    Global Variables Needed:
        dict_w_same_codes (dict, optional): Defaults to dict_w_same_codes.
        course_to_index (dict, optional): Defaults to course_to_index.
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        List of lists: 2-D Matrix where the rows are the unique courses being offered and the value of an element
                       in the row is a zero or one depending on whether it is essentially the same course as its
                       corresponding row.
    """  
    
    num_of_courses = len(possible_courses)
    
    A_matrix = []  
    for key in dict_w_same_codes.keys():
        currRow = [0]*num_of_courses
        for course in possible_courses:
            if key in course:
                currRow[course_to_index[course]] = 1

        A_matrix.append(currRow)

    return A_matrix

no_same_courses_matrix = no_same_courses_matrix()

with open(r'amplData\set_uniqueCourses.txt', 'w') as f:
    i=0
    for unique in dict_w_same_codes.keys():
        f.write("c" + str(i) + " ")
        i+=1

with open(r'amplData\no_same_courses_matrix.txt', 'w') as f:
    i=0
    for mainCourse in no_same_courses_matrix:
        f.write("c" + str(i) + " ")
        i+=1
        for course in mainCourse:
            f.write(str(course) + " ")
        f.write("\n")

####################################
# 11. Requirements Constraint Matrix:


hsaCodes = {'DANC', 'WRIT', 'ORST', 'PPA', 'DS', 'ARBT', 'JAPN', 'CHNT', 'MSL', 
            'CASA', 'ASIA', 'ART', 'GWS', 'GREK', 'GLAS', 'LATN', 'SPEC', 'GOVT', 
            'RUST', 'HMSC', 'SPCH', 'CHST', 'CREA', 'PORT', 'LEAD', 'ARCN', 'SPAN', 
            'ITAL', 'MLLC', 'MES', 'MS', 'PPE', 'RLIT', 'LGST', 'POST', 'LAST', 'FREN', 
            'RUSS', 'STS', 'GEOG', 'GRMT', 'ARBC', 'FHS', 'AMST', 'POLI', 'ARHI', 'MUS', 
            'MENA', 'LGCS', 'CLAS', 'KRNT', 'LIT', 'JPNT', 'ENGL', 'MCBI', 'CGS', 'FS', 
            'HIST', 'CHLT', 'CHIN', 'SOC', 'MOBI', 'FLAN',  'ECON', 'MCSI', 'EA', 
            'ANTH', 'FIN', 'EDUC', 'PHIL', 'GEOL', 'RLST', 'FWS', 'THEA', 'IR', 'GERM', 
            'ID', 'ASAM', 'HSA', 'KORE', 'HUM', 'AFRI', 'PSYC', }

# - TODO: Get this from user input file instead of hardcoding it. 
hsaConcentration = "ECON"


def requirements_matrix():
    """Creates matrix that ensures that desired requirements are met.
    
    1. Requirements (currently only designed for CS-Math majors):
    (This will be based on what the student chooses for the next semester.)
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
    
    
    Not adding Colloquia Row :--> because its not really a constraint since it doesnt
    have a fixed time nor does it count towards an overload  

    Global Variables Needed:
        dict_w_same_codes ([type], optional): [description]. Defaults to dict_w_same_codes.
        course_to_index ([type], optional): [description]. Defaults to course_to_index.
        possible_courses ([type], optional): [description]. Defaults to possible_courses.
        hsaCodes ([type], optional): [description]. Defaults to hsaCodes.
        hsaConcentration ([type], optional): [description]. Defaults to hsaConcentration.
        all_prev_courses ([type], optional): [description]. Defaults to all_prev_courses.

    Returns:
        List of lists: 2-D Matrix where each row represents a specific requirement and each column represents a specific course
    """    
    
    # Needed for HSA breadth requirement
    prev_course_codes = set()
    for course in all_prev_courses:
        currCode = re.search(r"[^\s]+", course)
        if currCode:
            currCode = currCode.group(0)
            if currCode not in prev_course_codes:
                prev_course_codes.add(currCode)        
    
    
    num_of_courses = len(possible_courses)
    
    # A_matrix will be very specific to CS-Math majors, I need to think about how I'll manage to do it in general.
    A_matrix = []  
    
    
    # First Row: Four Kernel Courses in Computer Science and Mathematics
    # - TODO: This can be optimized for space.
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
    
    for course in possible_courses:
        currCode = re.search(r"[^\s]+", course)
        if currCode:
            currCode = currCode.group(0)
        
        # First Row: Four Kernel Courses in Computer Science and Mathematics
        if (course[0:8]=="MATH 055") or (course[0:8]=="CSCI 060") or (course[0:8]=="CSCI081") or (course[0:8]=="CSCI 140"):
            firstRow[course_to_index[course]] = 1
        
        # Second Row: Two Computer Science Courses
        elif (course[0:8]=="CSCI 070") or (course[0:8]=="CSCI 131"):
            secondRow[course_to_index[course]] = 1
        
        # Third Row: Two Mathematics Courses   
        elif (course[0:8]== "MATH 131") or (course[0:8]=="MATH 171"):
            thirdRow[course_to_index[course]] = 1
        
        # Fourth Row: Clinic    
        elif (course[0:8]== "CSMT 183") or (course[0:8]=="CSMT 184"):
            fourthRow[course_to_index[course]] = 1
        
        # Fifth Row: Math courses above 100 (TODO: need to remove "strange" courses)    
        elif course[0:6]== "MATH 1":
            fifthRow[course_to_index[course]] = 1
        
        # Sixth Row: CS courses above 100 (TODO: need to remove "strange" courses):
        elif course[0:6]=="CSCI 1":
            sixthRow[course_to_index[course]] = 1
        
        # HSA Requirements:
        if currCode in hsaCodes:
            
            # Seventh Row: HSA Breadth Requirement
            if currCode != hsaConcentration:
                if currCode not in prev_course_codes:
                    seventhRow[course_to_index[course]] = 1
            
            # Eight Row: HSA Concentration Requirement
            else:
                eigthRow[course_to_index[course]] = 1
            
            # Ninth Row: HSA Mudd Hum Requirement
            t = course.split(' ') 
            if t[2][0:2] == "HM":
                ninthRow[course_to_index[course]] = 1

            # Tenth Row: HSA General Requirement
            tenthRow[course_to_index[course]] = 1
            
            
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

with open(r'amplData\requirements_matrix.txt', 'w') as f:
    i=1
    for requirement in requirements_matrix:
        f.write("r" + str(i) + " ")
        i+=1
        for course in requirement:
            f.write(str(course) + " ")
        f.write("\n")

######################################
# 12. Costs

def costs():
    """Row of costs corresponding to each possible course.

    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.
        course_to_index (dict, optional): Defaults to course_to_index.
        preferences (dict, optional): Defaults to myPreferences.

    Returns:
        List: Row of costs corresponding to each possible course. 
    """    
    num_of_courses = len(possible_courses)
    
    costs = [0]*num_of_courses
    
    for course in possible_courses:
        
        if course in preferences:
            costs[course_to_index[course]] = preferences[course]      
        
        # (TODO: Edit this based on survey results.)
        # Default costs for courses 
        else:
            # CS Courses = Cost of 5
            if (course[0:4]=="CSCI"):
                costs[course_to_index[course]] = 5
            
            # Math Courses = Cost of 4
            elif (course[0:4]=="MATH"):
                costs[course_to_index[course]] = 4
            
            # Philosophy Courses = Cost of 3
            elif (course[0:4]=="PHIL"):
                costs[course_to_index[course]] = 3
                
            # All other courses = Cost of 2
            else:
                costs[course_to_index[course]] = 2

    return costs
  
costs = costs()

#####################################
with open(r'amplData\course_names.txt', 'w') as f:
    i=0
    for course in possible_courses:
        course = course.replace(" ", "_")
        f.write(course + " ")
        
with open(r'amplData\courses.txt', 'w') as f:
    i=0
    for course in possible_courses:
        f.write(str(course_to_variable_name[course]) + " ")
        
with open(r'amplData\costs_names.txt', 'w') as f:
    i=0
    for cost in costs:
        course = possible_courses[i]
        course = course.replace(" ", "_")
        f.write(course + " " + str(cost) + " ")
        i+=1

with open(r'amplData\costs.txt', 'w') as f:
    i=0
    for cost in costs:
        f.write("x" + str(i) + " " + str(cost) + " ")
        i+=1
######################################