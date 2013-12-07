# Begin configuration
BAUDRATE = 115200
DEVICE = "/dev/ttyUSB0"
Emulate = False # Won't connect to the machine, will emulate the commands!

# For GenerateGcode and Send
filePath = "./GcodeGenerators/pyGerber2Gcode_CUI/out/"
fileName = "controller"
# Note: Don't forget to edit ./GcodeGenerators/pyGerber2Gcode_CUI/pygerber2gcode_cui_MOD.conf to match the name and board files

# For Zprobe
GRID_N_POINTS = (4,4)	# Number of points (AT LEAST 4 IN EACH DIRECTION, OTHERWISE INTERPOLATION WILL FAIL)
Zlift = 0.5 # mm # Lift between probings, it is relative so should be enough

# For Zprobe and Send
F_fastMove = 70000 # mm/s
F_slowMove = 20000 # mm/s
initial_Z_lowering_distance = -5 # Warning: Do not lower too much or you will potentially cause damage!

N_copies_X = 1 # Panelizing options!
N_copies_Y = 1
margin_copies_X = 5 # mm
margin_copies_Y = 5 # mm

# For Send
# IMPORTANT: Select the gcode that is to be milled (only one at a time)
showEtch=1
showEtch2=0
showEtch3=0
showDrill=0
showEdge=0 # Caution, buggy!

Zlift_milling = 1.0 # mm
Z_global_offset = -0.02 #-0.018 go deeper!

maxDistance = 1**2 # [mm^2] 2mm (longer moves will be split to regulate Z)
minDistance = 0.001**2 # [mm^2] 0.001mm is the smallest distance that will be sent

Z_PROBING_FILE = "Z_probing_data.p"
# End configuration

