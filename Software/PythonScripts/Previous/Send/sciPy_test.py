#From http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

samples = [[0.0, 0.21999999999999886, 0.40000000000000213, 0.5500000000000007, 0.620000000000001, 0.620000000000001, 0.5800000000000018, 0.5199999999999996, 0.4800000000000004, 0.40000000000000213, 0.26000000000000156, 0.120000000000001], [-0.07000000000000028, 0.03999999999999915, 0.15000000000000213, 0.26000000000000156, 0.3200000000000003, 0.35999999999999943, 0.33000000000000185, 0.3000000000000007, 0.26000000000000156, 0.23000000000000043, 0.120000000000001, 0.0], [-0.10999999999999943, 0.0, 0.03999999999999915, 0.120000000000001, 0.16000000000000014, 0.21999999999999886, 0.19000000000000128, 0.21999999999999886, 0.19000000000000128, 0.15000000000000213, 0.08000000000000185, 0.0], [-0.16000000000000014, -0.07000000000000028, 0.0, 0.08000000000000185, 0.15000000000000213, 0.19000000000000128, 0.19000000000000128, 0.21999999999999886, 0.21999999999999886, 0.16000000000000014, 0.10999999999999943, 0.0], [-0.07000000000000028, 0.0, 0.03999999999999915, 0.15000000000000213, 0.21999999999999886, 0.26000000000000156, 0.3000000000000007, 0.3200000000000003, 0.3200000000000003, 0.3000000000000007, 0.1999999999999993, 0.08000000000000185], [0.08000000000000185, 0.15000000000000213, 0.21999999999999886, 0.28999999999999915, 0.4299999999999997, 0.4800000000000004, 0.5199999999999996, 0.5899999999999999, 0.5800000000000018, 0.5199999999999996, 0.40000000000000213, 0.23000000000000043]]

grid_origin_X = float(0) # Initial point of the grid [mm]
grid_origin_Y = float(0)

grid_len_X = float(135) #135 # Distance to probe [mm]
grid_len_Y = float(84) #84

grid_N_X = int(12) #12 # Number of points
grid_N_Y = int(6) #6

grid_inc_X = grid_len_X/float(grid_N_X-1) # [mm]
grid_inc_Y = grid_len_Y/float(grid_N_Y-1)

grid_x = [ float(x_i)*grid_inc_X + grid_origin_X for x_i in range(grid_N_X) ]
grid_y = [ float(y_i)*grid_inc_Y + grid_origin_Y for y_i in range(grid_N_Y) ]

#probe_grid = [ [ 0 for i in range(grid_N_X) ] for j in range(grid_N_Y) ]

print np.array(samples)
print np.shape(np.array(samples))
print np.shape(np.array(grid_x))
workbed_height = interpolate.RectBivariateSpline(np.array(grid_y), np.array(grid_x), np.array(samples))

print workbed_height(15,16)

plt.ion() # Enable real-time plotting to avoid blocking behaviour for pyplot

# Define function over sparse 20x20 grid

x,y = np.mgrid[-1:1:20j,-1:1:20j]
z = (x+y)*np.exp(-6.0*(x*x+y*y))

plt.figure(1)
plt.pcolor(x,y,z)
plt.colorbar()
plt.title("Sparsely sampled function.")
plt.show()

# Interpolate function over new 70x70 grid

xnew,ynew = np.mgrid[-1:1:70j,-1:1:70j]
tck = interpolate.bisplrep(x,y,z,s=0)
znew = interpolate.bisplev(xnew[:,0],ynew[0,:],tck)

plt.figure(2)
plt.pcolor(xnew,ynew,znew)
plt.colorbar()
plt.title("Interpolated function.")
plt.show()

