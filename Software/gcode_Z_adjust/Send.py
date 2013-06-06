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
Emulate = 0
# End configuration

# Begin modules
import sys
from datetime import datetime
import time

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from matplotlib import cm

sys.path.append("../CycloneHost")
import GcodeViewer as gcv
import CycloneHost as cy
from helper import *
# End modules

filePath = "../GcodeGenerators/pyGerber2Gcode_CUI/out/"
fileName = "DTMF_Shield_etch" # sys.argv[1]





def pltShowNonBlocking():
	#plt.ion() # Enable real-time plotting to avoid blocking behaviour for plt.show()
	plt.draw()
	#plt.ioff() # Disable real-time plotting

def pltNewFig():
	fig = plt.figure()
	#plt.draw()
	return fig

def pltSetFig(fig):
	plt.figure(fig.number)

def pltRefresh(fig):
	fig.canvas.draw()

def pltShow():
	#plt.ion() # IMPORTANT: Enable real-time plotting
	plt.draw()
	#plt.ioff()







def probingResults(): # quick and dirty temporal code
	global Z_workbed_surface, x_points, y_points
#	x_points = [0.0, 12.272727272727273, 24.545454545454547, 36.81818181818182, 49.09090909090909, 61.36363636363637, 73.63636363636364, 85.9090909090909, 98.18181818181819, 110.45454545454547, 122.72727272727273, 135.0]
#	y_points = [0.0, 16.8, 33.6, 50.400000000000006, 67.2, 84.0]
#	probe_result = [[0.0, 0.2, 0.4, 0.53, 0.58, 0.6, 0.56, 0.53, 0.5, 0.44, 0.33, 0.2], [-0.03, 0.07, 0.16, 0.26, 0.32, 0.33, 0.33, 0.33, 0.29, 0.23, 0.15, 0.05], [-0.07, 0.0, 0.05, 0.12, 0.16, 0.2, 0.2, 0.22, 0.2, 0.16, 0.08, 0.0], [-0.07, -0.03, 0.04, 0.11, 0.15, 0.19, 0.2, 0.22, 0.22, 0.19, 0.11, 0.04], [0.0, 0.04, 0.08, 0.19, 0.23, 0.29, 0.33, 0.36, 0.37, 0.32, 0.2, 0.11], [0.13, 0.2, 0.27, 0.37, 0.44, 0.51, 0.55, 0.61, 0.64, 0.55, 0.41, 0.22]]
#	duration = 346.076061

	# DTMF board
#	x_points = [0.0, 17.5, 35.0, 52.5, 70.0]
#	y_points = [0.0, 13.333333333333334, 26.666666666666668, 40.0]
#	probe_result = [[0.0, 0.28000000000000114, 0.490000000000002, 0.5599999999999987, 0.5199999999999996], [0.0, 0.1700000000000017, 0.33000000000000185, 0.41000000000000014, 0.41000000000000014], [-0.030000000000001137, 0.08999999999999986, 0.21999999999999886, 0.3000000000000007, 0.33000000000000185], [-0.08999999999999986, 0.03999999999999915, 0.16000000000000014, 0.26000000000000156, 0.28999999999999915]]
#	duration = 102.808573
	
	x_points = [70.0, 87.5, 105.0, 122.5, 140.0]
	y_points = [0.0, 13.333333333333334, 26.666666666666668, 40.0]
	probe_result = [[0.0, -0.15000000000000213, -0.28000000000000114, -0.38000000000000256, -0.4299999999999997], [-0.08000000000000185, -0.20000000000000284, -0.33999999999999986, -0.4400000000000013, -0.490000000000002], [-0.15000000000000213, -0.26000000000000156, -0.370000000000001, -0.46000000000000085, -0.5100000000000016], [-0.21000000000000085, -0.26000000000000156, -0.35999999999999943, -0.4400000000000013, -0.490000000000002]]
	duration = 105.028261

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
	
	x_points = np.linspace(min(x_points),max(x_points),50) 
	y_points = np.linspace(min(y_points),max(y_points),50) 
	
	z_points = Z_workbed_surface(y_points,x_points)
	
#	plt.figure()
	plt.hold(True)
	
	z_cf = plt.pcolor(x_points, y_points, z_points, alpha=0.2, cmap=cm.copper, edgecolors='k', linewidths=0) # Show Z probing height, with a light-tone colormap
	plt.colorbar()
#	plt.title("Z probing results (interpolated) [mm]")
	plt.axis('equal') # 1:1 aspect ratio
#	pltShowNonBlocking()

def getZoffset(x,y):
	return Z_workbed_surface(y,x)[0][0]



plt.ion() # IMPORTANT: Enable real-time plotting

gcodeviewer = pltNewFig() # Define a new figure, this doesnt open a window by itself (real-time plotting disabled)

probingResults()
print "Must be zero:",floats(getZoffset(0,0))

# Display the Gcode that is going to be etched
(etch_moves, travel_moves, gcode_minXY_global, gcode_maxXY_global) = gcv.view(filePath,fileName,showEtch=1)
#(etch_moves, travel_moves) = gcv.view(filePath,fileName,showEtch1=1)
#(etch_moves, travel_moves) = gcv.view(filePath,fileName,showEtch2=1)
#(etch_moves, travel_moves) = gcv.view(filePath,fileName,showDrill=1)
#(etch_moves, travel_moves) = gcv.view(filePath,fileName,showEdge=1)

# Show delimiter rectangle
x_dat = [gcode_minXY_global[0],gcode_minXY_global[0],gcode_maxXY_global[0],gcode_maxXY_global[0],gcode_minXY_global[0]]
y_dat = [gcode_minXY_global[1],gcode_maxXY_global[1],gcode_maxXY_global[1],gcode_minXY_global[1],gcode_minXY_global[1]]
plt.plot(x_dat,y_dat)

pltRefresh(gcodeviewer) # Draw the figure contents, still no window
pltShow() # Open the window showing our figure

#plt.show() # THIS SHOULD BE COMMENTED, USE FOR DEBUG

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
	pltSetFig(gcodeviewer)
	toolPos_point, = plt.plot(0, 0, markersize=12, c='g', marker='x')
	pltShowNonBlocking()

F_slowMove = 200 # Move speed [mm/min]
F_fastMove = 700

F_drillMove = 50
F_edgeMove = 25
F_etchMove = 100


cy.connect(BAUDRATE, DEVICE, Emulate)

cy.sendCommand("G90\n") # Set absolute positioning

cy.homeZXY() # Home all the axis

drawTool(10, 20) # Show a marker on the gcode plot


# Move to the origin of the grid
cy.moveXY(x_points[0], y_points[0], F_fastMove)


# Warning: Do not lower too much or you will potentially cause damage!
initial_Z_lowering_distance = -10
cy.moveZrelSafe(initial_Z_lowering_distance,F_slowMove/2) # Move Z towards the PCB (saves some probing time for the first coord)

Z_origin_offset = cy.probeZ()
print "Z offset:", Z_origin_offset






toolPos_X = 0
toolPos_Y = 0
toolPos_Z = 0
toolPos_F = F_fastMove

X_dest = 0
Y_dest = 0
Z_dest = 0
F_dest = F_fastMove

cy.moveZrelSafe(5,F_slowMove)
toolPos_Z = 5

pltSetFig(gcodeviewer)

Zlift = 1.0

Z_manual_offset = 0.0

maxDistance = 2**2 # [mm^2] 2mm (longer moves will be split to regulate Z)
minDistance = 0.001**2 # [mm^2] 0.001mm is the smallest distance that will be sent

def splitLongEtchMove(distance):
	global toolPos_X, toolPos_Y, toolPos_Z, toolPos_F, X_dest, Y_dest, Z_dest, F_dest
	
	X_dest_tmp = toolPos_X
	Y_dest_tmp = toolPos_Y
	Z_dest_tmp = toolPos_Z
	F_dest_tmp = toolPos_Z
	
	#distance = distance**0.5 # [mm]
	N_steps = int((distance/maxDistance)**0.5) # **must be** >= 1
	
	print "Splitting", distance**0.5, "mm segment into", N_steps, "steps"
	
#	print "Orig:", toolPos_X, toolPos_Y, toolPos_Z, "Dest:", X_dest, Y_dest, Z_dest
	
	X_step = (X_dest-toolPos_X)/float(N_steps)
	Y_step = (Y_dest-toolPos_Y)/float(N_steps)
	Z_step = (Z_dest-toolPos_Z)/float(N_steps)
	F_step = (F_dest-toolPos_F)/float(N_steps)
	
	for i in range(N_steps) :
		X_dest_tmp = toolPos_X + X_step
		Y_dest_tmp = toolPos_Y + Y_step
		Z_dest_tmp = toolPos_Z + Z_step
		F_dest_tmp = toolPos_F + F_step
		
		Z_real = Z_dest_tmp+Z_origin_offset+getZoffset(X_dest_tmp, Y_dest_tmp)+Z_manual_offset
		cy.moveXYZ(X_dest_tmp, Y_dest_tmp, Z_real, F_dest_tmp)
		toolPos_refresh(X_dest_tmp, Y_dest_tmp, etching=1)
		
#		print "Move:",X_dest_tmp, Y_dest_tmp, Z_dest_tmp
		
		toolPos_X = X_dest_tmp
		toolPos_Y = Y_dest_tmp
		toolPos_Z = Z_dest_tmp
		toolPos_F = F_dest_tmp


raw_input("Turn on the spindle and press enter to begin...")

for path in etch_moves :
	toolRefresh = 0
	toolPos_draw(toolPos_X, toolPos_Y, etching=0)
	cy.moveZ(Z_origin_offset+getZoffset(X_dest, Y_dest)+Z_manual_offset+Zlift,F_fastMove) # Raise and move to next point
	X_dest = path[0][0]
	Y_dest = path[0][1]
	F_dest = F_fastMove
	print "  Traveling to:", str([X_dest, Y_dest]), "at Z:", Z_manual_offset+Zlift
	cy.moveXY(X_dest, Y_dest, F_dest)
	toolPos_draw(X_dest, Y_dest, etching=0)
	Z_dest = path[0][2]
	if Z_dest > 0:
		F_dest = F_slowMove
	else:
		F_dest = path[0][3] # We set the original speed if it is etching/drill
	cy.moveZ(Z_dest+Z_origin_offset+getZoffset(X_dest, Y_dest)+Z_manual_offset,F_dest)
#	print "Speed:",F_dest
	print "  Etching at Z:",Z_dest+Z_manual_offset
	toolPos_X = X_dest
	toolPos_Y = Y_dest
	toolPos_Z = Z_dest # Not sure..
	toolPos_F = F_dest
	
#	print path
	
	for coord in path[1:] :
		X_dest = coord[0]
		Y_dest = coord[1]
		Z_dest = coord[2]
		F_dest = coord[3]
		
		distance = (X_dest-toolPos_X)**2+(Y_dest-toolPos_Y)**2
		if distance >= maxDistance :
			splitLongEtchMove(distance)
		if distance < minDistance and (Z_dest-toolPos_Z)**2 < 0.001**2 : # Make sure it is not a Z movement
			print "Ignoring", distance**0.5, "mm segment!"
			continue
		Z_real = Z_dest+Z_origin_offset+getZoffset(X_dest, Y_dest)+Z_manual_offset
		cy.moveXYZ(X_dest, Y_dest, Z_real, F_dest)
#		print "Coords: Speed:",F_dest
		toolPos_refresh(X_dest, Y_dest, etching=1)
		
		toolPos_X = X_dest
		toolPos_Y = Y_dest
		toolPos_Z = Z_dest
		toolPos_F = F_dest

cy.homeZXY()
cy.close() # Close the serial port connection

raw_input("Done. Press enter to exit...")

