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

import CycloneHost.GcodeViewer as gcv
# End modules

# Gcode generation
import os
from subprocess import call
original_dir = os.getcwd()
os.chdir("./GcodeGenerators/pyGerber2Gcode_CUI/")
#call(["python","./pygerber2gcode_cui_MOD.py"])
call(["pypy","./pygerber2gcode_cui_MOD.py"]) # If you have "pypy" installed go ahead!
os.chdir(original_dir)


Z_PROBING_FILE = "Z_probing_data.p"


gcodeviewer = plt.figure()




#filePath = "./GcodeGenerators/pyGerber2Gcode_CUI/out/"
#fileName = "GNBoard" # sys.argv[1]

(etch_moves, travel_moves, gcode_minXY_global, gcode_maxXY_global) = gcv.view(filePath,fileName,showAll=1)

# Save the dimensions for the Z probing
Z_probing_data = {}
Z_probing_data['grid_origin'] = gcode_minXY_global
(grid_len_X,grid_len_Y) = (gcode_maxXY_global[0]-gcode_minXY_global[0], gcode_maxXY_global[1]-gcode_minXY_global[1])

# We take in account panelizing
grid_len_X *= N_copies_X
grid_len_X += N_copies_X*margin_copies_X

grid_len_Y *= N_copies_Y
grid_len_Y += N_copies_Y*margin_copies_Y

print("PANELIZING: There will be " + str(N_copies_X)+"x"+str(N_copies_Y) + " copies of this board")

Z_probing_data['grid_len'] = (grid_len_X,grid_len_Y)

saveToFile(Z_probing_data,Z_PROBING_FILE)

plt.show() # Open the window showing our figure

print("Press enter to exit...")
val = sys.stdin.readline()

