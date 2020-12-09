"""
Format:

List of lists: [
    [
        {set of courses}, 
        [lower bound l (at least l of the courses must be selected), upper bound u (at most u of the courses can be selected)]
    ] ,
    
    ... 
    
    ]

"""

default_alternates = [
    [{}, [0,0]], 
    [{}, [0,0]]
    ]

#TODO: Add alternates here (variable should be stored in the above format with the variable name as name_alternatives):


# Shaurya
shaurya_alternates = [[{ "STS 179L HM-01","RLST 113 HM-01"}, [0,1]],
                      [
                          { "STS 179L HM-01","RLST 150 AF-01" ,"RLST 113 HM-01" ,"MUS 003 HM-01", "ENGL 061 PZ-01" }, [0,2]]
                      ]

# Shreya
shreya_alternates = [
    [{"ENGR 102 HM-01", "ENGR 111 HM-01"}, [2,2]]
]

