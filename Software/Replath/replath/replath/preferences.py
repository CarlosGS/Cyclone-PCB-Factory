"""
RepRap preferences system. All preferences are accessed though this module.
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

import sys, os

def getHomeDir():
	if sys.platform=="win32":
		return os.path.join( os.environ.get("USERPROFILE"), "Application Data" )
	else:
		return os.environ.get("HOME")


class PreferenceHandler:
	# prefOwner is object from which '.pref_*' attributes will be written to / read from
	def __init__(self, prefOwner, fileName):
		if prefOwner:
			self.owner = prefOwner
		else:
			self.owner = self
		self.fileName = os.path.join( getHomeDir(), ".pyRepRap", fileName )

	# Save preferences to file
	def save(self):
		fileText = ""
		for a in dir(self.owner):
			if a[ :5 ] == "pref_":
				#print "Preference", a, "=", getattr(self.owner, a)
				attr = getattr(self.owner, a)													# Get attribute (object)
				fileText += a + '\t' + str( attr ) + '\t' + str( type(attr) )[ 7:-2 ] + '\n'	# Output line format: [Pref name]  [Pref Value]  [Pref Type]

		f = open(self.fileName, 'w')
		f.write(fileText)
		f.close()

	# Load preferences from file
	def load(self):
		if not os.path.exists(self.fileName):
			print "Preference file '" + self.fileName + "' does not exist, creating"
			# If preferences directory does not exist then create it
			dirPath = os.path.join( getHomeDir(), ".pyRepRap" )
			if not os.path.exists(dirPath):
				os.mkdir(dirPath)
			self.save()
		
		f = open(self.fileName, 'r')
		lines = f.read().split('\n')
		for r in lines:
			if len(r) > 0 and not r[ :1 ] == "#":			# Check line is not blank or commented out
				pref, val, dType = tuple( r.split('\t') )
				if dType == "int":
					val = int(val)
				elif dType == "float":
					val = float(val)
				elif dType == "long":
					val = long(val)
				elif dType == "bool":
					if val == "True":
						val = True
					else:
						val = False
				setattr(self.owner, pref, val)

