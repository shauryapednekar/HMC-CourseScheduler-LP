majors = {"CS-MATH",
          "CS",
          "MATH",
          "ENGR",
          }

"""
    CS-MATH:
    
    # The space at the end of major_reqs is important!
    major_reqs = "r1 0 r2 0 r3 0 r4 0 r5 0 r6 0 " 
    hsa_reqs = "r7 0 r8 0 r9 0 r10 0"

    1. Four Kernel Courses in Computer Science and Mathematics
    2. Two Computer Science Courses
    3. Two Mathematics Courses
    4. Clinic
    5. Math Electives
    6. CS Electives
    
    7. HSA Breadth
    8. HSA Concentration
    9. HSA Mudd Humms
    10. HSA General
"""


"""
    CS
    
    # The space at the end of major_reqs is important!
    major_reqs = "r1 0 r2 0 r3 0 r4 0 " 
    hsa_reqs = "r5 0 r6 0 r7 0 r8 0"
    
    1. CS Foundation Requirement
    2. CS Kernel Requirement
    3. CS Elective Requirement
    4. Clinic

    5. HSA Breadth
    6. HSA Concentration
    7. HSA Mudd Humms
    8. HSA General
"""

"""
    ENGR
    
    # The space at the end of major_reqs is important!
    major_reqs = "r1 0 r2 0 r3 0 r4 0 r5 0 " 
    hsa_reqs = "r6 0 r7 0 r8 0 r9 0"
    
    
    
    
    1. Engineering Design Requirement (w/o clinic)
    2. Engineering Systems Requirement
    3. Engr Science Requirement (e72 not added since its a half sem course)
    4. Clinic
    5. Electives
    
    6. HSA Breadth
    7. HSA Concentration
    8. HSA Mudd Humms
    9. HSA General
    
    
"""
# Default
default = {
    "major": "",
    "hsa_conc": "",
    "major_reqs": "",
    "hsa_reqs": "",
}

# Shaurya
shaurya = {
    "major": "CS-MATH",
    "hsa_conc": "ECON",
    "major_reqs": "r1 0 r2 0 r3 0 r4 0 r5 1 r6 1 ",
    "hsa_reqs": "r7 1 r8 0 r9 1 r10 1"
    }


# Shreya
shreya = {
    "major": "ENGR",
    "hsa_conc": "ECON",
    "major_reqs": "r1 0 r2 1 r3 0 r4 1 r5 2 ", 
    "hsa_reqs" : "r6 1 r7 1 r8 1 r9 0",
}



# TODO: Adjust Before Running!
curr_user = shreya

curr_major = curr_user["major"]
curr_desired_reqs = curr_user["major_reqs"] + curr_user["hsa_reqs"]
curr_hsa_conc = curr_user["hsa_conc"]