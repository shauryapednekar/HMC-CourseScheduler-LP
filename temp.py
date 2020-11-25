"""Main Course Scheduling Script"""

import json
import time
import re
import os
# import numpy as np

# User Inputs Needed
from user.previousCourses import all_prev_courses
from user.preferences import curr_preferences
from user.badCourses import bad_courses
from user.desiredReqs import curr_hsa_conc
from user.desiredReqs import curr_desired_reqs
from user.alternates import curr_alternates
from user.desiredReqs import curr_major

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
    # print("lis: ", lis)
    # print("all_prev_courses:", all_prev_courses)
    
    for elem in lis:
        if elem not in all_prev_courses:
            return False

    return True


with open(r"preReqs/all_prereqs_edited.json", encoding="utf-8") as f:
    prereqs_edited = json.load(f)
    
    
def next_sem_possible_courses_due_to_prereqs(all_prev_courses, possible_courses):
    """Creates list of possible courses according to previously taken courses
    and prereqs.

    Returns:
        list: list of possible courses according to previously taken courses
        and prereqs
    """

    list_of_possible_courses = []

    for course in possible_courses:
    
        # If the course has prereqs
        if course in prereqs_edited:
            
                curr_prereqs = prereqs_edited[course][1:]
                if ["POI"] in curr_prereqs:
                    curr_prereqs.remove(["POI"])

                # If prereqs are fulfilled, True will be present in temp
                # Otherwise, it will be only False values

                temp = ([helper_next_sem_possible_courses_due_to_prereqs (prereq, all_prev_courses)
                        for prereq in curr_prereqs])
                
                print(temp)
                if True in temp:
                    list_of_possible_courses.append(course)
                
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

    return list_of_possible_courses

possible_courses = possible_courses_func()

new_possible_courses = next_sem_possible_courses_due_to_prereqs(all_prev_courses, possible_courses)

if "ECON 150 CM-01" in new_possible_courses:
    print("fail")
else:
    print("success!!!")















