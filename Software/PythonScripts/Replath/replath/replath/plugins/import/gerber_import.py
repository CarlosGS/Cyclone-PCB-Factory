#######################################################################################################################################################
# This module plots gerber objects to reprap and / or a lineSet object (for pygame plotting). The gerber file is turned into objects in gerberlib.   #
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

import pygame, math
import replath.preferences
import reprap.shapeplotter as shapeplotter
import replath.baseplotters

import gerber_lib as gerberlib
from gerber_prefpanel import PreferencesPanel
from gerber_prefpanel import PreferencesDialog

Title = "Gerber"
SupportedFileExtensions = ['.pho', '.gbl', '.gtl', '.gbs', '.gts', '.gbo', '.gto', '.gbr', '.gbx', '.phd', '.spl', '.art', '.top', '.bot']
FileTitle = Title + " Files"


# Class to plot gerber file to polygon list
class plotter(replath.baseplotters.ImportPlotter):
	# Load plotter preferences
	def loadPreferences(self):
		# Default preferences
		self.pref_PlotMode = 1
		# Load preferences from file
		self.prefHandler = replath.preferences.PreferenceHandler(self,  "plotter_gerber.conf")
		self.prefHandler.load()
	
	# Run is executed when thread is started (in new thread)
	def run(self):
		self.alive = True
		self.feedbackHandler.setStatus("Opening file...")
		self.gerberFile = gerberlib.gerber(self.fileName)
		
		self.feedbackHandler.setStatus("Removing file offset...")
		# Remove file offset
		minX, minY, maxX, maxY = self.getFileLimitsXY()
		for e in self.gerberFile.flashes + self.gerberFile.traces:
			if e.type == gerberlib.FLASH:
				e.x -= minX
				e.y -= minY
			elif e.type == gerberlib.STROKE:
				e.x1 -= minX
				e.x2 -= minX
				e.y1 -= minY
				e.y2 -= minY
		
		# Fill plot mode ( for pen drawing )	# TODO - apply grouping to this plotter also to remove excess penup ops?
		if self.pref_plotMode == 0:
			# Plotting is pretty simple at the moment, plotter blindly follows gerber file and plots out each trace / flash individually.
			# Can be impoved by re-ordering drawing, and by combining connected traces into continual events / removing overlap
		
			# Plot all gerber flashes
			for i, f in enumerate(self.gerberFile.flashes):
				# Break if thread has been told to termiate
				if not self.alive:
					self.feedbackHandler.aborted()
					break
				progress = int( float(i) / float( len(self.gerberFile.flashes) ) * 100 )
				self.feedbackHandler.setStatus("Plotting flashes..." + str(progress) + "%")
				#f.printFlash()
				# Move is static flash type
				if f.aperture.isMacro: print "macro", f.aperture.macroName
				if f.aperture.apertureType == "C":
					# Using circular aperture
					if self.debug: print "aperture radius", radius, "mm"
					#self.shapePlot.plotCircle( f.x + self.offsetX, f.y + self.offsetY, f.aperture.radius, filled = True, fillDensity = self.fillDensity )
					self.toolpath.currentLayer.polygons.append( shapeplotter.circle( f.x, f.y, f.aperture.radius, self.arcResolution, self.fillDensity ) )
				elif f.aperture.apertureType == "R":
					# Using rectangular aperture
					#self.shapePlot.plotRectangle( f.x + self.offsetX, f.y + self.offsetY, f.aperture.width, f.aperture.height, self.fillDensity )
					self.toolpath.currentLayer.polygons.append( shapeplotter.rectangle( f.x, f.y, f.aperture.width, f.aperture.height, self.fillDensity ) )
				elif f.aperture.apertureType == "O":
					#self.shapePlot.plotEllipse( f.x + self.offsetX, f.y + self.offsetY, f.aperture.width / 2, f.aperture.height / 2, filled = True, fillDensity = self.fillDensity )
					self.toolpath.currentLayer.polygons.append( shapeplotter.ellipse( f.x, f.y, f.aperture.width / 2, f.aperture.height / 2, self.arcResolution, self.fillDensity ) )
			
			# Plot all gerber traces
			for i, t in enumerate(self.gerberFile.traces):
				# Break if thread has been told to termiate
				if not self.alive:
					self.feedbackHandler.aborted()
					break
				progress = int( float(i) / float( len(self.gerberFile.traces) ) * 100 )
				self.feedbackHandler.setStatus("Plotting strokes..." + str(progress) + "%")
				#t.printTrace()
				# Move is aperture open (pen down) type
				if t.aperture.isMacro: print "macro", f.aperture.macroName
				if t.aperture.apertureType == "C":
					# Using circular aperture
					if t.aperture.code == 12 or  t.aperture.code == 13: print  t.aperture.code
					if self.debug: print "aperture radius", t.aperture.radius, "mm"
					#self.shapePlot.plotMoveWithCircle( t.x1 + self.offsetX, t.y1 + self.offsetY, t.x2 + self.offsetX, t.y2 + self.offsetY, t.aperture.radius, self.fillDensity )
					self.toolpath.currentLayer.polygons.append( shapeplotter.circleStroke( t.x1, t.y1, t.x2, t.y2, t.aperture.radius, self.arcResolution, self.fillDensity ) )
				elif t.aperture.apertureType == "R":
					# Using rectangular aperture
					print "TODO - rectangle transition"
		
		# Isolation plot mode ( for routing )
		elif self.pref_plotMode == 1:
			self.pref_rasterResolution = 20.0		# dots per mm
			self.feedbackHandler.setStatus("Getting limits...")
			width = int( (maxX - minX) * self.pref_rasterResolution )
			height = int( (maxY - minY) * self.pref_rasterResolution )
			self.feedbackHandler.setStatus("Primary grouping entities...")
			groups = self.groupTracesPrimary(self.gerberFile.flashes + self.gerberFile.traces)
			self.feedbackHandler.setStatus("Secondary grouping entities...")
			groups = self.groupTracesSecondary(groups) 
			self.feedbackHandler.setStatus("Rastering / Vectorising...")

			self.surfaceFullRender = pygame.Surface( (width, height) )	#problem is background on layers, can we blit black only?
			self.surfaceFullRender.fill( [255, 255, 255] )
			for ig, g in enumerate(groups):
				if not self.alive:
					self.feedbackHandler.aborted()
					break
				progress = int( float(ig) / float( len(groups) ) * 100 )
				self.feedbackHandler.setStatus("Creating Paths..." + str(progress) + "%")
				self.plotToRaster(width, height, 0, 0, self.pref_rasterResolution, "test" + str(ig) + ".bmp", g)
				poly = shapeplotter.raster("test" + str(ig) + ".bmp", width, height)
				self.toolpath.currentLayer.polygons.append(poly)
			pygame.image.save(self.surfaceFullRender, "fullplot.bmp")
			#set_colorkey([255, 255, 255])	# transparency when blitting. use this in plotToRaser, to add to full plot surface TODO
			self.feedbackHandler.setStatus("Plotting...")
		
		# Smart fill mode (for pen)
		elif self.pref_plotMode == 2:
			self.pref_rasterResolution = 20.0		# dots per mm
			self.feedbackHandler.setStatus("Getting limits...")
			width = int( (maxX - minX) * self.pref_rasterResolution )
			height = int( (maxY - minY) * self.pref_rasterResolution )
			self.feedbackHandler.setStatus("Primary grouping entities...")
			groups = self.groupTracesPrimary(self.gerberFile.flashes + self.gerberFile.traces)
			self.feedbackHandler.setStatus("Secondary grouping entities...")
			groups = self.groupTracesSecondary(groups) 
			self.feedbackHandler.setStatus("Rastering / Vectorising...")

			self.surfaceFullRender = pygame.Surface( (width, height) )
			self.surfaceFullRender.fill( [255, 255, 255] )
			for ig, g in enumerate(groups):
				if not self.alive:
					self.feedbackHandler.aborted()
					break
				progress = int( float(ig) / float( len(groups) ) * 100 )
				self.feedbackHandler.setStatus("Creating Paths..." + str(progress) + "%")
				self.plotToRaster(width, height, 0, 0, self.pref_rasterResolution, "test" + str(ig) + ".bmp", g)
				poly = shapeplotter.raster("test" + str(ig) + ".bmp", width, height)
				self.toolpath.currentLayer.polygons.append(poly)
				polyFill = shapeplotter.fill(poly)
				self.toolpath.currentLayer.polygons.append(polyFill)
			self.feedbackHandler.setStatus("Plotting...")
		
		if self.alive:
			# Tell gui that plot is complete (redraw screen)
			self.feedbackHandler.plotComplete()
	
	# Return bounding limits of file (used for zeroing position)
	def getFileLimitsXY(self):
		minX, minY = 1000000, 1000000
		maxX, maxY = -1000000, -1000000
		for f in self.gerberFile.flashes:
			if f.aperture.apertureType == "C":
				leftDist = rightDist = upDist = downDist = f.aperture.radius
			else:
				leftDist = rightDist = upDist = downDist = 0
			
			minX = min(f.x - leftDist, minX)
			minY = min(f.y - downDist, minY)
			maxX = max(f.x + rightDist, maxX)
			maxY = max(f.y + upDist, maxY)
			
		for f in self.gerberFile.traces:
			if f.aperture.apertureType == "C":
				leftDist = rightDist = upDist = downDist = f.aperture.radius
			else:
				leftDist = rightDist = upDist = downDist = 0
			
			minX = min(f.x1 - leftDist, f.x2 - leftDist, minX)
			minY = min(f.y1 - downDist, f.y2 - downDist, minY)
			maxX = max(f.x1 + rightDist, f.x2 + rightDist, maxX)
			maxY = max(f.y1 + upDist, f.y2 + upDist, maxY)
		
		return minX, minY, maxX, maxY
	
	# Group a  list of entities (flashes and traces) into groups (lists) when they share common points
	def groupTracesPrimary(self, entList):
		groupList = []
		# Start with each entity in its own group
		for e in entList:
			groupList.append([e])
		groupMerges = []
		# Compare every entity to every other in all pairs of groups (all groups with all others). Make a list of all groups that have at least one common point (electrical connection)
		for iA, groupA in enumerate(groupList):
			progress = int( float(iA) / float( len(groupList) ) * 100 )
			self.feedbackHandler.setStatus("Primary grouping entities..." + str(progress) + "%")
			for iB, groupB in enumerate(groupList):
				for eA in groupA:
					for eB in groupB:
						if eA != eB and self.entsConnected(eA, eB):
							groupMerges.append( (iA, iB) )
	
		# Merge the groups with common connections
		for a, b in groupMerges:
			groupList[a] += groupList[b]
			groupList[b] = []
		# Remove old groups
		for i in range( groupList.count([]) ):
			groupList.remove([])
		return groupList

	# Secondary regrouping - will use raster comparison between groups to find ouverlaps TODO
	def groupTracesSecondary(self, groupList):
		#newGroupList = []
		newGroupList = groupList	# Temporary passthrough
		return newGroupList

	# If two enties are connected return true, otherwise false
	def entsConnected(self, e1, e2):
		if e1.type == gerberlib.FLASH and e2.type == gerberlib.FLASH:
			# This should not happen so return false anyway (saves some processing)
			return False
		elif e1.type == gerberlib.FLASH and e2.type == gerberlib.STROKE:
			return self.strokeFlashConnected(e2, e1)
		elif e1.type == gerberlib.STROKE and e2.type == gerberlib.FLASH:
			return self.strokeFlashConnected(e1, e2)
		elif e1.type == gerberlib.STROKE and e2.type == gerberlib.STROKE:
			return self.strokesConneted(e1, e2)
	
	# Return true if two strokes are connected
	def strokesConneted(self, s1, s2):
		if (s1.x1 == s2.x1 and s1.y1 == s2.y1) or (s1.x2 == s2.x1 and s1.y2 == s2.y1) or (s1.x1 == s2.x2 and s1.y1 == s2.y2) or (s1.x2 == s2.x2 and s1.y2 == s2.y2):
			return True
		return False
	
	# Return two if a stroke and flash are connected
	def strokeFlashConnected(self, s, f):
		if (s.x1 == f.x and s.y1 == f.y) or (s.x2 == f.x and s.y2 == f.y):
			return True
		return False
	
	# Plot a set of entities to bitmap
	def plotToRaster(self, width, height, offsetX, offsetY, scale, fileName, entities):
		surface = pygame.Surface( (width, height) )
		surface.fill( [255, 255, 255] )
		for e in entities:
			if e.type == gerberlib.FLASH:
				if e.aperture.isMacro: print "macro", e.aperture.macroName
				if e.aperture.apertureType == "C":
					# Using circular aperture
					x1, y1 = int( (e.x + offsetX) * scale ), int( (e.y + offsetY) * scale )
					r = int(e.aperture.radius * scale)
					pygame.draw.circle( surface, [0, 0, 0], ( x1, y1 ), r, 0 )
					pygame.draw.circle( self.surfaceFullRender, [0, 0, 0], ( x1, y1 ), r, 0 )
				elif e.aperture.apertureType == "R":
					# Using rectangular aperture
					x1, y1 = int( ( e.x + offsetX - (e.aperture.width / 2) ) * scale ), int( ( e.y + offsetY - (e.aperture.height / 2) ) * scale )
					pygame.draw.rect( surface, [0, 0, 0], (x1, y1, e.aperture.width * scale, e.aperture.height * scale), 0 )
					pygame.draw.rect( self.surfaceFullRender, [0, 0, 0], (x1, y1, e.aperture.width * scale, e.aperture.height * scale), 0 )
				elif e.aperture.apertureType == "O":
					# Using ellipse aperture
					pygame.draw.ellipse( surface, [0, 0, 0], (e.x + offsetX, e.y + offsetY, e.aperture.width / 2, e.aperture.height / 2), 0)	#TODO - check and finish
					pygame.draw.ellipse( self.surfaceFullRender, [0, 0, 0], (e.x + offsetX, e.y + offsetY, e.aperture.width / 2, e.aperture.height / 2), 0)	#TODO - check and finish
				else:
					print "E unknowsn"
			elif e.type == gerberlib.STROKE:
				if e.aperture.apertureType == "C":
					x1, y1 = int( e.x1 * scale ), int( e.y1 * scale )
					x2, y2 = int( e.x2 * scale ), int( e.y2 * scale )
					r = int(e.aperture.radius * scale)
					pygame.draw.circle( surface, [0, 0, 0], (x1, y1), r, 0 )	#temp inversion of y
					pygame.draw.circle( surface, [0, 0, 0], (x2, y2), r, 0 )	#temp inversion of y
					self.drawPolyLine( surface, [0, 0, 0], (x1, y1), (x2, y2), r * 2 )	# Allows variable line thickness depending on line angle (makes it consistant)
					# temp solution full render
					pygame.draw.circle( self.surfaceFullRender, [0, 0, 0], (x1, y1), r, 0 )	#temp inversion of y
					pygame.draw.circle( self.surfaceFullRender, [0, 0, 0], (x2, y2), r, 0 )	#temp inversion of y
					self.drawPolyLine( self.surfaceFullRender, [0, 0, 0], (x1, y1), (x2, y2), r * 2 )	# Allows variable line thickness depending on line angle (makes it consistant)
					
				else:
					print "E unknowns"
			else:
				print "E unnnknknk"
		pygame.image.save(surface, fileName)
		#self.surfaceFullRender.blit(surface, (0, 0))
	
	# Draw a line with consisant thickness
	def drawPolyLine(self, surface, colour, pointA, pointB, width):
		x1, y1 = pointA
		x2, y2 = pointB
		if x1 == x2:
			x = width / 2
			y = 0
		elif y1 == y2:
			x = 0
			y = width / 2
		else:
			theta = angleFromDeltas( x2 - x1, y2 - y1)
			x, y = calcCircle(theta, width / 2)
		xa, ya = x1 + x, y1 - y
		xb, yb = x1 - x, y1 + y
		xc, yc = x2 - x, y2 + y
		xd, yd = x2 + x, y2 - y
		pygame.draw.polygon( surface, colour, [(xa, ya), (xb, yb), (xc, yc), (xd, yd)], 0 )


#### Maths functions ####

# Return the coordinates of a point on a circle at theta (rad) with radius.
def calcCircle(theta, radius):
	x = math.cos( math.radians(theta) ) * radius
	y = math.sin( math.radians(theta) ) * radius
	return x, y
	
# Return the angle between the line between two points (2D coordinates) and vetical?
def angleFromDeltas( dx, dy ):
	radius = math.sqrt( ( dx * dx ) + ( dy * dy ) )
	#if radius != 0:
	dx, dy = dx / radius, dy / radius
	if dx > 0:
		if dy > 0:
			return math.asin(dx)
		elif dy < 0:
			return math.acos(dx) + math.radians(90)
		else:
			return 0
	elif dx < 0:
		if dy > 0:
			return math.asin(dy) + math.radians(270)
		elif dy < 0:
			return math.radians(180) - math.asin(dx)
		else:
			return 0
	else:
		return math.radians(-90)	# i think this should really be 90, it just makes thae program work wen its -90 :)
	#else:
	#	print "Radius cannot be zero!, returning 0 (angleFromDeltas, shapeplotter.py)"


# Def not a full calculation - only does two quadrants but this is ok for choosing line width as a line rotated 180 is the same line
def calcLineAngle(x1, y1, x2, y2):
	dx = max(x1, x2) - min(x1, x2)
	dy = max(y1, y2) - min(y1, y2)
	if dx != 0:
		return math.atan(dy / dx)
	else:
		return math.radians(90)


