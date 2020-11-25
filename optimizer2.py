"""Main Course Scheduling Script"""

import json
import time
import re
import os
import numpy as np

# # User Input Needed
from user.desiredReqs import curr_desired_reqs
from user.desiredReqs import curr_major


# SKELETAL:

    #     1. Get all courses offered next sem.

    #     2. Remove courses taken previously.

    #     3. Remove courses that I cannot take due to prereqs.

    #     4. (TODO - easy) Possibly add next sem courses that I
    #         have already permed into that arent already in courses.

    #     5. (TODO - easy) Possibly remove next sem courses that
    #         I absolutely do not want to take/won"t get in to.
    #         (TODO - easy) Possibly factor in preplacement here.

    #     --- Have all the courses that I am willing and able to take.

    #     6. Make a dictionary of of course name to variable name
    #        (and its index in "all_courses" string).
    #         - "all_courses" contains "possible_courses"
    #             + "all_prev_courses" + "prereq_courses" (all unique)

    #     --- By this time, we will have:
    #         - "raw_data" [dict]
    #         - "possible_courses" [list]
    #         - "course_to_variable_name" [dict]
    #         - "course_to_index" [dict]

    #     --- Constraints ---

    #     9. Complete time conflict constraint matrix.
    #         Ax <= 1;     each row of A represents a discrete point in time

    #     10. Complete no two same courses constraint matrix:
    #         Ax <= 1;     each row of A has a 1 for variables
    #         that are the same course (but different sections)

    #     11. Complete electives constraint matrix.

##################################################
# 1 - Getting all courses that are going to be offered:

with open(r"rawData/course_data.json", encoding="utf-8") as f:
    raw_data = json.load(f)

def possible_courses_func():
    """Nothing

    Returns:
        list: all courses (complete course code) being offered
    """

    return list(raw_data["data"]["courses"].keys())

###############################################
# 2 - Only Keep 3 Credit Courses:

def only_keep_three_credit_classes(raw_data, possible_courses):
    """Removes all half credit/PE courses.

    Global Variables Needed:
        raw_data (dict, optional): Defaults to raw_data.
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        list: possible three credit courses
    """
    possible = []

    for course in possible_courses:
        if raw_data["data"]["courses"][course]["courseCredits"] == "3.0":
            possible.append(course)

    return possible

#######################
# 3 - Remove Previously Taken Courses:

def remove_prev_courses(all_prev_courses, possible_courses):
    """Removes previously taken courses.

    Global Variables Needed:
        all_prev_courses (dict, optional): user"s previously taken courses.
        Defaults to all_prev_courses.
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        list: removes previously taken courses (all sections) from list of
        possible courses
    """
    # All sections of previously taken courses that are currently being offered
    repeated = set()

    for course in possible_courses:
        for prev_course in all_prev_courses:
            # To find all sections of the prev_course
            if prev_course in course:
                repeated.add(course)

    # possible_courses minus repeated
    output = []
    for course in possible_courses:
        if course not in repeated:
            output.append(course)

    return output

######################
# 4 - Remove courses that cannot be taken due to prereqs:


def subject_codes_func(possible_courses):
    """Finds all possible subject codes (such as "MATH" and "RLST" etc.).

    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        set: All unique subject codes
    """

    codes = set()
    for course in possible_courses:
        # Gets first word of course (until the first space)
        # - which is the subject code:
        curr_code = re.search(r"[^\s]+", course)
        if curr_code:
            curr_code = curr_code.group(0)
            if curr_code not in codes:
                codes.add(curr_code)

    return codes

# Prereqs Function that only needs to be run once ("untab" the following block):
    # def prereqs():
    #     """Collects prereqs for each course

    #     Global Variables Needed:
    #         possible_courses (list, optional): Defaults to possible_courses.
    #         raw_data (dict, optional): Defaults to raw_data.
    #         subject_codes (set, optional): Defaults to subject_codes.

    #     Returns:
    #         dict: Dictionary where the keys are the courses that contain
    #               prerequisites and its values are a list of the
    # prerequisites.
    #     """

    #     # Contains only the courses that have prereqs
    #     course_to_prereqs = {}

    #     for course in possible_courses:
    #         description = (raw_data["data"]["courses"][course]
    # ["courseDescription"])
    #         if not description:
    #             prereqs = ""
    #         elif "Prerequisite: " not in description:
    #             prereqs = ""

    #         # Only finding prereqs for courses that have "Prerequisite:" in
    #           their description
    #         else:
    #             prereqs = description.partition("Prerequisite: ")[2]


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
    #             # Finds all prereqs of the form {subject code}{x*} where x*
    #               is one or more numbers
    #             for course_code in subject_codes:
    #                 curr_code = course_code + "\s?[0-9]*"

    #                 if re.findall(curr_code, prereqs):
    #                     lis += re.findall(curr_code, prereqs)

    #             newLis = []
    #             # Normalizes prereqs format (eg. "CSCI5" --> "CSCI 005")
    #             for l in lis:
    #                 check = True
    #                 for course_code in subject_codes:
                          # eg. "CSCI 005"
    #                     if re.match(course_code + "\s[0-9]{3}", l):
    #                         pass

    #                     # eg. "CSCI005" --> "CSCI 005"
    #                     elif re.match(course_code + "[0-9]{3}", l):
    #                         n = len(course_code)
    #                         l = l[0:n] + " " + l[n:]
    #                         check = False
    #                         newLis.append(l)

    #                     # eg. "CSCI05" --> "CSCI 005"
    #                     elif re.match(course_code + "[0-9]{2}", l):
    #                         n = len(course_code)
    #                         l = l[0:n] + " 0" + l[n:]
    #                         check = False
    #                         newLis.append(l)

    #                     # eg. "CSCI5" --> "CSCI 005"
    #                     elif re.match(course_code + "[0-9]{1}", l):
    #                         n = len(course_code)
    #                         l = l[0:n] + " 00" + l[n:]
    #                         check = False
    #                         newLis.append(l)

    #                     # eg. "CSCI 05" --> "CSCI 005"
    #                     elif re.match(course_code + "\s[0-9]{2}", l):
    #                         n = len(course_code)+1
    #                         l = l[0:n] + "0" + l[n:]
    #                         check = False
    #                         newLis.append(l)

    #                     # eg. "CSCI 5" --> "CSCI 005"
    #                     elif re.match(course_code + "\s[0-9]{1}", l):
    #                         n = len(course_code)+1
    #                         l = l[0:n] + "00" + l[n:]
    #                         check = False
    #                         newLis.append(l)

    #                 # Makes sure prereq is a specific course
    #                   ("... MATH60", not "...MATH is recommended" for example)
    #                 if check:
    #                     newLis.append(l)

    #             # Adds ["POI"] to list of prereqs for appropriate courses
    #             if "permission of the instructor" in prereqs or
    #               "permission of instructor" in prereqs:
    #                 course_to_prereqs[course] = [[prereqs], newLis, ["POI"]]
    #             else:
    #                 course_to_prereqs[course] = [[prereqs], newLis]

    #     return course_to_prereqs


    # course_to_prereqs = prereqs()

    # with open(r"preReqs/prereqs.json", "w") as fp:
    #     json.dump(prereqs(), fp, indent=4)

with open(r"preReqs/all_prereqs_edited.json", encoding="utf-8") as f:
    prereqs_edited = json.load(f)

def helper_next_sem_possible_courses_due_to_prereqs(lis, all_prev_courses):
    """Helper function that checks whether the prereqs for a course have been
    fulfilled

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

def next_sem_possible_courses_due_to_prereqs(all_prev_courses, possible_courses):
    """Creates list of possible courses according to previously taken courses
    and prereqs.

    Returns:
        list: list of possible courses according to previously taken courses
        and prereqs
    """

    list_of_possible_courses = []

    for course in list_of_possible_courses:

        # If the course has prereqs
        if course in prereqs_edited:
            curr_prereqs = prereqs_edited[course][1:]
            if ["POI"] in curr_prereqs:
                curr_prereqs.remove(["POI"])

            # If prereqs are fulfilled, True will be present in temp
            # Otherwise, it will be only False values

            temp = ([helper_next_sem_possible_courses_due_to_prereqs (prereq, all_prev_courses)
                    for prereq in curr_prereqs])
            if True in temp:
                list_of_possible_courses.append(course)

        # If the course does not have prereqs
        else:
            list_of_possible_courses.append(course)

    return possible_courses

######################
# 5 - Add Courses for Which Permission of Instructor is Obtained
# (Regardless of Prereqs):

# -TODO:

def add_poi_courses():
    pass

#####################
# 6 - Remove Courses Which Should Never Be Included in the Solution:

def remove_bad_courses(possible_courses, bad_courses):
    res = []
    # repeated = []
    
    # for course in possible_courses:
    #     for bad_course in bad_courses:
    #         if bad_course == course:
    #             repeated.append(course)
    remove = set()
    for course in possible_courses:
        for bad_course in bad_courses:
            if bad_course in course:
                remove.add(course)
            
    for course in possible_courses:
        if course not in remove:
            res.append(course)     
        # if course not in bad_courses:
        #     res.append(course)
    
    return res

######################
# 7 - Dictionary of course_name -> var_name and course_name -> var_index

def course_code_to_variable_and_index(possible_courses):
    """Dictionary that maps complate course code to a variable of the format
    "xi" where "i" is the variable number



    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        tuple: tuple of two dictionaries:
                - course_to_variable_name: dict that maps complete course code
                to a variable of the format "xi" where "i" is the variable
                number

                - course_to_index: dict that maps complete_course_code to int i,
                  where i equals corresponding variable name in
                  course_to_variable_name

    """

    course_to_variable_name_dict = {}
    course_to_index_dict = {}
    j = 0

    for course in possible_courses:
        course_to_index_dict[course] = j
        course_to_variable_name_dict[course] = "x" + str(j)
        j += 1

    return course_to_variable_name_dict, course_to_index_dict

##########################
# 8 - Time Conflict Constraint

def time_conflict_matrix_func(course_code_to_variable_name, course_to_index, raw_data, possible_courses):
    """Creates a matrix that where each row represents the classes that are
    occuring during the time corresponding to that row.

    Global Variables Needed:
        course_to_variable_name (dict, optional):
        Defaults to course_to_variable_name.
        course_to_index (dict, optional): Defaults to course_to_index.
        raw_data (dict, optional): Defaults to raw_data.
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        list of lists: 2-D Matrix where each element of each row is a
        zero or one where 1 correspondings to the class occuring during the time
        corresponding to its row and 0 otherwise.
    """

    # Produces a list of all the possible reasonable times in ten
    # minute intervals in the following format:
    # [0800, 0810, 0820, 0830, 0840, 0850, 0900, 0910, ...]
    discrete_times = []

    for k in range(7, 10):
        for j in range(0, 6):
            curr_time = "0" + str(k) + str(j) + "0"
            curr_time = int(curr_time)
            discrete_times.append(curr_time)

    for k in range(10, 24):
        for j in range(0, 6):
            curr_time = "0" + str(k) + str(j) + "0"
            curr_time = int(curr_time)
            discrete_times.append(curr_time)

    days = "MTWRF"

    constraint_matrix = []
    for curr_time in discrete_times:     
        
        for day in days:
            
            curr_row = [0]*len(possible_courses)
        
            for curr_course in possible_courses:
                
                course = raw_data["data"]["courses"][curr_course]
                for item in course["courseSchedule"]:
                    
                    if day in item["scheduleDays"]:
                
                        start_time = item["scheduleStartTime"]
                        end_time = item["scheduleEndTime"]

                        # Removing the colon from "hh:mm" and then converting it to an int
                        start_time = int(start_time[0:2] + start_time[3:])
                        end_time = int(end_time[0:2] + end_time[3:])

                        # Not strictly greater than or less than because
                        # courses can take place back to back.
                        after_start_time = curr_time > start_time
                        before_end_time = curr_time < end_time
                        if after_start_time and before_end_time:
                            curr_row[course_to_index[curr_course]] = 1
                
            constraint_matrix.append(curr_row)

    return constraint_matrix

# Same as above function except using numpy for speed
# ("tab below block unless needed"):
    # import numpy as np
    # def time_conflict_matrix_np():
    #     """Same as time_conflict_matrix() except using numpy arrays for speed.

    #     Global Variables Needed:
    #         course_to_variable_name (dict, optional):
    #         Defaults to course_to_variable_name.
    #         course_to_index (dict, optional): Defaults to course_to_index.
    #         raw_data (dict, optional): Defaults to raw_data.
    #         possible_courses (list, optional): Defaults to possible_courses.

    #     Returns:
    #         list of lists: 2-D Matrix where each element of
    #         each row is a zero or one where 1 correspondings to the
    #         class occuring during the time corresponding to its row
    #         and 0 otherwise.
    #     """

    #     discrete_times = []

    #     # [0700, 0710, 0720, 0730, 0740, 0750, 0800, 0810, ...]
    #     # Produces a list of all the possible reasonable times
    #     # in ten minute intervals
    #     for k in range(7, 10):
    #         for j in range(0, 6):
    #             curr_time = "0" + str(k) + str(j) + "0"
    #             curr_time = int(curr_time)
    #             discrete_times.append(curr_time)

    #     for k in range(10, 24):
    #         for j in range(0, 6):
    #             curr_time = "0" + str(k) + str(j) + "0"
    #             curr_time = int(curr_time)
    #             discrete_times.append(curr_time)

    #     constraint_matrix = np.zeros(shape=(len(discrete_times), 2031))
    #     k = 0

    #     for curr_time in discrete_times:
    #         for curr_course in possible_courses:
    #             course = raw_data["data"]["courses"][curr_course]
    #             start_time = course["courseSchedule"][0]["scheduleStartTime"]
    #             end_time = course["courseSchedule"][0]["scheduleEndTime"]

    #             # Removing the semicolon from "hh:mm"
    #             # and then converting it to an int
    #             start_time = int(start_time[0:2] + start_time[3:])
    #             end_time = int(end_time[0:2] + end_time[3:])

    #             if curr_time >= start_time and curr_time <= end_time:
    #                 constraint_matrix[k][course_to_index[curr_course]] = 1
    #         k += 1

    #     return constraint_matrix

    # time_conflict_matrix_np = time_conflict_matrix_np()

################################
# 10 - No Two Same Courses Constraint:

def dict_w_same_codes_func(possible_courses):
    """Groups courses that are the same (but different
    sections/campuses) together

    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        dict: Format of dictionary returned is
                {Course Code : [all courses that have the same course code]}
    """

    same_codes = {}
    for course in possible_courses:
        # Possible error for courses such as
        # "CSCI 181Y" isnt the same as "CSCI 181B"
        if course[0:8] in same_codes:
            same_codes[course[0:8]].append(course)
        else:
            same_codes[course[0:8]] = [course]

    return same_codes

def no_same_courses_matrix_func(possible_courses, course_to_index, dict_w_same_codes):
    """Creates constraint matrix that ensures that the solution provided
        doesn"t include two courses that are essentially
       the same but at different campuses or different timings.
       In the mod file, the following condition ensures it: Ax <= 1

    Global Variables Needed:
        dict_w_same_codes (dict, optional): Defaults to dict_w_same_codes.
        course_to_index (dict, optional): Defaults to course_to_index.
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        List of lists: 2-D Matrix where the rows are the unique courses being
                       offered and the value of an element
                       in the row is a zero or one depending
                       on whether it is essentially the same course as its
                       corresponding row.
    """

    num_of_courses = len(possible_courses)

    constraint_matrix = []
    for key in dict_w_same_codes.keys():
        curr_row = [0]*num_of_courses
        for course in possible_courses:
            if key in course:
                curr_row[course_to_index[course]] = 1

        constraint_matrix.append(curr_row)

    return constraint_matrix

####################################
# 11. Requirements Constraint Matrix:

hsa_codes = {"DANC", "WRIT", "ORST", "PPA", "DS", "ARBT", "JAPN", "CHNT", "MSL",
            "CASA", "ASIA", "ART", "GWS", "GREK", "GLAS", "LATN", "SPEC",
            "GOVT", "RUST", "HMSC", "SPCH", "CHST", "CREA", "PORT", "LEAD",
            "ARCN", "SPAN", "ITAL", "MLLC", "MES", "MS", "PPE", "RLIT", "LGST",
            "POST", "LAST", "FREN", "RUSS", "STS", "GEOG", "GRMT", "ARBC",
            "FHS", "AMST", "POLI", "ARHI", "MUS", "MENA", "LGCS", "CLAS",
            "KRNT", "LIT", "JPNT", "ENGL", "MCBI", "CGS", "FS", "HIST", "CHLT",
            "CHIN", "SOC", "MOBI", "FLAN", "ECON", "MCSI", "EA", "ANTH",
            "FIN", "EDUC", "PHIL", "GEOL", "RLST", "FWS", "THEA", "IR", "GERM",
            "ID", "ASAM", "HSA", "KORE", "HUM", "AFRI", "PSYC"}

# Majors:

# CS-MATH Major
def cs_math_major_reqs_matrix_func(possible_courses,
                           all_prev_courses, 
                           dict_w_same_codes, 
                           course_to_index):
    
    num_rows = 6 # 6 requirements for the CS-math major
    
    constraint_matrix = np.zeros(shape=(num_rows, len(possible_courses)), dtype=int)   

    for course in possible_courses:
        curr_code = re.search(r"[^\s]+", course)
        if curr_code:
            curr_code = curr_code.group(0)

        # First Row: Four Kernel Courses in Computer Science and Mathematics
        if ((course[0:8] == "MATH 055") or
            (course[0:8] == "CSCI 060") or
            (course[0:8] == "CSCI 081") or
            (course[0:8] == "CSCI 140")):

            contraint_matrix[0][course_to_index[course]] = 1
        
        # Second Row: Two Computer Science Courses
        elif (course[0:8] == "CSCI 070") or (course[0:8] == "CSCI 131"):
            constraint_matrix[1][course_to_index[course]] = 1

        
        # Third Row: Two Mathematics Courses
        elif (course[0:8]== "MATH 131") or (course[0:8] == "MATH 171"):
            constraint_matrix[2][course_to_index[course]] = 1

        # Fourth Row: Clinic
        elif (course[0:8]== "CSMT 183") or (course[0:8] == "CSMT 184"):
            constraint_matrix[3][course_to_index[course]] = 1

        # Fifth Row: Math courses above 100
        # (TODO: need to remove "strange" courses)
        elif course[0:6]== "MATH 1":
            constraint_matrix[4][course_to_index[course]] = 1

        # Sixth Row: CS courses above 100
        # (TODO: need to remove "strange" courses):
        elif course[0:6] == "CSCI 1":
            constraint_matrix[5][course_to_index[course]] = 1

    
    return list(constraint_matrix)


# CS Major
def cs_major_reqs_matrix_func(possible_courses,
                           all_prev_courses, 
                           dict_w_same_codes, 
                           course_to_index):
    
    num_rows = 4 # 4 requirements for the CS major
    
    constraint_matrix = np.zeros(shape=(num_rows, len(possible_courses)), dtype=int)   

    for course in possible_courses:
        curr_code = re.search(r"[^\s]+", course)
        if curr_code:
            curr_code = curr_code.group(0)
 
        cs_foundation_requirement_courses = {
            "CSCI 060",
            "CSCI 042",
            "MATH 055",
            "CSCI 070",
            "CSCI 081",
        }
     
        cs_kernel_requirement_courses = {
            "CSCI 105",
            "CSCI 121",
            "CSCI 131",
            "CSCI 140"
        }
   
        cs_not_elective_requirement_courses = {
            "CSCI 195",
            "CSCI 192",
            "CSCI 191",
            "CSCI 190",
            "CSCI 189",
            "CSCI 188",
            "CSCI 184",
            "CSCI 183"
        }
        
        # First Row: CS Foundation Requirement
        if course[0:8] in cs_foundation_requirement_courses:
            contraint_matrix[0][course_to_index[course]] = 1
        
        # Second Row: CS Kernel Requirement
        elif course[0:8] in cs_kernel_requirement_courses:
            constraint_matrix[1][course_to_index[course]] = 1

        # Third Row: CS Elective Requirement
        # CS courses above 100
        elif (course[0:6] == "CSCI 1") and (course[0:8] not in cs_not_elective_requirement_courses):
            constraint_matrix[2][course_to_index[course]] = 1
            
        # Fourth Row: Clinic
        elif (course[0:8]== "CSMT 183") or (course[0:8] == "CSMT 184"):
            constraint_matrix[3][course_to_index[course]] = 1

    return list(constraint_matrix)

# ENGR Major
def engr_major_reqs_matrix_func(possible_courses,
                           all_prev_courses, 
                           dict_w_same_codes, 
                           course_to_index):
    
    num_rows = 5 # 5 requirements for the Engr major
    
    constraint_matrix = np.zeros(shape=(num_rows, len(possible_courses)), dtype=int)   

    for course in possible_courses:
        curr_code = re.search(r"[^\s]+", course)
        if curr_code:
            curr_code = curr_code.group(0)
        
        
        engr_design_requirement_courses = {
            "ENGR 004",
            "ENGR 080"
        }
        
        engr_systems_requirement_courses = {
            "ENGR 079",
            "ENGR 101",
            "ENGR 102"
        }
        
        engr_science_requirement_courses = {
            "ENGR 082",
            "ENGR 083",
            "ENGR 084",
            "ENGR 085",
            "ENGR 086"
        }
        
        engr_clinic_courses = {
            "ENGR 111",
            "ENGR 112",
            "ENGR 113"
        }
        
        # First Row: Engineering Design Requirement (w/o clinic)
        if course[0:8] in engr_design_requirement_courses:
            contraint_matrix[0][course_to_index[course]] = 1
        
        # Second Row: Engineering Systems Requirement
        elif course[0:8] in engr_systems_requirement_courses:
            constraint_matrix[1][course_to_index[course]] = 1
        
        # Third Row: Engr Science Requirement (e72 not added since its a half sem course)
        elif course[0:8] in engr_science_requirement_courses:
            constraint_matrix[2][course_to_index[course]] = 1
            
        # Fourth Row: Clinic
        elif course[0:8] in engr_clinic_courses:
            constraint_matrix[3][course_to_index[course]] = 1        
        
        # Fifth Row: Electives
        elif course[0:4] == "ENGR":
            constraint_matrix[4][course_to_index[course]] = 1

    return list(constraint_matrix)

# HSA:
def hsa_reqs_matrix(possible_courses, all_prev_courses, dict_w_same_codes, course_to_index, hsa_codes, hsa_concentration):
    
    # Needed for HSA breadth requirement
    prev_course_codes = set()
    for course in all_prev_courses:
        curr_code = re.search(r"[^\s]+", course)
        if curr_code:
            curr_code = curr_code.group(0)
            if curr_code not in prev_course_codes:
                prev_course_codes.add(curr_code)


    num_of_courses = len(possible_courses)
    
    hsa_constraint_matrix = np.zeros(shape=(4, num_of_courses), dtype=int)

    for course in possible_courses:
        curr_code = re.search(r"[^\s]+", course)
        
        if curr_code:
            curr_code = curr_code.group(0)

        # HSA Requirements (this stays the same for all majors):
        if curr_code in hsa_codes:

            # Seventh Row: HSA Breadth Requirement
            if curr_code != hsa_concentration:
                if curr_code not in prev_course_codes:
                    hsa_constraint_matrix[0][course_to_index[course]] = 1

            # Eight Row: HSA Concentration Requirement
            else:
                hsa_constraint_matrix[1][course_to_index[course]] = 1

            # Ninth Row: HSA Mudd Hum Requirement
            t = course.split(" ")
            if t[2][0:2] == "HM":
                hsa_constraint_matrix[2][course_to_index[course]] = 1

            # Tenth Row: HSA General Requirement
            hsa_constraint_matrix[3][course_to_index[course]] = 1

    return list(hsa_constraint_matrix)

# All Reqs:

def requirements_matrix_func(possible_courses, all_prev_courses, dict_w_same_codes, course_to_index, hsa_codes, hsa_concentration):
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


    Not adding Colloquia Row :--> because its not really a constraint
    since it doesnt have a fixed time nor does it count towards an overload

    Global Variables Needed:
        dict_w_same_codes ([type], optional): Defaults to dict_w_same_codes.
        course_to_index ([type], optional): Defaults to course_to_index.
        possible_courses ([type], optional): Defaults to possible_courses.
        hsa_codes ([type], optional): Defaults to hsa_codes.
        hsaConcentration ([type], optional): Defaults to hsaConcentration.
        all_prev_courses ([type], optional): Defaults to all_prev_courses.

    Returns:
        List of lists: 2-D Matrix where each row represents a
        specific requirement and each column represents a specific course
    """
    major_matrix = []
    
    if curr_major == "CS-MATH":
        major_matrix = cs_math_major_reqs_matrix_func(possible_courses, all_prev_courses, dict_w_same_codes, course_to_index)
    
    if curr_major == "CS":
        major_matrix = cs_major_reqs_matrix_func(possible_courses, all_prev_courses, dict_w_same_codes, course_to_index)
    
    if curr_major == "ENGR":
        major_matrix = engr_major_reqs_matrix_func(possible_courses, all_prev_courses, dict_w_same_codes, course_to_index)
        
    hsa_matrix = hsa_reqs_matrix(possible_courses, all_prev_courses, dict_w_same_codes, course_to_index, hsa_codes, hsa_concentration)
    
    return major_matrix + hsa_matrix

######################################
# 12. Costs

def costs_func(possible_courses, course_to_index, curr_preferences):
    """Row of costs corresponding to each possible course.

    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.
        course_to_index (dict, optional): Defaults to course_to_index.
        preferences (dict, optional): Defaults to myPreferences.

    Returns:
        List: Row of costs corresponding to each possible course.
    """
    num_of_courses = len(possible_courses)

    costs_row = [0]*num_of_courses

    for course in possible_courses:

        if course in curr_preferences:
            costs_row[course_to_index[course]] = curr_preferences[course]

        # (TODO: Edit this based on survey results.)
        # Default costs for courses
        else:
            # CS Courses = Cost of 5
            if course[0:4] == "CSCI":
                costs_row[course_to_index[course]] = 0

            # ENGR Courses = Cost of 4
            elif course[0:4] == "ENGR":
                costs_row[course_to_index[course]] = 7
            
            # Math Courses = Cost of 4
            elif course[0:4] == "MATH":
                costs_row[course_to_index[course]] = 0

            # Philosophy Courses = Cost of 3
            elif course[0:4] == "PHIL":
                costs_row[course_to_index[course]] = 0

            # All other courses = Cost of 2
            else:
                costs_row[course_to_index[course]] = 3

    return costs_row


######################################

def alternates_matrix_func(curr_alternates, possible_courses, course_to_index):
    n=len(possible_courses)
    
    matrix = []
    
    for item in curr_alternates:
        curr_row = [0]*n
        
        alt_courses = item[0]
        alt_limit = item[1]
        
        for course in possible_courses:
            if course in alt_courses:
                curr_row[course_to_index[course]] = 1
        
        matrix.append(curr_row)
    
    return matrix
            
######################################

def createDat(dir_path, filename):
    res = ""

    with open(dir_path + r"costs_names.txt", 'r') as f:
        costs_names = f.read()
        
    with open(dir_path + r"course_names.txt", 'r') as f:
        course_names = f.read()

    with open(dir_path + r"requirements_matrix.txt", 'r') as f:
        requirements_matrix = f.read()
        
    with open(dir_path + r"set_timeSlots.txt", 'r') as f:
        set_timeSlots = f.read()
        
    with open(dir_path + r"set_uniqueCourses.txt", 'r') as f:
        set_uniqueCourses = f.read()

    with open(dir_path + r"time_conflict_matrix.txt", 'r') as f:
        time_conflict_matrix = f.read()

    with open(dir_path + r"unique_courses_matrix.txt", 'r') as f:
        unique_courses_matrix = f.read()
        
    with open(dir_path + r"set_alternates.txt", 'r') as f:
        set_alternates = f.read()
    
    with open(dir_path + r"alternates_matrix.txt", 'r') as f:
        alternates_matrix = f.read()
        
    with open(dir_path + r"alternates_lower_limits.txt", 'r') as f:
        alternates_lower_limits = f.read()
        
    with open(dir_path + r"alternates_upper_limits.txt", 'r') as f:
        alternates_upper_limits = f.read()
        
                
    res += "set courses := " 
    res += "\n    "
    res += course_names + "\n;"
    res += "\n\n"


    res += "set requirements := "
    res += "\n    "
    res += "r1 r2 r3 r4 r5 r6 r7 r8 r9\n;"
    res += "\n\n"

    res += "set timeSlots := "
    res += "\n    "
    res += set_timeSlots + "\n;"
    res += "\n\n"

    res += "set uniqueCourses := "
    res += "\n    "
    res += set_uniqueCourses + "\n;"
    res += "\n\n"
    
    res += "set alternates := "
    res += "\n    "
    res += set_alternates + "\n;"
    res += "\n\n"

    res += "param costs := "
    res += "\n    "
    res += costs_names + "\n;"
    res += "\n\n"

    res += "param time : "
    res += "\n    "
    res += course_names + " := \n"
    res += "\n    "
    res += time_conflict_matrix + "\n;"
    res += "\n\n"

    res += "param counts : "
    res += "\n    "
    res += course_names + " := \n"
    res += "\n    "
    res += requirements_matrix + "\n;"
    res += "\n\n"

    res += "param necessary := "
    res += "\n    "
    res += curr_desired_reqs + "\n;"
    res += "\n\n"

    res += "param unique : "
    res += "\n    "
    res += course_names + " := \n"
    res += "\n    "
    res += unique_courses_matrix + "\n;"
    res += "\n\n"
    
    res += "param alternatesLowerLimits := "
    res += "\n    "
    res += alternates_lower_limits + "\n;"
    res += "\n\n"
    
    res += "param alternatesUpperLimits := "
    res += "\n    "
    res += alternates_upper_limits + "\n;"
    res += "\n\n"

    res += "param alternatesMatrix : "
    res += "\n    "
    res += course_names + " := \n"
    res += "\n    "
    res += alternates_matrix + "\n;"
    res += "\n\n"


    with open(r'./amplFiles/' + filename, 'w') as fp:
        fp.write(res)

#####################################

def create_ampl_command(dat_filename):
    
    data_file = '\\' + dat_filename + ".dat"
    
    ampl_mod_command = r"model 'C:\Users\Shaurya\Desktop\math187_project\amplFiles\model.mod'; "

    ampl_dat_command = r"data C:\Users\Shaurya\Desktop\math187_project\amplFiles" + data_file + r";"

    ampl_solve_command = r"solve;"

    ampl_option_command = r"option omit_zero_rows 1;"

    ampl_solver_command = r"option solver './cplex';"

    ampl_display_command = r"display x;"

    ampl_all_commands = ampl_mod_command + "\n" + ampl_dat_command + "\n" + ampl_solver_command + "\n" + ampl_solve_command + "\n" + ampl_option_command + "\n" + ampl_display_command

    with open('exec.run', 'w') as f:
        f.write(ampl_all_commands)
    

#####################################