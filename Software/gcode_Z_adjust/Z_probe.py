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

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

sys.path.append("../CycloneHost")
import CycloneHost as cy
# End modules

cy.connect(BAUDRATE, DEVICE, Emulate)

cy.sendCommand("G90\n") # Set absolute positioning

cy.homeZXY() # Home all the axis

# (x,y)
#grid_origin = (0,0)	# Initial point of the grid [mm]
#grid_len = (135,84)	# Distance to probe [mm]
#grid_N = (12,6)	# Number of points
grid_origin = (0,0)	# Initial point of the grid [mm]
grid_len = (80,60)	# Distance to probe [mm]
grid_N = (5,5)	# Number of points (AT LEAST 4 IN EACH DIRECTION, OTHERWISE INTERPOLATION WILL FAIL)

Zlift = 0.5 # mm

F_slowMove = 100

# Warning: Do not lower too much or you will potentially cause damage!
initial_Z_lowering_distance = -10
cy.moveZrelSafe(initial_Z_lowering_distance,F_slowMove) # Move Z towards the PCB (saves some probing time for the first coord)

(x_points, y_points, probe_result, Z_offset, duration) = cy.probeGrid(grid_origin, grid_len, grid_N, Zlift)

#x_points = [0.0, 12.272727272727273, 24.545454545454547, 36.81818181818182, 49.09090909090909, 61.36363636363637, 73.63636363636364, 85.9090909090909, 98.18181818181819, 110.45454545454547, 122.72727272727273, 135.0]
#y_points = [0.0, 16.8, 33.6, 50.400000000000006, 67.2, 84.0]
#probe_result = [[0.0, 0.2, 0.4, 0.53, 0.58, 0.6, 0.56, 0.53, 0.5, 0.44, 0.33, 0.2], [-0.03, 0.07, 0.16, 0.26, 0.32, 0.33, 0.33, 0.33, 0.29, 0.23, 0.15, 0.05], [-0.07, 0.0, 0.05, 0.12, 0.16, 0.2, 0.2, 0.22, 0.2, 0.16, 0.08, 0.0], [-0.07, -0.03, 0.04, 0.11, 0.15, 0.19, 0.2, 0.22, 0.22, 0.19, 0.11, 0.04], [0.0, 0.04, 0.08, 0.19, 0.23, 0.29, 0.33, 0.36, 0.37, 0.32, 0.2, 0.11], [0.13, 0.2, 0.27, 0.37, 0.44, 0.51, 0.55, 0.61, 0.64, 0.55, 0.41, 0.22]]
#duration = 346.076061

#x_points = [0.0, 17.5, 35.0, 52.5, 70.0]
#y_points = [0.0, 13.333333333333334, 26.666666666666668, 40.0]
#probe_result = [[0.0, 0.28000000000000114, 0.490000000000002, 0.5599999999999987, 0.5199999999999996], [0.0, 0.1700000000000017, 0.33000000000000185, 0.41000000000000014, 0.41000000000000014], [-0.030000000000001137, 0.08999999999999986, 0.21999999999999886, 0.3000000000000007, 0.33000000000000185], [-0.08999999999999986, 0.03999999999999915, 0.16000000000000014, 0.26000000000000156, 0.28999999999999915]]
#duration = 102.808573


# Show our grid
print "#--- Probing results [BEGIN COPY TO Send.py] ---"
print "x_points = ", x_points
print "y_points = ", y_points
print "probe_result = ", probe_result
print "duration = ", duration
print "#--- [END COPY TO Send.py] ---"

# Must be converted into arrays to use scipy
x_points = np.array(x_points)
y_points = np.array(y_points)
probe_result = np.array(probe_result)

def pltShowNonBlocking():
	plt.ion() # Enable real-time plotting to avoid blocking behaviour for plt.show()
	plt.show()
	plt.ioff() # Disable real-time plotting

plt.figure()
plt.pcolor(x_points, y_points, probe_result)
plt.colorbar()
plt.title("Z probing results [mm]")
plt.axis('equal') # 1:1 aspect ratio
pltShowNonBlocking()

# Interpolation
Z_workbed_surface = interpolate.RectBivariateSpline(y_points, x_points, probe_result)

x_points = np.linspace(min(x_points),max(x_points),100) 
y_points = np.linspace(min(y_points),max(y_points),100) 

z_points = Z_workbed_surface(y_points,x_points)
print z_points

plt.figure()
plt.pcolor(x_points, y_points, z_points)
plt.colorbar()
plt.title("Z probing results (interpolated) [mm]")
plt.axis('equal') # 1:1 aspect ratio
pltShowNonBlocking()

# TODO:
# - Export results to a file with a standarized format
# - 

cy.close() # Close the serial port connection

raw_input("Press enter to exit...")

