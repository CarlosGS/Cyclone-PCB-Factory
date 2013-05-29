# -*- encoding: utf-8 -*-
# Based on http://scipy-user.10969.n7.nabble.com/2D-Interpolation-td4248.html

import scipy
import scipy.interpolate 

def pltShowNonBlocking():
	plt.ion() # Enable real-time plotting to avoid blocking behaviour for plt.show()
	plt.show()
	plt.ioff() # Disable real-time plotting

# the two axes 
x = scipy.array([0.0, 12.272727272727273, 24.545454545454547, 36.81818181818182, 49.09090909090909, 61.36363636363637, 73.63636363636364, 85.9090909090909, 98.18181818181819, 110.45454545454547, 122.72727272727273, 135.0])
y = scipy.array([0.0, 16.8, 33.6, 50.400000000000006, 67.2, 84.0])

# make some pretend data 
gridy, gridx = scipy.meshgrid(x,y) 
z = scipy.array([[0.0, 0.2, 0.4, 0.53, 0.58, 0.6, 0.56, 0.53, 0.5, 0.44, 0.33, 0.2], [-0.03, 0.07, 0.16, 0.26, 0.32, 0.33, 0.33, 0.33, 0.29, 0.23, 0.15, 0.05], [-0.07, 0.0, 0.05, 0.12, 0.16, 0.2, 0.2, 0.22, 0.2, 0.16, 0.08, 0.0], [-0.07, -0.03, 0.04, 0.11, 0.15, 0.19, 0.2, 0.22, 0.22, 0.19, 0.11, 0.04], [0.0, 0.04, 0.08, 0.19, 0.23, 0.29, 0.33, 0.36, 0.37, 0.32, 0.2, 0.11], [0.13, 0.2, 0.27, 0.37, 0.44, 0.51, 0.55, 0.61, 0.64, 0.55, 0.41, 0.22]])

# create a spline interpolator 
spl = scipy.interpolate.RectBivariateSpline(y,x,z) 

# make some new axes to interpolate to 
nx = scipy.linspace(min(x),max(x),100) 
ny = scipy.linspace(min(y),max(y),100) 

# evaluate 
nz = spl(ny, nx) 

import matplotlib.pyplot as plt

plt.figure()
plt.pcolor(x, y, z)
plt.title("Datos [mm]")
plt.colorbar()
plt.axis('equal') # 1:1 aspect ratio
pltShowNonBlocking()

plt.figure()
plt.pcolor(nx, ny, nz)
plt.title("Datos interpolados [mm]")
plt.colorbar()
plt.axis('equal') # 1:1 aspect ratio
pltShowNonBlocking()

# Comprobación de que el error es mínimo
plt.figure()
plt.pcolor(x, y, spl(y,x) - z)
plt.title("Diferencia entre datos originales e interpolados (error) [mm]")
plt.colorbar()
plt.axis('equal') # 1:1 aspect ratio
pltShowNonBlocking()

raw_input("Press enter to exit...")

