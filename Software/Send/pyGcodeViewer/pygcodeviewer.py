#!/usr/bin/python
# coding: UTF-8

import wx
from string import *
from math import *
#from struct import *
import os
import sys
#import datetime
import locale
import re
#import time
#Global Constant
HUGE = 1e10
TINY = 1e-6
#MERGINE = 1e-6
INCH = 25.4 #mm
MIL = INCH/1000
WINDOW_X = 800
WINDOW_Y = 600
CENTER_X=200.0
CENTER_Y=200.0

#For file
IN_INCH_FLAG = 0
GCODE_EXT = '*.gcode'

#View
DEF_COLOR = 'BLACK'	#black

#Global variable
gXMIN = HUGE
gXMAX = -HUGE
gYMIN = HUGE
gYMAX = -HUGE
gZMIN = HUGE
gZMAX = -HUGE
gXSHIFT = 0
gYSHIFT = 0
gGCODE_DATA = ""
gGCODES = []
gUNIT = 1

#For Drawing 
gTHETA = pi/4.0
gPHI = pi/4.0
gPSI = 0.0
gVIEW_POINT = 0
gPATTERNS = []
gDRAWCONTOUR = []
gMAG = 1.0
gPRE_X = CENTER_X
gPRE_Y = CENTER_X
gMAG_MIN = 0.1
gMAG_MAX = 500.0
gDRAW_XSHIFT = 0.0
gDRAW_YSHIFT = 0.0
gDRAW_ZSHIFT = 0.0
gCENTER_X = 0.0
gCENTER_Y = 0.0
gCENTER_Z = 0.0
gDISP_GERBER = 1
gDISP_DRILL = 0
gDISP_EDGE = 0
gDISP_CONTOUR = 0

gMOVE_COLOR = 'BLUE'

gCOLORS = [
'AQUAMARINE','BLACK','BLUE','BLUE VIOLET','BROWN',
'CADET BLUE','CORAL','CORNFLOWER BLUE','CYAN','DARK GREY',
'DARK GREEN', 'DARK OLIVE GREEN', 'DARK ORCHID', 'DARK SLATE BLUE', 'DARK SLATE GREY',
'DARK TURQUOISE', 'DIM GREY', 'FIREBRICK', 'FOREST GREEN', 'GOLD',
'GOLDENROD', 'GREY', 'GREEN', 'GREEN YELLOW', 'INDIAN RED',
'KHAKI', 'LIGHT BLUE', 'LIGHT GREY', 'LIGHT STEEL BLUE', 'LIME GREEN',
'MAGENTA', 'MAROON', 'MEDIUM AQUAMARINE', 'MEDIUM BLUE', 'MEDIUM FOREST GREEN',
'MEDIUM GOLDENROD', 'MEDIUM ORCHID', 'MEDIUM SEA GREEN', 'MEDIUM SLATE BLUE', 'MEDIUM SPRING GREEN',
'MEDIUM TURQUOISE', 'MEDIUM VIOLET RED', 'MIDNIGHT BLUE', 'NAVY', 'ORANGE',
'ORANGE RED', 'ORCHID', 'PALE GREEN', 'PINK', 'PLUM',
'PURPLE', 'RED', 'SALMON', 'SEA GREEN', 'SIENNA',
'SKY BLUE', 'SLATE BLUE', 'SPRING GREEN', 'STEEL BLUE', 'TAN',
'THISTLE ', 'TURQUOISE', 'VIOLET', 'VIOLET RED', 'WHEAT',
'WHITE', 'YELLOW', 'YELLOW GREEN'
]

gMouseLeftDown = [0]*3
gMouseRightDown = [0]*3

#Window
class MainFrame(wx.Frame):
	def __init__(self, parent, id, title):
		global WINDOW_X, WINDOW_Y, gVIEW_POINT
		wx.Frame.__init__(self, parent, id, title, size=(WINDOW_X, WINDOW_Y))
		# Setting up the menu.
		filemenu= wx.Menu()
		menuOpen = filemenu.Append(wx.ID_OPEN,"&Open"," Open files")
		menuReload = filemenu.Append(wx.ID_REVERT,"&Reload"," Reload files")
		menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
		#setupmenu =  wx.Menu()
		#menuMachine = setupmenu.Append(wx.ID_SETUP,"&Machine setup"," Setup Machine")
		#menuConv = setupmenu.Append(wx.ID_VIEW_LIST,"&Convert setup"," Convert setup")
		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
		#menuBar.Append(setupmenu,"&Setup") # Adding the "filemenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

		#Event for Menu bar
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnReload, menuReload)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		#self.Bind(wx.EVT_MENU, self.OnConvSet, menuConv)
		#self.Bind(wx.EVT_MENU, self.OnSetup, menuMachine)


		panel = wx.Panel(self, -1)
		#panel.SetBackgroundColour('WHITE')
		vbox = wx.BoxSizer(wx.VERTICAL)

		#Display set
		panel1 = wx.Panel(panel, -1)
		#box1 = wx.StaticBox(panel1, -1, 'Display data')
		#sizer1 = wx.StaticBoxSizer(box1, orient=wx.VERTICAL)
		#grid1 = wx.GridSizer(2, 5, 0, 5)
		#self.cb1 = wx.CheckBox(panel1, -1, 'Pattern data')
		#self.cb1.SetValue(gDISP_GERBER)
		#grid1.Add(self.cb1)
		#self.cb2 = wx.CheckBox(panel1, -1, 'Drill data')
		#self.cb2.SetValue(gDISP_DRILL)
		#grid1.Add(self.cb2)
		#self.cb3 = wx.CheckBox(panel1, -1, 'Edge data')
		#self.cb3.SetValue(gDISP_EDGE)
		#grid1.Add(self.cb3)

		#self.cb4 = wx.CheckBox(panel1, -1, 'Contour data')
		#self.cb4.SetValue(gDISP_CONTOUR)
		#grid1.Add(self.cb4)

		vbox_view = wx.BoxSizer(wx.VERTICAL)
		radioList = ['XY', 'XZ', 'YZ', 'XYZ']
		rb1 = wx.RadioBox(panel1, label="View plain", choices=radioList, majorDimension=5, style=wx.RA_SPECIFY_COLS)
		rb1.SetSelection(int(gVIEW_POINT))
		vbox_view.Add(rb1, 0, wx.BOTTOM | wx.TOP, 9)

		#sizer1.Add(grid1)
		#panel1.SetSizer(sizer1)
		panel1.SetSizer(vbox_view)
		vbox.Add(panel1, 0, wx.BOTTOM | wx.TOP, 9)

		#Draw data
		panel2 = wx.Panel(panel, -1)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		#vbox1 = wx.BoxSizer(wx.VERTICAL)

		paint = Paint(panel2)
		#paint = Paint(hbox1)
		#sw = wx.ScrolledWindow(panel2)
		#paint = Paint(sw)
		#sw.SetScrollbars(20,20,55,40)

		#hbox1.Add(sw, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 2)
		hbox1.Add(paint, 1, wx.EXPAND | wx.ALL, 2)
		#vbox1.Add(paint, 0, wx.EXPAND | wx.ALL, 15)
		panel2.SetSizer(hbox1)
		#panel2.SetSizer(vbox1)
		vbox.Add(panel2, 1,  wx.LEFT | wx.RIGHT | wx.EXPAND, 2)
		#vbox.Add((-1, 25))

		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		#btn0 = wx.Button(panel, -1, 'Generate contour', size=(150, 30))
		#hbox5.Add(btn0, 0)
		#btn1 = wx.Button(panel, -1, 'Convert and Save', size=(150, 30))
		#hbox5.Add(btn1, 0)
		btn2 = wx.Button(panel, -1, 'Close', size=(70, 30))
		hbox5.Add(btn2, 0, wx.LEFT | wx.BOTTOM , 5)
		vbox.Add(hbox5, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

		#vbox1 = wx.BoxSizer(wx.VERTICAL)
		#self.progress1 = wx.StaticText(panel, -1, 'Progress')
		#vbox1.Add(self.progress1, 0, wx.LEFT)
		#self.gauge = wx.Gauge(panel, -1, 100, size=(500, 15))
		#vbox1.Add(self.gauge, 0, wx.LEFT)
		#vbox.Add(vbox1, 0, wx.ALIGN_LEFT | wx.LEFT, 10)

		panel.SetSizer(vbox)
		#status = self.CreateStatusBar()
		#rect = status.GetFieldRect(1)
		#self.gauge = wx.Gauge(status, -1, 100, wx.Point(rect.x + 2, rect.y + 2),wx.Size(rect.width - 4, rect.height - 4)) 
		self.Centre()
		self.Show(True)

		#Event
		#self.Bind(wx.EVT_CHECKBOX, self.OnGeber,self.cb1)
		#self.Bind(wx.EVT_CHECKBOX, self.OnDrill,self.cb2)
		#self.Bind(wx.EVT_CHECKBOX, self.OnEdge,self.cb3)
		#self.Bind(wx.EVT_CHECKBOX, self.OnContour,self.cb4)
		self.Bind(wx.EVT_BUTTON, self.OnExit, btn2)
		#self.Bind(wx.EVT_BUTTON, self.OnGenerate, btn0)
		#self.Bind(wx.EVT_BUTTON, self.OnConvert, btn1)
		self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox1, rb1)

	#functions
	def EvtRadioBox1(self,e):
		global gVIEW_POINT
		gVIEW_POINT = e.GetInt()
		self.Refresh(1)
	def OnGeber(self,e):
		global gDISP_GERBER
		gDISP_GERBER = int(self.cb1.IsChecked())
		self.Refresh(1)
	def OnDrill(self,e):
		global gDISP_DRILL, gDISP_EDGE
		gDISP_DRILL = int(self.cb2.IsChecked())
		self.Refresh(1)
	def OnEdge(self,e):
		global gDISP_EDGE
		gDISP_EDGE = int(self.cb3.IsChecked())
		self.Refresh(1)
	def OnContour(self,e):
		global gDISP_CONTOUR, gDRAWCONTOUR
		if(len(gDRAWCONTOUR) > 0):
			gDISP_CONTOUR = int(self.cb4.IsChecked())
		else:
			gDISP_CONTOUR = 0
			self.cb4.SetValue(0)
		self.Refresh(1)
	def OnExit(self,e):
		self.Close(True)  # Close the frame.
	def OnOpen(self,e):
		setup = OpenFiles(None, -1, 'Open Files')
		setup.ShowModal()
		setup.Destroy()
		self.Refresh(1)
	def OnReload(self,e):
		readGcodeFile()
#class Paint(wx.Panel):
class Paint(wx.ScrolledWindow):
	def __init__(self, parent):
		#wx.Panel.__init__(self, parent)
		wx.ScrolledWindow.__init__(self, parent,-1,style=wx.HSCROLL|wx.VSCROLL)
		global gDRAW_XSHIFT, gDRAW_YSHIFT, gDRAW_ZSHIFT		
		self.SetBackgroundColour('WHITE')

		#print self.GetScaleX()
		#print self.GetSize()
		#print self.GetScrollPageSize(wx.VERTICAL)
		#print self.GetScrollPageSize(wx.HORIZONTAL)
		#print self.GetViewStart()
		#print self.GetVirtualSize()
		self.Bind(wx.EVT_PAINT, self.OnPaint)

		#panel.Bind(wx.EVT_SCROLLWIN, self.OnScroll)
		self.SetScrollbars(10, 10, 100,100);
		#self.Bind(wx.EVT_SCROLLWIN, self.OnScroll)
		self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
		self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnDrag)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
		self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
		#self.Bind(wx.EVT_LEFT_DCLICK , self.OnMouseLeftDClick)
		#self.Bind(wx.EVT_RIGHT_DCLICK , self.OnMouseRightDClick)
		self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
		self.Bind(wx.EVT_RIGHT_UP, self.OnMouseRightUp)
		self.Bind(wx.EVT_MOTION , self.OnMouseMove) 
		paint_size = self.GetSize()
		gDRAW_XSHIFT =int(paint_size.x/2)
		gDRAW_YSHIFT =int(paint_size.y/2)
		self.Centre()
		self.Show(True)

	def OnKeyDown(self, event):
		keycode = event.GetKeyCode()
		print keycode
		#if keycode == wx.WXK_UP:

	#gerber
	def OnPaint(self, e):
		global gMAG, gDRAW_XSHIFT, gDRAW_YSHIFT, gDRAW_ZSHIFT, gCENTER_X, gCENTER_Y, gCENTER_Z, gPATTERNS, gMOVE_COLOR,gVIEW_POINT, CENTER_X, CENTER_Y
		dc = wx.PaintDC(self)
		#print self.GetViewStart()
		#print self.GetVirtualSize()
		#print self.GetSize()
		paint_size = self.GetSize()
		CENTER_X =int(paint_size.x/2)
		CENTER_Y =int(paint_size.y/2)
		#veiw_start = self.GetViewStart()
		veiw_start = self.CalcUnscrolledPosition(0,0)
		#print "Center x=" + str(CENTER_X) + ", Center x="+ str(CENTER_Y) 
		#print "pos=" + str(veiw_start)
		#print 'Mag' + str(gMAG) + ", x shift=" + str(gDRAW_XSHIFT-veiw_start[0]) + ", y shift=" + str(gDRAW_YSHIFT-veiw_start[1])
		#c=POINT(gCENTER_X, gCENTER_Y, gCENTER_Z)
		c=POINT(0.0, 0.0, 0.0)	#center of view point
		
		#
		coorc = POINT(gDRAW_XSHIFT-veiw_start[0],gDRAW_YSHIFT-veiw_start[1],gDRAW_ZSHIFT)
		coorx = POINT(gDRAW_XSHIFT-veiw_start[0]+20,gDRAW_YSHIFT-veiw_start[1],gDRAW_ZSHIFT)
		coory = POINT(gDRAW_XSHIFT-veiw_start[0],gDRAW_YSHIFT-veiw_start[1]-20,gDRAW_ZSHIFT)
		coorz = POINT(gDRAW_XSHIFT-veiw_start[0],gDRAW_YSHIFT-veiw_start[1],gDRAW_ZSHIFT+20)
		if(len(gPATTERNS) > 0):
			for patterns in gPATTERNS:
				#color = patterns.color
				for pattern in patterns.patterns:
					#print len(pattern.points)
					#print pattern.points
					if(gVIEW_POINT==0):	#XY
						p1x = pattern.points[0].x
						p1y = pattern.points[0].y
						p2x = pattern.points[1].x
						p2y = pattern.points[1].y
						#Draw coor
						dc.SetPen(wx.Pen('BLACK', 1, wx.SOLID))
						dc.DrawLines(([coorc.x,coorc.y],[coorx.x,coorx.y]))	#X axis
						dc.DrawLines(([coorc.x,coorc.y],[coory.x,coory.y]))	#Y axis
					elif(gVIEW_POINT==1):	#XZ
						p1x = pattern.points[0].x
						p1y = pattern.points[0].z
						p2x = pattern.points[1].x
						p2y = pattern.points[1].z
						dc.SetPen(wx.Pen('BLACK', 1, wx.SOLID))
						dc.DrawLines(([coorc.x,coorc.y],[coorx.x,coorx.y]))	#X axis
						dc.DrawLines(([coorc.x,coorc.y],[coory.x,coory.y]))	#Y axis
					elif(gVIEW_POINT==2):	#YZ
						p1x = pattern.points[0].y
						p1y = pattern.points[0].z
						p2x = pattern.points[1].y
						p2y = pattern.points[1].z
						dc.SetPen(wx.Pen('BLACK', 1, wx.SOLID))
						dc.DrawLines(([coorc.x,coorc.y],[coorx.x,coorx.y]))	#X axis
						dc.DrawLines(([coorc.x,coorc.y],[coory.x,coory.y]))	#Y axis
					else:
						p1,p2 = change_view(pattern.points[0],pattern.points[1],c)
						p1x = p1.x
						p1y = p1.y
						p2x = p2.x
						p2y = p2.y
						co1,co2 = change_view(POINT(0.0,0.0,0.0),POINT(20.0,0.0,0.0),c)
						dc.SetPen(wx.Pen('BLACK', 1, wx.SOLID))
						point1 = [co1.x+gDRAW_XSHIFT-veiw_start[0],co1.y+gDRAW_YSHIFT-veiw_start[1]]
						point2 = [co2.x+gDRAW_XSHIFT-veiw_start[0],-co2.y+gDRAW_YSHIFT-veiw_start[1]]
						dc.DrawLines((point1,point2))	#X axis
						co1,co2 = change_view(POINT(0.0,0.0,0.0),POINT(0.0,20.0,0.0),c)
						point1 = [co1.x+gDRAW_XSHIFT-veiw_start[0],co1.y+gDRAW_YSHIFT-veiw_start[1]]
						point2 = [co2.x+gDRAW_XSHIFT-veiw_start[0],-co2.y+gDRAW_YSHIFT-veiw_start[1]]
						dc.DrawLines((point1,point2))	#Y axis
						dc.DrawLines(([coorc.x,coorc.y],[coorc.x,coorc.y-20]))	#Z axis
					x1 = p1x * gMAG + gDRAW_XSHIFT-veiw_start[0]
					y1 = -p1y * gMAG + gDRAW_YSHIFT-veiw_start[1]
					x2 = p2x * gMAG + gDRAW_XSHIFT-veiw_start[0]
					y2 = -p2y * gMAG + gDRAW_YSHIFT-veiw_start[1]
					if(pattern.style == 0):	#move
						dc.SetPen(wx.Pen(gMOVE_COLOR, 1, wx.DOT_DASH))
						dc.DrawLines(([x1,y1],[x2,y2]))
					if(pattern.style == 1):
						dc.SetPen(wx.Pen(patterns.color, 1, wx.SOLID))
						dc.DrawLines([[x1,y1],[x2,y2]])
					if(pattern.style == 2 or pattern.style == 3):
						dc.SetPen(wx.Pen(color, 1, wx.SOLID))
						dc.DrawArcPoint(pattern.p1,pattern.p2,pattern.center)
	def OnMouseWheel(self, event):
		global gMAG, gMAG_MIN, gMAG_MAX, gDRAW_XSHIFT, gDRAW_YSHIFT, WINDOW_X, WINDOW_Y, CENTER_X, CENTER_Y, gPRE_X, gPRE_Y
		pos = event.GetPosition()
		w = event.GetWheelRotation()
		#mag_cont += copysign(1.0, w)
		pre_mag = gMAG
		gMAG += copysign(1.0, w)
		#gMAG += w/100.0
		#gMAG = 1
		gDRAW_XSHIFT = float(CENTER_X) - (gMAG*(float(pos.x)-gDRAW_XSHIFT))/pre_mag
		gDRAW_YSHIFT = float(CENTER_Y) - (gMAG*(float(pos.y)-gDRAW_YSHIFT))/pre_mag
		gPRE_X = float(pos.x)
		gPRE_Y = float(pos.y)
		if(gMAG < gMAG_MIN):
			gMAG = gMAG_MIN
			gDRAW_XSHIFT = CENTER_X
			gDRAW_YSHIFT = CENTER_Y
		if(gMAG > gMAG_MAX):
			gMAG = gMAG_MAX
			gDRAW_XSHIFT = float(CENTER_X) - (gMAG*(float(pos.x)-gDRAW_XSHIFT))/pre_mag
			gDRAW_YSHIFT = float(CENTER_Y) - (gMAG*(float(pos.y)-gDRAW_YSHIFT))/pre_mag
		#print 'Mag' + str(gMAG) + ", x shift=" + str(gDRAW_XSHIFT) + ", y shift=" + str(gDRAW_YSHIFT)
		#print 'OnMouseWheel' + str(pos) + ", w=" + str(gMAG)
		#self.OnPaint(event)
		self.Refresh(1)
	def OnDrag(self, event):
		pos = event.GetPosition()
		print "Drag: pos=" + str(pos)
		#self.Refresh(1)
	def OnScroll(self, event):
		global gDRAW_XSHIFT, gDRAW_YSHIFT
		pos = self.GetViewStart()
		print "pos=" + str(pos)
		gDRAW_XSHIFT -= pos[0]
		gDRAW_YSHIFT -= pos[1]
		print "X shif=" + str(gDRAW_XSHIFT) + ", Y shift=" + str(gDRAW_YSHIFT)
		#self.Refresh(1)
	def OnMouseLeftDown(self, event):
		global gMouseLeftDown
		pos = event.GetPosition()
		gMouseLeftDown[0] = 1
		gMouseLeftDown[1] = pos.x
		gMouseLeftDown[2] = pos.y
		#print "Left Down: pos=" + str(pos)
	def OnMouseRightDown(self, event):
		global gMouseRightDown
		pos = event.GetPosition()
		gMouseRightDown[0] = 1
		gMouseRightDown[1] = pos.x
		gMouseRightDown[2] = pos.y
		#print "Right Down: pos=" + str(pos)
	def OnMouseLeftUp(self, event):
		global gMouseLeftDown, gMAG, gDRAW_XSHIFT, gDRAW_YSHIFT, CENTER_X, CENTER_Y
		pos = event.GetPosition()
		size = self.GetSize()
		if gMouseLeftDown[0]:
			gMouseLeftDown[0] = 0
			pre_mag = gMAG
			dx = pos.x - gMouseLeftDown[1]
			dy = pos.y - gMouseLeftDown[2]
			cx = pos.x - dx/2
			cy = pos.y - dy/2
			if(dx > 0):
				gMAG = float(size.x)/float(dx/pre_mag)
			elif(dx < 0):
				gMAG = -float(pre_mag)/float(dx)
			#print "gmag=" + str(gMAG)
			if(dy > 0):
				if(gMAG > float(size.y)/float(dy/pre_mag)):
					gMAG = float(size.y)/float(dy/pre_mag)
			
			gDRAW_XSHIFT = float(CENTER_X) - (gMAG*(float(cx)-gDRAW_XSHIFT))/pre_mag
			gDRAW_YSHIFT = float(CENTER_Y) - (gMAG*(float(cy)-gDRAW_YSHIFT))/pre_mag
			if(gMAG < gMAG_MIN):
				gMAG = gMAG_MIN
				gDRAW_XSHIFT = CENTER_X
				gDRAW_YSHIFT = CENTER_Y
			if(gMAG > gMAG_MAX):
				gMAG = gMAG_MAX
				gDRAW_XSHIFT = float(CENTER_X) - (gMAG*(float(cx)-gDRAW_XSHIFT))/pre_mag
				gDRAW_YSHIFT = float(CENTER_Y) - (gMAG*(float(cy)-gDRAW_YSHIFT))/pre_mag

			self.Refresh(1)
			#print "X shif=" + str(gDRAW_XSHIFT) + ", Y shift=" + str(gDRAW_YSHIFT)
			#print "Left UP: pos=" + str(pos) + ", dx=" + str(dx) + ", dy=" + str(dy) + ", cx=" + str(cx) + ", cy=" + str(cy) + ", mag=" + str(gMAG)
	def OnMouseRightUp(self, event):
		global gMouseRightDown, gMAG
		pos = event.GetPosition()
		if gMouseRightDown[0]:
			gMouseRightDown[0] = 0
			dx = pos.x - gMouseRightDown[1]
			dy = pos.y - gMouseRightDown[2]
			dist = sqrt(dx*dx + dy*dy)/gMAG
			print dist
	def OnMouseLeftDClick(self, event):
		pos = event.GetPosition()
	def OnMouseRightDClick(self, event):
		pos = event.GetPosition()
	def OnMouseMove(self, event):
		pos = event.GetPosition()

class OpenFiles(wx.Dialog):
	def __init__(self, parent, id, title):
		global IN_INCH_FLAG, gGCODES, gCOLORS, GCODE_EXT, DEF_COLOR
		wx.Dialog.__init__(self, parent, id, title, size=(250, 210))
		self.dirname=''

		panel = wx.Panel(self, -1)
		sizer = wx.GridBagSizer(0, 0)

		text1 = wx.StaticText(panel, -1, 'G code file')
		sizer.Add(text1, (0, 0), flag= wx.LEFT | wx.TOP, border=10)

		self.gcode = wx.TextCtrl(panel, -1)
		#self.gcode.SetValue(gGERBER_FILE)
		sizer.Add(self.gcode, (0, 1), (1, 3), wx.TOP | wx.EXPAND, 5)

		button1 = wx.Button(panel, -1, 'Browse...', size=(-1, 30))
		sizer.Add(button1, (0, 4), (1, 1), wx.TOP | wx.LEFT | wx.RIGHT , 5)

		text2 = wx.StaticText(panel, -1, 'G code color')
		sizer.Add(text2, (1, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.gcode_color = wx.ComboBox(panel, -1, choices=gCOLORS, style=wx.CB_READONLY)
		self.gcode_color.SetValue(str(DEF_COLOR))
		sizer.Add(self.gcode_color, (1, 1), (1, 3), wx.TOP | wx.EXPAND, 5)


		radioList = ['mm', 'inch']
		rb1 = wx.RadioBox(panel, label="unit of Input file", choices=radioList, majorDimension=3, style=wx.RA_SPECIFY_COLS)
		rb1.SetSelection(int(IN_INCH_FLAG))
		sizer.Add(rb1, (2, 0), (1, 5), wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT , 10)

		#sbox1 = wx.StaticBox(panel, -1, 'Read files')
		#vbox1 = wx.StaticBoxSizer(box1, orient=wx.VERTICAL)
		#sizer1.Add(grid1)

		button4 = wx.Button(panel, -1, 'Append Open', size=(-1, 30))
		sizer.Add(button4, (4, 2), (1, 1),  wx.LEFT, 10)

		button5 = wx.Button(panel, -1, 'New Open', size=(-1, 30))
		sizer.Add(button5, (4, 3), (1, 1),  wx.LEFT, 10)

		button6 = wx.Button(panel, -1, 'Close', size=(-1, 30))
		sizer.Add(button6, (4, 4), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)

		sizer.AddGrowableCol(2)
        
		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.
		self.Bind(wx.EVT_BUTTON, self.OnGcodeOpen, button1)
		self.Bind(wx.EVT_BUTTON, self.OnAppend, button4)
		self.Bind(wx.EVT_BUTTON, self.OnNEW, button5)
		self.Bind(wx.EVT_BUTTON, self.OnClose, button6)	
		self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox1, rb1)

		#self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		#self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

		self.Centre()
		self.Show(True)

	#Events
	def EvtRadioBox1(self, e):
		global IN_INCH_FLAG
		if(e.GetInt()==0): #milli
			IN_INCH_FLAG = 0
		elif(e.GetInt()==1): #Inch
			IN_INCH_FLAG = 1
	def OnGcodeOpen(self,e):
		global GCODE_EXT
		""" Open a file"""
		dlg = wx.FileDialog(self, "Choose a output G-code file", self.dirname, "", GCODE_EXT, wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			self.gcode.SetValue(os.path.join(self.dirname, self.filename))
		dlg.Destroy()

	def OnAppend(self,e):
		global IN_INCH_FLAG, gGCODES, gXMIN, gXMAX, gYMIN, gYMAX, gZMIN, gZMAX, gCENTER_X, gCENTER_Y, gCENTER_Z
		if(self.gcode.GetValue()):
			gGCODES.append(GCODE(self.gcode.GetValue(),self.gcode_color.GetValue()))
		set_unit()
		readGcodeFile()
		gCENTER_X = (gXMIN + gXMAX)/2
		gCENTER_Y = (gYMIN + gYMAX)/2
		gCENTER_Z = (gZMIN + gZMAX)/2
		#gerber2draw()
		self.Close(True)  # Close the frame.
	def OnNEW(self,e):
		global IN_INCH_FLAG, gGCODES, gPATTERNS, gXMIN, gXMAX, gYMIN, gYMAX, gZMIN, gZMAX, gCENTER_X, gCENTER_Y, gCENTER_Z
		gGCODES = []
		gPATTERNS = []
		if(self.gcode.GetValue()):
			gGCODES.append(GCODE(self.gcode.GetValue(),self.gcode_color.GetValue()))
		set_unit()
		readGcodeFile()
		gCENTER_X = (gXMIN + gXMAX)/2
		gCENTER_Y = (gYMIN + gYMAX)/2
		gCENTER_Z = (gZMIN + gZMAX)/2
		#gerber2draw()
		self.Close(True)  # Close the frame.
	def OnClose(self,e):
		self.Close(True)  # Close the frame.

#Set Class
class POINT:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
class LINE:
	def __init__(self, style, line, speed, points):
		self.style = style
		self.line = line
		self.speed = speed
		self.points = points

class ARC:
	def __init__(self,style, line, speed, plain, p1, p2, center):
		self.style = style
		self.line = line
		self.speed = speed
		self.plain = plain
		self.p1 = p1
		self.p2 = p2
		self.center = center

class GCODE:
	def __init__(self, name, color):
		self.name = name
		self.color = color

class PATTERN:
	def __init__(self, color,patterns):
		self.color = color
		self.patterns = patterns

#functions
def main():
	app = wx.App()
	MainFrame(None, -1, 'pyGerber2Gcode')
	app.MainLoop()

def set_unit():
	global IN_INCH_FLAG, gUNIT, INCH
	if (IN_INCH_FLAG):
		gUNIT = INCH
	else:
		gUNIT = 1.0

def readGcodeFile():
	global gGCODES, gXMIN, gXMAX, gYMIN, gYMAX, gZMIN, gZMAX

	for gcodes in gGCODES:
		try:
			f = open(gcodes.name,'r')
		except IOError, (errno, strerror):
			error_dialog("Unable to open the file" + gcodes.name + "\n",1)
		else:
			pre_x = 0.0
			pre_y = 0.0
			pre_z = 0.0
			x = pre_x
			y = pre_y
			z = pre_z
			s = 0
			l = 1
			style = 0
			patterns = []
			while 1:
				gcode = f.readline()
				if not gcode:
					break
				flag = 0
				#parse g code
				gg = re.search("[gG]([\d]+)\D",gcode)
				xx = re.search("[xX]([\d\.\-]+)\D",gcode)
				yy = re.search("[yY]([\d\.\-]+)\D",gcode)
				zz = re.search("[zZ]([\d\.\-]+)\D",gcode)
				ss = re.search("[fF]([\d\.\-]+)\D",gcode)
				if (gg):
					style = int(gg.group(1))
				if (xx):
					x = float(xx.group(1))
					flag = 1
				if (yy):
					y = float(yy.group(1))
					flag = 1
				if (zz):
					z = float(zz.group(1))
					flag = 1
				if (ss):
					s = float(ss.group(1))
				if(style == 1 or style == 0):
					if(flag):
						point1 = POINT(pre_x,pre_y,pre_z)
						point2 = POINT(x,y,z)
						patterns.append(LINE(style,l,s,[point1,point2]))
						
				elif(style == 2 or style == 3):
						i=0
						j=0
						k=0
						ii = re.search("[iI]([\d\.\-]+)\D",gcode)
						jj = re.search("[jJ]([\d\.\-]+)\D",gcode)
						kk = re.search("[kK]([\d\.\-]+)\D",gcode)
						rr = re.search("[rR]([\d\.\-]+)\D",gcode)
						if(ii):
							i = float(rr.group(1))
						if(jj):
							j = float(rr.group(1))
						if(kk):
							k = float(rr.group(1))
						center = POINT(i,j,k)
						point1 = POINT(pre_x,pre_y,pre_z)
						point2 = POINT(x,y,z)
						if(style == 3):
							tmp_point = point2
							point2 = point1
							point1 = point2
						if(rr):
							r = float(rr.group(1))
							c1,c2 = calc_center(point1,point2,r,plain)
							center = c1
							if(r < 0):
								center = c2
						patterns.append(ARC(style,l,s,plain,point1,point2,center))
				elif(style == 17):
						plain = 0
				elif(style == 18):
						plain = 1
				elif(style == 19):
						plain = 2
				if(x > gXMAX):
					gXMAX = x
				if(x < gXMIN):
					gXMIN = x
				if(y > gYMAX):
					gYMAX = y
				if(y < gYMIN):
					gYMIN = y
				if(z > gZMAX):
					gZMAX = z
				if(z < gZMIN):
					gZMIN = z
				pre_x = x
				pre_y = y
				pre_z = z					
				l += 1
			gPATTERNS.append(PATTERN(gcodes.color,patterns))
			f.close()

def calc_center(p1,p2,r,plain):
	r = copysign(1.0, r) * r
	if(plain == 0):	#XY
		if(p1.x == p2.x):
			dx = (p2.x - p1.x)/2
			dy = sqrt(r*r-dx*dx)
			c1 = POINT(p1.x+dx,p1.y+dy,p1.z)
			c2 = POINT(p1.x+dx,p1.y-dy,p1.z)
		elif(p1.y == p2.y):
			dy = (p2.y - p1.y)/2
			dx = sqrt(r*r-dy*dy)
			c1 = POINT(p1.x+dx,p1.y+dy,p1.z)
			c2 = POINT(p1.x-dx,p1.y+dy,p1.z)
		else:
			a = (p2.y - p1.y)/(p2.x - p1.x)
			av = -1/a
			bv = (p2.y -+ p1.y)/2 - av * (p2.x + p1.x)/2
			dx = sqrt(r*r/(av*av+1))
			dy = av * dx
			cx = (p2.x + p1.x)/2
			cy = (p2.y + p1.y)/2
			c1 = POINT(p1.x+dx,p1.y-dy,p1.z)
			c2 = POINT(p1.x-dx,p1.y+dy,p1.z)
#	if(plain == 1):	#ZX
#	if(plain == 2):	#YZ
	return [c1,c2]

def rot_coor(p):
	global gTHETA, gPHI, gPSI
	dx = c.x-p.x
	dy = c.y-p.y
	ang = atan2(dy,dx) + gTHETA
	r = sqrt(dx*dx+dy*dy)

def change_view(p1,p2,c):
	global gTHETA, gPHI, gPSI
	pp1 = POINT(0.0,0.0,0.0)
	pp2 = POINT(0.0,0.0,0.0)
	# rot around z
	dx1 = p1.x-c.x
	dy1 = p1.y-c.y
	ang1 = atan2(dy1,dx1) + gTHETA
	dx2 = p2.x-c.x
	dy2 = p2.y-c.y
	ang2 = atan2(dy2,dx2) + gTHETA
	r1 = sqrt(dx1*dx1+dy1*dy1)
	r2 = sqrt(dx2*dx2+dy2*dy2)

	pp1.x = c.x+r1*cos(ang1)
	pp1.y = c.y+r1*sin(ang1)
	pp2.x = c.x+r2*cos(ang2)
	pp2.y = c.y+r2*sin(ang2)

	# rot around x
	dy1 = pp1.y-c.y
	dz1 = pp1.z-c.z
	ang1 = atan2(dy1,dz1) + gPHI
	dz2 = pp2.z-c.z
	dy2 = pp2.y-c.y
	ang2 = atan2(dy2,dz2) + gPHI
	r1 = sqrt(dz1*dz1+dy1*dy1)
	r2 = sqrt(dz2*dz2+dy2*dy2)

	pp1.z = c.z+r1*cos(ang1)
	pp1.y = c.y+r1*sin(ang1)+p1.z
	pp2.z = c.z+r2*cos(ang2)
	pp2.y = c.y+r2*sin(ang2)+p2.z

	# rot around y
	dx1 = pp1.x-c.x
	dz1 = pp1.z-c.z
	ang1 = atan2(dx1,dz1) + gPSI
	dz2 = pp2.z-c.z
	dx2 = pp2.x-c.x
	ang2 = atan2(dx2,dz2) + gPSI
	r1 = sqrt(dz1*dz1+dx1*dx1)
	r2 = sqrt(dz2*dz2+dx2*dx2)

	pp1.z = c.z+r1*cos(ang1)
	pp1.x = c.y+r1*sin(ang1)
	pp2.z = c.z+r2*cos(ang2)
	pp2.x = c.y+r2*sin(ang2)


	return pp1,pp2

def circle_points(cx,cy,r,points_num):
	points=[]
	if(points_num <= 2):
		print "Too small angle at Circle"
		return
	i = points_num
	while i > 0:
		cir_x=cx+r*cos(2.0*pi*float(i)/float(points_num))
		cir_x=cx+r*cos(2.0*pi*float(i)/float(points_num))
		cir_y=cy+r*sin(2.0*pi*float(i)/float(points_num))
		points.extend([cir_x,cir_y])
		i -= 1
	cir_x=cx+r*cos(0.0)
	cir_y=cy+r*sin(0.0)
	points.extend([cir_x,cir_y])
	return points

def arc_points(cx,cy,r,s_angle,e_angle,kaku):
	points=[]
	if(s_angle == e_angle):
		print "Start and End angle are same"
	int(kaku)
	if(kaku <= 2):
		print "Too small angle"
	ang_step=(e_angle-s_angle)/(kaku-1)
	i = 0
	while i < kaku:
		arc_x=cx+r*cos(s_angle+ang_step*float(i))
		arc_y=cy+r*sin(s_angle+ang_step*float(i))
		points.extend([arc_x,arc_y])
		i += 1

	return points



def error_dialog(error_mgs,sw):
	print error_mgs
	if(sw):
		#raw_input("\n\nPress the enter key to exit.")
		sys.exit()

if __name__ == "__main__":
	main()
