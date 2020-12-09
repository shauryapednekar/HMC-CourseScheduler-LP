# Courses that begin with the following shouldnt appear in the solution
default_bad_courses = set()

# Shaurya
shaurya_bad_courses = {
    "CSCI_181V_PO-01",
    "CSCI_186_HM-01",
    "CSCI_184_HM-01",
    "CSCI_191_PO",
    "MATH 197",
    "MATH_0", # Any courses starting with MATH 0
    "CSCI_0"
    }

# Shreya
shreya_bad_courses = {
    "PHYS",
    "MATH",
    "BIOl",
    "CSCI",
    "CHEM",
    "ECON"
}


################################

# The following function is used in curr_user.py
def hyphens_to_spaces(bad_courses):
    res = set()
    for course in bad_courses:
        course = course.replace("_", " ")
        res.add(course)
        
    return res

