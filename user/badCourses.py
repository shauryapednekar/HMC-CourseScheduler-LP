# Courses that shouldnt appear in the solution
default_bad_courses = set()

# Shaurya
shaurya_bad_courses = set()

shaurya_bad_courses = {
    "CSCI_181V_PO-01",
    "CSCI_186_HM-01",
    "CSCI_184_HM-01",
    "CSCI_191_PO",
    "MATH 197",
    "MATH_0", # Any courses starting with MATH 0
    "CSCI_0"
    }

shreya_bad_courses = {
    "PHYS",
    "MATH",
    "BIOl",
    "CSCI",
    "CHEM",
    "ECON"
}


################################
# -TODO: Set to current user
bad_courses = shaurya_bad_courses
################################

def helper():
    res = set()
    for course in bad_courses:
        course = course.replace("_", " ")
        res.add(course)
        
    return res

bad_courses = helper()
