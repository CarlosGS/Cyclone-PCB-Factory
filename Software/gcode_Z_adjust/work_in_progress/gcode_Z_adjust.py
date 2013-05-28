#!/usr/bin/python

# AUTHOR:
#   Carlosgs (http://carlosgs.es)
# LICENSE:
#   Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)
#
# DISCLAIMER:
#   This software is provided "as is", and you use the software at your own risk. Under no
#   circumstances shall Carlosgs be liable for direct, indirect, special, incidental, or
#   consequential damages resulting from the use, misuse, or inability to use this software,
#   even if Carlosgs has been advised of the possibility of such damages.
#
# CREDIT:
#   Based on Etch_Z_adjust.1.8.py from http://www.cnczone.com/forums/pcb_milling/82628-cheap_simple_height-probing.html (multiple authors)

# Begin configuration
BAUDRATE = 115200
DEVICE = "/dev/ttyUSB0"
# End configuration

# Begin modules
import sys

sys.path.append("../CycloneHost")
import CycloneHost as cy
# End modules

fileToFeed = "../GcodeGenerators/pyGerber2Gcode_CUI/out/printshield_pcb.gcode" # sys.argv[1] # Will use this later on to load 
gcode = open(fileToFeed, "r")

cy.connect(BAUDRATE, DEVICE)

cy.sendCommand("G90\n") # Set absolute positioning

cy.homeZXY() # Home all the axis

F_slowMove = 200 # Move speed [mm/min?]
F_fastMove = 700

initial_Z_lowering_distance = -15
cy.moveZ(initial_Z_lowering_distance,F_slowMove)

def get_num(line,char_ptr,num_chars):
	char_ptr=char_ptr+1
	numstr = ''
	good = '-.0123456789'
	while char_ptr < num_chars:
		digit = line[char_ptr]
		if good.find(digit) != -1:
			numstr = numstr + digit
			char_ptr = char_ptr + 1
		else: break
	return numstr

currentLine = 0.0
lines = gcode.readlines()
totalLines = len(lines)
for line in lines:
	currentLine = currentLine + 1
	print "Reading:", line, "({0:.1f}%)".format((currentLine / totalLines)*100)
	cy.sendCommand(line)
	
	# Height to consider etching
	etch_definition = 0
	
	grid_clearance = 0.01
	
	# Check for max and min values in your ngc file
	is_first_X = True
	is_first_Y = True
	is_first_Z = True

	# check each line
	line_ptr=0
	num_lines=len(file_in)
	while line_ptr < num_lines:
		line = file_in[line_ptr]
		X_start = X_dest
		Y_start = Y_dest
		Z_start = Z_dest
		
	# check each character
		char_ptr = 0
		num_chars= len(line)
		while char_ptr < num_chars:
		char = line[char_ptr]
		if '(;'.find(char) != -1:
			break
		elif char == 'G' :
			G_dest = get_num(line,char_ptr,num_chars)
		elif char == 'X' :
			X_dest = float(get_num(line,char_ptr,num_chars))
		elif char == 'Y' :
			Y_dest = float(get_num(line,char_ptr,num_chars))
		elif char == 'Z' :
			Z_dest = float(get_num(line,char_ptr,num_chars))
		char_ptr = char_ptr + 1
		
		# if the line is an etch move, then replace the line with an etch call
		if G_dest == '01' and Z_dest > etch_definition:

		line = 'O200 call [%.4f] [%.4f] [%.4f] [%.4f]\n' % (X_start, Y_start, X_dest, Y_dest)

		# and now check for max and min X and Y values
		if is_first_X == True :
			X_min = X_dest
			X_max = X_dest
			is_first_X = False
		else : (X_min, X_max) = test_X(X_min, X_max)

		if is_first_Y == True :
			Y_min = Y_dest
			Y_max = Y_dest
			is_first_Y = False
		else : (Y_min, Y_max) = test_Y(Y_min, Y_max)
		 
		file_out.append(line)
		line_ptr=line_ptr+1

if is_first_X == False :

	# then there were etch moves so get to work!

	# first stretch the X and Y max and min values a _tiny_ amount so the grid is just outside all the etch points
	X_min = X_min - grid_clearance
	X_max = X_max + grid_clearance
	Y_min = Y_min - grid_clearance
	Y_max = Y_max + grid_clearance

	# Use max and min values for the etch moves to work out the probe grid dimensions
	X_span = X_max - X_min
	X_grid_origin = X_min 
	Y_span = Y_max - Y_min
	Y_grid_origin = Y_min


gcode.close()

cy.close() # Close the serial port connection

