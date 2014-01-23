"""
RepRap plugins system. All plugins are accessed though this module.
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

import os, sys

# All modules used by plugins must be imported here to ensure inclusion in py2exe build
import replath.preferences, replath.baseplotters, wx.wizard

PLUGIN_IMPORT	= 1
PLUGIN_OUTPUT	= 2
PLUGIN_TOOLHEAD	= 3
#print "OSP='" + sys.platform + "'"

if sys.platform == "win32":
	# Windows
	print "winp"
	pluginsPath = os.path.join( os.getcwd(), "plugins" )
else:
	# Linux
	pluginsPath = "/usr/local/share/replath/plugins"

print "Plugins loading from path'" + pluginsPath + "'"

pluginsFolders = {PLUGIN_IMPORT:"import", PLUGIN_OUTPUT:"output", PLUGIN_TOOLHEAD:"toolhead"}

def loadPlugins(pluginsFolder, suffix):
	oldDir = os.getcwd()
	os.chdir(pluginsFolder)
	sys.path.append(pluginsFolder)
	plugins = []
	files = os.listdir(pluginsFolder)
	for p in files:
		if p[ -len(suffix): ] ==  suffix:
			newPlugin =  __import__( p[ :-3 ] ) 
			plugins.append(newPlugin)
			print "Loading plugin '" + newPlugin.Title + "' from file '" + p + "'"
	os.chdir(oldDir)
	sys.path.remove(pluginsFolder)
	return plugins

"""
def getPluginsList(pluginType):
	plugins = loadPlugins( os.path.join( pluginsPath, pluginsFolders[pluginType] ), "_" + pluginsFolders[pluginType] + ".py")
	pluginList = []
	for p in plugins:
		pluginList.append(p.Title)
	return pluginList
"""

def getPlugin(pluginType, index):
	plugins = loadPlugins( os.path.join( pluginsPath, pluginsFolders[pluginType] ), "_" + pluginsFolders[pluginType] + ".py")
	return plugins[index]

def getPlugins(pluginType):
	return loadPlugins( os.path.join( pluginsPath, pluginsFolders[pluginType] ), "_" + pluginsFolders[pluginType] + ".py")
	
def listTitles(plugins):
	pluginList = []
	for p in plugins:
		pluginList.append(p.Title)
	return pluginList
