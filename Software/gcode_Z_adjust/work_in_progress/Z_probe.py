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
# End configuration

# Begin modules
import sys

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

sys.path.append("../CycloneHost")
import CycloneHost as cy
# End modules

cy.connect(BAUDRATE, DEVICE)

cy.sendCommand("G90\n") # Set absolute positioning

cy.homeZXY() # Home all the axis

# (x,y)
grid_origin = (0,0)	# Initial point of the grid [mm]
grid_len = (135,84)	# Distance to probe [mm]
grid_N = (12,6)	# Number of points

Zlift = 0.5 # mm

# Warning: Do not lower too much or you will potentially cause damage!
initial_Z_lowering_distance = -15
cy.moveZrelSafe(initial_Z_lowering_distance,F_slowMove) # Move Z towards the PCB (saves some probing time for the first coord)

(x_points, y_points, probe_result, Z_offset, duration) = cy.probeGrid(grid_origin, grid_len, grid_N, Zlift)

# Show our grid
print "--- Probing results ---"
print "-> X points:", x_points
print "-> Y points:", y_points
print "-> Grid:", probe_result
print "-> Duration:", duration

plt.ion() # Enable real-time plotting to avoid blocking behaviour for pyplot

plt.figure(1)
plt.pcolor(np.array(x_points), np.array(y_points), np.array(probe_result))
plt.colorbar()
plt.title("Z probing results [mm]")
plt.show()

# TODO:
# - Export results to a file with a standarized format
# - 

cy.close() # Close the serial port connection

raw_input("Press enter to exit...")

