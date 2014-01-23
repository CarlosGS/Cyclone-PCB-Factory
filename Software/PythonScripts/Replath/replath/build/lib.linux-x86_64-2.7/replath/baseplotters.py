"""
Base classes for import, export and toolhead plugins
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

import threading, reprap

class ImportPlotter(threading.Thread):
	"""Base class for import plotter plugins"""
	def __init__(	self, fileName,	toolpath,
					feedbackHandler = False,
					arcResolution = False,
					fillDensity = 4,
					debug = False ):
		"""Create plotter plugin with filename, toolpath (reprap.toolpath.Object object), feedback handler (feedback handler object), fill density (lines / mm) and debug"""
		
		threading.Thread.__init__(self)
		
		self.fileName = fileName
		self.toolpath = toolpath
		self.feedbackHandler = feedbackHandler
		self.arcResolution = arcResolution
		self.fillDensity = fillDensity
		self.debug = debug
		
		self.loadPreferences()
	
	def terminate(self):
		"""Tell thread to terminate ASAP (result of GUI 'Stop' button)"""
		self.alive = False
	
	def run(self):
		"""Run is executed when thread is started (in new thread)
		This should be defined in derived plugin class"""
		raise NotImplementedError('Import plotter plugin must define a .run() method!')
	
	def getFileLimitsXY(self):
		"""Return bounding limits of file (used for zeroing position)
		This should be defined in derived plugin class"""
		raise NotImplementedError('Import plotter plugin must define a .getFileLimitsXY() method!')

	def loadPreferences(self):
		"""Load preferences from file
		This should be defined in derived plugin class"""
		raise NotImplementedError('Import plotter plugin must define a .loadPreferences() method!')


class ExportPlotter(threading.Thread):
	"""Base class for export plotter plugins"""
	def __init__(	self, toolpath, toolhead,
					feedbackHandler = False,
					outputFilename = False):
		"""Create output plotter plugin with toolpath (reprap.toolpath.Object object), toolhead (toolhead plugin object), feedback handler (feedback handler object) and output file name"""
		
		threading.Thread.__init__(self)
		
		self.toolpath = toolpath
		self.feedbackHandler = feedbackHandler
		self.toolhead = toolhead
		self.toolhead.output = self
		self.outputFilename = outputFilename
		
		self.loadPreferences()
	
	def terminate(self):
		"""Tell thread to terminate ASAP (result of GUI 'Stop' button)"""
		self.alive = False
		if dir(self).count("feedbackHandler"):
			self.feedbackHandler.setStatus("Aborting plot...")
	
	def run(self):
		"""Run is executed when thread is started (in new thread)
		This should be defined in derived plugin class"""
		raise NotImplementedError('Export plotter plugin must define a .run() method!')
	
	def cartesianMove(self, x, y, z, units = reprap.UNITS_MM):
		"""Perform cartesian movement
		This should be defined in derived plugin class"""
		raise NotImplementedError('Export plotter plugin must define a .cartesianMove() method!')

	def loadPreferences(self):
		"""Load preferences from file
		This should be defined in derived plugin class"""
		raise NotImplementedError('Export plotter plugin must define a .loadPreferences() method!')


class Tool:
	"""Base class for tool plugins"""
	def __init__(self):
		"""Create tool object"""
		self.loadPreferences()
		self.toolInUse = False
	
	def prepare(self):
		"""Switch on tool / prepare for use (e.g. switch on cutter)
		This should be defined in derived plugin class"""
		raise NotImplementedError('Toolhead plugin must define a .prepare() method!')
	
	def idle(self):
		"""Switch off tool (e.g. switch off cutter)
		This should be defined in derived plugin class"""
		raise NotImplementedError('Toolhead plugin must define a .idle() method!')
	
	def ready(self):
		"""Tool use about to start, make sure it is ready (e.g. dip paintbrush)
		This should be defined in derived plugin class"""
		raise NotImplementedError('Toolhead plugin must define a .ready() method!')
	
	def start(self):
		"""Start tool use (e.g. lower cutter)
		This should be defined in derived plugin class"""
		raise NotImplementedError('Toolhead plugin must define a .start() method!')
	
	def stop(self):
		"""End tool use (e.g. raise cutter)
		This should be defined in derived plugin class"""
		raise NotImplementedError('Toolhead plugin must define a .stop() method!')




