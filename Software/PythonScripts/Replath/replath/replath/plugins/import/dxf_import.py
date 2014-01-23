#######################################################################################################################################################
# This module plots dxf entities to reprap and / or a lineSet object (for pygame plotting). The dxf file is turned into entities in dxflib.           #
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

import math, threading
import replath.preferences
import reprap.shapeplotter as shapeplotter
import replath.baseplotters

import dxf_lib as dxflib
#from dxf_prefpanel import PreferencesPanel

Title = "DXF Cad"
SupportedFileExtensions = ['.dxf']
FileTitle = Title + " Files"


# Class to plot dxf files to polygon list
class plotter(replath.baseplotters.ImportPlotter):
	# Load plotter preferences
	def loadPreferences(self):
		# Load preferences from file
		self.prefHandler = replath.preferences.PreferenceHandler(self,  "plotter_dxf.conf")
		self.prefHandler.load()
	
	# Run is executed when thread is started (in new thread)
	def run(self):
		self.alive = True
		
		self.feedbackHandler.setStatus("Opening file...")
		self.dxfFile = dxflib.dxf( self.fileName )
		#self.dxfFile.printEnts()
		
		self.feedbackHandler.setStatus("Removing file offset...")
		# Remove file offset
		minX, minY, maxX, maxY = self.getFileLimitsXY()
		print "dxf m&ms", minX, minY, maxX, maxY
		for e in self.dxfFile.entities:
			if e.type == "LINE":
				e.startX -= minX
				e.startY -= minY
				e.endX -= minX
				e.endY -= minY
			elif e.type == "CIRCLE" or e.type == "ARC":
				e.centreX -= minX
				e.centreY -= minY
		
		# Start plot of entities
		for i, e in enumerate(self.dxfFile.entities):
			progress = int( float(i) / float( len(self.dxfFile.entities) ) * 100 )
			self.feedbackHandler.setStatus("Drawing entities..." + str(progress) + "%")
			# Break if thread has been told to termiate
			if not self.alive:
				self.feedbackHandler.aborted()
				break
			if e.type == "LINE":
				self.toolpath.currentLayer.polygons.append( shapeplotter.line( (e.startX, e.startY, e.endX, e.endY) ) )
				print "line makes", shapeplotter.line( (e.startX, e.startY, e.endX, e.endY) ), len(shapeplotter.line( (e.startX, e.startY, e.endX, e.endY) ).points)
			elif e.type == "CIRCLE":
				self.toolpath.currentLayer.polygons.append( shapeplotter.circle( e.centreX, e.centreY, e.radius, self.arcResolution ) )
			elif e.type == "ARC":
				self.toolpath.currentLayer.polygons.append( shapeplotter.arc( e.centreX, e.centreY, e.radius, math.radians(e.startAngle), math.radians(e.endAngle), resolution = self.arcResolution ) )
		
		if self.alive:
			# Tell gui that plot is complete (redraw screen)
			self.feedbackHandler.plotComplete()
	
	# Return bounding limits of file (used for zeroing position)
	def getFileLimitsXY(self):
		minX, minY = 1000000, 1000000
		maxX, maxY = -1000000, -1000000
		for e in self.dxfFile.entities:
			if e.type == "LINE":
				minX = min(minX, e.startX, e.endX)
				minY = min(minY, e.startY, e.endY)
				maxX = max(maxX, e.startX, e.endX)
				maxY = max(maxY, e.startY, e.endY)
			elif e.type == "CIRCLE" or e.type == "ARC":
				minX = min(minX, e.centreX - e.radius)
				minY = min(minY, e.centreY - e.radius)
				maxX = max(maxX, e.centreX + e.radius)
				maxY = max(maxY, e.centreY + e.radius)
		
		return minX, minY, maxX, maxY
	
	# Tell thread to terminate ASAP (result of GUI 'Stop' button)
	def terminate(self):
		self.alive = False


