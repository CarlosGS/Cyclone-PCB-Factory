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
from matplotlib import cm

sys.path.append("../CycloneHost")
import GcodeViewer as gcv
# End modules

# Temporary path to speedup testing
import os
from subprocess import call
os.chdir("../GcodeGenerators/pyGerber2Gcode_CUI/")
call(["pypy","./pygerber2gcode_cui_MOD.py"])
os.chdir("../../gcode_Z_adjust")





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




plt.ion() # IMPORTANT: Enable real-time plotting

gcodeviewer = pltNewFig() # Define a new figure, this doesnt open a window by itself (real-time plotting disabled)




filePath = "../GcodeGenerators/pyGerber2Gcode_CUI/out/"
fileName = "DTMF_Shield_etch" # sys.argv[1]

gcv.view(filePath,fileName,showAll=1)



pltRefresh(gcodeviewer) # Draw the figure contents, still no window
pltShow() # Open the window showing our figure

raw_input("Press enter to exit...")

