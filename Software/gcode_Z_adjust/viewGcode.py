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

sys.path.append("../CycloneHost")
import GcodeViewer as gcv
# End modules

# Temporary path to speedup testing
#import os
#from subprocess import call
#os.chdir("../GcodeGenerators/pyGerber2Gcode_CUI/")
#call(["pypy","./pygerber2gcode_cui_MOD.py"])
#os.chdir("../../gcode_Z_adjust")

filePath = "../GcodeGenerators/pyGerber2Gcode_CUI/out/"
fileName = "printshield" # sys.argv[1]

gcv.view(filePath,fileName)

raw_input("Press enter to exit...")

