import reprap, replath.preferences, replath.baseplotters
from pen_prefpanel import PreferencesPanel

Title = "Pen"

class tool(replath.baseplotters.Tool):
	def loadPreferences(self):
		# Default preferences
		self.pref_penDownPos = 0
		self.pref_penUpPos = 0
		# Load preferences from file
		self.prefHandler = replath.preferences.PreferenceHandler(self,  "toolhead_pen.conf")
		self.prefHandler.load()
	
	def prepare(self):
		pass
	
	def idle(self):
		pass
	
	def ready(self):
		pass
	
	def start(self):
		if not self.toolInUse:
			self.toolInUse = True
			self.output.cartesianMove(None, None, self.pref_penDownPos, units = reprap.UNITS_STEPS)
	
	def stop(self):
		if self.toolInUse:
			self.toolInUse = False
			self.output.cartesianMove(None, None, self.pref_penUpPos, units = reprap.UNITS_STEPS)



