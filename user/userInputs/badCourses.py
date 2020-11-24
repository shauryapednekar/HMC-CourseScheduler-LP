shaurya_bad_courses = set()
shaurya_bad_courses = {
    "CSCI_181V_PO-01",
    "CSCI_186_HM-01",
    "CSCI_184_HM-01",
    "CSCI_191_PO",
    "MATH_03",
    "MATH 197",
    "CSCI_036",
    "MATH_0",
    "CSCI0"
    }

bad_courses = shaurya_bad_courses


def helper():
    res = set()
    for course in bad_courses:
        course = course.replace("_", " ")
        res.add(course)
        
    return res

bad_courses = helper()

# print(bad_courses)