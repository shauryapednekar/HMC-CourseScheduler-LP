from user.userData.alternates import *
from user.userData.badCourses import *
from user.userData.desiredReqs import *
from user.userData.preferences import *
from user.userData.previousCourses import *

# current dat filename:
curr_dat_filename = "test19" #TODO

# alternates.py
curr_alternates = shaurya_alternates #TODO

#badCourses.py
curr_bad_courses = shaurya_bad_courses #TODO

# desiredReqs.py
curr_desired_reqs_all = shaurya_desired_reqs_details #TODO

# preferences.py

curr_preferences = shaurya_preferences #TODO

# previousCourses.py
curr_previous_courses = shaurya_previous_courses #TODO



# DATA CLEANING:

# alternates.py

#badCourses.py
curr_bad_courses = hyphens_to_spaces(curr_bad_courses)

# desiredReqs.py
curr_major = curr_desired_reqs_all["major"]
curr_desired_reqs = curr_desired_reqs_all["major_reqs"] + curr_desired_reqs_all["hsa_reqs"]
curr_hsa_conc = curr_desired_reqs_all["hsa_conc"]
curr_num_reqs = num_requirements[curr_major]

# preferences.py

# previousCourses.py
lis = []
for key in curr_previous_courses:
    lis.append(curr_previous_courses[key])
curr_previous_courses = set().union(*lis)