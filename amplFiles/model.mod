set courses; 
set requirements;
set timeSlots;
set uniqueCourses;
set alternates;

param costs {j in courses}; 

param time {i in timeSlots, j in courses};

param counts {i in requirements, j in courses};

param necessary {i in requirements};

param unique {i in uniqueCourses, j in courses};

param alternatesLowerLimits {i in alternates};

param alternatesUpperLimits {i in alternates};

param alternatesMatrix {i in alternates, j in courses};

var x {j in courses} integer >= 0, <=1; 

maximize Happiness: sum {j in courses} costs[j]*x[j];

subject to Alts {i in alternates}:
    alternatesUpperLimits[i] <= sum {j in courses} (alternatesMatrix[i,j]) * x[j] <= alternatesUpperLimits[i];

subject to Reqs {i in requirements}:
    sum {j in courses} (counts[i,j]) * x[j] >= necessary[i];

subject to TimeConflicts {i in timeSlots}:
    sum {j in courses} (time[i,j] * x[j]) <= 1;
    
subject to EnrollmentBounds:
    4 <= sum {i in courses} x[i] <= 6;
    
subject to Uniqueness {i in uniqueCourses}:
    sum {j in courses} (unique[i,j]) * x[j] <= 1;

