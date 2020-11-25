"""
Format:

List of lists: [
    [
        set of courses, 
        [lower bound, upper bound]
    ]
    
    ]

"""

default_alternates = [
    [{}, [0,0]], 
    [{}, [0,0]]
    ]


# Shaurya
shaurya_alternates = [[{ "STS 179L HM-01","RLST 113 HM-01"}, [0,1]],
                      [
                          { "STS 179L HM-01","RLST 150 AF-01" ,"RLST 113 HM-01" ,"MUS 003 HM-01", "ENGL 061 PZ-01" }, [0,2]]
                      ]



curr_alternates = shaurya_alternates