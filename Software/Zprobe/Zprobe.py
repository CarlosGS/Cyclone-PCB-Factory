#!/usr/bin/python

###### Cyclone PCB console v0.1 ######
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
#   This software is provided “as is," and you use the software at your own risk. Under no
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
#gcode = open(fileToFeed, "r")

millis_wait = 0.1 # Delay used when re-trying to send/receive from the serial port [seconds]
serial_timeout = 0.1 # Timeout for the serial port [seconds]

def getCurrentTime():
	timeNow = datetime.now()
	print "Time:",str(timeNow)
	return timeNow

def emptyMachineRecvBuffer():
	response = CNC_Machine.readline()
	while response != '':
		print "IGNO: ", response
		time.sleep(millis_wait) # Wait some milliseconds between attempts
		response = CNC_Machine.readline()

def sendToMachine(line):
	emptyMachineRecvBuffer()
	CNC_Machine.write(line)
	print "SENT: ", line

def recvFromMachine():
	response = CNC_Machine.readline()
	if response != '':
		print "RECV: ", response
	return response

def machineSaysOK():
	response = recvFromMachine()
	if response[:2] == "ok":
		return 1
	return 0

def waitForOK():
	print "Waiting for confirmation"
	while machineSaysOK() != 1:
		#print "."
		time.sleep(millis_wait) # Wait some milliseconds between attempts

def checkConnection():
	sendToMachine("G21\n") # We check the connection setting millimiters as the unit and waiting for the OK response
	time.sleep(0.5)
	while machineSaysOK() != 1:
		sendToMachine("G21\n")
		time.sleep(millis_wait) # Wait some milliseconds between attempts

print "Connecting to Cyclone..."

CNC_Machine = serial.Serial(DEVICE, BAUDRATE, timeout = serial_timeout)

print "Serial port opened, checking connection..."

time.sleep(0.5)

checkConnection();

print "CONNECTED"

time.sleep(1)

sendToMachine("G90\n") # Set absolute positioning
waitForOK()

def machineHomeZXY():
	print "Homing all axis..."
	sendToMachine("G28 Z0\n") # move Z to min endstop
	waitForOK()
	sendToMachine("G28 X0\n") # move X to min endstop
	waitForOK()
	sendToMachine("G28 Y0\n") # move Y to min endstop
	waitForOK()

machineHomeZXY() # Home all the axis

F_slowMove = 200 # Move speed [mm/min?]
F_fastMove = 600

def floats(val): # This is used to convert a float value to a string (avoiding exponent notation)
	return '{:f}'.format(float(val)) # It would be interesting to truncate the decimals that aren't used

def machineToCoords(X,Y,Z,F):
	print "Moving to:"
	sendToMachine("G1 X"+floats(X)+" Y"+floats(Y)+" Z"+floats(Z)+" F"+floats(F)+"\n")
	waitForOK()

def machineToCoordsXY(X,Y,F):
	print "Moving to:"
	sendToMachine("G1 X"+floats(X)+" Y"+floats(Y)+" F"+floats(F)+"\n")
	waitForOK()

def machineToCoordsZ(Z,F):
	print "Moving Z absolute:"
	sendToMachine("G1 Z"+floats(Z)+" F"+floats(F)+"\n")
	waitForOK()

def machineToCoordsZrelative(Z,F):
	print "Moving Z relative:"
	sendToMachine("G91\n") # Set relative positioning
	waitForOK()
	sendToMachine("G1 Z"+floats(Z)+" F"+floats(F)+"\n")
	waitForOK()
	sendToMachine("G90\n") # Set absolute positioning
	waitForOK()

grid_origin_X = float(0) # Initial point of the grid
grid_origin_Y = float(0)

grid_len_X = float(135) # Distance to probe [mm]
grid_len_Y = float(84)

grid_N_X = int(12) # Number of points
grid_N_Y = int(6)

grid_inc_X = grid_len_X/float(grid_N_X-1) # mm
grid_inc_Y = grid_len_Y/float(grid_N_Y-1)

probe_grid = [ [ 0 for i in range(grid_N_X) ] for j in range(grid_N_Y) ]

# Show our grid
for row in probe_grid:
	print row

print "Probing begins!"
print "WARNING: Keep an eye on the machine, unplug if something goes wrong!"
beginTime = getCurrentTime() # Store current time in a variable, will be used to measure duration of the probing

# Warning: Do not lower too much or you will cause damage!
# machineToCoordsZrelative(-10,F_slowMove/2) # Move Z towards the PCB (saves some probing time for the first coord)

def machineProbeZ():
	print "Probing Z"
	sendToMachine("G30\n") # Launch probe command
	response = recvFromMachine() # Read the response, it is a variable time so we make multiple attempts
	while response == '':
		#print "."
		time.sleep(millis_wait) # Wait some milliseconds between attempts
		response = recvFromMachine()
	response_vals = response.split() # Split the response (i.e. "ok Z:1.23")
	if response_vals[0][:2] == "ok":
		Zres = response_vals[1][2:] # Ignore the "Z:" and read the coordinate
		print "Result is Z=",Zres
		return float(Zres)
	return 400 # Error case, it has never happened :)

def isOdd(number):
	if number % 2 == 0:
		return 0 # Even number
	else:
		return 1 # Odd number

for x_i in range(grid_N_X):
	x_val = float(x_i)*grid_inc_X+grid_origin_X;
	optimal_range = range(grid_N_Y)
	if isOdd(x_i): # This creates a more optimal path for the probing
		optimal_range = reversed(optimal_range)
	for y_i in optimal_range:
		y_val = float(y_i)*grid_inc_Y+grid_origin_Y;
		machineToCoordsXY(x_val,y_val,F_fastMove)
		val = machineProbeZ()
		machineToCoordsZrelative(0.5,F_fastMove/2)
		probe_grid[y_i][x_i]= val

# Once we have all the points, we set the origin as (0,0) and offset the rest of values
ZoffsetOrigin = probe_grid[0][0]
probe_grid = [[elem - ZoffsetOrigin for elem in row] for row in probe_grid]

# Return to the grid's origin
machineToCoordsZrelative(10,F_slowMove)
machineToCoordsXY(grid_origin_X,grid_origin_Y,F_fastMove)


# Show our grid
print "Result:"
print probe_grid # Right now I am copying this to an Octave script for the visualizations

# TODO:
# - Export results to a file with a standarized format
# - 

print "Finished probing!"
getCurrentTime()
print "Probing duration:",str(datetime.now()-beginTime)




#response = CNC_Machine.readline()
#print "  ", response,
#while response[:2] != "ok":
#	print "  ", response,
#	response = CNC_Machine.readline()

#currentLine = 0.0
#lines = gcode.readlines()
#totalLines = len(lines)
#for line in lines:
#	currentLine = currentLine + 1
#	print line, "({0:.1f}%)".format((currentLine / totalLines)*100),
#	CNC_Machine.write(line)
#	
#	response = CNC_Machine.readline()
#	print "  ", response,
#	while response[:2] != "ok":
#		print "  ", response,
#		response = CNC_Machine.readline()


#gcode.close()
CNC_Machine.close() # Close the serial port


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
