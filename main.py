"""Main Course Scheduling Script"""

import json
import time
import re
import os
import numpy as np

# User Inputs Needed
from user.previousCourses import all_prev_courses
from user.preferences import curr_preferences
from user.badCourses import bad_courses
from user.desiredReqs import curr_hsa_conc
from user.desiredReqs import curr_desired_reqs
from user.alternates import curr_alternates
from user.desiredReqs import curr_major


# All Functions
from optimizer2 import * 


def main(selected=False, test_num=0, major="CS-Math"):
    
    if selected:
        possible_courses = list(curr_preferences.keys())
    
    else:
         
        possible_courses = possible_courses_func()
        
        possible_courses = only_keep_three_credit_classes(raw_data, 
                                                        possible_courses)
        
        possible_courses = remove_prev_courses(all_prev_courses,
                                            possible_courses)
        
        subject_codes = subject_codes_func(possible_courses)
        
        possible_courses = next_sem_possible_courses_due_to_prereqs(all_prev_courses, possible_courses)
        
        possible_courses = remove_bad_courses(possible_courses, bad_courses)
    
    course_to_variable_name, course_to_index = course_code_to_variable_and_index(possible_courses)
    
    variable_name_to_course = ({value : key for key, value in
                            course_to_variable_name.items()})
    
    time_conflict_matrix = time_conflict_matrix_func(course_to_variable_name,
                                                course_to_index,
                                                raw_data,
                                                possible_courses)
    
    dict_w_same_codes = dict_w_same_codes_func(possible_courses)
    
    no_same_courses_matrix = no_same_courses_matrix_func(possible_courses,
                                                    course_to_index,
                                                    dict_w_same_codes)

    hsa_concentration = curr_hsa_conc
    
    requirements_matrix = requirements_matrix_func(possible_courses,
                                              all_prev_courses,
                                              dict_w_same_codes,
                                              course_to_index,
                                              hsa_codes,
                                              hsa_concentration)

    costs = costs_func(possible_courses,
                  course_to_index,
                  curr_preferences)

    alternates_matrix = alternates_matrix_func(curr_alternates,
                                               possible_courses,
                                               course_to_index)
    
    dir_path = r"amplData/" + str(test_num) + "/"
    
    os.makedirs(os.path.dirname(dir_path), exist_ok=True)
    
    with open(dir_path + r"set_timeSlots.txt", "w+") as f:
        i = 0
        for times in time_conflict_matrix:
            f.write("t" + str(i) + " ")
            i += 1

    with open(dir_path + r"time_conflict_matrix.txt", "w") as f:
        i = 0
        for times in time_conflict_matrix:
            f.write("t" + str(i) + " ")
            i += 1
            for c in times:
                f.write(str(c) + " ")
            f.write("\n    ")
            
    with open(dir_path + r"set_uniqueCourses.txt", "w") as f:
        i = 0
        for unique in dict_w_same_codes.keys():
            f.write("c" + str(i) + " ")
            i += 1

    with open(dir_path + r"unique_courses_matrix.txt", "w") as f:
        i = 0
        for mainCourse in no_same_courses_matrix:
            f.write("c" + str(i) + " ")
            i += 1
            for c in mainCourse:
                f.write(str(c) + " ")
            f.write("\n    ")
            
    with open(dir_path + r"requirements_matrix.txt", "w") as f:
        i = 1
        for requirement in requirements_matrix:
            f.write("r" + str(i) + " ")
            i += 1
            for c in requirement:
                f.write(str(c) + " ")
            f.write("\n    ")
    
    with open(dir_path + r"course_names.txt", "w") as f:
        i = 0
        for c in possible_courses:
            c = c.replace(" ", "_")
            f.write(c + " ")

    with open(dir_path+ r"costs_names.txt", "w") as f:
        i = 0
        for cost in costs:
            c = possible_courses[i]
            c = c.replace(" ", "_")
            f.write(c + " " + str(cost) + " ")
            i += 1
    
    with open(dir_path + r"set_alternates.txt", "w") as f:
        i = 0
        for alternate in alternates_matrix:
            f.write("a" + str(i) + " ")
            i += 1
            
        f.write("\n")
        
    with open(dir_path + r"alternates_lower_limits.txt", "w") as f:
        i = 0
        for alternate in curr_alternates:
            f.write("a" + str(i) + " " + str(alternate[1][0]) + " ")
            i += 1
            
        f.write("\n")
    
    with open(dir_path + r"alternates_upper_limits.txt", "w") as f:
        i = 0
        for alternate in curr_alternates:
            f.write("a" + str(i) + " " + str(alternate[1][1]) + " ")
            i += 1
            
        f.write("\n")
    
    with open(dir_path + r"alternates_matrix.txt", "w") as f:
        i = 0
        for alternate in alternates_matrix:
            f.write("a" + str(i) + " ")
            i += 1
            for c in alternate:
                f.write(str(c) + " ")
            f.write("\n    ")
    
    time.sleep(3)
    
    createDat(dir_path, "test" + str(test_num) + ".dat")
    
main(selected=False, test_num=8)