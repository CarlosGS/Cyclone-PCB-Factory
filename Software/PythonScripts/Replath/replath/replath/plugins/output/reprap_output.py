#!/usr/bin/env python

import threading, reprap, replath.preferences
from reprap_prefpanel import PreferencesPanel

Title = "Serial SNAP RepRap"
FileOutput = False

class output(replath.baseplotters.ExportPlotter):
	# Load plotter preferences
	def loadPreferences(self):
		# Default preferences
		self.pref_stepsPerMillimeterX, self.pref_stepsPerMillimeterY, self.pref_stepsPerMillimeterZ = 30, 30, 30
		self.pref_limitX, self.pref_limitY = 0, 0
		self.pref_enableLimit = False
		self.pref_torque = 65
		self.pref_speed = 180
		self.pref_serialPort = 0
		self.pref_baudRate = 19200
		self.pref_timeout = 60
		
		# Load preferences from file
		self.prefHandler = replath.preferences.PreferenceHandler(self,  "output_reprap.conf")
		self.prefHandler.load()
	
	# Start plot (as new thread)
	def run(self):
		self.alive = True
		
		self.feedbackHandler.setStatus("Configuring RepRap...")
		if self.pref_enableLimit:
			reprap.cartesian.x.limit = self.pref_limitX
			reprap.cartesian.y.limit = self.pref_limitY
		else:
			reprap.cartesian.x.limit = 0
			reprap.cartesian.y.limit = 0
		
		
		
		try:
			# Initialise serial port.
			reprap.openSerial( self.pref_serialPort, self.pref_baudRate, self.pref_timeout )
		except reprap._RepRapError:
			self.feedbackHandler.showMessagePopup("You do not have the required permissions to access the serial port.\nTry granting your user permissions (recommended) or run as root (less recommended).")
			self.alive = False
			self.feedbackHandler.aborted()
		
		if self.alive:
			# Prepare reprap for use
			reprap.cartesian.x.active = True
			reprap.cartesian.y.active = True
			reprap.cartesian.z.active = True
			reprap.cartesian.x.setNotify()
			reprap.cartesian.y.setNotify()
			reprap.cartesian.z.setNotify()
			reprap.cartesian.setSpeed(self.pref_speed)
			reprap.cartesian.setPower(self.pref_torque)
			self.feedbackHandler.setStatus("Reseting axies...")
			reprap.cartesian.homeReset()
		
			self.toolhead.prepare()
			self.feedbackHandler.setStatus("Starting plot...")
		
			# Start plot
			for layer in self.toolpath.layers:
				reprap.cartesian.homeReset()
				self.curX, self.curY =  0, 0
				for ip, polygon in enumerate(layer.polygons):
					if not self.alive:
						self.feedbackHandler.aborted()
						break
					progress = int( float(ip) / float( len(layer.polygons) ) * 100 )
					self.feedbackHandler.setStatus("Plotting polygons..." + str(progress) + "%")
					self.toolhead.ready()
					x1, y1 = polygon.points[0].x + self.toolpath.offsetX, polygon.points[0].y + self.toolpath.offsetY
					#x2, y2 = reprap.cartesian.x.getPos(), reprap.cartesian.y.getPos()
					# If we are not in the polygon start place, switch off tool and move there
					if (x1 != self.curX) or (y1 != self.curY):
						self.toolhead.stop()
						self.cartesianMove(x1, y1, None)
					# Start tool
					self.toolhead.start()
					polygon.pointsPlotted = 0
					# Plot polygon
					for p in polygon.points[ 1: ]:
						if not self.alive:
							self.feedbackHandler.aborted()
							break
						x2, y2 = p.x + self.toolpath.offsetX, p.y + self.toolpath.offsetY
						# If we need to move somwhere, do it
						if (x1 != x2) or (y1 != y2):
							self.cartesianMove(x2, y2, None)
						polygon.pointsPlotted += 1
					#x1, y1 = x2, y2
		
			self.toolhead.stop()
			self.toolhead.idle()
			reprap.cartesian.homeReset()
			reprap.cartesian.free()
			reprap.closeSerial()
		
		if self.alive:
			# Tell gui that plot is complete (redraw screen)
			self.feedbackHandler.plotComplete()
	
	
	# Translate a cartesian movement into whatever the output plugin does with it (called locally and by toolhead)
	def cartesianMove(self, x, y, z, units = reprap.UNITS_MM):
		#print "cm", x, y, z
		if units == reprap.UNITS_MM:
			if x != None:
				self.curX = x
				x = int(x * self.pref_stepsPerMillimeterX)
			if y != None:
				self.curY = y
				y = int(y * self.pref_stepsPerMillimeterY)
			if z != None:
				self.curZ = z
				z = int(z * self.pref_stepsPerMillimeterZ)
		reprap.cartesian.seek( (x, y, z), waitArrival = True )





