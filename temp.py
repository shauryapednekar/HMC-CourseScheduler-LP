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


def costs_func(raw_data, possible_courses, course_to_index, curr_preferences, keywords={}, profs = {}):
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














