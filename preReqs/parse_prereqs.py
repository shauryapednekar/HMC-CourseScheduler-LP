import json
import re

##################################################
# 1 - Getting all courses that are going to be offered:

with open(r"../rawData/course_data.json", encoding="utf-8") as f:
    rawData = json.load(f)

def possible_courses():
    """Nothing

    Returns:
        list: all courses (complete course code) being offered
    """

    return list(rawData["data"]["courses"].keys())

possible_courses = possible_courses()

###############################################

# with open(r"prereqs1_edited_by_hand.json", encoding="utf-8") as f:
#     prereqs_edited = json.load(f)
    

def subject_codes():
    """Finds all possible subject codes (such as "MATH" and "RLST" etc.).

    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.

    Returns:
        set: All unique subject codes
    """

    codes = set()
    for course in possible_courses:
        # Gets first word of course (until the first space)
        # - which is the subject code:
        curr_code = re.search(r"[^\s]+", course)
        if curr_code:
            curr_code = curr_code.group(0)
            if curr_code not in codes:
                codes.add(curr_code)

    return codes

subject_codes = subject_codes()
    
    
# Prereqs Function that only needs to be run once ("untab" the following block):
def prereqs():
    """Collects prereqs for each course

    Global Variables Needed:
        possible_courses (list, optional): Defaults to possible_courses.
        rawData (dict, optional): Defaults to rawData.
        subject_codes (set, optional): Defaults to subject_codes.

    Returns:
        dict: Dictionary where the keys are the courses that contain
                prerequisites and its values are a list of the
prerequisites.
    """

    # Contains only the courses that have prereqs
    course_to_prereqs = {}

    for course in possible_courses:
        
        # if course not in prereqs_edited:
        description = (rawData["data"]["courses"][course]
["courseDescription"])
        
        if not description:
            prereqs = ""
        elif ("Prerequisite: " not in description) and ("Prerequisites: " not in description):
            prereqs = ""

        # Only finding prereqs for courses that have "Prerequisite:" in
        # their description
        else:
            if "Prerequisite:" in description:
                prereqs = description.partition("Prerequisite: ")[2]
            elif "Prerequisites:" in description:
                prereqs = description.partition("Prerequisites: ")[2]


            replacement_dict = {
                "Arabic": "ARBC",
                "Mathematics": "MATH",
                "Math": "MATH",
                "Korean": "KORE",
                "Writing 1": "WRIT 001",
                "Anthropology": "ANTH",
                "Art": "ART",
                "Physics": "PHYS",
                "Biology": "BIOL",
                "Chemistry": "CHEM",
                "Computer Science": "CSCI",
                "Economics": "ECON",
                "Engineering": "ENGR",
                "French": "FREN",
                "Government": "GOVT",
                "Psychology": "PSYC",
                "Spanish": "SPAN"
            }
            # Replaces subject names to corresponding subject codes
            for key in replacement_dict:
                prereqs = prereqs.replace(key, replacement_dict[key])

            lis = []
            # Finds all prereqs of the form {subject code}{x*} where x*
            # is one or more numbers
            for course_code in subject_codes:
                curr_code = course_code + "\s?[0-9]*"

                if re.findall(curr_code, prereqs):
                    lis += re.findall(curr_code, prereqs)

            newLis = []
            # Normalizes prereqs format (eg. "CSCI5" --> "CSCI 005")
            for l in lis:
                check = True
                for course_code in subject_codes:
                    # eg. "CSCI 005"
                    if re.match(course_code + "\s[0-9]{3}", l):
                        pass

                    # eg. "CSCI005" --> "CSCI 005"
                    elif re.match(course_code + "[0-9]{3}", l):
                        n = len(course_code)
                        l = l[0:n] + " " + l[n:]
                        check = False
                        newLis.append(l)

                    # eg. "CSCI05" --> "CSCI 005"
                    elif re.match(course_code + "[0-9]{2}", l):
                        n = len(course_code)
                        l = l[0:n] + " 0" + l[n:]
                        check = False
                        newLis.append(l)

                    # eg. "CSCI5" --> "CSCI 005"
                    elif re.match(course_code + "[0-9]{1}", l):
                        n = len(course_code)
                        l = l[0:n] + " 00" + l[n:]
                        check = False
                        newLis.append(l)

                    # eg. "CSCI 05" --> "CSCI 005"
                    elif re.match(course_code + "\s[0-9]{2}", l):
                        n = len(course_code)+1
                        l = l[0:n] + "0" + l[n:]
                        check = False
                        newLis.append(l)

                    # eg. "CSCI 5" --> "CSCI 005"
                    elif re.match(course_code + "\s[0-9]{1}", l):
                        n = len(course_code)+1
                        l = l[0:n] + "00" + l[n:]
                        check = False
                        newLis.append(l)

                # Makes sure prereq is a specific course
                # ("... MATH60", not "...MATH is recommended" for example)
                if check:
                    newLis.append(l)

            # Adds ["POI"] to list of prereqs for appropriate courses
            if ("permission of the instructor" in prereqs or 
                "permission of instructor" in prereqs):
                course_to_prereqs[course] = [[prereqs], newLis, ["POI"]]
            else:
                course_to_prereqs[course] = [[prereqs], newLis]

    return course_to_prereqs


course_to_prereqs = prereqs()

with open(r"prereqs.json", "w") as fp:
    json.dump(prereqs(), fp, indent=4)