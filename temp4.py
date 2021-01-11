from excel.excel_to_var import curr_alternates as excel_alternatives
from excel.excel_to_var import curr_previous_courses as excel_previous_courses
from excel.excel_to_var import curr_preferences as excel_curr_preferences
from excel.excel_to_var import curr_hsa_conc as excel_hsa_conc
from excel.excel_to_var import curr_desired_reqs as excel_desired_reqs
from excel.excel_to_var import curr_num_reqs as excel_num_reqs

from user.curr_user import *

if curr_alternates != excel_alternatives:
    print("curr_alternatives: " , curr_alternates)
    print("excel_alternatives: ", excel_alternatives)
    print()
    print()
    
if curr_previous_courses != excel_previous_courses:
    # print("curr_previous_courses: ",curr_previous_courses)
    # print("excel_previous_courses: ",excel_previous_courses)
    for course in curr_previous_courses:
        if course not in excel_previous_courses:
            print(course)
    print()
    print()

if curr_preferences != excel_curr_preferences:
    print("curr_preferences: ", curr_preferences)
    print("excel_previous_courses: ", excel_previous_courses)
    print()
    print()

if curr_desired_reqs != excel_desired_reqs:
    print("curr_desired_reqs: ", curr_desired_reqs)
    print("excel_desired_reqs: ", excel_desired_reqs)
    print()
    print()

if curr_num_reqs != excel_num_reqs:
    print("curr_desired_reqs: ", curr_desired_reqs)
    print("excel_num_reqs: ", excel_num_reqs)
    print()
    print()
