import reprap, replath.preferences, replath.baseplotters
from pen_prefpanel import PreferencesPanel

Title = "Paint Brush"

class tool(replath.baseplotters.Tool):
	def loadPreferences(self):
		# Default preferences
		self.pref_toolDownPos = 15
		self.pref_toolUpPos = 5
		self.pref_dippotX = 10
		self.pref_dippotY = 10
		self.pref_dippotZ = 15
		self.pref_strokesPerDip = 3
		# Load preferences from file
		self.prefHandler = replath.preferences.PreferenceHandler(self,  "toolhead_pen.conf")
		self.prefHandler.load()
	
	def prepare(self):
		self.strokesSinceDip = 0
	
	def idle(self):
		pass
		
	def ready(self):
		# Need to do distance traveled instead really, as a circle may have 100s of lines in.
		if self.strokesSinceDip >= self.pref_strokesPerDip:
			# Brush dip routine
			self.output.cartesianMove(None, None, self.pref_toolUpPos, units = reprap.UNITS_MM)
			self.output.cartesianMove(self.pref_dippotX, self.pref_dippotY, None, units = reprap.UNITS_MM)
			self.output.cartesianMove(None, None, self.pref_dippotZ, units = reprap.UNITS_MM)
			self.output.cartesianMove(None, None, self.pref_toolUpPos, units = reprap.UNITS_MM)
		else:
			self.strokesSinceDip += 1
	
	def start(self):
		if not self.toolInUse:
			self.toolInUse = True
			self.output.cartesianMove(None, None, self.pref_toolDownPos, units = reprap.UNITS_MM)
	
	def stop(self):
		if self.toolInUse:
			self.toolInUse = False
			self.output.cartesianMove(None, None, self.pref_toolUpPos, units = reprap.UNITS_MM)



