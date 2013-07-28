#!/usr/bin/pypy
# coding: UTF-8

from string import *
from math import *
#from struct import *
import os
import sys
#import datetime
import locale
import re
from datetime import datetime
from time import mktime
import gerber_merge as gm


#Global Constant
HUGE = 1e10
TINY = 1e-6
SMALL = 1e-3
MERGINE = 1e-4
INCH = 25.4 #mm
MIL = INCH/1000
WINDOW_X = 800
WINDOW_Y = 600
CENTER_X=200.0
CENTER_Y=200.0

#For CNC machine
INI_X = 0
INI_Y = 0
INI_Z = 5.0
MOVE_HEIGHT = 1.0
XY_SPEED = 100
Z_SPEED = 60
DRILL_SPEED = 50	#Drill down speed
DRILL_DEPTH = -1.2#Drill depth
CUT_DEPTH = -0.07	#pattern cutting depth
TOOL_D = 0.1		#Tool diameter
TOOL_2PASS_D = 0.5		#Tool diameter
TOOL_3PASS_D = 1		#Tool diameter
DRILL_D = 0.8		#Drill diameter
EDGE_TOOL_D = 1.0		#Edge Tool diameter
EDGE_DEPTH = -1.2 #edge depth
EDGE_SPEED = 80	#Edge cut speed
EDGE_Z_SPEED = 60	#Edge down speed
Z_STEP_DRILL = -0.3
Z_STEP_EDGE = -0.5

#for convert
MCODE_FLAG = 0
MERGE_DRILL_DATA = 0
LEFT_X = 5.0
LOWER_Y = 5.0
#For file
OUT_INCH_FLAG = 0
IN_INCH_FLAG = 1
CAD_UNIT = MIL/10
DRILL_UNIT = INCH
EDGE_UNIT = MIL/10
GERBER_EXT = '*.gtl'
DRILL_EXT = '*.drl'
EDGE_EXT = '*.gbr'
GCODE_EXT = '*.ngc'
GDRILL_EXT = '*.ngc'
GEDGE_EXT = '*.ngc'

MM_PER_ARC_SEGMENT = 0.5 # [mm] This is used to reduce resolution

#View
GERBER_COLOR = 'BLACK'	#black
DRILL_COLOR = 'BLUE'
EDGE_COLOR = 'GREEN YELLOW'
CONTOUR_COLOR = 'MAGENTA'

#
GERBER_DIR = ""
FRONT_FILE = ""
BACK_FILE = ""
DRILL_FILE = ""
EDGE_FILE = ""
MIRROR_FRONT = 0
MIRROR_BACK = 0
MIRROR_DRILL = 0
MIRROR_EDGE = 0
ROT_ANG = 0
OUT_DIR = ""
OUT_FRONT_FILE = ""
OUT_FRONT_2PASS_FILE = ""
OUT_FRONT_3PASS_FILE = ""
OUT_BACK_FILE = ""
OUT_BACK_2PASS_FILE = ""
OUT_BACK_3PASS_FILE = ""
OUT_DRILL_FILE = ""
OUT_EDGE_FILE = ""

#Global variable
gXMIN = HUGE
gYMIN = HUGE
gXMAX = -HUGE
gYMAX = -HUGE
gXSHIFT = 0
gYSHIFT = 0
gFRONT_DATA = ""
gBACK_DATA = ""
gFRONT_2PASS_DATA = ""
gBACK_2PASS_DATA = ""
gFRONT_3PASS_DATA = ""
gBACK_3PASS_DATA = ""
gDRILL_DATA = ""
gEDGE_DATA = ""
gTMP_X = INI_X 
gTMP_Y = INI_Y
gTMP_Z = INI_Z
gTMP_DRILL_X = INI_X 
gTMP_DRILL_Y = INI_Y
gTMP_DRILL_Z = INI_Z
gTMP_EDGE_X = INI_X 
gTMP_EDGE_Y = INI_Y
gTMP_EDGE_Z = INI_Z
gGERBER_TMP_X = 0
gGERBER_TMP_Y = 0
gDCODE = [0]*100
g54_FLAG = 0
gFIG_NUM = 0
gDRILL_TYPE = [0]*100
gDRILL_D = 0
gPOLYGONS = []
gLINES = []
gLINES2 = []
gEDGES = []
gDRILLS = []
gDRILL_LINES = []
gGCODES = []
gUNIT = 1

gGERBER_FILE = ""
gDRILL_FILE = ""
gEDGE_FILE = ""

gGCODE_FILE = ""
gGDRILL_FILE = ""
gGEDGE_FILE = ""

#For Drawing 
gPATTERNS = []
gDRAWDRILL = []
gDRAWEDGE = []
gDRAWCONTOUR = []
gMAG = 1.0
gPRE_X = CENTER_X
gPRE_Y = CENTER_X
gMAG_MIN = 0.1
gMAG_MAX = 100.0
gDRAW_XSHIFT = 0.0
gDRAW_YSHIFT = 0.0
gDISP_GERBER = 1
gDISP_DRILL = 0
gDISP_EDGE = 0
gDISP_CONTOUR = 0

TEST_POINTS1 =[]
TEST_POINTS2 =[]
TEST_POINT_R = 0.01

PRE_IN_FLAG = -1

def floats(val): # This is used to convert a float value to a string (avoiding exponent notation)
	return '{:f}'.format(float(val)) # It truncates the decimals that aren't used
	#return '{:.3f}'.format(float(val)) # It truncates the decimals that aren't used

#Set Class
class DRAWPOLY:
	def __init__(self, points, color ,delete):
		self.points = points
		self.color = color
		self.delete = delete

class POLYGON:
	def __init__(self, x_min, x_max, y_min, y_max, points, delete):
		self.x_min = x_min
		self.x_max = x_max
		self.y_min = y_min
		self.y_max = y_max
		self.points = points
		self.delete = delete

class LINE:
	def __init__(self, x1, y1, x2, y2, inside, delete):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.inside = inside
		self.delete = delete
class LINE2:
	def __init__(self, p1, p2, inside, delete):
		self.p1 = p1
		self.p2 = p2
		self.inside = inside
		self.delete = delete

class POINT:
	def __init__(self, x, y, inside, delete):
		self.x = x
		self.y = y
		self.inside = inside
		self.delete = delete

class DRILL:
	def __init__(self, x, y, d, delete):
		self.x = x
		self.y = y
		self.d = d
		self.delete = delete

class D_DATA:
	def __init__(self, atype, mod1, mod2):
		self.atype = atype
		self.mod1 = mod1
		self.mod2 = mod2

class GCODE:
	def __init__(self, x1, y1, x2, y2, gtype, mod1, mod2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.gtype = gtype
		self.mod1 = mod1
		self.mod2 = mod2

#functions
def main():
	global TOOL_D
	if len(sys.argv) > 1:
		read_config(sys.argv[1])
	else :
		read_config("pygerber2gcode_cui_MOD.conf")
	set_unit()
	gcode_init()
	front_poly = []
	back_poly = []
	front_poly_2pass = []
	back_poly_2pass = []
	front_poly_3pass = []
	back_poly_3pass = []
	if FRONT_FILE:
		#print("Front file =",FRONT_FILE
		front_gerber = read_Gerber(GERBER_DIR,FRONT_FILE)
		#front_gerber = gm.merge_lines(front_gerber)
		front_gerber = gm.check_duplication(front_gerber)
		#print(len(front_gerber)
		front_poly = gerber2polygon(front_gerber)
		#print(len(front_poly)
		front_poly = gm.merge(front_poly, LINE, gLINES,gLINES2)
		if abs(float(ROT_ANG)) > TINY:
			front_poly = rot_poly(front_poly)
		if MIRROR_FRONT:
			front_poly = mirror_poly(front_poly)
		print(len(front_poly))
		if TOOL_2PASS_D > 0:
			print("Processing 2nd pass...")
			PREV_TOOL_D = TOOL_D
			TOOL_D = TOOL_2PASS_D # Set the thicker tool
			#print("Front file =",FRONT_FILE
			front_gerber_2pass = read_Gerber(GERBER_DIR,FRONT_FILE)
			#front_gerber = gm.merge_lines(front_gerber)
			front_gerber_2pass = gm.check_duplication(front_gerber_2pass)
			#print(len(front_gerber)
			front_poly_2pass = gerber2polygon(front_gerber_2pass)
			#print(len(front_poly)
			front_poly_2pass = gm.merge(front_poly_2pass, LINE, gLINES,gLINES2)
			if abs(float(ROT_ANG)) > TINY:
				front_poly_2pass = rot_poly(front_poly_2pass)
			if MIRROR_FRONT:
				front_poly_2pass = mirror_poly(front_poly_2pass)
			print(len(front_poly_2pass))
			TOOL_D = PREV_TOOL_D
		if TOOL_3PASS_D > 0:
			print("Processing 3nd pass...")
			PREV_TOOL_D = TOOL_D
			TOOL_D = TOOL_3PASS_D # Set the thicker tool
			#print("Front file =",FRONT_FILE
			front_gerber_3pass = read_Gerber(GERBER_DIR,FRONT_FILE)
			#front_gerber = gm.merge_lines(front_gerber)
			front_gerber_3pass = gm.check_duplication(front_gerber_3pass)
			#print(len(front_gerber)
			front_poly_3pass = gerber2polygon(front_gerber_3pass)
			#print(len(front_poly)
			front_poly_3pass = gm.merge(front_poly_3pass, LINE, gLINES,gLINES2)
			if abs(float(ROT_ANG)) > TINY:
				front_poly_3pass = rot_poly(front_poly_3pass)
			if MIRROR_FRONT:
				front_poly_3pass = mirror_poly(front_poly_3pass)
			print(len(front_poly_3pass))
			TOOL_D = PREV_TOOL_D
	if BACK_FILE:
		back_gerber = read_Gerber(GERBER_DIR,BACK_FILE)
		#back_gerber = gm.merge_lines(back_gerber)
		back_gerber = gm.check_duplication(back_gerber)
		back_poly = gerber2polygon(back_gerber)
		back_poly = gm.merge(back_poly, LINE, gLINES,gLINES2)
		if abs(float(ROT_ANG)) > TINY:
			back_poly = rot_poly(back_poly)
		if MIRROR_BACK:
			back_poly = mirror_poly(back_poly)
		print(len(back_poly))
		if TOOL_2PASS_D > 0:
			print("Processing 2nd pass...")
			PREV_TOOL_D = TOOL_D
			TOOL_D = TOOL_2PASS_D # Set the thicker tool
			back_gerber_2pass = read_Gerber(GERBER_DIR,BACK_FILE)
			#back_gerber = gm.merge_lines(back_gerber)
			back_gerber_2pass = gm.check_duplication(back_gerber_2pass)
			back_poly_2pass = gerber2polygon(back_gerber_2pass)
			back_poly_2pass = gm.merge(back_poly_2pass, LINE, gLINES,gLINES2)
			if abs(float(ROT_ANG)) > TINY:
				back_poly_2pass = rot_poly(back_poly_2pass)
			if MIRROR_BACK:
				back_poly_2pass = mirror_poly(back_poly_2pass)
			print(len(back_poly_2pass))
			TOOL_D = PREV_TOOL_D
		if TOOL_3PASS_D > 0:
			print("Processing 3nd pass...")
			PREV_TOOL_D = TOOL_D
			TOOL_D = TOOL_3PASS_D # Set the thicker tool
			back_gerber_3pass = read_Gerber(GERBER_DIR,BACK_FILE)
			#back_gerber = gm.merge_lines(back_gerber)
			back_gerber_3pass = gm.check_duplication(back_gerber_3pass)
			back_poly_3pass = gerber2polygon(back_gerber_3pass)
			back_poly_3pass = gm.merge(back_poly_3pass, LINE, gLINES,gLINES2)
			if abs(float(ROT_ANG)) > TINY:
				back_poly_3pass = rot_poly(back_poly_3pass)
			if MIRROR_BACK:
				back_poly_3pass = mirror_poly(back_poly_3pass)
			print(len(back_poly_3pass))
			TOOL_D = PREV_TOOL_D
	if DRILL_FILE:
		read_Drill_file(GERBER_DIR,DRILL_FILE)
		if(len(gDRILLS) > 0):
			do_drill()
	if EDGE_FILE:
		readEdgeFile(GERBER_DIR,EDGE_FILE)
		if(len(gEDGES) > 0):
			mergeEdge()
			edge2gcode()
	#gm.merge(gPOLYGONS, LINE, gLINES,gLINES2)

	end(front_poly,back_poly,front_poly_2pass,back_poly_2pass,front_poly_3pass,back_poly_3pass)

def read_config(config_file):
	global INI_X, INI_Y, INI_Z, MOVE_HEIGHT, OUT_INCH_FLAG, IN_INCH_FLAG, MCODE_FLAG, XY_SPEED, Z_SPEED, LEFT_X, LOWER_Y, DRILL_SPEED, DRILL_DEPTH, CUT_DEPTH, TOOL_D, TOOL_2PASS_D, TOOL_3PASS_D, DRILL_D, CAD_UNIT, EDGE_TOOL_D, EDGE_DEPTH, EDGE_SPEED, EDGE_Z_SPEED, MERGE_DRILL_DATA, Z_STEP_DRILL, Z_STEP_EDGE, GERBER_COLOR, DRILL_COLOR, EDGE_COLOR , CONTOUR_COLOR, GERBER_EXT, DRILL_EXT, EDGE_EXT, GCODE_EXT, GDRILL_EXT, GEDGE_EXT, DRILL_UNIT, EDGE_UNIT, CUT_FLAG, CUT_OV
	global GERBER_DIR,FRONT_FILE,BACK_FILE,DRILL_FILE,EDGE_FILE,MIRROR_FRONT,MIRROR_BACK,MIRROR_DRILL,MIRROR_EDGE,ROT_ANG
	global OUT_DIR,OUT_FRONT_FILE,OUT_FRONT_2PASS_FILE,OUT_FRONT_3PASS_FILE,OUT_BACK_FILE,OUT_BACK_2PASS_FILE,OUT_BACK_3PASS_FILE,OUT_DRILL_FILE,OUT_EDGE_FILE
	with open(config_file,'r') as f:
		while 1:
			config = f.readline()
			#print(config
			if not config:
				break
			#cfg = re.search("([A-Z\_]+)[\d\s\ ]*\=[\ \"]*([\s\/\-\d\.\_]+)\"*",config)
			cfg = re.search("([A-Z0-9\_]+)[\d\s\ ]*\=[\ \"]*([^\ \"\n\r]+)\"*",config) # FIXED: Now variable names can have numbers
			if (cfg):
				#print(str(cfg.group(1)),"=",str(cfg.group(2))
				if(cfg.group(1)=="INI_X"):
					#print("ini x =",cfg.group(2)
					INI_X = float(cfg.group(2))
				if(cfg.group(1)=="INI_Y"):
					INI_Y = float(cfg.group(2))
				if(cfg.group(1)=="INI_Z"):
					INI_Z = float(cfg.group(2))
				if(cfg.group(1)=="MOVE_HEIGHT"):
					MOVE_HEIGHT = float(cfg.group(2))
				if(cfg.group(1)=="OUT_INCH_FLAG"):
					OUT_INCH_FLAG = int(cfg.group(2))
				if(cfg.group(1)=="IN_INCH_FLAG"):
					IN_INCH_FLAG = int(cfg.group(2))
				if(cfg.group(1)=="CUT_FLAG"):
					CUT_FLAG = int(cfg.group(2))
				if(cfg.group(1)=="CUT_OV"):
					CUT_OV = float(cfg.group(2))
				if(cfg.group(1)=="MCODE_FLAG"):
					MCODE_FLAG = int(cfg.group(2))
				if(cfg.group(1)=="XY_SPEED"):
					XY_SPEED = int(cfg.group(2))
				if(cfg.group(1)=="Z_SPEED"):
					Z_SPEED = int(cfg.group(2))
				if(cfg.group(1)=="LEFT_X"):
					LEFT_X = float(cfg.group(2))
				if(cfg.group(1)=="LOWER_Y"):
					LOWER_Y = float(cfg.group(2))
				if(cfg.group(1)=="DRILL_SPEED"):
					DRILL_SPEED = int(cfg.group(2))
				if(cfg.group(1)=="DRILL_DEPTH"):
					DRILL_DEPTH = float(cfg.group(2))
				if(cfg.group(1)=="CUT_DEPTH"):
					CUT_DEPTH = float(cfg.group(2))
				if(cfg.group(1)=="TOOL_D"):
					TOOL_D = float(cfg.group(2))
				if(cfg.group(1)=="TOOL_2PASS_D"):
					TOOL_2PASS_D = float(cfg.group(2))
				if(cfg.group(1)=="TOOL_3PASS_D"):
					TOOL_3PASS_D = float(cfg.group(2))
				if(cfg.group(1)=="DRILL_D"):
					DRILL_D = float(cfg.group(2))
				if(cfg.group(1)=="CAD_UNIT"):
					CAD_UNIT = float(cfg.group(2))
				if(cfg.group(1)=="DRILL_UNIT"):
					DRILL_UNIT = float(cfg.group(2))
				if(cfg.group(1)=="EDGE_UNIT"):
					EDGE_UNIT = float(cfg.group(2))
				if(cfg.group(1)=="EDGE_TOOL_D"):
					EDGE_TOOL_D = float(cfg.group(2))
				if(cfg.group(1)=="EDGE_DEPTH"):
					EDGE_DEPTH = float(cfg.group(2))
				if(cfg.group(1)=="EDGE_SPEED"):
					EDGE_SPEED = int(cfg.group(2))
				if(cfg.group(1)=="EDGE_Z_SPEED"):
					EDGE_Z_SPEED = int(cfg.group(2))
				if(cfg.group(1)=="MERGE_DRILL_DATA"):
					MERGE_DRILL_DATA = int(cfg.group(2))
				if(cfg.group(1)=="Z_STEP_DRILL"):
					Z_STEP_DRILL = float(cfg.group(2))
				if(cfg.group(1)=="Z_STEP_EDGE"):
					Z_STEP_EDGE = float(cfg.group(2))
				if(cfg.group(1)=="GERBER_COLOR"):
					GERBER_COLO = str(cfg.group(2))
				if(cfg.group(1)=="DRILL_COLOR"):
					DRILL_COLOR = str(cfg.group(2))
				if(cfg.group(1)=="EDGE_COLOR"):
					EDGE_COLOR = str(cfg.group(2))
				if(cfg.group(1)=="CONTOUR_COLOR"):
					CONTOUR_COLOR = str(cfg.group(2))
				if(cfg.group(1)=="GERBER_EXT"):
					GERBER_EXT = str(cfg.group(2))
				if(cfg.group(1)=="DRILL_EXT"):
					DRILL_EXT = str(cfg.group(2))
				if(cfg.group(1)=="EDGE_EXT"):
					EDGE_EXT = str(cfg.group(2))
				if(cfg.group(1)=="GCODE_EXT"):
					GCODE_EXT = str(cfg.group(2))
				if(cfg.group(1)=="GDRILL_EXT"):
					GDRILL_EXT = str(cfg.group(2))
				if(cfg.group(1)=="GEDGE_EXT"):
					GEDGE_EXT = str(cfg.group(2))

				if(cfg.group(1)=="GERBER_DIR"):
					#print("dir =",cfg.group(2)
					GERBER_DIR = str(cfg.group(2))
				if(cfg.group(1)=="FRONT_FILE"):
					#print("front =",cfg.group(2)
					FRONT_FILE = str(cfg.group(2))
				if(cfg.group(1)=="BACK_FILE"):
					BACK_FILE = str(cfg.group(2))
				if(cfg.group(1)=="DRILL_FILE"):
					DRILL_FILE = str(cfg.group(2))
				if(cfg.group(1)=="EDGE_FILE"):
					EDGE_FILE = str(cfg.group(2))
				if(cfg.group(1)=="MIRROR_FRONT"):
					MIRROR_FRONT = int(cfg.group(2))
				if(cfg.group(1)=="MIRROR_BACK"):
					MIRROR_BACK = int(cfg.group(2))
				if(cfg.group(1)=="MIRROR_DRILL"):
					MIRROR_DRILL = int(cfg.group(2))
				if(cfg.group(1)=="MIRROR_EDGE"):
					MIRROR_EDGE = int(cfg.group(2))
				if(cfg.group(1)=="ROT_ANG"):
					ROT_ANG = float(cfg.group(2))
				if(cfg.group(1)=="OUT_DIR"):
					OUT_DIR = str(cfg.group(2))
				if(cfg.group(1)=="OUT_FRONT_FILE"):
					OUT_FRONT_FILE = str(cfg.group(2))
				if(cfg.group(1)=="OUT_BACK_FILE"):
					OUT_BACK_FILE = str(cfg.group(2))
				if(cfg.group(1)=="OUT_FRONT_2PASS_FILE"):
					OUT_FRONT_2PASS_FILE = str(cfg.group(2))
				if(cfg.group(1)=="OUT_BACK_2PASS_FILE"):
					OUT_BACK_2PASS_FILE = str(cfg.group(2))
				if(cfg.group(1)=="OUT_FRONT_3PASS_FILE"):
					OUT_FRONT_3PASS_FILE = str(cfg.group(2))
				if(cfg.group(1)=="OUT_BACK_3PASS_FILE"):
					OUT_BACK_3PASS_FILE = str(cfg.group(2))
				if(cfg.group(1)=="OUT_DRILL_FILE"):
					OUT_DRILL_FILE = str(cfg.group(2))
				if(cfg.group(1)=="OUT_EDGE_FILE"):
					OUT_EDGE_FILE = str(cfg.group(2))
		f.close()
		return
	raise Exception("Unable to open the file " + config_file + "\n")

def set_unit():
	global IN_INCH_FLAG, OUT_INCH_FLAG, gUNIT, INCH
	if (IN_INCH_FLAG and not OUT_INCH_FLAG):
		gUNIT = INCH
	elif(not IN_INCH_FLAG and OUT_INCH_FLAG):
		gUNIT = 1.0/INCH
	else:
		gUNIT = 1.0


def points_revers(points):
	return_points = []
	i = len(points)-1
	while i>0:
		return_points = return_points + [points[i-1],points[i]]
		i -=2	

	return return_points

def gcode_init():
	global gFRONT_DATA, gBACK_DATA, gFRONT_2PASS_DATA, gBACK_2PASS_DATA, gFRONT_3PASS_DATA, gBACK_3PASS_DATA, gDRILL_DATA, gEDGE_DATA
	gFRONT_DATA += "(Generated by " + sys.argv[0] +" )\n"
	gFRONT_DATA += "( " + get_date() +" )\n"
	gFRONT_DATA += "(Initialize)\n"
	#gFRONT_DATA += "G92 X" + floats(INI_X) + " Y" + floats(INI_Y) + " Z" + floats(INI_Z) + "\n"
	if OUT_INCH_FLAG:
		gFRONT_DATA += "(Set to inch unit)\n"
		gFRONT_DATA += "G20\n"

	gFRONT_DATA += "\n" + "(Start form here)\n"
	if MCODE_FLAG:
		gFRONT_DATA += "(Spindl and Coolant ON)\n"
		gFRONT_DATA += "M03\n"
		gFRONT_DATA += "M08\n"
	gBACK_DATA = gFRONT_DATA
	gDRILL_DATA = gFRONT_DATA
	gEDGE_DATA = gFRONT_DATA
	gBACK_2PASS_DATA = gFRONT_DATA
	gFRONT_2PASS_DATA = gFRONT_DATA
	gBACK_3PASS_DATA = gFRONT_DATA
	gFRONT_3PASS_DATA = gFRONT_DATA

def get_date():
	#d = datetime.datetime.today()
	d = datetime.today()
	return d.strftime("%Y-%m-%d %H:%M:%S")

def read_Gerber(dirname,filename):
	#global IN_INCH_FLAG
	global gGCODES
	gGCODES = []
	print("Parse Gerber data")
	(data,f) = open_file(dirname, filename)
	for gerber in data:
		if not gerber:
			break
		# print(gerber
		if (gerber.find("%MOIN") != -1):
			IN_INCH_FLAG = 1

		if (gerber.find("%ADD") != -1):
			parse_add(gerber)
		if(gerber.find("%AM") != -1):
			#do nothing
			print("Ignoring %AM...")
		if (gerber.find("D") == 0):
			parse_d(gerber)
		if (gerber.find("G") != -1):
			parse_g(gerber)
		#if (find(gerber, "X") != -1 or find(gerber, "Y") != -1):
		if (gerber.find("X") == 0):
			parse_xy(gerber)
	f.close()
	return gGCODES

def parse_add(gerber):
	global gDCODE,D_DATA
	dn = re.search("ADD([\d]+)([a-zA-Z]+)\,([\d\.]+)[a-zA-Z]+([\d\.]+)\W*",gerber)
	dm = re.search("ADD([\d]+)([a-zA-Z]+)\,([\d\.]+)\W*",gerber)
	mod2 = 0
	if (dn):
		d_num = dn.group(1)
		aperture_type = dn.group(2)
		mod1 = dn.group(3)
		mod2 = dn.group(4)
	elif (dm):
		d_num = dm.group(1)
		aperture_type = dm.group(2)
		mod1 = dm.group(3)
	else:
		return

	gDCODE[int(d_num)] = D_DATA(aperture_type,mod1,mod2)
def parse_d(gerber):
	global g54_FLAG, gFIG_NUM
	#print(gerber
	index_d=gerber.find("D")
	index_ast=gerber.find("*")
	g54_FLAG = 1
	gFIG_NUM=gerber[index_d+1:index_ast]
def parse_g(gerber):
	global gTMP_X, gTMP_Y, gTMP_Z, g54_FLAG, gFIG_NUM
	index_d=gerber.find("D")
	index_ast=gerber.find("*")
	if (gerber.find("54",1,index_d) !=-1):
		g54_FLAG = 1
	else:
		g54_FLAG = 0

	gFIG_NUM=gerber[index_d+1:index_ast]

def parse_xy(gerber):
	global gTMP_X, gTMP_Y, gTMP_Z, g54_FLAG, gFIG_NUM
	d=0
	xx = re.search("X([\d\.\-]+)\D",gerber)
	yy = re.search("Y([\d\-]+)\D",gerber)
	dd = re.search("D([\d]+)\D",gerber)
	if (xx):
		x = xx.group(1)
		if (x != gTMP_X):
			gTMP_X = x

	if (yy):
		y = yy.group(1)
		if (y != gTMP_Y):
			gTMP_Y = y
	if (dd):
		d = dd.group(1)

	if (g54_FLAG):
		parse_data(x,y,d)

# TODO: ADD SUPPORT FOR OVAL TYPE!
def parse_data(x,y,d):
	global gDCODE, gFIG_NUM,INCH, TOOL_D, CAD_UNIT, gGERBER_TMP_X, gGERBER_TMP_Y, gGCODES, gUNIT
	mod1 = float(gDCODE[int(gFIG_NUM)].mod1) * gUNIT
	mod2 = float(gDCODE[int(gFIG_NUM)].mod2) * gUNIT
	x = float(x) * CAD_UNIT
	y = float(y) * CAD_UNIT
	if(d == "03" or d == "3"):
		#Flash
		if( gDCODE[int(gFIG_NUM)].atype == "C"):
			#Circle
			gGCODES.append(GCODE(x,y,0,0,1,mod1,0))
		elif(gDCODE[int(gFIG_NUM)].atype ==  "R"):
			#Rect
			#Change to line
			gGCODES.append(GCODE(x,y,0,0,2,mod1,mod2))
		elif(gDCODE[int(gFIG_NUM)].atype ==  "O"):
			gGCODES.append(GCODE(x,y,0,0,6,mod1,mod2))
			#print("Oval 03"
		else: print("UNSUPPORTED SHAPE TYPE: " + str(gDCODE[int(gFIG_NUM)].atype))
	elif(d == "02" or d == "2"):
		#move  w light off
		gGERBER_TMP_X = x
		gGERBER_TMP_Y = y
	elif(d == "01" or d == "1"):
		#move w Light on
		if(gDCODE[int(gFIG_NUM)].atype == "C"):
			gGCODES.append(GCODE(gGERBER_TMP_X,gGERBER_TMP_Y,x,y,3,mod1,mod2))
		elif(gDCODE[int(gFIG_NUM)].atype == "R"):
			#Rect
			gGCODES.append(GCODE(gGERBER_TMP_X,gGERBER_TMP_Y,x,y,4,mod1,mod2))
		elif(gDCODE[int(gFIG_NUM)].atype == "O"):
			gGCODES.append(GCODE(gGERBER_TMP_X,gGERBER_TMP_Y,x,y,4,mod1,mod2)) # TODO FIX: This oval will be shown as a rectangle!
			print("Oval pad will appear as a rectangle!")
		else: print("UNSUPPORTED SHAPE TYPE: " + str(gDCODE[int(gFIG_NUM)].atype))
		gGERBER_TMP_X = x
		gGERBER_TMP_Y = y


def gerber2polygon(gGCODES):
	#global gPOLYGONS,gGCODES, TOOL_D
	global gPOLYGONS
	gPOLYGONS = []	#initialize
	for gcode in gGCODES:
		if(gcode.gtype == 0):
			continue
		x1=gcode.x1
		y1=gcode.y1
		x2=gcode.x2
		y2=gcode.y2
		mod1=gcode.mod1 + float(TOOL_D)
		mod2=gcode.mod2 + float(TOOL_D)
		if(gcode.gtype == 1):
			gPOLYGONS.append(POLYGON(x1-mod1/2,x1+mod1/2,y1-mod1/2,y1+mod1/2,circle_points(x1,y1,mod1/2,20),0))
		elif(gcode.gtype == 2):
			points = [x1-mod1/2,y1-mod2/2,x1-mod1/2,y1+mod2/2,x1+mod1/2,y1+mod2/2,x1+mod1/2,y1-mod2/2,x1-mod1/2,y1-mod2/2]
			gPOLYGONS.append(POLYGON(x1-mod1/2,x1+mod1/2,y1-mod2/2,y1+mod2/2,points,0))
		elif(gcode.gtype == 3):
			line2poly(x1,y1,x2,y2,mod1/2,1,8)
		elif(gcode.gtype == 4):
			line2poly(x1,y1,x2,y2,mod2/2,0,8)
		elif(gcode.gtype == 5):
			line2poly(x1,y1,x2,y2,mod1/2,2,8)
		elif(gcode.gtype == 6): # Oval (no rotation)
			width = abs(mod1) # abs((x1+mod1/2)-(x1-mod1/2)) # abs(x_max-x_min)
			height = abs(mod2) # abs((y1+mod2/2)-(y1-mod2/2)) # abs(y_max-y_min)
			deg90=pi/2.0
			npoints = 16
			x1 = x1 - width/2
			y1 = y1 - height/2
			if width > height: # (___)
				radius = height/2
				# arc_points(cx,cy,r,s_angle,e_angle,kaku)
				points = [x1+width-radius,y1]
				points = points + arc_points(x1+width-radius,y1+radius,radius,-deg90,deg90,npoints)
				points = points + arc_points(x1+radius,y1+radius,radius,deg90,3*deg90,npoints)
				points = points + [x1+width-radius,y1]
			else: # 0
				radius = width/2
				# arc_points(cx,cy,r,s_angle,e_angle,kaku)
				points = [x1+width,y1+height-radius]
				points = points + arc_points(x1+radius,y1+height-radius,radius,0,2*deg90,npoints)
				points = points + arc_points(x1+radius,y1+radius,radius,2*deg90,4*deg90,npoints)
				points = points + [x1+width,y1+height-radius]
			#points = [x1-mod1/2,y1-mod2/2,x1-mod1/2,y1+mod2/2,x1+mod1/2,y1+mod2/2,x1+mod1/2,y1-mod2/2,x1-mod1/2,y1-mod2/2]
			#gPOLYGONS.append(POLYGON(x1-mod1/2,x1+mod1/2,y1-mod2/2,y1+mod2/2,points,0))
			polygon(points)
			# POLYGON arguments: (x_min, x_max, y_min, y_max, points, delete)
	return gPOLYGONS

def line2poly(x1,y1,x2,y2,r,atype,ang_n):
	points = []
	deg90=pi/2.0
	dx = x2-x1
	dy = y2-y1
	ang=atan2(dy,dx)
	xa1=x1+r*cos(ang+deg90)
	ya1=y1+r*sin(ang+deg90)
	xa2=x1-r*cos(ang+deg90)
	ya2=y1-r*sin(ang+deg90)
	xb1=x2+r*cos(ang+deg90)
	yb1=y2+r*sin(ang+deg90)
	xb2=x2-r*cos(ang+deg90)
	yb2=y2-r*sin(ang+deg90)
	if(atype==1):
		points = points + arc_points(x1,y1,r,ang+3*deg90,ang+deg90,ang_n)
		points = points + arc_points(x2,y2,r,ang+deg90,ang-deg90,ang_n)
		points = points + [xa2,ya2]
	elif(atype==2):
		points = points + [xa2,ya2,xa1,ya1]
		points = points + arc_points(x2,y2,r,ang+deg90,ang-deg90,ang_n)
		points = points + [xa2,ya2]
	elif(atype==3): # Oval #TODO FIX
		points = (xa1,ya1,xb1,yb1,xb2,yb2,xa2,ya2,xa1,ya1)
#		width = abs(xa1-xb2)
#		height = abs(ya1-yb2)
#		if width > height:
#			points = points + arc_points(x1+r,y1,r,ang+3*deg90,ang+deg90,ang_n)
#			points = points + arc_points(x2-r,y2,r,ang+1*deg90,ang-deg90,ang_n)
#			points = points + [xa2+r,ya2]
#		else:
#			r = width/2
#			points = points + arc_points(x1+r,y1+r,r,ang+2*deg90,ang+deg90-deg90,ang_n)
#			points = points + arc_points(x2-r,y2-r,r,ang+0*deg90,ang-deg90-deg90,ang_n)
#			ya1=y1+r*sin(ang+deg90)
#			points = points + [xa1,ya1]
	else:
		points = (xa1,ya1,xb1,yb1,xb2,yb2,xa2,ya2,xa1,ya1)
	polygon(points)

def polygon(points):
	global HUGE, gPOLYGONS, gXMIN, gYMIN, gXMAX, gYMAX
	x_max=-HUGE
	x_min=HUGE
	y_max=-HUGE
	y_min=HUGE
	if(len(points)<=2):
		print("Error: polygon point")
		return
	i = 0
	while i< len(points):
		if(points[i] > x_max):
			x_max=points[i]
		if(points[i] < x_min):
			x_min=points[i]
		if(points[i+1] > y_max):
			y_max=points[i+1]
		if(points[i+1] < y_min):
			y_min=points[i+1]
		i += 2

	gPOLYGONS.append(POLYGON(x_min,x_max,y_min,y_max,points,0))

	if(gXMIN>x_min):
		gXMIN = x_min
	if(gYMIN>y_min):
		gYMIN=y_min
	if(gXMAX<x_max):
		gXMAX = x_max
	if(gYMAX<y_max):
		gYMAX=y_max

def circle_points(cx,cy,r,points_num):
	int(points_num)
	
	new_points_num = int( (2.0*pi*float(r))/float(MM_PER_ARC_SEGMENT) ) # Automatic resolution (reduces gcode file size)
	if new_points_num < 4 :
		new_points_num = 4
	elif  new_points_num > 50 :
		new_points_num = 50
	
	#print("Modifying CIRCLE points_num from",points_num,"to",new_points_num
	points_num = new_points_num
#	print("Circle: Radius:", str(r), "Points:", points_num
	points=[]
#	if(points_num <= 2):
#		print("Too small angle at Circle"
#		return
	i = points_num
	while i > 0:
		cir_x=cx+r*cos(2.0*pi*float(i)/float(points_num))
		cir_y=cy+r*sin(2.0*pi*float(i)/float(points_num))
		points.extend([cir_x,cir_y])
		i -= 1
	cir_x=cx+r*cos(0.0)
	cir_y=cy+r*sin(0.0)
	points.extend([cir_x,cir_y])
	return points

def gcode_end():
	#global gFRONT_DATA, gBACK_DATA, gDRILL_DATA, gEDGE_DATA, MCODE_FLAG
	end_data = ""
	end_data += "\n(Goto to Initial position)\n"
	#Goto initial Z position
	end_data += "G0 Z" + floats(MOVE_HEIGHT) + "\n"
	if MCODE_FLAG:
		#STOP Coolant
		end_data += "M09\n"
		#STOP spindl
		end_data += "M05\n"	
	#Goto initial X-Y position
	end_data += "G0 X" + floats(INI_X) + " Y" + floats(INI_Y) + "\n"
	#Goto initial Z position
	end_data += "G0 Z" + floats(INI_Z) + "\n"
	#Program END
	#end_data += "M30\n"
	#end_data += "%\n"
	return end_data

def end(front_poly,back_poly,front_poly_2pass,back_poly_2pass,front_poly_3pass,back_poly_3pass):
	global gFRONT_DATA, gBACK_DATA, gFRONT_2PASS_DATA, gBACK_2PASS_DATA, gFRONT_3PASS_DATA, gBACK_3PASS_DATA, gDRILL_DATA, gEDGE_DATA
	if OUT_FRONT_FILE and front_poly:
		gFRONT_DATA += polygon2gcode(front_poly,CUT_DEPTH,XY_SPEED, Z_SPEED)
		gFRONT_DATA += gcode_end()
		write_file(OUT_DIR,OUT_FRONT_FILE,gFRONT_DATA)
	if OUT_FRONT_2PASS_FILE and front_poly_2pass:
		gFRONT_2PASS_DATA += polygon2gcode(front_poly_2pass,CUT_DEPTH,XY_SPEED, Z_SPEED)
		gFRONT_2PASS_DATA += gcode_end()
		write_file(OUT_DIR,OUT_FRONT_2PASS_FILE,gFRONT_2PASS_DATA)
	if OUT_FRONT_3PASS_FILE and front_poly_3pass:
		gFRONT_3PASS_DATA += polygon2gcode(front_poly_3pass,CUT_DEPTH,XY_SPEED, Z_SPEED)
		gFRONT_3PASS_DATA += gcode_end()
		write_file(OUT_DIR,OUT_FRONT_3PASS_FILE,gFRONT_3PASS_DATA)
	if OUT_BACK_FILE and back_poly:
		gBACK_DATA += polygon2gcode(back_poly,CUT_DEPTH,XY_SPEED, Z_SPEED)
		gBACK_DATA += gcode_end()
		write_file(OUT_DIR,OUT_BACK_FILE,gBACK_DATA)
	if OUT_BACK_2PASS_FILE and back_poly_2pass:
		gBACK_2PASS_DATA += polygon2gcode(back_poly_2pass,CUT_DEPTH,XY_SPEED, Z_SPEED)
		gBACK_2PASS_DATA += gcode_end()
		write_file(OUT_DIR,OUT_BACK_2PASS_FILE,gBACK_2PASS_DATA)
	if OUT_BACK_3PASS_FILE and back_poly_3pass:
		gBACK_3PASS_DATA += polygon2gcode(back_poly_3pass,CUT_DEPTH,XY_SPEED, Z_SPEED)
		gBACK_3PASS_DATA += gcode_end()
		write_file(OUT_DIR,OUT_BACK_3PASS_FILE,gBACK_3PASS_DATA)
	if OUT_DRILL_FILE:
		gDRILL_DATA += gcode_end()
		write_file(OUT_DIR,OUT_DRILL_FILE,gDRILL_DATA)
	if OUT_EDGE_FILE:
		gEDGE_DATA += gcode_end()
		write_file(OUT_DIR,OUT_EDGE_FILE,gEDGE_DATA)

def polygon2gcode(gPOLYGONS,height,xy_speed,z_speed):
	#global gPOLYGONS
	print("Convert to G-code")
	#print(len(gPOLYGONS)
	#i=0
	ret_data = ""
	for poly in gPOLYGONS:
		if (poly.delete):
			continue
		ret_data += path(height,xy_speed,z_speed,poly.points)
		#print(i
		#i+=1
	return ret_data
def path(height,xy_speed,z_speed,points):
	global gFRONT_DATA, gXSHIFT, gYSHIFT, gTMP_X, gTMP_Y, gTMP_Z
	ret_data = ""
	out_data = "G1"
	gcode_tmp_flag = 0
	if(len(points) % 2):
		print("Number of points is illegal ")
	#move to Start position
	ret_data += move(points[0]+float(gXSHIFT),points[1]+float(gYSHIFT))
	#move to cuting heght
	if(height != gTMP_Z):
		gTMP_Z=height
		ret_data += "G1 Z" + floats(height) + " F" + floats(z_speed) + "\n"
	i = 0
	while i< len(points):
		px=points[i]+gXSHIFT
		py=points[i+1]+gYSHIFT
		if (px != gTMP_X):
			gTMP_X=px
			out_data +=" X" + floats(px)
			gcode_tmp_flag = 1
		if(py != gTMP_Y):
			gTMP_Y=py
			out_data +=" Y" + floats(py)
			gcode_tmp_flag=1
		if(gcode_tmp_flag):
			#Goto initial X-Y position
			out_data +=" F" + floats(xy_speed)
			ret_data += out_data + "\n"
			out_data ="G1"
		gcode_tmp_flag=0
		i += 2
	#print(gFRONT_DATA
	return ret_data
def move(x,y):
	global gFRONT_DATA, MOVE_HEIGHT, gTMP_X, gTMP_Y, gTMP_Z
	ret_data = ""
	out_data = "G0"
	gcode_tmp_flag = 0
	if(x != gTMP_X):
		gTMP_X = x
		out_data += " X" + floats(x)
		gcode_tmp_flag=1
	if(y != gTMP_Y):
		gTMP_Y = y
		out_data +=" Y" + floats(y)
		gcode_tmp_flag = 1
	if(MOVE_HEIGHT!=gTMP_Z):
		gTMP_Z = MOVE_HEIGHT
		#Goto moving Z position
		ret_data += "G0 Z" + floats(MOVE_HEIGHT) + "\n"
	if(gcode_tmp_flag):
		#Goto X-Y position
		ret_data += out_data + "\n"
	return ret_data

def arc_points(cx,cy,r,s_angle,e_angle,kaku):
	int(kaku)
	float(r)
	float(cx)
	float(cy)
	arc_angle = float(abs(s_angle-e_angle))
	
	new_kaku = int( (arc_angle*float(r))/float(MM_PER_ARC_SEGMENT) ) # Automatic resolution (reduces gcode file size)
	if new_kaku < 8 :
		new_kaku = 8
	elif new_kaku > 50 :
		new_kaku = 50
	if kaku != new_kaku:
		#print("Modifying ARC points from",kaku,"to",new_kaku
		kaku = new_kaku
#	print("Arc: Radius:", str(r), "Points:", kaku
	
	points=[]
	if(s_angle == e_angle):
		print("Start and End angle are same")
	if(kaku <= 2):
		print("Too small angle")
		arc_x=float(cx+r*cos(float(s_angle))) # Draw a line
		arc_y=float(cy+r*sin(float(s_angle)))
		points.extend([arc_x,arc_y])
		arc_x=float(cx+r*cos(float(e_angle)))
		arc_y=float(cy+r*sin(float(e_angle)))
		points.extend([arc_x,arc_y])
		return points
	ang_step=float((float(e_angle)-float(s_angle))/float(kaku-1))
	i = 0
	while i < kaku:
		arc_x=float(cx+r*cos(float(s_angle)+ang_step*float(i)))
		arc_y=float(cy+r*sin(float(s_angle)+ang_step*float(i)))
		points.extend([arc_x,arc_y])
		i += 1

	return points

def calc_shift():
	global gXSHIFT, gYSHIFT, gXMIN, gYMIN, LEFT_X, LOWER_Y
	gXSHIFT = LEFT_X - gXMIN
	gYSHIFT = LOWER_Y - gYMIN
	#print("x_shift=" + str(gXSHIFT) + "y_shift=" + str(gYSHIFT)

def polygon2line(points,sw):
	global gLINES,gLINES2
	i = 0
	while i< len(points)-2:
		if(sw):
			gLINES2.append(LINE(points[i],points[i+1],points[i+2],points[i+3],0,0))
		else:
			gLINES.append(LINE(points[i],points[i+1],points[i+2],points[i+3],0,0))
		i += 2

def rot_poly(polygons):
	#gXMIN, gYMIN, gXMAX, gYMAX,gROT_ANG,
	xc = (gXMIN+gXMAX)/2
	yc = (gYMIN+gYMAX)/2
	rot_ang = pi * float(ROT_ANG)/180
	for polygon in polygons:
		if(polygon.delete):
			continue
		i = 0
		while i < len(polygon.points)-1:
			x = polygon.points[i]
			y = polygon.points[i + 1]
			dx = x-xc
			dy = y-yc
			r = sqrt(dx*dx + dy*dy)
			ini_ang = atan2(dy,dx)
			new_ang = ini_ang + rot_ang
			polygon.points[i] = xc + r * cos(new_ang)
			polygon.points[i + 1] = yc + r * sin(new_ang)
			i += 2
	return polygons
def mirror_poly(polygons):
	#gXMIN, gYMIN, gXMAX, gYMAX,gROT_ANG,
	xc = (gXMIN+gXMAX)/2
	yc = (gYMIN+gYMAX)/2
	for polygon in polygons:
		if(polygon.delete):
			continue
		i = 0
		while i < len(polygon.points)-1:
			x = polygon.points[i]
			y = polygon.points[i + 1]
			dx = x-xc
			#dy = y-cy
			polygon.points[i] = xc - dx
			#new_ y = y
			i += 2
	return polygons
def rot_point(x,y):
	#print("rot ang =",ang
	add_ang = pi * float(ROT_ANG)/180
	xc = (gXMIN+gXMAX)/2
	yc = (gYMIN+gYMAX)/2
	dx = x-xc
	dy = y-yc
	r = sqrt(dx*dx + dy*dy)
	ini_ang = atan2(dy,dx)
	rot_ang = ini_ang + add_ang
	new_x =xc + r * cos(rot_ang)
	new_y =yc + r * sin(rot_ang)
	#print(new_x
	return new_x,new_y

def mirror_point(x,y):
	xc = (gXMIN+gXMAX)/2
	yc = (gYMIN+gYMAX)/2
	dx = x-xc
	return xc - dx, y
#Drill 
def read_Drill_file(dirname,drill_file):
	global gDRILL_D, gDRILL_TYPE, DRILL_UNIT,gUNIT,INCH
	(data,f) = open_file(dirname, drill_file)
	print("Read and Parse Drill data")
	drill_d_unit = DRILL_UNIT
	for drill in data:
		if not drill:
			continue
		drill_data = re.search("T([\d]+)C([\d\.]+)",drill)
		drill_num = re.search("T([\d]+)[^C\d]*",drill)
		if(drill_data):
			gDRILL_TYPE[int(drill_data.group(1))] = drill_data.group(2)
		if(drill_num):
			#print(drill_d_unit
			gDRILL_D=float(gDRILL_TYPE[int(drill_num.group(1))]) * drill_d_unit
			#gDRILL_D=float(gDRILL_TYPE[int(drill_num.group(1))]) * gUNIT
		if (drill.find("G") != -1):
			parse_drill_g(drill)
		elif (drill.find("X") != -1 or drill.find("Y") != -1):
			parse_drill_xy(drill)
		if (drill.find("INCH") != -1):
			drill_d_unit = INCH
			#print("Drill Diameter = INCH"
		if (drill.find("M72") != -1):
			#print("Drill unit = INCH"
			DRILL_UNIT = INCH
	f.close()

def parse_drill_g(drill):
	global gDRILL_LINES, gDRILL_D, DRILL_UNIT
	#print("Drill G";
	#xx = re.search("X([\d\.-]+)\D",drill)
	#yy = re.search("Y([\d\.-]+)\D",drill)
	xy = re.search("X([\d\.-]+)Y([\d\.-]+)\D[\d]+X([\d\.-]+)Y([\d\.-]+)",drill)
	#if(xx):
	#	x=float(xx.group(1)) * DRILL_UNIT
	#if(yy):
	#	y=float(yy.group(1)) * DRILL_UNIT
	if(xy):
		x1=float(xy.group(1)) * DRILL_UNIT
		y1=float(xy.group(2)) * DRILL_UNIT
		x2=float(xy.group(3)) * DRILL_UNIT
		y2=float(xy.group(4)) * DRILL_UNIT
		#print("x1=" + str(x1) + "y1=" + str(y1) + "x2=" + str(x2) + "y2=" + str(y2)
		#print("gDRILL_D =",gDRILL_D
		gDRILL_LINES.append(DRILL_LINE(x1,y1,x2,y2,gDRILL_D,0))

def parse_drill_xy(drill):
	global gDRILLS,gDRILL_D, DRILL_UNIT
	xx = re.search("X([\d\.-]+)[^\d\.\-]*",drill)
	yy = re.search("Y([\d\.-]+)[^\d\.\-]*",drill)
	if(xx):
		x=float(xx.group(1)) * DRILL_UNIT
	if(yy):
		y=float(yy.group(1)) * DRILL_UNIT
	#print("gDRILL_D =",gDRILL_D
	gDRILLS.append(DRILL(x,y,gDRILL_D,0))

def do_drill():
	global DRILL_SPEED, DRILL_DEPTH, gDRILLS, gDRILL_LINES, MOVE_HEIGHT, gDRILL_DATA, gFRONT_DATA, gTMP_DRILL_X, gTMP_DRILL_Y, gTMP_DRILL_Z, gTMP_X, gTMP_Y, gTMP_Z,MERGE_DRILL_DATA, gDRILL_D, DRILL_D, gXSHIFT, gYSHIFT
	drill_data = ""
	drill_mergin = 0.02
	calc_shift()
	if(MERGE_DRILL_DATA):
		gTMP_DRILL_X = gTMP_X
		gTMP_DRILL_Y = gTMP_Y
		gTMP_DRILL_Z = gTMP_Z
	for drill in gDRILLS:
		x = drill.x
		y = drill.y
		if abs(float(ROT_ANG)) > TINY:
			x,y = rot_point(x,y)
		if MIRROR_DRILL:
			x,y = mirror_point(x,y)
		x = x + gXSHIFT
		y = y + gYSHIFT
		#print("drill.d=" + str(drill.d) + ", DRILL_D=" + str(DRILL_D)
		#move to hole position
		#print("drill_d =", drill.d, " , DRILL_D =",DRILL_D
		if(drill.d > DRILL_D + drill_mergin):
			cir_r = drill.d/2 - DRILL_D/2
			#print(cir_r
			#drill_data += move_drill(drill.x-cir_r,drill.y)
			drill_data += drill_hole(x,y,cir_r)
		else:
			drill_data += move_drill(x,y)
			#Drill
			if(DRILL_SPEED):
				drill_data += "G1 Z" + floats(DRILL_DEPTH) + " F" + floats(DRILL_SPEED) + "\n"
			else:
				drill_data += "G1 Z" + floats(DRILL_DEPTH) + "\n"
		#Goto moving Z position
		drill_data += "G0 Z" + floats(MOVE_HEIGHT) + "\n"
		gTMP_DRILL_Z = MOVE_HEIGHT
	#print("len gDRILL_LINES=" +str(len(gDRILL_LINES))
	for drill_l in gDRILL_LINES:
		x1 = drill_l.x1
		y1 = drill_l.y1
		x2 = drill_l.x2
		y2 = drill_l.y2	
		if abs(float(ROT_ANG)) > TINY:
			x1,y1 = rot_point(x1,y1)
			x2,y2 = rot_point(x2,y2)
		if MIRROR_DRILL:
			x1,y1 = mirror_point(x1,y1)
			x2,y2 = mirror_point(x2,y2)
		x1 = x1 + gXSHIFT
		y1 = y1 + gYSHIFT
		x2 = x2 + gXSHIFT
		y2 = y2 + gYSHIFT

		drill_data += drill_line(x1,y1,x2,y2,drill_l.d)
		#Goto moving Z position
		drill_data += "G0 Z" + floats(MOVE_HEIGHT) + "\n"
		gTMP_DRILL_Z = MOVE_HEIGHT
	gDRILL_DATA += drill_data
	if(MERGE_DRILL_DATA):
		gFRONT_DATA += drill_data
		gTMP_X = gTMP_DRILL_X 
		gTMP_Y = gTMP_DRILL_Y
		gTMP_Z = gTMP_DRILL_Z
def move_drill(x,y):
	global MOVE_HEIGHT, gTMP_DRILL_X, gTMP_DRILL_Y, gTMP_DRILL_Z
	xy_data = "G0"
	out_data = ""
	#print(out_data
	gcode_tmp_flag = 0
	if(x != gTMP_DRILL_X):
		gTMP_DRILL_X = x
		xy_data += " X" + floats(x)
		gcode_tmp_flag=1
	if(y != float(gTMP_DRILL_Y)):
		gTMP_DRILL_Y = y
		xy_data += " Y" + floats(y)
		gcode_tmp_flag = 1
	if(MOVE_HEIGHT!=gTMP_DRILL_Z):
		gTMP_DRILL_Z = MOVE_HEIGHT
		#Goto moving Z position
		out_data = "G0 Z" + floats(MOVE_HEIGHT) + "\n"
	if(gcode_tmp_flag):
		#Goto initial X-Y position
		return out_data + xy_data + "\n"
	else:
		return ""
def draw_drill_line(x1,y1,x2,y2,d):
	global DRILL_D
	drill_mergin = 0.02
	ang_n = 100
	points = []
	deg90 = pi/2.0
	if(d > DRILL_D + drill_mergin):
		r = d/2 - DRILL_D/2
		dx = x2-x1
		dy = y2-y1
		ang=atan2(dy,dx)
		xa1=x1+r*cos(ang+deg90)
		ya1=y1+r*sin(ang+deg90)
		xa2=x1-r*cos(ang+deg90)
		ya2=y1-r*sin(ang+deg90)
		xb1=x2+r*cos(ang+deg90)
		yb1=y2+r*sin(ang+deg90)
		xb2=x2-r*cos(ang+deg90)
		yb2=y2-r*sin(ang+deg90)
		points = points + arc_points(x1,y1,r,ang+3*deg90,ang+deg90,ang_n)
		points = points + arc_points(x2,y2,r,ang+deg90,ang-deg90,ang_n)
		points = points + [xa2,ya2]
	else:
		points = [x1,y1,x2,y2]
	return points

def drill_line(x1,y1,x2,y2,d):
	global MOVE_HEIGHT, gTMP_DRILL_X, gTMP_DRILL_Y, gTMP_DRILL_Z, DRILL_SPEED, DRILL_DEPTH, Z_STEP_DRILL, XY_SPEED, DRILL_D ,gDRAWDRILL_LINE
	out_data = ""
	gcode_tmp_flag = 0
	z_step_n = int(float(DRILL_DEPTH)/float(Z_STEP_DRILL)) + 1
	z_step = float(DRILL_DEPTH)/z_step_n
	if(MOVE_HEIGHT != gTMP_DRILL_Z):
		gTMP_DRILL_Z = MOVE_HEIGHT
		out_data += "G0 Z" + floats(gTMP_DRILL_Z) + "\n"
	points = []
	ang_n = 100
	drill_mergin = 0.02
	deg90=pi/2.0
	if(d > DRILL_D + drill_mergin):
		r = d/2 - DRILL_D/2
		dx = x2-x1
		dy = y2-y1
		ang=atan2(dy,dx)
		xa1=x1+r*cos(ang+deg90)
		ya1=y1+r*sin(ang+deg90)
		xa2=x1-r*cos(ang+deg90)
		ya2=y1-r*sin(ang+deg90)
		xb1=x2+r*cos(ang+deg90)
		yb1=y2+r*sin(ang+deg90)
		xb2=x2-r*cos(ang+deg90)
		yb2=y2-r*sin(ang+deg90)
		points = points + arc_points(x1,y1,r,ang+3*deg90,ang+deg90,ang_n)
		points = points + arc_points(x2,y2,r,ang+deg90,ang-deg90,ang_n)
		points = points + [xa2,ya2]
		tmp_x = xa2
		tmp_y = ya2
	else:
		points = [x1,y1,x2,y2]
		tmp_x = x2
		tmp_y = y2
	#gDRAWDRILL_LINE.append(DRAWPOLY(points,"",0))
	out_data += "G0 X" + floats(tmp_x) + " Y" + floats(tmp_y) + "\n"
	#print(z_step_n
	#print(len(points)
	i = 1
	while i <= z_step_n:
		gTMP_DRILL_Z = i*z_step
		out_data += "G0 Z" + floats(gTMP_DRILL_Z) + " F" + floats(DRILL_SPEED) + "\n"
		j = 0
		cricle_data = "G1"
		while j< len(points):
			px=points[j]
			py=points[j+1]
			if (px != gTMP_DRILL_X):
				gTMP_DRILL_X=px
				cricle_data +=" X" + floats(px)
				gcode_tmp_flag = 1
			if(py != gTMP_DRILL_Y):
				gTMP_DRILL_Y=py
				cricle_data +=" Y" + floats(py)
				gcode_tmp_flag=1
			if(gcode_tmp_flag):
				#Goto initial X-Y position
				cricle_data +=" F" + floats(XY_SPEED)
				out_data += cricle_data + "\n"
				cricle_data ="G1"
			gcode_tmp_flag=0
			j += 2
		i += 1

	gTMP_DRILL_X = tmp_x
	gTMP_DRILL_Y = tmp_y
	return out_data

def drill_hole(cx,cy,r):
	global MOVE_HEIGHT, gTMP_DRILL_X, gTMP_DRILL_Y, gTMP_DRILL_Z, DRILL_SPEED, DRILL_DEPTH, Z_STEP_DRILL, XY_SPEED
	out_data = ""
	gcode_tmp_flag = 0
#	r = r/2.0 # REDUCE DRILL SIZE
	z_step_n = int(float(DRILL_DEPTH)/float(Z_STEP_DRILL)) + 1
	z_step = float(DRILL_DEPTH)/z_step_n
	#print("r=" + str(r)
	if(MOVE_HEIGHT != gTMP_DRILL_Z):
		gTMP_DRILL_Z = MOVE_HEIGHT
		out_data += "G0 Z" + floats(gTMP_DRILL_Z) + " F" + floats(DRILL_SPEED) + "\n" # MOD
#	out_data += "G0 X" + floats(cx+r) + " Y" + floats(cy) + "\n"\
	out_data += "G0 X" + floats(cx) + " Y" + floats(cy) + "\n" # CENTER OF THE DRILL
#	out_data += "G17\n"	#Set XY plane
	points = circle_points(cx,cy,r,100)
	i = 1
	while i <= z_step_n:
		gTMP_DRILL_Z = i*z_step
#		out_data += "G0 Z" + floats(gTMP_DRILL_Z) + " F" + floats(DRILL_SPEED) + "\n"
		j = 0
		cricle_data = "G1"
		while j< len(points):
			px=points[j]
			py=points[j+1]
			if (px != gTMP_DRILL_X):
				gTMP_DRILL_X=px
				cricle_data +=" X" + floats(px)
				gcode_tmp_flag = 1
			if(py != gTMP_DRILL_Y):
				gTMP_DRILL_Y=py
				cricle_data +=" Y" + floats(py)
				gcode_tmp_flag=1
			if(gcode_tmp_flag):
				#Goto initial X-Y position
				cricle_data +=" F" + floats(XY_SPEED)
#				out_data += cricle_data + "\n" # DON'T MOVE XY WHILE DRILLING
				cricle_data ="G1"
			gcode_tmp_flag=0
			j += 2
		i += 1
	DRILL_DESIRED_DIAM = 2*(r + DRILL_D/2)
	out_data += "G0 Z" + floats(DRILL_DEPTH) + " F" + floats(DRILL_SPEED) + " D" + floats(DRILL_DESIRED_DIAM) + "\n" # MOD
	gTMP_DRILL_X = cx+r
	gTMP_DRILL_Y = cy
	return out_data

def drill_hole_test(cx,cy,r):
	global MOVE_HEIGHT, gTMP_DRILL_X, gTMP_DRILL_Y, gTMP_DRILL_Z, DRILL_SPEED, DRILL_DEPTH, Z_STEP_DRILL, XY_SPEED
	out_data = ""
	gcode_tmp_flag = 0
	z_step_n = int(DRILL_DEPTH/Z_STEP_DRILL) + 1
	z_step = DRILL_DEPTH/z_step_n
	#print("r=" + str(r)
	if(MOVE_HEIGHT != gTMP_DRILL_Z):
		gTMP_DRILL_Z = MOVE_HEIGHT
		out_data += "G0 Z" + floats(gTMP_DRILL_Z) + "\n"
	out_data += "G0 X" + floats(cx-r) + " Y" + floats(cy) + "\n"
	out_data += "G17\n"	#Set XY plane
	i = 1
	while i <= z_step_n:
		gTMP_DRILL_Z = i*z_step
		out_data += "G0 Z" + floats(gTMP_DRILL_Z) + " F" + floats(DRILL_SPEED) + "\n"
		#Circle
		out_data += "G02 X" + floats(cx+r) + " Y" + floats(cy) + " R" + floats(r) + " F" + floats(XY_SPEED) + "\n"
		out_data += "G02 X" + floats(cx-r) + " Y" + floats(cy) + " R" + floats(r) + " F" + floats(XY_SPEED) + "\n"
		#out_data += "G03X" + str(cx+r) + "Y" + str(cy) + "I" + str(cx) + "J" + str(cy) + "F" + str(XY_SPEED) + "\n"
		#out_data += "G03X" + str(cx-r) + "Y" + str(cy) + "I" + str(cx) + "J" + str(cy) + "F" + str(XY_SPEED) + "\n"
		i += 1

	gTMP_DRILL_X = cx+r
	gTMP_DRILL_Y = cy
	return out_data
#For edge
def readEdgeFile(dirname,edge_file):
	global gTMP_EDGE_X, gTMP_EDGE_Y, gTMP_EDGE_Z, gEDGE_DATA, gEDGES
	(data,f) = open_file(dirname, edge_file)

	pre_x = gTMP_EDGE_X
	pre_y = gTMP_EDGE_Y
	for edge in data:
		if not edge:
			continue
		xx = re.search("X([\d\.\-]+)\D",edge)
		yy = re.search("Y([\d\-]+)\D",edge)
		dd = re.search("D([\d]+)\D",edge)
		if (xx):
			x = float(xx.group(1)) * EDGE_UNIT
			#if (x != gTMP_EDGE_X):
				#gTMP_EDGE_X = x
		if (yy):
			y = float(yy.group(1)) * EDGE_UNIT
			#if (y != gTMP_Y):
				#gTMP_EDGE_Y = y
		if (dd):
			if(dd.group(1) == "1" or dd.group(1) == "01"):
				gEDGES.append(POLYGON(0, 0, 0, 0, [pre_x,pre_y,x,y], 0))
				#gEDGES.append(LINE(pre_x,pre_y,x,y,0,0))
			elif(dd.group(1) == "2" or dd.group(1) == "02"):
				pre_x = x
				pre_y = y
	f.close()

def mergeEdge():
	global gTMP_EDGE_X, gTMP_EDGE_Y, gTMP_EDGE_Z, gEDGE_DATA, gEDGES, MERGINE
	for edge1 in gEDGES:
		if(edge1.delete):
			continue
		tmp_points1 = edge1.points
		for edge2 in gEDGES:
			if(edge2.delete or edge2 == edge1):
				continue
			tmp_points2 = edge2.points	
			dist1 = gm.calc_dist(edge1.points[0],edge1.points[1],edge2.points[0], edge2.points[1])
			dist2 = gm.calc_dist(edge1.points[0],edge1.points[1],edge2.points[len(edge2.points)-2], edge2.points[-1])
			dist3 = gm.calc_dist(edge1.points[len(edge1.points)-2],edge1.points[-1],edge2.points[0], edge2.points[1])
			dist4 = gm.calc_dist(edge1.points[len(edge1.points)-2],edge1.points[-1],edge2.points[len(edge2.points)-2], edge2.points[-1])
			if(dist2 < MERGINE):
				#join
				del tmp_points1[0:2]
				tmp_points1 = tmp_points2 + tmp_points1
				edge2.delete = 1
			elif(dist3 < MERGINE):
				#join
				del tmp_points2[0:2]
				tmp_points1 = tmp_points1 + tmp_points2
				edge2.delete = 1
			elif(dist1 < MERGINE):
				#join
				tmp_points2 = points_revers(tmp_points2)
				del tmp_points1[0:2]
				tmp_points1 = tmp_points2 + tmp_points1
				edge2.delete = 1
			elif(dist4 < MERGINE):
				#join
				tmp_points2 = points_revers(tmp_points2)
				del tmp_points2[0:2]
				tmp_points1 = tmp_points1 + tmp_points2
				edge2.delete = 1
			edge1.points=tmp_points1
def edge2gcode():
	global gEDGE_DATA, gXSHIFT, gYSHIFT, gTMP_EDGE_X, gTMP_EDGE_Y, gTMP_EDGE_Z, gEDGES, EDGE_TOOL_D, EDGE_DEPTH, EDGE_SPEED, EDGE_Z_SPEED, Z_STEP_EDGE
	out_data = "G1"
	gcode_tmp_flag = 0
	z_step_n = int(EDGE_DEPTH/Z_STEP_EDGE) + 1
	z_step = EDGE_DEPTH/z_step_n
	j = 1
	while j <= z_step_n:
		z_depth = j*z_step
		for edge in gEDGES:
			if(edge.delete):
				continue
			points = edge.points
			if(len(points) % 2):
				error_dialog("Error:Number of points is illegal ",0)
				#print("Number of points is illegal "
			#print("x=" + str(gTMP_EDGE_X) + ", y=" + str(gTMP_EDGE_Y)
			#print("x=" + str(float(points[0])+float(gXSHIFT)) + ", y=" + str(float(points[1])+float(gYSHIFT))
			#move to Start position
			gEDGE_DATA += move_edge(float(points[0]),float(points[1]))
			#move to cuting heght
			if(z_depth != gTMP_EDGE_Z):
				gTMP_EDGE_Z=z_depth
				gEDGE_DATA += "G1 Z" + floats(z_depth) + " F" + floats(EDGE_Z_SPEED) + "\n"
			i = 0
			while i< len(points):
				px=float(points[i])
				py=float(points[i+1])
				if abs(float(ROT_ANG)) > TINY:
					px,py = rot_point(px,py)
				if MIRROR_DRILL:
					px,py = mirror_point(px,py)
				px=px+float(gXSHIFT)
				py=py+float(gYSHIFT)
				if (px != gTMP_EDGE_X):
					gTMP_EDGE_X=px
					out_data +=" X" + floats(px)
					gcode_tmp_flag = 1
				if(py != gTMP_EDGE_Y):
					gTMP_EDGE_Y=py
					out_data +=" Y" + floats(py)
					gcode_tmp_flag=1
				if(gcode_tmp_flag):
					#Goto initial X-Y position
					out_data +=" F" + floats(EDGE_SPEED)
					gEDGE_DATA += out_data + "\n"
					out_data ="G1"
				gcode_tmp_flag=0
				i += 2
		j += 1
def move_edge(x,y):
	global MOVE_HEIGHT, gTMP_EDGE_X, gTMP_EDGE_Y, gTMP_EDGE_Z
	if abs(float(ROT_ANG)) > TINY:
		x,y = rot_point(x,y)
	if MIRROR_DRILL:
		x,y = mirror_point(x,y)
	x=x+float(gXSHIFT)
	y=y+float(gYSHIFT)
	xy_data = "G0"
	out_data = ""
	#print(out_data
	gcode_tmp_flag = 0
	if(x != gTMP_EDGE_X):
		gTMP_EDGE_X = x
		xy_data += " X" + floats(x)
		gcode_tmp_flag=1
	if(y != gTMP_EDGE_Y):
		gTMP_EDGE_Y = y
		xy_data += " Y" + floats(y)
		gcode_tmp_flag = 1
	if(MOVE_HEIGHT!=gTMP_EDGE_Z):
		gTMP_EDGE_Z = MOVE_HEIGHT
		#Goto moving Z position
		out_data = "G0 Z" + floats(MOVE_HEIGHT) + "\n"
	if(gcode_tmp_flag):
		#Goto initial X-Y position
		return out_data + xy_data + "\n"
	else:
		return ""
def points_revers(points):
	return_points = []
	i = len(points)-1
	while i>0:
		return_points = return_points + [points[i-1],points[i]]
		i -=2	
	return return_points
def open_file(dirname, filename):
	file_name = os.path.join(dirname, filename)
	with open(file_name,'r') as f:
		ret = f.read()
		return (ret.split("\n"),f)
	raise Exception("Unable to open the file " + file_name + "\n")
def write_file(dirname,filename,datas):
	file_name = os.path.join(dirname, filename)
	if(datas):
		f = open(file_name, 'w')
		f.write(datas)
		f.close()
	else:
		print("ERROR : No save data")
if __name__ == "__main__":
	main()
