# HMC Course Scheduler

Get your individualized optimal course schedule for the upcoming semester!

Here's how:

1. Update the google sheet found here: https://docs.google.com/spreadsheets/d/1SeTpNHbI5gJV2mem-YL_pVhyniszCaz-dS4rmn5y2Vg/edit?usp=sharing.

2. Save the sheet in as an excel file into the top directory of the project folder.
   
2. In userInputs.py, update the excel filename and sheet name if needed.
   
3. Run `python main.py`
   
4. Run `ampl exec.run` (include full filepath for exec.run). [Requires ampl and the cplex solver installed on your machine.]

Voila! You now have the optimal course schedule based on your preferences and requirements.


## About the Software

This program using mixed integer linear programming in order to create an optimal course schedule for a Harvey Mudd student for their upcoming semester. The code written in python (mainly in func.py) creates the data file (.dat file) and the model file (.mod file) --> examples can be found in .\amplFiles. The exec.run file (created after running main.py) contains the commands needed for AMPL's cplex solver to run and output the optimal course schedule.
