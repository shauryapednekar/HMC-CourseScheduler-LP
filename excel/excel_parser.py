import pandas as pd
from userInput import *


df = pd.read_excel(excel_file_name, sheet_name= excel_sheet_name)

# print(df)

# print(df.columns.ravel())

def clean_list(l):
    """Removes nan values from lists

    Args:
        l (list): list that needs to be cleaned
    """
    return [x for x in l if str(x) != 'nan']

# Preferences:
courses = df.iloc[:, 0].tolist()
courses_ranking = df.iloc[:, 1].tolist()

cleaned_courses = clean_list(courses)

cleaned_course_ranking = [int(x) for x in courses_ranking if str(x) != 'nan' ]

curr_preferences = {}

for i in range(len(cleaned_courses)):
    curr_preferences[cleaned_courses[i]] = cleaned_course_ranking[i]
   
# Requirements:

reqs = df.iloc[:, 4].tolist()

reqs = clean_list(reqs) 
reqs, curr_major, curr_hsa_conc = reqs[:-2], reqs[-2], reqs[-1]

count = 1

curr_desired_reqs = ""
for req in reqs:
    curr_desired_reqs += "r" + str(count) + " " + str(req) + " "
    count += 1
    
# print(curr_desired_reqs)

# -TODO: Add support for other majors
num_requirements = {
    "CS-MATH": "r1 r2 r3 r4 r5 r6 r7 r8 r9 r10",
    "CS": "r1 r2 r3 r4 r5 r6 r7 r8",
    "ENGR":  "r1 r2 r3 r4 r5 r6 r7 r8 r9"
}

curr_num_reqs = num_requirements[curr_major]


########################## Previous Courses
curr_previous_courses = df.iloc[:, 6].tolist()

curr_previous_courses = set(clean_list(curr_previous_courses))

# print(curr_previous_courses)


######################## Bad Courses:
curr_bad_courses = df.iloc[: , 8].tolist()
curr_bad_courses = set(clean_list(curr_bad_courses))

# print(curr_bad_courses)


######################## Alternates:
lower_bounds = df.iloc[: , 10].tolist()
upper_bounds = df.iloc[: , 11].tolist()

lower_bounds = [int(x) for x in lower_bounds if str(x) != 'nan']
upper_bounds = [int(x) for x in upper_bounds if str(x) != 'nan']

curr_alternates = []

for i in range(len(lower_bounds)):
    alternates = df.iloc[i, 12:].tolist()
    alternates = set(clean_list(alternates))
    curr_ele = [alternates, [lower_bounds[i], upper_bounds[i]]]
    curr_alternates.append(curr_ele)
    # print(alternates)
    
# print(curr_alternates)
    

############


