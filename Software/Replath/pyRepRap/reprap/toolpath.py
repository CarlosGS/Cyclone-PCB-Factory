"""
This module contains the classed used for internal storage of toolpath instructions.
The module can also import/export Intermediate Toolpath Language (ITL) files
which are pyRepRap's native file format.
"""

# Python module properties
__author__ = "Stefan Blanke (greenarrow) (greenarrow@users.sourceforge.net)"
__license__ = "GPL 3.0"
__licence__ = """
pyRepRap is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyRepRap is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyRepRap.  If not, see <http://www.gnu.org/licenses/>.
"""

import xml.dom.minidom
from xml.dom.minidom import Node


# Point within a polygon
class Point:
	def __init__(self, x = None, y = None, z = None):
		self.x, self.y, self.z = x, y, z

# Polygon within a layer
class Polygon:
	def __init__(self, index = None, points = None, closed = False, clone = None, offsetX = 0, offsetY = 0, scale = 1, tool = None, material = None):
		if points != None:
			self.points = points
		else:
			self.points = []
		self.index = index
		self.closed = closed
		self.clone = clone
		self.offsetX = offsetX
		self.offsetY = offsetY
		self.scale = scale
		self.pointsPlotted = 0
		self.tool = tool
		self.material = material
		self.pointsPlotted = 0
	
	def addPoint(self, point):
		self.points.append(point)
	
	def addPoints(self, points):
		self.points += points
	
	def addPolygon(self, poly):
		self.points += poly.points

# Layer within a toolpath
class Layer:
	def __init__(self, index = None, polygons = None, workingHeight = None, idleHeight = None):
		self.index = index
		if polygons != None:
			self.polygons = polygons
		else:
			self.polygons = []
		self.workingHeight = workingHeight
		self.idleHeight = idleHeight

# Toolpath object - describes full parameters for machine build
class Object:
	def __init__(self, layers = None, scale = 1):
		if layers != None:
			self.layers = layers
		else:
			self.currentLayer = Layer()
			self.layers = [ self.currentLayer ]
		self.offsetX = 0
		self.offsetY = 0
		self.scale = 1
		self.version = 0.3
		self.units = "mm"
		self.debug = False
	
	# Read toolpath object from XML based Intermediate Toolpath Language file
	def readITL(self, filename):
		doc = xml.dom.minidom.parse(filename)
		self.layers = []
		for smilNode in doc.getElementsByTagName("ITL"):
			self.version = smilNode.getAttribute("version")
			self.layerCount = int(smilNode.getAttribute("layers"))
			self.units = smilNode.getAttribute("units")
			offset = smilNode.getAttribute("offset")
			offsetParts = offset.split(',')
			self.offsetX, self.offsetY = float(offsetParts[0]), float(offsetParts[1])
			self.scale = float(smilNode.getAttribute("scale"))
			for layerNode in smilNode.getElementsByTagName("LAYER"):
				if layerNode.getAttribute("index") == "None":
					index = None
				else:
					index = int(layerNode.getAttribute("index"))
				if layerNode.getAttribute("workingHeight") == "None":
					workingHeight = None
				else:
					workingHeight = float(layerNode.getAttribute("workingHeight"))
				if layerNode.getAttribute("idleHeight") == "None":
					idleHeight = None
				else:
					idleHeight = float(layerNode.getAttribute("idleHeight"))
				currentLayer = Layer(index, workingHeight = workingHeight, idleHeight = idleHeight)
				if self.debug: print "Layer index", index
				for polygonNode in layerNode.getElementsByTagName("POLYGON"):
					if polygonNode.getAttribute("index") == "None":
						index = None
					else:
						index = int(polygonNode.getAttribute("index"))
					if polygonNode.getAttribute("clone") == "None":
						clone = None
					else:
						clone = int(polygonNode.getAttribute("clone"))
					if polygonNode.getAttribute("closed") == "True":
						closed = True
					else:
						closed = False
					offset = polygonNode.getAttribute("offset")
					offsetParts = offset.split(',')
					offsetX, offsetY = float(offsetParts[0]), float(offsetParts[1])
					scale = float(polygonNode.getAttribute("scale"))
					if polygonNode.getAttribute("tool") == "None":
						tool = None
					else:
						tool = polygonNode.getAttribute("tool")
					if polygonNode.getAttribute("material") == "None":
						material = None
					else:
						material = polygonNode.getAttribute("material")
					if self.debug: print "Polygon index", index
					polygon = Polygon(index, closed = closed, clone = clone, offsetX = offsetX, offsetY = offsetY, scale = scale, tool = tool, material = material)
					for d in polygonNode.childNodes:
						if d.nodeType == Node.TEXT_NODE:
							lines = d.data.splitlines()
							for l in lines:
								parts = l.split('\t')
								for i in range( parts.count('') ):
									parts.remove('')
								if len(parts) > 0:
									if self.debug: print parts, parts[0][0], parts[1][0]
									if parts[0][0] == "X" and parts[1][0] == "Y":
										polygon.addPoint( Point( float(parts[0][ 1: ]), float(parts[1][ 1: ]) ) )
					if len(polygon.points):
						currentLayer.polygons.append(polygon)
				self.layers.append(currentLayer)
	
	# Write toolpath object to XML based Intermediate Toolpath Language file
	def writeITL(self, filename):
		itl = '<ITL version = "0.2" layers="' + str( len(self.layers) ) + '" units="mm" offset="' + str(self.offsetX) + ',' + str(self.offsetY) + '" scale="' + str(self.scale) + '">\n'
		for layer in self.layers:
			# Index starts at one as zero is used in clone to mean not clone
			itl += '\t<LAYER index="' + str(layer.index) + '" workingHeight="' + str(layer.workingHeight) + '" idleHeight="' + str(layer.idleHeight) + '">\n'
			for polygon in layer.polygons:
				#itl += '\t\t<TOOL name="' + toolName + '" index="0">\n'
				itl += '\t\t<POLYGON index="' + str(polygon.index) + '" clone="' + str(polygon.clone) + '" closed="' + str(polygon.closed) + '" offset="' + str(polygon.offsetX) + ',' + str(polygon.offsetY) + '" scale="' + str(polygon.scale) + '" tool="' + str(polygon.tool) + '" material="' + str(polygon.material) + '">\n'
				for pointIndex, point in enumerate(polygon.points):
					itl += '\t\t\t'
					if point.x != None:
						itl += 'X' + str(point.x) + '\t'
					if point.y != None:
						itl += 'Y' + str(point.y) + '\t'
					if point.z != None:
						itl += 'Z' + str(point.z) + '\t'
					if itl[-1] == '\t':
						itl = itl[ :-1] + '\n'
				itl += '\t\t</POLYGON>\n'
				#itl += '\t\t</TOOL>\n'
		itl += '\t</LAYER>\n'
		itl += '</ITL>\n'
		f = open(filename, 'w')
		f.write(itl)
		f.close()

