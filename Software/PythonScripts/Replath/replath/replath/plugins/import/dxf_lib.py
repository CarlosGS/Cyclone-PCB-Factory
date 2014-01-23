#######################################################################################################################################################
# This module reads a dxf file is turns it into entities (line, circle etc).                                                                          #
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

# Class for entities (circle, line etc)
class dxfEntity():
	def __init__( self ):
		self.data = []
	def addLine( self, line ):
		self.data.append( line )
	def decode( self ):
		# Some programs will not enter Z data - better idea, make code accept missing?	TODO
		self.startZ = 0
		self.endZ = 0
		self.centreZ = 0
		
		self.type = self.data[0][:-1]	
		for i in range( 1, len(self.data) - 1, 2 ):
			param = self.data[i][:-1].strip()
			value = self.data[i + 1][:-1].strip()
			#print "param '" + param + "' = '" + value + "'"
			if self.type == "CIRCLE":
				if param == "100":
					self.subclass = value
				elif param == "39":
					self.thickness = float(value)
				elif param == "10":
					self.centreX = float(value)
				elif param == "20":
					self.centreY = float(value)
				elif param == "30":
					self.centreZ = float(value)
				elif param == "40":
					self.radius = float(value)
				elif param == "210":
					self.extrusionDirX = float(value)
				elif param == "220":
					self.extrusionDirY = float(value)
				elif param == "230":
					self.extrusionDirZ = float(value)
			elif self.type == "LINE":
				if param == "100":
					self.subclass = value
				elif param == "39":
					self.thickness = float(value)
				elif param == "10":
					self.startX = float(value)
				elif param == "20":
					self.startY = float(value)
				elif param == "30":
					self.startZ = float(value)
				elif param == "11":
					self.endX = float(value)
				elif param == "21":
					self.endY = float(value)
				elif param == "31":
					self.endZ = float(value)
				elif param == "210":
					self.extrusionDirX = float(value)
				elif param == "220":
					self.extrusionDirY = float(value)
				elif param == "230":
					self.extrusionDirZ = float(value)
			elif self.type == "ARC":
				if param == "100":
					self.subclass = value
				elif param == "39":
					self.thickness = float(value)
				elif param == "10":
					self.centreX = float(value)
				elif param == "20":
					self.centreY = float(value)
				elif param == "30":
					self.centreZ = float(value)
				elif param == "40":
					self.radius = float(value)
				elif param == "50":
					self.startAngle = float(value)
				elif param == "51":
					self.endAngle = float(value)
				elif param == "210":
					self.extrusionDirX = float(value)
				elif param == "220":
					self.extrusionDirY = float(value)
				elif param == "230":
					self.extrusionDirZ = float(value)
			elif self.type == "ELLIPSE":
				if param == "100":
					#Subclass marker (AcDbEllipse)
					pass
				elif param == "10":#
					self.centreX = float(value)
				elif param == "20":#
					self.centreY = float(value)
				elif param == "30":
					self.centreZ = float(value)
				elif param == "11":#
					#Endpoint of major axis, relative to the center (in WCS) DXF: X value; APP: 3D point
					self.endX = float(value)
				elif param == "21":
					#DXF: Y and Z values of endpoint of major axis, relative to the center (in WCS)
					self.endY = float(value)
				elif param == "31":
					#DXF: Y and Z values of endpoint of major axis, relative to the center (in WCS)
					self.endZ = float(value)
				elif param == "210":	
					#Extrusion direction (optional; default = 0, 0, 1) DXF: X value; APP: 3D vector
					pass
				elif param == "220":
					#DXF: Y and Z values of extrusion direction  (optional)
					pass
				elif param == "230":
					#DXF: Y and Z values of extrusion direction  (optional)
					pass
				elif param == "40":#
					#Ratio of minor axis to major axis
					self.minorMajorRatio = float(value)
				elif param == "41":#
					#Start parameter (this value is 0.0 for a full ellipse)
					self.startAngle = float(value)
				elif param == "42":#
					#End parameter (this value is 2pi for a full ellipse)
					self.endAngle = float(value)
				#The group codes 41 and 42 are the start and end values for u in the equation below. The magnitude of the codes 11,21,31 vector is equal to 1/2 of the major axis which is the a value in the equation. The point 10,20,30 is the c value in the equation. Knowing all these, we can calculate the b value to complete the equation.

# Class for gerber file (main)
class dxf():
	def __init__( self, fileName ):
		dxfFile = open( fileName, "r" )
		fileLines =  dxfFile.readlines() 
		entStart = 0
		currentEntStart = 0
		self.entities = []
		lineIsCommand = False
		currentEnt = False
		for n in range( 0, len(fileLines) ):
			line = fileLines[n][:-1].strip()
			#print "'" + line + "'"
			if line == "ENTITIES":
				entStart = n
			elif line == "CIRCLE" or fileLines[n][:-1] == "LINE" or fileLines[n][:-1] == "ARC" or fileLines[n][:-1] == "ELLIPSE":
				if not currentEnt:
					currentEnt = dxfEntity()
					lineIsCommand = False
				else:
					print "DXF Read Error"
			elif line == "0":				# end of shape
				if currentEnt and lineIsCommand:
					self.entities.append( currentEnt )
					currentEnt = False
			if currentEnt:
				currentEnt.addLine( fileLines[n] )
				lineIsCommand = not lineIsCommand	# set for next loop

		for e in self.entities:
			e.decode()

	def printEnts( self ):			
		for e in self.entities:
			if e.type == "LINE":
				print e.type, "from [", e.startX, e.startY, e.startZ, "] to [", e.endX, e.endY, e.endZ, "]"
			elif e.type == "CIRCLE":
				print e.type, "centre [", e.centreX, e.centreY, e.centreZ, "], radius [", e.radius, "]"
			elif e.type == "ARC":
				print e.type, "centre [", e.centreX, e.centreY, e.centreZ, "], radius [", e.radius, "] start [", e.startAngle, "] end [", e.endAngle, "]" 
			elif e.type == "ELLIPSE":
				print e.type, "centre [", e.centreX, e.centreY, e.centreZ, "], start [", e.startAngle, "] end [", e.endAngle, "] more"


			

