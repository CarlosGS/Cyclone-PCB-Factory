"""
This module provides a pyGame surface as a wxPython object.
I.e. it lets you use pyGame within a wx frame.

Code derived / inspired from a vague combination of :

BufferedCanvas -- Double-buffered, flicker-free canvas widget
Copyright (C) 2005, 2006 Daniel Keep
(GNU Lesser General Public License)

and

wxPython wiki : http://wiki.wxpython.org/IntegratingPyGame (Assumed GNU compatible)

and some work of my own.


Example :

import wxpygame
class DrawCanvas(wxpygame.wxSDLPanel):
	def __init__( self, parent, ID=-1 ):
		wxpygame.wxSDLPanel.__init__( self, parent,ID )
	
	def draw(self):
		surface = self.getSurface()
		if not surface is None:
			pygame.draw.circle( surface, (250, 0, 0), (100, 100), 50 )
			pygame.display.flip()

"""

# Python module properties
__author__ = "Stefan Blanke (greenarrow) (greenarrow@users.sourceforge.net)"
__license__ = "GPL 3.0"
__credits__ = "Daniel Keep for his wx BufferedCanvas that showed me how to make a pyGame wx canvas"
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

import wx, pygame, os, sys

class wxSDLPanel(wx.Panel):
	buffer = None
	backbuffer = None
	def __init__(self, parent, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_FULL_REPAINT_ON_RESIZE):
		wx.Panel.__init__(self,parent,ID,pos,size,style)
		self.initialized = False
		self.resized = False
		self._surface = None
		self.needsDrawing = True
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_MOTION, self.MouseMove)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
		self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
		self.Bind(wx.EVT_IDLE, self.OnIdle)

	def OnIdle(self, ev):
		if not self.initialized or self.resized:
			if not self.initialized:
				# get the handle
				hwnd = self.GetHandle()
				
				os.environ['SDL_WINDOWID'] = str(hwnd)
				if sys.platform == 'win32':
					os.environ['SDL_VIDEODRIVER'] = 'windib'
				
				pygame.init()
				
				
				self.initialized = True
			else:
				self.resized = False
			x,y = self.GetSizeTuple()
			self._surface = pygame.display.set_mode((x,y))
		
		if self.needsDrawing:
			self.draw()
		
		"""for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				pygame.quit()
				sys.exit()
			elif (event.type == pygame.MOUSEMOTION):
				self.MouseMove()
			elif (event.type == pygame.MOUSEBUTTONDOWN):
				print "md pygame"
				self.OnMouseDown()
			elif (event.type == pygame.MOUSEBUTTONUP):
				self.OnMouseUp()
		"""

	def OnPaint(self, ev):
		self.needsDrawing = True

	def OnSize(self, ev):
		self.resized = True

	def draw(self):
		raise NotImplementedError('please define a .draw() method!')

	def getSurface(self):
		return self._surface
		
	def update(self):
		self.Refresh()
		print "r"
		
	#def getSize(self):
	#	return self.w, self.h
		
	def MouseMove(self, event):
		raise NotImplementedError('please define a .MouseMove() method!')  
	def OnMouseDown(self, event):
		raise NotImplementedError('please define a .OnMouseDown() method!')  
	def OnMouseUp(self, event):
		raise NotImplementedError('please define a .OnMouseUp() method!')  
	def OnMouseWheel(self, event):
		raise NotImplementedError('please define a .OnMouseWheel() method!')  
	

#pygame.display.quit()




