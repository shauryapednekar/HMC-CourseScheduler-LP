# HMC Course Scheduler

Get your individualized optimal course schedule for the upcoming semester!

Here's how:

1. Update the sheet corresponding with your major in the Preferences.xlsx file with your individual preferences.
2. In excel\excel_parser.py:
   1. Update the curr_dat_filename variable (line 4) to your desired filename for the .dat file (in case you would like to run the program multiple times with varying preferences, otherwise it can be left as is).
   2. Update the excel_sheet_name variable (line 8) to sheet name containing your individual preferences within the excel sheet.
3. In main.py:
   1. In the main() function's arguments, let selected=True if you only want to include the courses from preferences.py or False if you want to include all possible courses.
4. Run `python main.py`
5. Run `ampl exec.run` (include full filepath for exec.run).

Voila! You now have the optimal course schedule based on your preferences and requirements.
