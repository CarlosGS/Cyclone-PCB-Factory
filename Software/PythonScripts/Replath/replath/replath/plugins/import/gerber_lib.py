#######################################################################################################################################################
# This module reads a gerber file is turns it into objects (flashes and traces).                                                                      #
#######################################################################################################################################################
"""
Licenced under GNU v2 and the 'I'm not going to help you kill people licence'. The latter overrules the former.
        
I'm not going to help you kill people licence v1:
The use of this software in any form for any purposes relating to any form of military activity or
research either directly or via subcontracts is strictly prohibited.
Any company or organisation affiliated with any military organisations either directly or through
subcontracts are strictly prohibited from using any part of this software.

GNU licence:        
RepRap Gerber Plotter is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free Software Foundation; 
either version 2 of the License, or (at your option) any later version.

RepRap Gerber Plotter is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have received a copy of 
the GNU General Public License along with File Hunter; if not, write to 
the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import math
import time # temp testing

# Define constants
FS_ABSOLUTE = 1			# coordinate modes
FS_INCREMENTAL = 2		#
const_mmPerInch = 25.4

FLASH = 1
STROKE = 2

# Class for gerber aperture. Reads line from gerber file and extracts code, type & modifiers
class aperture:
	def __init__( self, paramString, units ):
		#print "GA string '" + paramString + "'"
		commorPos = paramString.find( ',' )
		#print paramString[ 3 : commorPos - 1 ]
		if len( paramString[ 3 : commorPos - 1 ] ) > 3:	#better way of doing this?
			#print "aperture is macro, need tostate hereh?"
			self.isMacro = True
			self.code = int( paramString[ 3 : 5 ] )	#not perfect
			self.macroName = paramString[ 5 : commorPos ]
			print "am name '" + self.macroName + "'"
		else:
			self.isMacro = False
			self.code = int( paramString[ 3 : commorPos - 1 ] )
		self.apertureType = paramString[ commorPos - 1 : commorPos ]
		modString = paramString[ commorPos + 1 : -1 ]
		self.modifiers = []
		lastDiv = 0
		divPos = modString.find( 'X' )
		while divPos > 0:
			self.modifiers.append( modString[ lastDiv : divPos ] )
			modString = modString[ divPos + 1 : ]
			lastDiv = divPos
			divPos = modString.find( 'X' )
		self.modifiers.append( float(modString) )

		if self.apertureType == "C":
			self.radius = ( float( self.modifiers[0] ) / 2 )		# convert from diameter
			if units == "IN":
				self.radius = self.radius * const_mmPerInch
		elif self.apertureType == "R":
			self.width = float( self.modifiers[0] )
			self.height = float( self.modifiers[1] )
			if units == "IN":
				self.width = self.width * const_mmPerInch
				self.height = self.height * const_mmPerInch
		elif self.apertureType == "O":
			self.width = float( self.modifiers[0] )
			self.height = float( self.modifiers[1] )
			if units == "IN":
				self.width = self.width * const_mmPerInch
				self.height = self.height * const_mmPerInch
		else:
			print "Aperture type '" + self.apertureType + "' unsupported"

#Class for gerber aperture macro
class apertureMacro:
	def __init__(self, paramString, units):
		print "AM", paramString
		starPos = paramString.find('*')
		commorPos = paramString.find(',')
		self.name = paramString[ 2:starPos ]
		print "name '" + self.name + "'"
		self.primitiveNumber = int( paramString[ starPos + 1:commorPos ] )
		print "pn '" + str(self.primitiveNumber) + "'"
		if paramString[ -1: ] == "*":
			remainParamString = paramString[ commorPos + 1:-1 ]
			modifiers = remainParamString.split(',')
			print modifiers
		
			if self.primitiveNumber == 5:
				print "polygon"
				self.exposure = int( modifiers[0] )
				self.numVerticies = int( modifiers[1] )
				self.centreX = int( modifiers[2] )
				self.centreY = int( modifiers[3] )
				self.diameter = modifiers[4]			#this is strange
				self.rotation = float( modifiers[5] )	#in degrees
				print "self.exposure", self.exposure, "self.numVerticies", self.numVerticies, "self.centreX", self.centreX, "self.centreY", self.centreY, "self.diameter", self.diameter, "self.rotation", self.rotation
			else:
				print "Aperture macro type", self.primitiveNumber, "not handled"



# Class for a gerber flash (move and flash aperture)
class gerberFlash:
	def __init__(self, x, y, aperture):
		self.type = FLASH
		self.x, self.y, self.aperture = x, y, aperture
		#print "create flash with aperture", aperture
		#self.radius = self.aperture.radius
	def printFlash(self):
		print "FLASH", self.x, self.y, self.aperture

# Class for a gerber trace (aperture open move)
class gerberTrace:
	def __init__(self, x1, y1, x2, y2, aperture):
		self.type = STROKE
		self.x1, self.y1, self.x2, self.y2, self.aperture = x1, y1, x2, y2, aperture
	def printTrace(self):
		print "TRACE", self.x1, self.y1, self.x2, self.y2, self.aperture


class gerber:
	def __init__(self, fileName):
		self.fileName = fileName
		
		self.apertures = {}
		self.apertureMacros = {}
		self.currentAperture = False
		self.currentX, self.currentY = 0, 0
		self.xCoordinateOffset, self.yCoordinateOffset = 0, 0
		self.xCoordinateScale, self.yCoordinateScale = 1, 1
		
		# All flash and trace objects stored here
		self.flashes = []
		self.traces = []
		self.debug = False # TODO pass this in
		
		f = open( self.fileName, 'r' )
		lines = f.readlines()
		# Do actual parsing of file
		self.parseLines(lines)
		#print self.apertures

	# Parse all lines of the gerber file
	def parseLines( self, lines ):
		for i in range( len(lines) ):
			l = lines[i]
			#print "Reading line '" + l[ : -1 ] + "'"
			firstChr = l[ : 1 ]
			lastChr = l[ -2 : -1 ]
			if firstChr == "G" and lastChr == "*":
				self.cmdGcode( l[ 1 : -2 ] )
			elif firstChr == "D" and lastChr == "*":
				self.cmdDcode( l[ 1 : -2 ] )
			elif firstChr == "%" and lastChr == "%":
				self.cmdParameter( l[ 1 : -2 ] )
			elif firstChr == "%":
				while l[ -2:-1 ] != "%":
					print "j '" + l[ -1: ] + "'"
					lines[i] = lines[i][ :-1] + lines[ i + 1 ]
					lines.remove( lines[ i + 1 ] )
					lines.append("")	# to keep for loop happy
					l = lines[i]
				self.cmdParameter( l[ 1:-2 ] )
			elif firstChr == "X" and lastChr == "*":
				self.cmdMove( l[ : -2 ] )
			elif firstChr == "M" and lastChr == "*":
				self.cmdMisc( l[ 1 : -2 ] )
			elif l[ : -1 ] == "":
				pass
			else:
				print "Line error! '" + l[ : -1 ] + "'"

	# Handle an M code
	def cmdMisc( self, mstring ):
		code = int( mstring[ : 2 ] )
		remains = mstring[ 2: ]
		print "MCODE", code, remains

	# Handle a G code
	def cmdGcode( self, gstring ):
		code = int( gstring[ : 2 ] )
		remains = gstring[ 2: ]
		if code == 0:
			print "Move", "[COMMAND UNSUPORTED!]"
		elif code == 1:
			print "Linear interpolation (1X scale)", "[COMMAND UNSUPORTED!]"			#TODO ADD
		elif code == 2:
			print "Clockwise circular interpolation", "[COMMAND UNSUPORTED!]"
		elif code == 3:
			print "Counterclockwise circular interpolation", "[COMMAND UNSUPORTED!]"
		elif code == 4:
			# Ignore Line
			#print "Comment", remains
			comment = False
		elif code == 10:
			print "Linear interpolation (10X scale)", "[COMMAND UNSUPORTED!]"
		elif code == 11:
			print "Linear interpolation (0.1X scale)", "[COMMAND UNSUPORTED!]"
		elif code == 12:
			print "Linear interpolation (0.01X scale)", "[COMMAND UNSUPORTED!]"
		elif code == 36:
			print "Turn on Polygon Area Fill", "[COMMAND UNSUPORTED!]"
		elif code == 37:
			print "Turn off Polygon Area Fill", "[COMMAND UNSUPORTED!]"
		elif code == 54:
			if remains[ : 1 ] == "D":
				self.selectTool( int( remains[ 1 : ] ) )
		elif code == 70:
			if self.debug: print "Specify inches"							# why are there two ways of setting units?
			self.units = "IN"
		elif code == 71:
			if self.debug: print "Specify millimeters"
			self.units = "MM"
		elif code == 74:
			print "Disable 360 deg circular interpolation (single quadrant)", "[COMMAND UNSUPORTED!]"
		elif code == 75:
			print "Enable 360 deg circular interpolation (multiquadrant)", "[COMMAND UNSUPORTED!]"		#TODO
		elif code == 90:
			if self.debug: print "Absolute coordinate format"
			self.FSparameter = FS_ABSOLUTE
		elif code == 91:
			if self.debug: print "Incremental coordinate format - This mode is not supported"
			self.FSparameter = FS_INCREMENTAL

		else:
			print "COMMAND UNKNOWN"

	#Handle D code	- weird eagle inconsistancy?
	def cmdDcode( self, paramString ):
		if self.debug: print "Tool prepare"
		self.selectTool( int(paramString) )
	
	def selectTool( self, tool ):
		#print tool
		self.currentAperture = self.apertures[ tool ]
		#print "select tool", tool, self.currentAperture, self.currentAperture.code
		#if self.debug: print "    Selecting aperture", int( remains[ 1 : ] )
		#print currentAperture.modifiers[0]

	# Handle a parameter
	def cmdParameter( self, paramString ):
		#print "Parameter", paramString, paramString[ : 2]

		if paramString[ : 3 ] == "ADD" and paramString[ -1 : ] == "*":
			# Add a new aperture
			newAperture = aperture( paramString, self.units )
			self.apertures[ newAperture.code ] = newAperture

		elif paramString[ :2 ] == "AM" and paramString[ -1 : ] == "*":
			newApertureMacro = apertureMacro(paramString, self.units)
			self.apertureMacros[ newApertureMacro.name ] = newApertureMacro
			
		elif paramString[ :2 ] == "AS" and paramString[ -1 : ] == "*":
			print "Param AS Unsuported"

		elif paramString[ :2 ] == "FS" and paramString[ -1 : ] == "*":
			xInt = int( paramString[5] )
			xDec = int( paramString[6] )
			yInt = int( paramString[8] )
			yDec = int( paramString[9] )

			if paramString[2] == "L":
				self.xCoordinateScale = 1 / math.pow(10, xDec)
				self.yCoordinateScale = -1 / math.pow(10, yDec)		#not sure this is perfect
			elif paramString[2] == "T":
				self.xCoordinateScale = 1
				self.yCoordinateScale = 1							# need to find out why some gerber have y in minus values, but do all need inverting? think this is ok now
			if paramString[3] == "A":
				print "abs"				#TODO
			elif paramString[3] == "I":
				print "Incremental Coordinates not currently supported"
			print "finish this"

		elif paramString[ :2 ] == "IF" and paramString[ -1 : ] == "*":
			print "Param IF Unsuported"
			
		elif paramString[ :2 ] == "IJ" and paramString[ -1 : ] == "*":
			print "Param IJ Unsuported"
			
		elif paramString[ :2 ] == "IN" and paramString[ -1 : ] == "*":
			print "Param IN Unsuported"
			
		elif paramString[ :2 ] == "IO" and paramString[ -1 : ] == "*":
			print "Param IO Unsuported"
			
		elif paramString[ : 2 ] == "IP" and paramString[ -1 : ] == "*":		#TODO
			print "TODO polatiry = ", paramString[ 2 : -1 ]
			
		elif paramString[ :2 ] == "IR" and paramString[ -1 : ] == "*":
			print "Param IR Unsuported"
			
		elif paramString[ :2 ] == "KO" and paramString[ -1 : ] == "*":
			print "Param KO Unsuported"
			
		elif paramString[ :2 ] == "LN" and paramString[ -1 : ] == "*":
			print "Param LN Unsuported"
			
		elif paramString[ :2 ] == "LP" and paramString[ -1 : ] == "*":		#TODO
			print "Param LP Unsuported"
			
		elif paramString[ :2 ] == "MI" and paramString[ -1 : ] == "*":
			print "Param MI Unsuported"
			
		elif paramString[ : 2 ] == "MO" and paramString[ -1 : ] == "*":
			# Set units
			self.units = paramString[ 2 : -1 ]
			
		elif paramString[ :2 ] == "OF" and paramString[ -1 : ] == "*":
			# Offset
			aPos = paramString.find('A')
			bPos = paramString.find('B')
			self.xCoordinateOffset = float( paramString[ aPos + 1:bPos ] )
			self.yCoordinateOffset = float( paramString[ bPos + 1:-1 ] )
			
		elif paramString[ :2 ] == "PF" and paramString[ -1 : ] == "*":
			print "Param PF Unsuported"
			
		elif paramString[ :2 ] == "SF" and paramString[ -1 : ] == "*":
			print "Param SF Unsuported"
			
		elif paramString[ :2 ] == "SR" and paramString[ -1 : ] == "*":
			print "Param SR Unsuported"
			
		else:
			print "PARAMETER UNKNOWN"

	# Hande a move
	def cmdMove( self, moveString ):
		yPos = moveString.find( 'Y' )
		dPos = moveString.find( 'D' )
		x = ( float( moveString[ 1 : yPos ] ) * float(self.xCoordinateScale) ) + self.xCoordinateOffset
		y = ( float( moveString[ yPos + 1 : dPos ] ) * -float(self.yCoordinateScale) ) + self.yCoordinateOffset		# still need minus?
		# If inches convert to mm
		if self.units == "IN":
			x = x * const_mmPerInch
			y = y * const_mmPerInch
		# Get move type (aperture open, aperture closed, flash)
		d = int( moveString[ dPos + 1 : ] )
		if self.debug: print "Move [", x, "mm,", y, "mm],", d
		if d == 1:
			#if self.currentAperture.code == 12 or self.currentAperture.code == 13: print "trace", self.currentAperture.code
			self.traces.append( gerberTrace( self.currentX, self.currentY, x, y, self.currentAperture ) )
		elif d == 2:
			pass	# no entity information required
			# Move is aperture closed (pen up) type
		elif d == 3:
			#print "create flash with ms", moveString
			self.flashes.append( gerberFlash( x, y, self.currentAperture ) )
			#if self.currentAperture.code == 12 or self.currentAperture.code == 13: print "flash", self.currentAperture.code
		self.currentX, self.currentY = x, y






