import pandas as pd
from userInput import *

df = pd.read_excel(excel_file_name, sheet_name= excel_sheet_name)

df.columns = ["Meta-Preferences",
              "Meta-Preferences Input",
              "Blank",
              
              "Course Preferences",
              "Course Rankings",
              "Blank",
              
              "Default Course Preferences",
              "Default Course Rankings",
              "Blank",
              
              "Requirements",
              "Requirements Input",
              "Blank",
              
              "Courses Taken Previously",
              "Blank",
              
              "Courses you do not want",
              "Blank",
              
              "Alternatives",
              "Total Number of Courses",
              'Set 1', 'Set 2', 'Set 3', 'Set 4', 'Set 5', 'Set 6', 'Set 7', 'Set 8', 'Set 9', 'Set 10', 'Set 11', 'Set 12', 'Set 13', 'Set 14', 'Set 15', 'Set 16', 'Set 17', 'Set 18', 'Set 19', 'Set 20', 'Set 21', 'Set 22', 'Set 23', 'Set 24', 'Set 25', 'Set 26', 'Set 27', 'Set 28', 'Set 29', 'Set 30', 'Set 31', 'Set 32', 'Set 33', 'Set 34', 'Set 35'
              ]

def clean_list(l):
    """Removes nan values from lists

    Args:
        l (list): list that needs to be cleaned
    """
    return [x for x in l if str(x) != 'nan']
    
########################## Meta-Preferences
meta_preferences = clean_list(df["Meta-Preferences Input"].tolist())

# If user wants to consider only selected courses or not
if meta_preferences[0] == "Only courses from the Course Preferences column":
    only_selected = True
else:
    only_selected = False

# If user wants to consider requirements
if meta_preferences[1] == "Yes":
    consider_requirements = True
else:
    consider_requirements = False

curr_major = meta_preferences[2]
curr_hsa_conc = meta_preferences[3]
    
########################## Course Preferences:
courses = df["Course Preferences"].tolist() 
course_rankings = df["Course Rankings"].tolist()
cleaned_courses = clean_list(courses)
cleaned_course_rankings = [int(x) for x in course_rankings if str(x) != 'nan' ]
# Creates dictionary in {course: ranking} format
curr_preferences = {}
for i in range(len(cleaned_courses)):
    curr_preferences[cleaned_courses[i]] = cleaned_course_rankings[i]
   

########################## Default Course Preferences:
default_courses = clean_list(df["Default Course Preferences"].tolist())
default_course_rankings = clean_list(df["Default Course Rankings"].tolist())

curr_default_preferences = [[course, course_ranking] for course, course_ranking in zip(default_courses, default_course_rankings)]

curr_base_ranking = curr_default_preferences[0][1]
    
# print(curr_default_preferences)

########################## Requirements:

# Number of different requirements by major
num_requirements = {
    "CS-MATH": 10,
    "CS": 8,
    "ENGR": 9
}

# Creates list of desired reqs from the excel sheet
if consider_requirements:
    reqs = clean_list(df["Requirements Input"].tolist()) 
else:
    # list of zeroes if user does not want program to consider reqs
    reqs = [0 for i in range(num_requirements[curr_major])]

# Creating string thats needed for the .dat file in ampl
count = 1
curr_desired_reqs = ""
for req in reqs:
    curr_desired_reqs += "r" + str(count) + " " + str(req) + " "
    count += 1

# -TODO: Add support for other majors
# The following format is needed for the .dat file in ampl
requirements_string = {
    "CS-MATH": "r1 r2 r3 r4 r5 r6 r7 r8 r9 r10",
    "CS": "r1 r2 r3 r4 r5 r6 r7 r8",
    "ENGR":  "r1 r2 r3 r4 r5 r6 r7 r8 r9"
}

curr_num_reqs = requirements_string[curr_major]

########################## Previous Courses
curr_previous_courses = df["Courses Taken Previously"].tolist()

curr_previous_courses = set(clean_list(curr_previous_courses))

######################## Bad Courses:
curr_bad_courses = df["Courses you do not want"].tolist()
curr_bad_courses = set(clean_list(curr_bad_courses))

######################## Alternates:
x = df.iloc[: , 14:]
num_alts = x.shape[1]
lower_bounds = []
upper_bounds = []
curr_alternates = []

for i in range(num_alts):
    curr_alt = df.iloc[:, i+17]
    curr_alt = [x for x in curr_alt if str(x) != 'nan']
    if curr_alt == []:
        break
    lower_bounds.append(int(curr_alt[0]))
    upper_bounds.append(int(curr_alt[1]))
    curr_ele = [curr_alt[2:], [curr_alt[0], curr_alt[1]]]
    curr_alternates.append(curr_ele)

# print(curr_alternates)