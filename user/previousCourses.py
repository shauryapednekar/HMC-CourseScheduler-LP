
shaurya = {
    "first_sem_courses": {
        "BIOL 023",
        "CHEM 023A",
        "CSCI 005",
        "CSCI 005L",
        "MATH 021",
        "MATH 030",  # not really
        "MATH 030G",
        "MATH 035",
        "PE 004",
        "PE 043",
        "PE 240",
        "PHYS 023",
        "POLI 120",
        "WRIT 001",
    },

    "second_sem_courses": {
        "BIOL 052",
        "CHEM 023",
        "CHEM 024",
        "HSA 010",
        "MATH 040",
        "MATH 045",
        "MATH 055",
        "PE 035B",
        "PE 043",
        "PHYS 024",
    },

    "third_sem_courses": {
        "CSCI 060",
        "CSCI 189",
        "ECON 104",
        "ENGR 079",
        "ENGR 079P",
        "MATH 060",
        "MATH 065",
        "PE 008B",
        "PE 043",
        "PHYS 050",
        "PHYS 051",
    },

    "fourth_sem_courses": {
        "CSCI 070",
        "CSCI 070L",
        "CSCI 081",
        "ECON 053",
        "ECON 136",
        "MATH 171",
        "PHIL 090",
    },

    "fifth_sem_courses": {
        "CSCI 131",
        "CSCI 140",
        "CSCI 195",
        "ECON 129",
        "MATH 113",
        "MATH 131",
        "MATH 187",
    }
}

shreya = {
    
    "first_sem_courses": {
        "BIOL 023",
        "CHEM 023A",
        "CSCI 005",
        "CSCI 005L",
        "MATH 021",
        "MATH 030",  # not really
        "MATH 030G",
        "MATH 035",
        "PHYS 023",
        "WRIT 001",
    },
    
    "second_sem_courses": {
        "BIOL 052",
        "CHEM 023",
        "CHEM 024",
        "HSA 010",
        "MATH 040",
        "MATH 045",
        "PHYS 024",
        "ENGR 004"
    },
    
    "third_sem_courses": {
        "CSCI 060",
        "CSCI 189",
        "ECON 104",
        "ENGR 079",
        "ENGR 079P",
        "MATH 060",
        "MATH 065",
        "PE 008B",
        "PE 043",
        "PHYS 051",
        "MATH 055"
    },
    
    "fourth_sem_courses": {
        "CSCI 070",
        "CSCI 070L",
        "ENGR 072",
        "ENGR 084",
        "ENGR 191",
        "PHYS 050",
        "PSYC 040",
    },
    
    "fifth_sem_courses": {
        "ENGR 085",
        "ENGR 083",
        "ENGR 101",
        "PHIL 090",
        "ECON 129",
        "ENGR 191"
    }
    
}


lis = []
curr_user = shreya

for key in curr_user:
    lis.append(curr_user[key])
    
    
all_prev_courses = set().union(*lis)


# first_sem_courses+second_sem_courses + \
#     third_sem_courses+fourth_sem_courses+fifth_sem_courses
