
from user.userInputs.desiredReqs import curr_desired_reqs

dir_path = r"amplData/2/"
def createDat(dir_path):
    res = ""
    filename = "test1.dat"

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
        
        
    res += "set courses := " 
    res += "\n    "
    res += course_names + "\n;"
    res += "\n\n"


    res += "set requirements := "
    res += "\n    "
    res += "r1 r2 r3 r4 r5 r6 r7 r8 r9 r10\n;"
    res += "\n\n"

    res += "set timeSlots := "
    res += "\n    "
    res += set_timeSlots + "\n;"
    res += "\n\n"

    res += "set uniqueCourses := "
    res += "\n    "
    res += set_uniqueCourses + "\n;"
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

    with open(r'./amplFiles/' + filename, 'w') as fp:
        fp.write(res)