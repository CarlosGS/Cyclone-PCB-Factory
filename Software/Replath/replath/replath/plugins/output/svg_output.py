#######################################################################################################################################################
# This module write SVG files                                                                                                                         #
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
#from smil_prefpanel import PreferencesPanel	# change this
import reprap	#remove?

Title = "SVG File"
FileOutput = True
Wildcard = 'SVG files (*.svg)|*.svg'

class output(replath.baseplotters.ExportPlotter):
	# Load plotter preferences
	def loadPreferences(self):
		self.pref_svgScale = 20
		
		self.prefHandler = replath.preferences.PreferenceHandler(self,  "output_svg.conf")
		self.prefHandler.save()  #temp
		self.prefHandler.load()
	
	# Start plot (as new thread)
	def run(self):
		self.alive = True
		self.svg = SVG(self.pref_svgScale)
		self.toolOn = False
		self.startX, self.startY, self.startZ = 0, 0, 0
		
		self.svg.writeFile(self.outputFilename)
		
		if self.alive:
			# Tell gui that plot is complete (redraw screen)
			self.feedbackHandler.plotComplete()
	
	# Translate a cartesian movement into whatever the output plugin does with it (called locally and by toolhead)
	def cartesianMove(self, x, y, z, units = reprap.UNITS_MM):
		print "[svg], cm", x, y, "tool =", self.toolOn
		if self.toolOn:
			self.svg.addLine( self.startX, self.startY, self.startZ, x, y, z )
		self.startX, self.startY, self.startZ = x, y, z


# Class for smil file
class SVG():
	def __init__(self, scale):
		self.scale = scale
		self.lines = []
		self.maxX, self.maxY = 0, 0
	def addLine(self, x1, y1, z1, x2, y2, z2):
		self.lines.append( (x1, y1, z1, x2, y2, z2) )
		print "svg new line", x1, y1, " ->", x2, y2
	
	def generateSVG(self):
		self.svgText = ""
		colour = 'red'
		for l in self.lines:
			x1, y1, z1, x2, y2, z2 = l
			self.svgText += '    <line x1="' + str( int(x1 * self.scale) ) + '" y1="' + str( int(y1 * self.scale) ) + '" x2="' + str( int(x2 * self.scale) ) + '" y2="' + str( int(y2 + self.scale) ) + '" stroke="' + colour + '" />\n'
			self.maxX = max(self.maxX, x1, x2)
			self.maxY = max(self.maxY, y1, y2)
		self.svgText += '  </g>\n</svg>\n'
		self.svgText = '<?xml version="1.0"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n<svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="' +  str(int(self.maxX * self.scale)) + '" width="' + str(int(self.maxY * self.scale)) + '">\n  <g style="fill-opacity:1.0; stroke:black; stroke-width:1;">\n' + self.svgText

	def writeFile(self, fileName):
		self.generateSVG()
		f = open( fileName, 'w' )
		f.write(self.svgText)
		f.close()


