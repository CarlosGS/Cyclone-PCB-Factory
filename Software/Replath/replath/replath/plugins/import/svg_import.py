#######################################################################################################################################################
# This module plots gerber objects to reprap and / or a lineSet object (for pygame plotting). The gerber file is turned into objects in gerber_lib.   #
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

import threading
import reprap.shapeplotter
import replath.baseplotters

import svg_lib as svglib
#from svg_prefpanel import PreferencesPanel

Title = "SVG"
SupportedFileExtensions = ['.svg']
FileTitle = Title + " Files"


# Class to plot gerber file to polygon list
class plotter(replath.baseplotters.ImportPlotter):
	# Load plotter preferences
	def loadPreferences(self):
		pass

	# Run is executed when thread is started (in new thread)
	def run(self):
		self.alive = True
		self.feedbackHandler.setStatus("Opening file...")
		
		# TODO plot here
		
		if self.alive:
			# Tell gui that plot is complete (redraw screen)
			self.feedbackHandler.plotComplete()
	
	def getFileLimitsXY(self):
		minX, minY = 1000000, 1000000
		maxX, maxY = 0, 0
		# Calc limits
		return minX, minY, maxX, maxY
	
	# Tell thread to terminate ASAP (result of GUI 'Stop' button)
	def terminate(self):
		self.alive = False




