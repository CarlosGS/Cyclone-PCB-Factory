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
from configuration import * # load settings
# End configuration

# Begin modules
import sys
from datetime import datetime
import time

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from matplotlib import cm

from misc import *

import CycloneHost.GcodeViewer as gcv
import CycloneHost.Controller as cy
from CycloneHost.helper import *
# End modules


def probingResults(): # quick and dirty temporal code
	global Z_workbed_surface, x_points, y_points
	
	# Load the Z data file
	Z_probing_data = loadFromFile(Z_PROBING_FILE)
	
	x_points =  Z_probing_data['x_points']
	y_points =  Z_probing_data['y_points']
	probe_result =  Z_probing_data['probe_result']
	probe_duration =  Z_probing_data['probe_duration']

	# Must be converted into arrays to use scipy
	x_points = np.array(x_points)
	y_points = np.array(y_points)
	probe_result = np.array(probe_result)
	
	# Setup interpolation object
	Z_workbed_surface = interpolate.RectBivariateSpline(y_points, x_points, probe_result)
	
	# Evaluate the interpolation in a 50x50 grid for display
	x_points = np.linspace(min(x_points),max(x_points),50) 
	y_points = np.linspace(min(y_points),max(y_points),50) 
	z_points = Z_workbed_surface(y_points,x_points)
	
	# This will show the Z probing result behind the actual PCB layout, for reference
	plt.hold(True)
	z_cf = plt.pcolor(x_points, y_points, z_points, alpha=0.2, cmap=cm.copper, edgecolors='k', linewidths=0) # Show Z probing height, with a light-tone colormap
	plt.colorbar()
	plt.axis('equal') # 1:1 aspect ratio

def getZoffset(x,y): # Returns the offset using interpolation
	return Z_workbed_surface(y,x)[0][0]



plt.ion() # IMPORTANT: Enable real-time plotting

gcodeviewer = pltNewFig() # Define a new figure, this doesnt open a window by itself (real-time plotting disabled)

# Load the probing results (this will plot the copper level in the background too)
probingResults()
#print("Must be zero, otherwise the interpolation is wrong!: " + floats(getZoffset(0,0)))

# Display the Gcode that is going to be etched
(etch_moves, travel_moves, gcode_minXY, gcode_maxXY) = gcv.view(filePath,fileName,0,showEtch,showEtch2,showEtch3,showDrill,showEdge)
#(etch_moves, travel_moves) = gcv.view(filePath,fileName,showEtch1=1)
#(etch_moves, travel_moves) = gcv.view(filePath,fileName,showEtch2=1)
#(etch_moves, travel_moves) = gcv.view(filePath,fileName,showDrill=1)
#(etch_moves, travel_moves) = gcv.view(filePath,fileName,showEdge=1)

(boardSizeX,boardSizeY,gcode_minXY_global, gcode_maxXY_global) = gcv.boardSize(filePath,fileName)

# Show delimiter rectangle
#x_dat = [gcode_minXY_global[0],gcode_minXY_global[0],gcode_maxXY_global[0],gcode_maxXY_global[0],gcode_minXY_global[0]]
#y_dat = [gcode_minXY_global[1],gcode_maxXY_global[1],gcode_maxXY_global[1],gcode_minXY_global[1],gcode_minXY_global[1]]
#plt.plot(x_dat,y_dat)

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


cy.connect(BAUDRATE, DEVICE, Emulate)

cy.sendCommand("G90\n") # Set absolute positioning

cy.homeZXY() # Home all the axis

drawTool(10, 20) # Show a marker on the gcode plot


# Move to the origin of the grid
cy.moveXY(x_points[0], y_points[0], F_fastMove)


# Warning: Do not lower too much or you will potentially cause damage!
initial_Z_lowering_distance = -10
cy.moveZrelSafe(initial_Z_lowering_distance,F_slowMove) # Move Z towards the PCB (saves some probing time for the first coord)

Z_origin_offset = cy.probeZ()
print("Z offset: " + str(Z_origin_offset) )


toolPos_X = 0
toolPos_Y = 0
toolPos_Z = 0
toolPos_F = F_fastMove

X_dest = 0
Y_dest = 0
Z_dest = 0
F_dest = F_fastMove

# Move Z up 5mm, once we have the Z=0 reference. We will then pause to allow user remove electrodes and turn on the spindle
cy.moveZrelSafe(5,F_slowMove)
toolPos_Z = 5

pltSetFig(gcodeviewer)

def splitLongEtchMove(distance):
	global toolPos_X, toolPos_Y, toolPos_Z, toolPos_F, X_dest, Y_dest, Z_dest, F_dest
	
	X_dest_tmp = toolPos_X
	Y_dest_tmp = toolPos_Y
	Z_dest_tmp = toolPos_Z
	F_dest_tmp = toolPos_Z
	
	#distance = distance**0.5 # [mm]
	N_steps = int((distance/maxDistance)**0.5) # **must be** >= 1
	
	print("Splitting " + str(distance**0.5) + "mm segment into " + str(N_steps) + " steps")
	
#	print("Orig: " + (toolPos_X,toolPos_Y,toolPos_Z) + " Dest: " + (X_dest, Y_dest, Z_dest))
	
	X_step = (X_dest-toolPos_X)/float(N_steps)
	Y_step = (Y_dest-toolPos_Y)/float(N_steps)
	Z_step = (Z_dest-toolPos_Z)/float(N_steps)
	F_step = (F_dest-toolPos_F)/float(N_steps)
	
	for i in range(N_steps) :
		X_dest_tmp = toolPos_X + X_step
		Y_dest_tmp = toolPos_Y + Y_step
		Z_dest_tmp = toolPos_Z + Z_step
		F_dest_tmp = toolPos_F + F_step
		
		Z_real = Z_dest_tmp+Z_origin_offset+getZoffset(X_dest_tmp, Y_dest_tmp)+Z_global_offset
		cy.moveXYZ(X_dest_tmp, Y_dest_tmp, Z_real, F_dest_tmp)
		toolPos_refresh(X_dest_tmp, Y_dest_tmp, etching=1)
		
#		print("Move: " + (X_dest_tmp, Y_dest_tmp, Z_dest_tmp) )
		
		toolPos_X = X_dest_tmp
		toolPos_Y = Y_dest_tmp
		toolPos_Z = Z_dest_tmp
		toolPos_F = F_dest_tmp


print("Turn on the spindle and press enter to begin...")
val = sys.stdin.readline()

def doPath(X_offset=0, Y_offset=0):
	global toolPos_X, toolPos_Y, toolPos_Z, toolPos_F, X_dest, Y_dest, Z_dest, F_dest
	for path in etch_moves :
		toolRefresh = 0
		toolPos_draw(toolPos_X, toolPos_Y, etching=0)
		cy.moveZ(Z_origin_offset+getZoffset(X_dest, Y_dest)+Z_global_offset+Zlift_milling,F_fastMove) # Raise and move to next point
		X_dest = path[0][0]+X_offset
		Y_dest = path[0][1]+Y_offset
		F_dest = F_fastMove
		print("  Traveling to: " + str([X_dest, Y_dest]) + " at Z:" + str(Z_global_offset+Zlift_milling) )
		cy.moveXY(X_dest, Y_dest, F_dest)
		toolPos_draw(X_dest, Y_dest, etching=0)
		Z_dest = path[0][2]
		if Z_dest > 0:
			F_dest = F_slowMove
		else:
			F_dest = path[0][3] # We set the original speed if it is etching/drill
		cy.moveZ(Z_dest+Z_origin_offset+getZoffset(X_dest, Y_dest)+Z_global_offset,F_dest)
	#	print("Speed:",F_dest)
		print("  Etching at Z: " + str(Z_dest+Z_global_offset) )
		toolPos_X = X_dest
		toolPos_Y = Y_dest
		toolPos_Z = Z_dest # Not sure..
		toolPos_F = F_dest
	
	#	print(path)
	
		for coord in path[1:] :
			X_dest = coord[0]+X_offset
			Y_dest = coord[1]+Y_offset
			Z_dest = coord[2]
			F_dest = coord[3]
		
			distance = (X_dest-toolPos_X)**2+(Y_dest-toolPos_Y)**2
			if distance >= maxDistance :
				splitLongEtchMove(distance)
			if distance < minDistance and (Z_dest-toolPos_Z)**2 < 0.001**2 : # Make sure it is not a Z movement
				print("Ignoring " + str(distance**0.5) + "mm segment!")
				continue
			Z_real = Z_dest+Z_origin_offset+getZoffset(X_dest, Y_dest)+Z_global_offset
			cy.moveXYZ(X_dest, Y_dest, Z_real, F_dest)
	#		print("Coords: Speed: " + str(F_dest))
			toolPos_refresh(X_dest, Y_dest, etching=1)
		
			toolPos_X = X_dest
			toolPos_Y = Y_dest
			toolPos_Z = Z_dest
			toolPos_F = F_dest

# Panelizing supported!
for x_i in range(N_copies_X):
	for y_i in range(N_copies_Y):
		doPath(x_i*(boardSizeX+margin_copies_X), y_i*(boardSizeY+margin_copies_Y))

cy.homeZXY() # It is important to send a blocking command in the end
cy.close() # Close the connection with Cyclone

print("Done. Press enter to exit...")
val = sys.stdin.readline()

