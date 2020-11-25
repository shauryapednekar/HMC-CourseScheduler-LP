data_file = r"\test6.dat"

ampl_mod_command = r"model 'C:\Users\Shaurya\Desktop\math187 project\amplFiles\model.mod'; "

ampl_dat_command = r"data C:\Users\Shaurya\Desktop\math187 project\amplFiles" + data_file + r";"

ampl_solve_command = r"solve;"

ample_option_command = r"option omit_zero_rows 1;"

ampl_display_command = r"display x;"

ampl_all_commands = ampl_mod_command + "\n" + ampl_dat_command + "\n" + ampl_solve_command + "\n" + ample_option_command + "\n" + ampl_display_command

print(ampl_all_commands)