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

# Begin configuration
BAUDRATE = 115200
DEVICE = "/dev/ttyUSB0"
Emulate = 1
# End configuration

# Begin modules
import sys
from datetime import datetime
import time

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

sys.path.append("../CycloneHost")
import GcodeViewer as gcv
import CycloneHost as cy
# End modules

filePath = "../GcodeGenerators/pyGerber2Gcode_CUI/out/"
fileName = "printshield" # sys.argv[1]

# Display the Gcode that is going to be etched
(etch_moves, travel_moves, gcodeviewer) = gcv.view(filePath,fileName,showEtch=1)
figId = gcodeviewer.number

def pltShowNonBlocking():
	plt.ion() # Enable real-time plotting to avoid blocking behaviour for plt.show()
	plt.show()
	plt.ioff() # Disable real-time plotting

toolPos_point = []

def toolPos_draw(x, y, etching=0):
	if etching:
		color = 'r'
	else:
		color = 'g'
	toolPos_point.set_data(x, y)
	toolPos_point.set_color(color)
	gcodeviewer.canvas.draw()

toolRefreshSteps = 1
toolRefresh = 0
def toolPos_refresh(x, y, etching=0):
	global toolRefresh
	if toolRefresh >= toolRefreshSteps:
		toolPos_draw(toolPos_X, toolPos_Y, etching)
		toolRefresh = 0
	toolRefresh = toolRefresh + 1

def drawTool(x, y):
	global toolPos_point
	plt.figure(figId)
	toolPos_point, = plt.plot(0, 0, markersize=12, c='g', marker='x')
	pltShowNonBlocking()

F_slowMove = 200 # Move speed [mm/min?]
F_fastMove = 700

F_etchMove = F_slowMove
F_drillMove = 50
F_edgeMove = 25


cy.connect(BAUDRATE, DEVICE, Emulate)

cy.sendCommand("G90\n") # Set absolute positioning

cy.homeZXY() # Home all the axis

drawTool(10, 20) # Show a marker on the gcode plot



# Warning: Do not lower too much or you will potentially cause damage!
initial_Z_lowering_distance = -20
#cy.moveZrelSafe(initial_Z_lowering_distance,F_slowMove/2) # Move Z towards the PCB (saves some probing time for the first coord)

Z_origin_offset = cy.probeZ()
print "Z offset:", Z_origin_offset


Z_workbed_surface = []

def probingResults():
	global Z_workbed_surface
	x_points = [0.0, 12.272727272727273, 24.545454545454547, 36.81818181818182, 49.09090909090909, 61.36363636363637, 73.63636363636364, 85.9090909090909, 98.18181818181819, 110.45454545454547, 122.72727272727273, 135.0]
	y_points = [0.0, 16.8, 33.6, 50.400000000000006, 67.2, 84.0]
	probe_result = [[0.0, 0.2, 0.4, 0.53, 0.58, 0.6, 0.56, 0.53, 0.5, 0.44, 0.33, 0.2], [-0.03, 0.07, 0.16, 0.26, 0.32, 0.33, 0.33, 0.33, 0.29, 0.23, 0.15, 0.05], [-0.07, 0.0, 0.05, 0.12, 0.16, 0.2, 0.2, 0.22, 0.2, 0.16, 0.08, 0.0], [-0.07, -0.03, 0.04, 0.11, 0.15, 0.19, 0.2, 0.22, 0.22, 0.19, 0.11, 0.04], [0.0, 0.04, 0.08, 0.19, 0.23, 0.29, 0.33, 0.36, 0.37, 0.32, 0.2, 0.11], [0.13, 0.2, 0.27, 0.37, 0.44, 0.51, 0.55, 0.61, 0.64, 0.55, 0.41, 0.22]]
	duration = 346.076061

	# Show our grid
#	print "--- Probing results ---"
#	print "-> X points:", x_points
#	print "-> Y points:", y_points
#	print "-> Grid:", probe_result
#	print "-> Duration:", duration

	# Must be converted into arrays to use scipy
	x_points = np.array(x_points)
	y_points = np.array(y_points)
	probe_result = np.array(probe_result)
	
#	plt.figure()
#	plt.pcolor(x_points, y_points, probe_result)
#	plt.colorbar()
#	plt.title("Z probing results [mm]")
#	plt.axis('equal') # 1:1 aspect ratio
#	pltShowNonBlocking()
	
	# Interpolation
	Z_workbed_surface = interpolate.RectBivariateSpline(y_points, x_points, probe_result)
	
	x_points = np.linspace(min(x_points),max(x_points),100) 
	y_points = np.linspace(min(y_points),max(y_points),100) 
	
	z_points = Z_workbed_surface(y_points,x_points)
	
	plt.figure()
	plt.pcolor(x_points, y_points, z_points)
	plt.colorbar()
	plt.title("Z probing results (interpolated) [mm]")
	plt.axis('equal') # 1:1 aspect ratio
	pltShowNonBlocking()

def getZoffset(x,y):
	return Z_workbed_surface(y,x)[0][0]

probingResults()


#print "Zero:",str(getZoffset(0,0))






toolPos_X = 0
toolPos_Y = 0
toolPos_Z = 0

X_dest = 0
Y_dest = 0
Z_dest = 0


cy.moveZrelSafe(10,F_slowMove)
toolPos_Z = 10

plt.figure(figId)

Zlift = 0.5

Z_manual_offset = 0.02+10

maxDistance = 1**2 # [mm^2] 5mm (longer moves will be split to regulate Z)
minDistance = 0.005**2 # [mm^2] 0.005mm is the smallest distance that will be sent

def splitLongEtchMove(distance):
	global toolPos_X, toolPos_Y, toolPos_Z, X_dest, Y_dest, Z_dest
	
	X_dest_tmp = toolPos_X
	Y_dest_tmp = toolPos_Y
	Z_dest_tmp = toolPos_Z
		
	#distance = distance**0.5 # [mm]
	N_steps = int((distance/maxDistance)**0.5) # **must be** >= 1
	
	print "Splitting", distance**0.5, "mm segment into", N_steps, "steps"
	
	print "Orig:", toolPos_X, toolPos_Y, toolPos_Z, "Dest:", X_dest, Y_dest, Z_dest
	
	X_step = (X_dest-toolPos_X)/float(N_steps)
	Y_step = (Y_dest-toolPos_Y)/float(N_steps)
	Z_step = (Z_dest-toolPos_Z)/float(N_steps)
	
	for i in range(N_steps) :
		X_dest_tmp = toolPos_X + X_step
		Y_dest_tmp = toolPos_Y + Y_step
		Z_dest_tmp = toolPos_Z + Z_step
	
		Z_real = Z_dest_tmp+Z_origin_offset+getZoffset(X_dest_tmp, Y_dest_tmp)+Z_manual_offset
		cy.moveXYZ(X_dest_tmp, Y_dest_tmp, Z_real, F_etchMove)
		toolPos_refresh(X_dest_tmp, Y_dest_tmp, etching=1)
		
		print "Move:",X_dest_tmp, Y_dest_tmp, Z_dest_tmp
		
		toolPos_X = X_dest_tmp
		toolPos_Y = Y_dest_tmp
		toolPos_Z = Z_dest_tmp

for path in etch_moves :
	toolRefresh = 0
	toolPos_draw(toolPos_X, toolPos_Y, etching=0)
	cy.moveZrel(Zlift,F_fastMove) # Raise and move to next point
	X_dest = path[0][0]
	Y_dest = path[0][1]
	cy.moveXY(X_dest, Y_dest, F_fastMove)
	toolPos_draw(X_dest, Y_dest, etching=0)
	cy.moveZrel(-Zlift,F_slowMove)
	
	toolPos_X = X_dest
	toolPos_Y = Y_dest
	toolPos_Z = Z_dest # Not sure..
	
	for coord in path[1:] :
		X_dest = coord[0]
		Y_dest = coord[1]
		Z_dest = coord[2]
		
		distance = (X_dest-toolPos_X)**2+(Y_dest-toolPos_Y)**2
		if distance >= maxDistance :
			splitLongEtchMove(distance)
		if distance < minDistance :
			print "Ignoring", distance**0.5, "mm segment!"
			continue
		Z_real = Z_dest+Z_origin_offset+getZoffset(X_dest, Y_dest)+Z_manual_offset
		cy.moveXYZ(X_dest, Y_dest, Z_real, F_etchMove)
		toolPos_refresh(X_dest, Y_dest, etching=1)
		
		toolPos_X = X_dest
		toolPos_Y = Y_dest
		toolPos_Z = Z_dest

cy.close() # Close the serial port connection

raw_input("Done. Press enter to exit...")

