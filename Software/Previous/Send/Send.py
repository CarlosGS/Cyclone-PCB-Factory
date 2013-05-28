#!/usr/bin/python

###### Cyclone PCB console v0.2 ######
#
# DESCRIPTION:
#   Controller for the Cyclone PCB Factory:
#     "a 3D printable CNC machine for PCB manufacture" (http://www.thingiverse.com/thing:49484)
#   This software has been tested with a Sanguinololu board running a modified Marlin firmware
#   that supports the G30 probing G-code.
#
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
#   This script was created using as a base:
#     "Upload GCode to SpereBot" by Tgfuellner http://www.thingiverse.com/thing:9941 (CC-BY-SA)
#   Please refer to http://carlosgs.es for more information on this probing method
#
# REQUISITE:
#   http://pyserial.sourceforge.net
#   Installation on Ubuntu: sudo aptitude install python-serial
#
######################################

# Begin configuration
BAUDRATE = 115200
DEVICE = "/dev/ttyUSB0"
# End configuration

import sys
import serial
import time
from datetime import datetime

#fileToFeed = sys.argv[1]  # Will use this later on to load 
gcode = open("/home/carlosgs/GitRepos/Cyclone-PCB-Factory/Software/Send/pyGerber2Gcode_CUI/out/printshield_drill.gcode", "r")

millis_wait = 0.5 # Delay used when re-trying to send/receive from the serial port [seconds]
serial_timeout = 5 # Timeout for the serial port [seconds]

OK_response = "ok" # First two characters of an OK response (case insensitive)

def getCurrentTime():
	timeNow = datetime.now()
	print "Time:", str(timeNow)
	return timeNow

def emptyMachineRecvBuffer(): # We could also use flushInput(), but showing the data that is being discarded is useful for debugging
	while CNC_Machine.inWaiting() > 0:
		response = CNC_Machine.readline()
		if response != '':
			print "IGNO: ", response
		time.sleep(millis_wait) # Wait some milliseconds between attempts

def sendToMachine(line):
	emptyMachineRecvBuffer()
	CNC_Machine.write(line)
	print "SENT: ", line

def recvFromMachine():
	response = CNC_Machine.readline()
	if response != '':
		print "RECV: ", response
	else:
		print "RECV: Receive timed out!"
	return response

def machineSaysOK():
	response = recvFromMachine()
	if response[:2].lower() == OK_response.lower():
		return 1
	return 0

def waitForOK(): # This is a blocking function
	print "Waiting for confirmation"
	while machineSaysOK() != 1:
		print "  Checking again..."
		time.sleep(millis_wait) # Wait some milliseconds between attempts

def cyclone.sendCommand(command): # Send command and wait for OK
	if len(command) > 2:
		sendToMachine(command)
		waitForOK()

def checkConnection():
	print "Checking the connection..."
	sendToMachine("G21\n") # We check the connection setting millimiters as the unit and waiting for the OK response
	time.sleep(0.5)
	while machineSaysOK() != 1:
		sendToMachine("G21\n")
		time.sleep(millis_wait) # Wait some milliseconds between attempts

cyclone.connect(BAUDRATE, DEVICE)

cyclone.sendCommand("G90\n") # Set absolute positioning

def machineHomeZXY():
	print "Homing all axis..."
	cyclone.sendCommand("G28 Z0\n") # move Z to min endstop
	cyclone.sendCommand("G28 X0\n") # move X to min endstop
	cyclone.sendCommand("G28 Y0\n") # move Y to min endstop

homeZXY() # Home all the axis


F_slowMove = 200 # Move speed [mm/min?]
F_fastMove = 700

def floats(val): # This is used to convert a float value to a string (avoiding exponent notation)
	return '{:.3f}'.format(float(val)) # It truncates the decimals that aren't used

def machineToCoords(X, Y, Z, F):
	print "Moving to:"
	cyclone.sendCommand("G1 X"+floats(X)+" Y"+floats(Y)+" Z"+floats(Z)+" F"+floats(F)+"\n")

def machineToCoordsXY(X, Y, F):
	print "Moving to:"
	cyclone.sendCommand("G1 X"+floats(X)+" Y"+floats(Y)+" F"+floats(F)+"\n")

def machineToCoordsZ(Z, F):
	print "Moving Z absolute:"
	cyclone.sendCommand("G1 Z"+floats(Z)+" F"+floats(F)+"\n")

def machineToCoordsZrelative(Z, F):
	print "Moving Z relative:"
	cyclone.sendCommand("G91\n") # Set relative positioning
	cyclone.sendCommand("G1 Z"+floats(Z)+" F"+floats(F)+"\n")
	cyclone.sendCommand("G90\n") # Set absolute positioning

'''

grid_origin_X = float(0) # Initial point of the grid [mm]
grid_origin_Y = float(0)

grid_len_X = float(135) #135 # Distance to probe [mm]
grid_len_Y = float(84) #84

grid_N_X = int(12) #12 # Number of points
grid_N_Y = int(6) #6

grid_inc_X = grid_len_X/float(grid_N_X-1) # [mm]
grid_inc_Y = grid_len_Y/float(grid_N_Y-1)

probe_grid = [ [ 0 for i in range(grid_N_X) ] for j in range(grid_N_Y) ]

# Show our grid (initialised as zeros)
for row in probe_grid:
	print row

print "Probing begins!"
print "WARNING: Keep an eye on the machine, unplug if something goes wrong!"
beginTime = getCurrentTime() # Store current time in a variable, will be used to measure duration of the probing

 # Move to grid's origin
machineToCoordsXY(grid_origin_X, grid_origin_Y, F_fastMove)

# Warning: Do not lower too much or you will potentially cause damage!
initial_Z_lowering_distance = -15
cyclone.sendCommand("M121\n") # Enable endstops (for protection! it should tap the copper SLOWLY)
machineToCoordsZrelative(initial_Z_lowering_distance,F_slowMove) # Move Z towards the PCB (saves some probing time for the first coord)
cyclone.sendCommand("M120\n") # Disable endstops (we only use them for homing)

def machineProbeZ():
	print "Probing Z"
	sendToMachine("G30\n") # Launch probe command
	response = recvFromMachine() # Read the response, it is a variable run time so we may need to make multiple attempts
	while response == '':
		#print "."
		time.sleep(millis_wait) # Wait some milliseconds between attempts
		response = recvFromMachine()
	response_vals = response.split() # Split the response (i.e. "ok Z:1.23")
	if response_vals[0][:2].lower() == OK_response.lower():
		Zres = response_vals[1][2:] # Ignore the "Z:" and read the coordinate value
		print "Result is Z=",Zres
		return float(Zres)
	return 400 # Error case, don't worry: it has never happened :)

def isOdd(number):
	if number % 2 == 0:
		return 0 # Even number
	else:
		return 1 # Odd number

Z_probing_lift = 0.5 # lift between Z probings [mm]
# Note: The lift is relative to the PCB board, you can usually set a low value to speedup the process.
# But PLEASE keep an eye for possible collisions!

for x_i in range(grid_N_X): # For each point on the grid...
	x_val = float(x_i)*grid_inc_X + grid_origin_X; # Calculate X coordinate
	optimal_range = range(grid_N_Y)
	if isOdd(x_i): # This optimises a bit the probing path
		optimal_range = reversed(optimal_range)
	for y_i in optimal_range:
		y_val = float(y_i)*grid_inc_Y + grid_origin_Y; # Calculate Y coordinate
		machineToCoordsXY(x_val, y_val, F_fastMove) # Move to position
		probe_grid[y_i][x_i] = machineProbeZ() # Do the Z probing
		machineToCoordsZrelative(Z_probing_lift, F_fastMove/2) # Lift the probe

# Once we have all the points, we set the origin as (0,0) and offset the rest of values
ZoffsetOrigin = probe_grid[0][0]
print "The origin Z height is", ZoffsetOrigin
probe_grid = [[elem - ZoffsetOrigin for elem in row] for row in probe_grid]

# Return to the grid's origin
machineToCoordsZrelative(10, F_slowMove) # Lift Z
machineToCoordsXY(grid_origin_X, grid_origin_Y, F_fastMove) # Move to grid's origin


# Show our grid
print "Result:"
print probe_grid # Right now I am copying this to an Octave script for the visualizations

# TODO:
# - Export results to a file with a standarized format
# - 

print "Finished probing!"
getCurrentTime()
print "Probing duration:", str(datetime.now() - beginTime)
'''

initial_Z_lowering_distance = -15
machineToCoordsZrelative(initial_Z_lowering_distance,F_slowMove)

currentLine = 0.0
lines = gcode.readlines()
totalLines = len(lines)
for line in lines:
	currentLine = currentLine + 1
	print line, "({0:.1f}%)".format((currentLine / totalLines)*100)
	cyclone.sendCommand(line)

gcode.close()

# IMPORTANT: Before closing the serial port we must make a blocking move in order to wait for all the buffered commands to end
cyclone.sendCommand("G28 Z0\n") # move Z to min endstop

CNC_Machine.close() # Close the serial port connection


# Bilinear interpolation code by Raymond Hettinger from http://stackoverflow.com/a/8662355
def bilinear_interpolation(x, y, points):
	'''Interpolate (x,y) from values associated with four points.

	The four points are a list of four triplets:  (x, y, value).
	The four points can be in any order.  They should form a rectangle.

		>>> bilinear_interpolation(12, 5.5,
		...                        [(10, 4, 100),
		...                         (20, 4, 200),
		...                         (10, 6, 150),
		...                         (20, 6, 300)])
		165.0
	'''
	# See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

	points = sorted(points)			   # order points by x, then by y
	(x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

	if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
		raise ValueError('points do not form a rectangle')
	if not x1 <= x <= x2 or not y1 <= y <= y2:
		raise ValueError('(x, y) not within the rectangle')

	return (q11 * (x2 - x) * (y2 - y) +
			q21 * (x - x1) * (y2 - y) +
			q12 * (x2 - x) * (y - y1) +
			q22 * (x - x1) * (y - y1)
		) / ((x2 - x1) * (y2 - y1) + 0.0)

