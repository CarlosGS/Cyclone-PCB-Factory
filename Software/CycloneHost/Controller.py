#!/usr/bin/python

###### Cyclone Host v1.0 ######
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

# Begin modules
import sys
import serial
import time
from datetime import datetime

import random

from CycloneHost.helper import *
# End modules

# Begin configuration. It is overwritten when running connect()
BAUDRATE = 115200
DEVICE = "/dev/ttyUSB0"
Emulate = 0
# End configuration

lastDrillPos = [0,0,0]

seconds_wait = 0.5 # Delay used when re-trying to send/receive from the serial port [seconds]
serial_timeout = 5 # Timeout for the serial port [seconds]

OK_response = "ok" # First two characters of an OK response (case insensitive)

CNC_Machine = []

def connect(baudrate, device, emulate = 0):
	global CNC_Machine, Emulate, BAUDRATE, DEVICE
	BAUDRATE = baudrate
	DEVICE = device
	print("Connecting to Cyclone...")
	if emulate == 0:
		CNC_Machine = serial.Serial(DEVICE, BAUDRATE, timeout = serial_timeout)
		Emulate = 0
	else:
		Emulate = 1
		print("EMULATING MACHINE!")
	print("Serial port opened, checking connection...")
	time.sleep(2)
	checkConnection()
	print("Connected!")

def flushRecvBuffer(): # We could also use flushInput(), but showing the data that is being discarded is useful for debugging
	if Emulate:
		return
	while CNC_Machine.inWaiting() > 0:
		response = CNC_Machine.readline()
#		if response != '': print("IGNO: " + response)
		time.sleep(seconds_wait) # Wait some milliseconds between attempts

def sendLine(line):
	if Emulate == 0:
		flushRecvBuffer()
		CNC_Machine.write(line)
#	print("SENT: " + line)

def recvLine():
	if Emulate:
		response = "ok\n" # Asume OK
	else:
		response = CNC_Machine.readline()
#	if response != '': print("RECV: " + response)
#	else: print("RECV: Receive timed out!")
	return response

def recvOK():
	response = recvLine()
	if response[:2].lower() == OK_response.lower():
		return 1
	return 0

def waitForOK(command="",timeoutResend=30): # This is a blocking function
#	print("Waiting for confirmation")
	i = 0
	cmnd = command[:3].lower()
	timeoutResend = float(timeoutResend)
	#timeoutResend = 5.0 # Resend command every 5 seconds, error recovery
	#if cmnd == "g28": timeoutResend = 60.0 # Homing moves will take more than 5 seconds
	i_timeout = int(timeoutResend/float(serial_timeout+seconds_wait))
#	print("i_timeout = " + str(i_timeout))
	while recvOK() != 1:
		print("  Checking again... timeout: " + str(i_timeout) )
		time.sleep(seconds_wait) # Wait some milliseconds between attempts
		if cmnd != "g30" and i >= i_timeout: # WARNING: Commands that take >5s may have problems here!
			print("  WATCHOUT! RESENDING: " + str(command) )
			sendLine(command)
			i = 0
		else:
			i = i + 1

def sendCommand(command,timeoutResend=15): # Send command and wait for OK
	sendLine(command)
	waitForOK(command,timeoutResend)

def checkConnection():
#	print("Checking the connection...")
	sendLine("G21\n") # We check the connection setting millimiters as the unit and waiting for the OK response
	time.sleep(0.5)
	while recvOK() != 1:
		sendLine("G21\n")
		time.sleep(seconds_wait) # Wait some milliseconds between attempts

def homeZXY():
	global lastDrillPos
	print("Homing all axis...")
	timeoutResend=30
	sendCommand("G28 Z0\n",timeoutResend) # move Z to min endstop
	sendCommand("G28 X0\n",timeoutResend) # move X to min endstop
	sendCommand("G28 Y0\n",timeoutResend) # move Y to min endstop
	if Emulate:
		time.sleep(2)
	lastDrillPos = [0,0,0]
	print("Done homing")

def moveXYZ(X, Y, Z, F):
	global lastDrillPos
#	print("Moving to:")
	if F <= 0:
		print("ERROR: F <= 0")
	sendCommand("G1 X"+floats(X)+" Y"+floats(Y)+" Z"+floats(Z)+" F"+floats(F)+"\n")
	if Emulate:
		dist = ((X-lastDrillPos[0])**2+(Y-lastDrillPos[1])**2+(Z-lastDrillPos[2])**2)**0.5 # [mm]
		speed = float(F)/60.0 # [mm/s]
		time.sleep(float(dist)/speed)
	lastDrillPos = [X,Y,Z]

def moveXY(X, Y, F):
	global lastDrillPos
#	print("Moving to:")
	if F <= 0:
		print("ERROR: F <= 0")
	sendCommand("G1 X"+floats(X)+" Y"+floats(Y)+" F"+floats(F)+"\n")
	if Emulate:
		dist = ((X-lastDrillPos[0])**2+(Y-lastDrillPos[1])**2)**0.5 # [mm]
		speed = float(F)/60.0 # [mm/s]
		time.sleep(float(dist)/speed)
	lastDrillPos = [X,Y,lastDrillPos[2]]

def moveZ(Z, F):
	global lastDrillPos
#	print("Moving Z absolute:")
	if F <= 0:
		print("ERROR: F <= 0")
	sendCommand("G1 Z"+floats(Z)+" F"+floats(F)+"\n")
	if Emulate:
		dist = abs(Z-lastDrillPos[2]) # [mm]
		speed = float(F)/60.0 # [mm/s]
		time.sleep(float(dist)/speed)
	lastDrillPos = [lastDrillPos[0],lastDrillPos[1],Z]

def moveZrel(Z, F):
	global lastDrillPos
#	print("Moving Z relative:")
	if F <= 0:
		print("ERROR: F <= 0")
	sendCommand("G91\n") # Set relative positioning
	sendCommand("G1 Z"+floats(Z)+" F"+floats(F)+"\n")
	if Emulate:
		dist = abs(Z) # [mm]
		speed = float(F)/60.0 # [mm/s]
		time.sleep(float(dist)/speed)
	lastDrillPos = [lastDrillPos[0],lastDrillPos[1],lastDrillPos[2]+Z] # Relative movement
	sendCommand("G90\n") # Set absolute positioning

def moveZrelSafe(Z, F):
	if F <= 0:
		print("ERROR: F <= 0")
	print("Moving Z " + str(Z) + "mm safely...")
	sendCommand("M121\n") # Enable endstops (for protection! usually it should **NOT** hit neither the endstop nor the PCB)
	moveZrel(Z, F)
	dist = abs(Z) # [mm]
	speed = float(F)/60.0 # [mm/s]
	wait = float(dist)/speed # [s]
	time.sleep(wait) # Wait for the movement to finish, this way the M121 command is effective
	print("   Done moving Z!")
	sendCommand("M120\n") # Disable endstops (we only use them for homing)

def probeZ():
	print("Probing Z")
	sendLine("G30\n") # Launch probe command
	response = recvLine() # Read the response, it is a variable run time so we may need to make multiple attempts
	while response == '':
		#print(".")
		time.sleep(seconds_wait) # Wait some milliseconds between attempts
		response = recvLine()
	if Emulate:
		response = "ok Z"+str(random.gauss(0, 0.25))+"\n" # Generate random measure
	response_vals = response.split() # Split the response (i.e. "ok Z1.23")
	if response_vals[0][:2].lower() == OK_response.lower():
		Zres = response_vals[1][2:] # Ignore the "Z:" and read the coordinate value
		print("Result is Z = " + str(Zres))
		return float(Zres)
	return 400 # Error case, don't worry: it has never happened :)

def close():
	# IMPORTANT: Before closing the serial port we must make a blocking move in order to wait for all the buffered commands to end
	sendCommand("G28 Z0\n") # move Z to min endstop
	if Emulate == 0:
		CNC_Machine.close() # Close the serial port connection

def probeGrid(grid_origin, grid_len, grid_N, Zlift, F_fastMove, F_slowMove):
	grid_origin_X = float(grid_origin[0]) # Initial point of the grid [mm]
	grid_origin_Y = float(grid_origin[1])
	
	grid_len_X = float(grid_len[0]) # Distance to probe [mm]
	grid_len_Y = float(grid_len[1])
	
	grid_N_X = int(grid_N[0]) # Number of points
	grid_N_Y = int(grid_N[1])
	
	Z_probing_lift = float(Zlift) # lift between Z probings [mm]
	
	grid_inc_X = grid_len_X/float(grid_N_X-1) # [mm]
	grid_inc_Y = grid_len_Y/float(grid_N_Y-1)
	
	x_points = [ float(x_i)*grid_inc_X + grid_origin_X for x_i in range(grid_N_X) ] # Calculate X coordinates
	y_points = [ float(y_i)*grid_inc_Y + grid_origin_Y for y_i in range(grid_N_Y) ] # Calculate X coordinates
	
	probe_result = [ [ 0 for j in range(grid_N_X) ] for i in range(grid_N_Y) ]
	
	# Show our grid (initialised as zeros)
	for row in probe_result:
		print(str(row))
	
	print("Probing begins!")
	print("WARNING: Keep an eye on the machine, unplug if something goes wrong!")
	beginTime = datetime.now() # Store current time in a variable, will be used to measure duration of the probing
	
	 # Move to grid's origin
	moveXY(grid_origin_X, grid_origin_Y, F_fastMove)
	
	for x_i in range(grid_N_X): # For each point on the grid...
		x_val = float(x_i)*grid_inc_X + grid_origin_X # Calculate X coordinate
		optimal_range = range(grid_N_Y)
		if isOdd(x_i): # This optimises a bit the probing path
			optimal_range = reversed(optimal_range)
		for y_i in optimal_range:
			y_val = float(y_i)*grid_inc_Y + grid_origin_Y # Calculate Y coordinate
			moveXY(x_val, y_val, F_fastMove) # Move to position
			probe_result[y_i][x_i] = probeZ() # Do the Z probing
			moveZrel(Z_probing_lift, F_slowMove) # Lift the probe

	# Once we have all the points, we set the origin as (0,0) and offset the rest of values
	Z_offset = probe_result[0][0]
	print("The origin Z height is " + str(Z_offset))
	probe_result = [[elem - Z_offset for elem in row] for row in probe_result]

	# Return to the grid's origin
	moveZrel(10, F_slowMove) # Lift Z
	moveXY(grid_origin_X, grid_origin_Y, F_fastMove) # Move to grid's origin
	
	duration = datetime.now() - beginTime
	print("Probing duration:" + str(duration))
	duration_s = duration.total_seconds()
	
	return (x_points, y_points, probe_result, Z_offset, duration_s)




