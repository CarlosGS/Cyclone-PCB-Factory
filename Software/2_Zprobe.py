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
from misc import *

import CycloneHost.Controller as cy
# End modules

# Load the Z data file
Z_probing_data = loadFromFile(Z_PROBING_FILE)


cy.connect(BAUDRATE, DEVICE, Emulate)

cy.sendCommand("G90\n") # Set absolute positioning

cy.homeZXY() # Home all the axis

# (x,y)
#grid_origin = (0,0)	# Initial point of the grid [mm]
#grid_len = (135,84)	# Distance to probe [mm]
#GRID_N_POINTS = (12,6)	# Number of points
#grid_origin = (0,0)	# Initial point of the grid [mm]
#grid_len = (80,60)	# Distance to probe [mm]

# Use the max values generated when loading the gerber files
grid_origin = Z_probing_data['grid_origin']
grid_len = Z_probing_data['grid_len']


# Initial Z lowering for speed up the first probe
cy.moveZrelSafe(initial_Z_lowering_distance,F_slowMove) # Move Z towards the PCB (saves some probing time for the first coord)

# Do the probing itself
(x_points, y_points, probe_result, Z_offset, probe_duration) = cy.probeGrid(grid_origin, grid_len, GRID_N_POINTS, Zlift, F_fastMove, F_slowMove)

#x_points = [0.0, 17.5, 35.0, 52.5, 70.0]
#y_points = [0.0, 13.333333333333334, 26.666666666666668, 40.0]
#probe_result = [[0.0, 0.28000000000000114, 0.490000000000002, 0.5599999999999987, 0.5199999999999996], [0.0, 0.1700000000000017, 0.33000000000000185, 0.41000000000000014, 0.41000000000000014], [-0.030000000000001137, 0.08999999999999986, 0.21999999999999886, 0.3000000000000007, 0.33000000000000185], [-0.08999999999999986, 0.03999999999999915, 0.16000000000000014, 0.26000000000000156, 0.28999999999999915]]
#duration = 102.808573

# Save the values to the Z probing file
Z_probing_data['x_points'] = x_points
Z_probing_data['y_points'] = y_points
Z_probing_data['probe_result'] = probe_result
Z_probing_data['probe_duration'] = probe_duration
saveToFile(Z_probing_data,Z_PROBING_FILE)

# Show our grid
print("#--------   Probing results   ---------")
print("x_points = " + str(x_points) )
print("y_points = " + str(y_points) )
print("probe_result = " + str(probe_result) )
print("probe_duration = " + str(probe_duration) )
print("#--------------------------------------")

# Display values

# Must be converted into arrays to use scipy
x_points = np.array(x_points)
y_points = np.array(y_points)
probe_result = np.array(probe_result)

plt.ion() # IMPORTANT: Enable real-time plotting

plt.figure()
plt.pcolor(x_points, y_points, probe_result)
plt.colorbar()
plt.title("Z probing results [mm]")
plt.axis('equal') # 1:1 aspect ratio
pltShowNonBlocking()

# Interpolation
Z_workbed_surface = interpolate.RectBivariateSpline(y_points, x_points, probe_result)

# Evaluate the interpolation in a 50x50 grid for display
x_points = np.linspace(min(x_points),max(x_points),100) 
y_points = np.linspace(min(y_points),max(y_points),100) 
z_points = Z_workbed_surface(y_points,x_points)
#print( str(z_points) )

plt.figure()
plt.pcolor(x_points, y_points, z_points)
plt.colorbar()
plt.title("Z probing results (interpolated) [mm]")
plt.axis('equal') # 1:1 aspect ratio
pltShowNonBlocking()

cy.close() # Close the connection with Cyclone

print("Press enter to exit...")
val = sys.stdin.readline()

