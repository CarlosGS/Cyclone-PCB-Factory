"""
This module plots many shapes a polygon objects containing a series of lines
The Polygon object can be found in reprap.toolpath
"""

# Python module properties
__author__ = "Stefan Blanke (greenarrow) (greenarrow@users.sourceforge.net)"
__license__ = "GPL 3.0"
__credits__ = "Author of potrace"
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

import math, os
import toolpath

# Fill modes
FILL_LOCUS = 1
FILL_LINES = 2

debug = False

def line(line):
	"""Returns polygon for line (x1, y2, x2, y2) as a Polygon object"""
	poly = toolpath.Polygon()
	x1, y1, x2, y2 = line
	poly.addPoint( toolpath.Point(x1, y1) )
	poly.addPoint( toolpath.Point(x2, y2) )
	return poly

def point(point):
	"""Returns polygon for point (x, y) as a Polygon Object"""
	poly = toolpath.Polygon()
	x, y = point
	poly.addPoint( toolpath.Point(x, y) )
	return poly

def arc(x, y, radius, startAngle, endAngle, resolution):
	"""Returns polygon an arc with x, y, radius, start angle (radians), end engle (radians) and resolution (lines per mm) a Polygon object"""
	# This function works in degrees but takes parameters in radians
	poly = toolpath.Polygon()
	if debug: print "Plotting arc at", x, y, "from", startAngle, "(", math.degrees(startAngle), ") to", endAngle, "(", math.degrees(endAngle), ")"
	startAngle, endAngle = math.degrees(startAngle), math.degrees(endAngle)
	circumference = float(2) * math.pi * float(radius)
	angleDiv = ( float(360) / float( circumference * resolution ) )# + ( 360 % int( circumference * resolution ) )
	lastX, lastY = _calcCircle( startAngle, radius )
	# compensate for arc going beyond 360 deg
	if startAngle > endAngle:
		endAngle += 360								
	# make detail proportional to radius to always give good resolution
	for theta in _frange( startAngle, endAngle + angleDiv, angleDiv ):
		cx, cy = _calcCircle(theta, radius)
		poly.addPoint( toolpath.Point(x + cx, y + cy) )
	return poly

def circle(x, y, radius, resolution, fillDensity = False):
	"""Returns polygon for a filled circle with x, y, radius, resolution (lines per mm) and fill density (lines per mm) as a Polygon object"""
	poly = toolpath.Polygon()
	if fillDensity:
		numFills = int( float(fillDensity) * float(radius) )
	else:
		numFills = 1
	for d in range( 1, numFills + 1 ):
		r = ( float(d) / float(numFills) ) * float(radius)
		if debug: print "using r", r, "mm"
		poly.addPolygon( arc( x, y, r, math.radians(0), math.radians(360), resolution ) )
	return poly

def ellipse(x, y, a, b, resolution, fillDensity = False):
	"""Returns polygon for a filled ellipse with x, y, a, b, resolution (lines per mm) and fill density (lines per mm) as a Polygon object"""
	poly = toolpath.Polygon()
	if not resolution:
		resolution = self.circleResolution
	if fillDensity:
		if a > b:
			largerDimension = a
		else:
			largerDimension = b
		numFills = int( float(fillDensity) * float(largerDimension) )
	else:
		numFills = 1
	startAngle, endAngle = 0, 360
	# Not really cicumference but will do?
	circumference = float(2) * math.pi * float( float( a + b ) / 2 )
	angleDiv = ( float(360) / float( circumference * resolution ) ) # + ( 360 % int( circumference * resolution ) )
	lastX, lastY = _calcEllipse( startAngle, a, b )
	# Compensate for arc going beyond 360 deg
	if startAngle > endAngle:
		endAngle += 360
	for d in range( 1, numFills + 1 ):
		ra = ( float(d) / float(numFills) ) * float(a)
		rb = ( float(d) / float(numFills) ) * float(b)
		for theta in _frange( startAngle, endAngle + angleDiv, angleDiv ):
			newX, newY = _calcEllipse( theta, ra, rb )
			aLine = poly.addPoint( toolpath.Point(newX + x , newY + y) )
			if debug: print "aLine", aLine
	return poly

# Return polygon for a filled rectangle
def rectangle(x, y, width, height, fillDensity = False):
	"""Returns polygon for line x, y, width, height and fill density (lines per mm) as a Polygon object"""
	poly = toolpath.Polygon()
	numFillsY = int( float(fillDensity) * float(height) )
	cornerX, cornerY = x - ( width / 2 ), y - ( height / 2 )
	invert = False

	for dy in range( 0, numFillsY + 1 ):
		ry = ( float(dy) / float(numFillsY) ) * float(height)
		line1 = (cornerX, cornerY + ry, cornerX + width, cornerY + ry )
		line2 = (cornerX, cornerY + ry, cornerX + width, cornerY - ry )
		if invert:
			line1 = _reverseLine(line1)
		invert = not invert
		x1, y1, x2, y2 = line1
		poly.addPoint( toolpath.Point(x1, y1) )
		poly.addPoint( toolpath.Point(x2, y2) )
		
	poly.addPoint( toolpath.Point(cornerX, cornerY) )
	poly.addPoint( toolpath.Point(cornerX, cornerY + height) )
	poly.addPoint( toolpath.Point(cornerX + width, cornerY) )
	poly.addPoint( toolpath.Point(cornerX + width, cornerY + height) )
	return poly

def circleStroke(x1, y1, x2, y2, radius, resolution, fillDensity = False ):
	"""Returns polygon for a photoplotter moving stroke using a circular aperture with x, y, radius, resolution (lines per mm) and fill density (lines per mm) as a Polygon object"""
	poly = toolpath.Polygon()
	deltaY = y2 - y1
	deltaX = x2 - x1
	if x1 == x2 and y1 == y2:
		#print "this is not a move, this is why software like eagle that uses drm on your own files....is crap"
		poly.addPolygon( circle( x1, y1, radius, resolution = resolution, fillDensity = fillDensity ) )
	else:
		if debug: print "PMWC, fill density", fillDensity
		#Plot central line
		poly.addPoint( toolpath.Point(x1, y1) )
		poly.addPoint( toolpath.Point(x2, y2) )
		# For each locus
		numFills = int( float(fillDensity) * float(radius) )
		for d in range( 1, numFills + 1 ):
			r = ( float(d) / float(numFills) ) * float(radius)
			if debug: print "using r", r, "mm"
			theta = _angleFromDeltas( deltaX, deltaY )
			rsintheta = r * math.sin( theta )
			rcostheta = r * math.cos( theta )
			# Makes sure angle is in correct quadrant
			if deltaX > 0:
				startOffset = math.radians(90)
				endOffset = math.radians(-90)
			else:
				startOffset = math.radians(-90)
				endOffset = math.radians(90)
			if deltaY < 0:
				startOffset = -startOffset
				endOffset = -endOffset
			# Plot side lines and end arcs (simi-circles) of locus
			# reversing these point lets locus be drawn in one continual motion
			poly.addPoint( toolpath.Point(x2 - rsintheta, y2 + rcostheta) )
			poly.addPoint( toolpath.Point(x1 - rsintheta, y1 + rcostheta) )
			poly.addPolygon( arc(x1, y1, r, theta + startOffset, theta + endOffset, resolution, fillDensity = False) )
			poly.addPoint( toolpath.Point(x1 + rsintheta, y1 - rcostheta) )
			poly.addPoint( toolpath.Point(x2 + rsintheta, y2 - rcostheta) )
			poly.addPolygon( arc(x2, y2, r, theta - startOffset, theta - endOffset, resolution, fillDensity = False) )
	return poly

def fill(polygon, fillDensity):
	pass

def raster(fileName, originalWidth, originalHeight, svg = False):
	"""Returns polygon for a vectorised raster as a Polygon object.
	Uses external potrace program to convert raster file into polygon(s)
	"""
	poly = toolpath.Polygon()
	if svg:
		os.system("potrace --svg --output " + fileName[ :-3 ] + "svg " + fileName)
	os.system("potrace --alphamax 0 --turdsize 5 --backend gimppath --output " + fileName[ :-3 ] + "gimppath " + fileName)
	os.system("rm " + fileName)
	f = open(fileName[ :-3 ] + "gimppath")
	pathLines = f.readlines()
	f.close()
	os.system("rm " + fileName[ :-3 ] + "gimppath")
	scale = 0.005	# temp - competely arbitary
	# 1 / 200, i.e 1 / (resolution = 20 * 100 for some reason)
	for l in pathLines:
		parts = l.split(' ')
		isPoint = False
		for i, p in enumerate(parts):
			if p == 'TYPE:':
				ptype = int(parts[i + 1])
				isPoint = True
			elif p == 'X:':
				x = float(parts[i + 1]) * scale
			elif p == 'Y:':
				y = float(parts[i + 1]) * scale
		if isPoint:
			poly.addPoint( toolpath.Point(x, y) )
			#print "NEW POINT", x, y, ptype
	# This should not be assumed?
	poly.closed = True

	"""
	#this needs to be done on all paths at same time
	maxX, maxY = 0, 0
	for p in points:
		x, y, t = p
		maxX = max(maxX, x)
		maxY = max(maxY, y)
	print "max", maxX, maxY		
	#print "read", len(points), "points"
	scaleX = originalWidth / maxX
	scaleY = originalHeight / maxY
	print "scales", scaleX, scaleY
	for i in range(len(points)):
		x, y, y = points[i]
		x = x * scaleX
		y = y * scaleY
		points[i] = x, y, t
	"""
	#should make this return a list of all found polygons
	return poly


############# General Maths Functions #############

# Return the coordinates of a point on a circle at theta (rad) with radius.
def _calcCircle(theta, radius):
	x = math.cos( math.radians(theta) ) * radius
	y = math.sin( math.radians(theta) ) * radius
	return x, y

# Return the coordinates of a point on an ellipse at theta (rad) with a and b.
def _calcEllipse(theta, a, b):
	x = math.cos( math.radians(theta) ) * a
	y = math.sin( math.radians(theta) ) * b
	return x, y

# Reverse line (swap x1, y1 and x2, y2)
def _reverseLine( line ):
	x1, y1, x2, y2 = line
	return x2, y2, x1, y1

# Return the angle between the line between two points (2D coordinates) and vetical?
def _angleFromDeltas( dx, dy ):
	radius = math.sqrt( ( dx * dx ) + ( dy * dy ) )
	#if radius != 0:
	dx, dy = dx / radius, dy / radius
	if dx > 0:
		if dy > 0:
			return math.asin(dx)
		elif dy < 0:
			return math.acos(dx) + math.radians(90)
		else:
			#print "moo1"
			return 0
	elif dx < 0:
		if dy > 0:
			return math.asin(dy) + math.radians(270)
		elif dy < 0:
			return math.radians(180) - math.asin(dx)
		else:
			#print "moo2"
			return 0
	else:
		return math.radians(-90)	# i think this should really be 90, it just makes thae program work wen its -90 :)
	#else:
	#	print "Radius cannot be zero!, returning 0 (_angleFromDeltas, shapeplotter.py)"

# Range function accepting floats (by Dinu Gherman)
def _frange(start, end=None, inc=None):
	if end == None:
		end = start + 0.0
		start = 0.0
	if inc == None:
		inc = 1.0
	L = []
	while 1:
		next = start + len(L) * inc
		if inc > 0 and next >= end:
			break
		elif inc < 0 and next <= end:
			break
		L.append(next)
	return L

# Return length of vector
def _calcVectorLength(line):
	x1, y1, x2, y2 = line
	deltaX = max(x1, x2) - min(x1, x2)
	deltaY = max(y1, y2) - min(y1, y2)
	return math.sqrt( math.pow(deltaX, 2) + math.pow(deltaY, 2) )



