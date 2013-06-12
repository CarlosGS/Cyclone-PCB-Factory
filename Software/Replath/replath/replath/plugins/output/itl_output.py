#######################################################################################################################################################
# This module write ITL toolpath files                                                                                                               #
#######################################################################################################################################################
"""
Licensed under GPL v2 and the 'I'm not going to help you kill people licence'. The latter overrules the former.
        
I'm not going to help you kill people licence v1.1:
The use of this software in any form for any purposes relating to any form of military activity or
research either directly or via subcontracts is strictly prohibited.
Any company or organisation affiliated with any military organisations either directly or through
subcontracts are strictly prohibited from using any part of this software.
Individuals who work for the above mentioned organisations working on PERSONAL or open source projects unrelated
to above mentioned organisations in their own time may use this software.

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

import threading, replath.preferences
import reprap	#remove?
#from itl_prefpanel import PreferencesPanel

Title = "ITL File"
FileOutput = True
Wildcard = 'ITL files (*.itl)|*.itl'

class output(replath.baseplotters.ExportPlotter):
	# Load plotter preferences
	def loadPreferences(self):
		# make polygon merging an option TODO
		self.pref_bypassToolhead = True		# this is hidden preference at the moment
		#self.pref_roundingFigures = 2
		self.prefHandler = replath.preferences.PreferenceHandler(self,  "output_itl.conf")
		self.prefHandler.load()
	
	# Start plot (as new thread)
	def run(self):
		self.alive = True
		if self.pref_bypassToolhead:
			self.toolpath.writeITL(self.outputFilename)
		else:
			"""
			self.itl = ITL()
			self.curZ = 0
			for poly in self.polygons:
				if not self.alive:
					self.feedbackHandler.aborted()
					break
				#print "plot poly", poly.points, "pc", poly.closed
				x1, y1 = poly.points[0]
				self.cartesianMove(x1, y1, None)
				self.toolhead.start()
				for p in poly.points[ 1: ]:
					x2, y2 = p
					if (x1 != x2) or (y1 != y2):
						self.cartesianMove(x2, y2, None)
				x1, y1 = x2, y2
				self.toolhead.stop()
				self.itl.finishPolygon(poly.closed)
			self.itl.writeFile(self.outputFilename)
			"""
			self.feedbackHandler.showMessagePopup("ITL plotting with toolhead needs re-implementing")
		
		if self.alive:
			# Tell gui that plot is complete (redraw screen)
			self.feedbackHandler.plotComplete()
	
	# Translate a cartesian movement into whatever the output plugin does with it (called locally and by toolhead)
	def cartesianMove(self, x, y, z, units = reprap.UNITS_MM):
		#if z != None:
		#	self.itl.addCoordinate( x, y, z )
		if x != None and y != None:
			self.itl.addCoordinate( x, y, z )
		# TODO, should we round coordinates




"""
def writeFile(self, fileName):
	itl = f.generateITL()
	f = open( fileName, 'w' )
	f.write(itl)
	f.close()
"""
"""
# Simple class for layer
class layer():
	def __init__(self, polygons = False):
		if polygons:
			self.polygons = polygons
		else:
			self.polygons = []
		self.currentPolygon = spolygon()
	def finishPolygon(self, closed):
		if closed:
			self.currentPolygon.closed = 1
		else:
			self.currentPolygon.closed = 0
		self.polygons.append(self.currentPolygon)
		self.currentPolygon = spolygon()
		
	def getPolygons(self):
		return self.polygons

# Simple class for polygon (single tool movement path)
class spolygon():
	def __init__(self):
		self.coordinates = []
		self.closed = False
	
	def addCoordinate(self, x, y, z):
		self.coordinates.append( (x, y, z) )
	
	def getCoordinates(self):
		return self.coordinates

# Class for itl file
class ITL():
	def __init__(self, polygons = False):
		if polygons:
			self.layers = [ layer(polygons) ]
		else:
			self.layers = []
			self.currentLayer = layer()
		
	def addCoordinate(self, x, y, z):
		self.currentLayer.currentPolygon.addCoordinate(x, y, z)
	
	def finishPolygon(self, closed):
		self.currentLayer.finishPolygon(closed)
	
	def newLayer(self):
		self.layers.append(self.currentLayer)
		self.currentLayer = layer()
	
	def generateITL(self):
		#self.finishPolygon(False)
		self.newLayer()
		toolName = "pen"	# temp
		itl = '<SSIL LayerCount="' + str( len(self.layers) ) + '" Units="mm">\n'
		for layerIndex, layer in enumerate(self.layers):
			itl += '\t<LAYER index="' + str(layerIndex) + '" >\n'
			for polygonIndex, polygon in enumerate( layer.getPolygons() ):
				itl += '\t\t<TOOL Name="' + toolName + '" index="0">\n'
				itl += '\t\t\t<THREAD index="' + str(polygonIndex) + '">\n'
				for coordinateIndex, coordinate in enumerate( polygon.getCoordinates() ):
					x, y, z = coordinate
					itl += '\t\t\t\t<POINT X="' + str(x) + '" Y="' + str(y) + '" index="' + str(coordinateIndex) + '"/>\n'		# add z support here
				itl += '\t\t\t</THREAD>\n'
			itl += '\t\t</TOOL>\n'
		itl += '\t</LAYER>\n'
		itl += '</SSIL>\n'
		
	def generateITL2(self):
		#self.finishPolygon()
		#self.newLayer()
		toolName = "pen"	# temp
		offsetX, offsetY = 0, 0
		itl = '<SSIL version = "0.2" layers="' + str( len(self.layers) ) + '" units="mm" offset="' + str(offsetX) + ',' + str(offsetY) + '">\n'
		for layerIndex, layer in enumerate(self.layers):
			# Index starts at one as zero is used in clone to mean not clone
			itl += '\t<LAYER index="' + str(layerIndex + 1) + '" >\n'
			for polygonIndex, polygon in enumerate( layer.getPolygons() ):
				itl += '\t\t<TOOL name="' + toolName + '" index="0">\n'
				if polygon.closed:
					closed = '1'
				else:
					closed = '0'
				if polygon.clone:
					clone = str(clone)
				else:
					clone = '0'
				itl += '\t\t\t<POLYGON index="' + str(polygonIndex) + '" closed="' + closed + '" clone="' + clone + '" offset="' + str(polygon.offsetX) + ',' + str(polygon.offsetY) + '" scale="' + str(polygon.scale) + '">\n'
				for coordinateIndex, coordinate in enumerate( polygon.getCoordinates() ):
					x, y, z = coordinate
					itl += '\t\t\t\tX' + str(x) + '\tY' + str(y) + '\n'
				itl += '\t\t\t</POLYGON>\n'
				itl += '\t\t</TOOL>\n'
		itl += '\t</LAYER>\n'
		itl += '</SSIL>\n'
		
	def generatePlainTextITL(self):
		self.finishPolygon()
		self.newLayer()
		toolName = "pen"	# temp
		itl = 'LayerCount ' + str( len(self.layers) ) + '\n'
		itl += "UNITS mm"
		for layerIndex, layer in enumerate(self.layers):
			itl += 'LAYER ' + str(layerIndex) + '\n'
			for polygonIndex, polygon in enumerate( layer.getPolygons() ):
				itl += 'TOOL ' + toolName + ' 0\n'
				itl += 'THREAD ' + str(polygonIndex) + '\n'
				for coordinateIndex, coordinate in enumerate( polygon.getCoordinates() ):
					x, y, z = coordinate
					itl += 'I' + str(coordinateIndex) + ' X' + str(x) + ' Y' + str(y) + '\n'		# add z support here
				itl += 'END THREAD\n'
			itl += 'END TOOL\n'
		itl += 'END LAYER\n'
		itl += 'EOF\n'
	
	def writeFile(self, fileName):
		self.generateITL2()
		#self.generatePlainTextITL()
		#print itl
		f = open( fileName, 'w' )
		f.write(itl)
		f.close()
"""

