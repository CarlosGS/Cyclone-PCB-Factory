import reprap, replath.preferences, replath.baseplotters
#from router_prefpanel import PreferencesPanel

Title = "Router"

class tool(replath.baseplotters.Tool):
	def loadPreferences(self):
		# Default preferences
		self.pref_toolDownPos = 0
		self.pref_toolUpPos = 0
		# Load preferences from file
		self.prefHandler = replath.preferences.PreferenceHandler(self,  "toolhead_router.conf")
		self.prefHandler.load()
	
	def prepare(self):
		pass
		# Switch on motor here TODO
	
	def idle(self):
		pass
		# Switch off motor here TODO
	
	def ready(self):
		pass
	
	def start(self):
		if not self.toolInUse:
			self.toolInUse = True
			self.output.cartesianMove(None, None, self.pref_toolDownPos, units = reprap.UNITS_STEPS)
	
	def stop(self):
		if self.toolInUse:
			self.toolInUse = False
			self.output.cartesianMove(None, None, self.pref_toolUpPos, units = reprap.UNITS_STEPS)



