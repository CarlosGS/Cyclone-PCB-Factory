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

# Begin modules
import sys

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

sys.path.append("../CycloneHost")
import GcodeParser as gcp
# End modules

filePath = "../GcodeGenerators/pyGerber2Gcode_CUI/out/"
fileName = "printshield" # sys.argv[1]

def plotPoints(path_list, color, linewidth): # Thanks to pprzemek (http://stackoverflow.com/questions/2282727/draw-points-using-matplotlib-pyplot-x1-y1-x2-y2)
	for path in path_list :
		a = np.array(path)
		line, = plt.plot(a[:,0], a[:,1], color, linewidth=linewidth*2)
		line.set_antialiased(False) # turn off antialising

plt.figure(1)

drill_diam = 0.8
etch_diam = 0.1
edge_diam = 2.4
linewidth_travel_move = etch_diam/2

#	b: blue
#	g: green
#	r: red
#	c: cyan
#	m: magenta
#	y: yellow
#	k: black
#	w: white

drill_color = 'r'
etch_color = 'g'
edge_color = 'b'
travel_color = 'c'

plt.subplot(121)
plt.hold(True)
plt.title("Original Gcode")
plt.axis('equal') # 1:1 aspect ratio

print "\n Loading etch..."
gcode_file = filePath+fileName+"_etch.gcode"
(etch_moves, travel_moves, grid_origin, grid_size) = gcp.parseGcodeRaw(gcode_file)
plotPoints(etch_moves, etch_color, etch_diam)
plotPoints(travel_moves, travel_color, linewidth_travel_move)

print "\n Loading drill..."
gcode_file = filePath+fileName+"_drill.gcode"
(etch_moves, travel_moves, grid_origin, grid_size) = gcp.parseGcodeRaw(gcode_file)
plotPoints(etch_moves, drill_color, drill_diam)
plotPoints(travel_moves, travel_color, linewidth_travel_move)

print "\n Loading edge..."
gcode_file = filePath+fileName+"_edge.gcode"
(etch_moves, travel_moves, grid_origin, grid_size) = gcp.parseGcodeRaw(gcode_file)
plotPoints(etch_moves, edge_color, edge_diam)
plotPoints(travel_moves, travel_color, linewidth_travel_move)


plt.subplot(122)
plt.hold(True)
plt.title("Optimized (closest neighbour)")
plt.axis('equal') # 1:1 aspect ratio

print "\n Loading etch..."
gcode_file = filePath+fileName+"_etch.gcode"
(etch_moves, travel_moves, grid_origin, grid_size) = gcp.parseGcodeRaw(gcode_file)
(etch_moves, travel_moves) = gcp.optimize(etch_moves)
plotPoints(etch_moves, etch_color, etch_diam)
plotPoints(travel_moves, travel_color, linewidth_travel_move)

print "\n Loading drill..."
gcode_file = filePath+fileName+"_drill.gcode"
(etch_moves, travel_moves, grid_origin, grid_size) = gcp.parseGcodeRaw(gcode_file)
(etch_moves, travel_moves) = gcp.optimize(etch_moves)
plotPoints(etch_moves, drill_color, drill_diam)
plotPoints(travel_moves, travel_color, linewidth_travel_move)

print "\n Loading edge..."
gcode_file = filePath+fileName+"_edge.gcode"
(etch_moves, travel_moves, grid_origin, grid_size) = gcp.parseGcodeRaw(gcode_file)
(etch_moves, travel_moves) = gcp.optimize(etch_moves)
plotPoints(etch_moves, edge_color, edge_diam)
plotPoints(travel_moves, travel_color, linewidth_travel_move)


plt.ion() # Enable real-time plotting to avoid blocking behaviour for pyplot
plt.show()

raw_input("Press enter to exit...")

