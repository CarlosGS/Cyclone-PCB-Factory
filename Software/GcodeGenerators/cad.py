#!/usr/bin/env python
#
# cad.py
#
# Neil Gershenfeld
#
# (c) Massachusetts Institute of Technology 2007
# Permission granted for experimental and personal use;
# license for commercial sale available from MIT.
#
#Altered by R Parsons (AKA: Capo) to output gcode with the '.gcode' extension as opposed to '.g'. 
#Also the default variables were changed to metric values
DATE = "7/12/010"

from numpy import *
import scipy.signal.signaltools
from string import *
from Tkinter import *
from tkFileDialog import *
import Image, ImageTk, ImageDraw, ImageFont, ImageOps
import os, struct
#import time

class point:
   #
   # an xyz point
   #
   def __init__(self,x,y,z=0):
      self.x = x
      self.y = y
      self.z = z

class cad_variables:
   #
   # cad variables
   #
   def __init__(self):
      self.xmin = 0 # minimum x value to render
      self.xmax = 0 # maximum x value to render
      self.ymin = 0 # minimum y value to render
      self.ymax = 0 # maximum y value to render
      self.zmin = 0 # minimum z value to render
      self.zmax = 0 # maximum z value to render
      self.zlist = [] # z values to render
      self.nx = 0 # number of x points to render
      self.ny = 0 # number of y points to render
      self.nz = 1 # number of z points to render
      self.rz = 0 # perspective view z rotation (degrees)
      self.rx = 0 # perspective view x rotation (degrees)
      self.units = 'in' # file units
      self.function = '0' # cad function
      self.toolpaths = [] # toolpaths
      self.x = [] # x triangulation
      self.y = [] # y triangulation
      self.z = [] # z triangulation
      self.labels = [] # display labels
      self.image_r = array(0) # red array
      self.image_g = array(0) # green array
      self.image_b = array(0) # blue array
      self.image_min = 0 # image min value
      self.image_max = 0 # image max value
      self.stop = 0 # stop rendering
      self.nplot = 200 # plot window size
      self.inches_per_unit = 1 # file units
      self.views = 'xyzr'
      self.cam = '' # CAM export type
      self.editor_width = 30 # editor width
      self.editor_height = 10 # editor height
   def view(self,arg):
      global canvas_xy,canvas_yz,canvas_xz,canvas_xyz
      if (arg == 'xy'):
         view_frame2.grid_forget()
         view_frame3.grid_forget()
         canvas_xy.grid_forget()
         self.views = 'xy'
         self.nplot = 2*int(string_window_size.get()) # plot window size
         canvas_xy = Canvas(view_frame2, width=self.nplot, height=self.nplot)
         imxy = Image.new("RGBX",(self.nplot,self.nplot),'black')
         image_xy = ImageTk.PhotoImage(imxy)
         canvas_xy.create_image(self.nplot/2,self.nplot/2,image=image_xy)
         canvas_xy.bind('<Motion>',msg_xy)
         canvas_xy.grid(row=0,column=0)
         view_frame2.grid(row=2,column=0)
      elif (arg == 'xyzr'):
         view_frame2.grid_forget()
         view_frame3.grid_forget()
         canvas_xy.grid_forget()
         canvas_yz.grid_forget()
         canvas_xz.grid_forget()
         canvas_xyz.grid_forget()
         self.views = 'xyzr'
         self.nplot = int(string_window_size.get()) # plot window size
         canvas_xy = Canvas(view_frame3, width=self.nplot, height=self.nplot)
         canvas_yz = Canvas(view_frame3, width=self.nplot, height=self.nplot)
         canvas_xz = Canvas(view_frame3, width=self.nplot, height=self.nplot)
         canvas_xyz = Canvas(view_frame3, width=self.nplot, height=cad.nplot)
         imxy = Image.new("RGBX",(self.nplot,self.nplot),'black')
         image_xy = ImageTk.PhotoImage(imxy)
         canvas_xy.create_image(self.nplot/2,self.nplot/2,image=image_xy)
         canvas_xy.bind('<Motion>',msg_xy)
         canvas_xy.grid(row=0,column=0)
         imyz = Image.new("RGBX",(self.nplot,self.nplot),'black')
         image_yz = ImageTk.PhotoImage(imyz)
         canvas_yz.create_image(self.nplot/2,self.nplot/2,image=image_yz)
         canvas_yz.bind('<Motion>',msg_yz)
         canvas_yz.grid(row=0,column=1)
         imxz = Image.new("RGBX",(self.nplot,self.nplot),'black')
         image_xz = ImageTk.PhotoImage(imxz)
         canvas_xz.create_image(self.nplot/2,self.nplot/2,image=image_xz)
         canvas_xz.bind('<Motion>',msg_xz)
         canvas_xz.grid(row=1,column=0)
         imxyz = Image.new("RGBX",(self.nplot,self.nplot),'black')
         image_xyz = ImageTk.PhotoImage(imxyz)
         canvas_xyz.create_image(self.nplot/2,self.nplot/2,image=image_xyz)
         canvas_xyz.bind('<Motion>',msg_nomsg)
         canvas_xyz.grid(row=1,column=1)
         view_frame3.grid(row=2,column=0)
      else:
         print "view not supported"          
   def nxplot(self):
      xwidth = self.xmax - self.xmin
      ywidth = self.ymax - self.ymin
      zwidth = self.zmax - self.zmin
      if ((xwidth >= ywidth) & (xwidth >= zwidth)):
         n = int(self.nplot*xwidth/float(xwidth))
      elif ((ywidth >= xwidth) & (ywidth >= zwidth)):
         n = int(self.nplot*xwidth/float(ywidth))
      else:
         n = int(self.nplot*xwidth/float(zwidth))
      return n
   def nyplot(self):
      xwidth = self.xmax - self.xmin
      ywidth = self.ymax - self.ymin
      zwidth = self.zmax - self.zmin
      if ((xwidth >= ywidth) & (xwidth >= zwidth)):
         n = int(self.nplot*ywidth/float(xwidth))
      elif ((ywidth >= xwidth) & (ywidth >= zwidth)):
         n = int(self.nplot*ywidth/float(ywidth))
      else:
         n = int(self.nplot*ywidth/float(zwidth))
      return n
   def nzplot(self):
      xwidth = self.xmax - self.xmin
      ywidth = self.ymax - self.ymin
      zwidth = self.zmax - self.zmin
      if ((xwidth >= ywidth) & (xwidth >= zwidth)):
         n = int(self.nplot*zwidth/float(xwidth))
      elif ((ywidth >= xwidth) & (ywidth >= zwidth)):
         n = int(self.nplot*zwidth/float(ywidth))
      else:
         n = int(self.nplot*zwidth/float(zwidth))
      return n

cad = cad_variables()

class cad_text:
   def __init__(self,x,y,z=0,text='',size=10,color='#ff0000',anchor=CENTER):
      self.x = x
      self.y = y
      self.z = z
      self.text = text
      self.size = size
      self.color = color
      self.anchor = anchor

class im_class:
   #
   # for PIL images
   #
   def __init__(self):
      self.xy = 0
      self.xz = 0
      self.yz = 0
      self.xyz = 0
      self.intensity_xy = 0
      self.intensity_xz = 0
      self.intensity_yz = 0
      self.intensity_xyz = 0

im = im_class()

class images_class:
   #
   # for PhotoImages
   #
   def __init__(self):
      self.xy = 0
      self.xz = 0
      self.yz = 0
      self.xyz = 0

images = images_class()

class CA_states:
   #
   # CA state definition class
   #
   def __init__(self):
      self.empty = 0
      self.interior = 1
      self.edge = (1 << 1) # 2
      self.north = (1 << 2) # 4
      self.west = (2 << 2) # 8
      self.east = (3 << 2) # 12
      self.south = (4 << 2) # 16
      self.stop = (5 << 2) # 20
      self.corner = (6 << 2) # 24

class rule_table:
   #
   # CA rule table class
   #
   # 0 = empty
   # 1 = interior
   # 2 = edge
   # edge+direction = start
   #
   def __init__(self):
      self.table = zeros(2**(9*2),uint32)
      self.s = CA_states()
      #
      # 1 0:
      #
      # 011
      # 111
      # 111
      self.add_rule(0,1,1,1,1,1,1,1,1,self.s.north)
      # 101
      # 111
      # 111
      self.add_rule(1,0,1,1,1,1,1,1,1,self.s.east)
      #
      # 2 0's:
      #
      # 001
      # 111
      # 111
      self.add_rule(0,0,1,1,1,1,1,1,1,self.s.east)
      # 100
      # 111
      # 111
      self.add_rule(1,0,0,1,1,1,1,1,1,self.s.east)
      # 010
      # 111
      # 111
      self.add_rule(0,1,0,1,1,1,1,1,1,self.s.east)
      # 011
      # 110
      # 111
      self.add_rule(0,1,1,1,1,0,1,1,1,self.s.south)
      # 110
      # 011
      # 111
      self.add_rule(1,1,0,0,1,1,1,1,1,self.s.east)
      # 101
      # 011
      # 111
      self.add_rule(1,0,1,0,1,1,1,1,1,self.s.east)
      # 101
      # 110
      # 111
      self.add_rule(1,0,1,1,1,0,1,1,1,self.s.south)
      # 011
      # 111
      # 110
      self.add_rule(0,1,1,1,1,1,1,1,0,self.s.corner)
      # 011
      # 111
      # 101
      self.add_rule(0,1,1,1,1,1,1,0,1,self.s.north)
      # 110
      # 111
      # 101
      self.add_rule(1,1,0,1,1,1,1,0,1,self.s.west)
      # 101
      # 111
      # 110
      self.add_rule(1,0,1,1,1,1,1,1,0,self.s.south)
      # 101
      # 111
      # 011
      self.add_rule(1,0,1,1,1,1,0,1,1,self.s.east)
      #
      # 3 0's:
      #
      # 001
      # 011
      # 111
      self.add_rule(0,0,1,0,1,1,1,1,1,self.s.east)
      # 010
      # 011
      # 111
      self.add_rule(0,1,0,0,1,1,1,1,1,self.s.east)
      # 010
      # 110
      # 111
      self.add_rule(0,1,0,1,1,0,1,1,1,self.s.south)
      # 010
      # 111
      # 011
      self.add_rule(0,1,0,1,1,1,0,1,1,self.s.east)
      # 010
      # 111
      # 110
      self.add_rule(0,1,0,1,1,1,1,1,0,self.s.south)
      # 110
      # 011
      # 011
      self.add_rule(1,1,0,0,1,1,0,1,1,self.s.east)
      # 011
      # 110
      # 110
      self.add_rule(0,1,1,1,1,0,1,1,0,self.s.south)
      # 101
      # 011
      # 011
      self.add_rule(1,0,1,0,1,1,0,1,1,self.s.east)
      # 101
      # 110
      # 110
      self.add_rule(1,0,1,1,1,0,1,1,0,self.s.south)
      # 011
      # 011
      # 011
      self.add_rule(0,1,1,0,1,1,0,1,1,self.s.north)
      #
      # 4 0's:
      #
      # 001
      # 011
      # 011
      self.add_rule(0,0,1,0,1,1,0,1,1,self.s.east)
      # 100
      # 110
      # 110
      self.add_rule(1,0,0,1,1,0,1,1,0,self.s.south)
      # 010
      # 011
      # 011
      self.add_rule(0,1,0,0,1,1,0,1,1,self.s.east)
      # 010
      # 110
      # 110
      self.add_rule(0,1,0,1,1,0,1,1,0,self.s.south)
      # 001
      # 110
      # 110
      self.add_rule(0,0,1,1,1,0,1,1,0,self.s.south)
      # 100
      # 011
      # 011
      self.add_rule(1,0,0,0,1,1,0,1,1,self.s.east)
      #
      # 5 0's:
      #
      # 000 
      # 011
      # 011
      self.add_rule(0,0,0,0,1,1,0,1,1,self.s.east)
      #
      # edge states
      #
      # 200
      # 211
      # 211
      self.add_rule(2,0,0,2,1,1,2,1,1,self.s.east+self.s.edge)
      # 201
      # 211
      # 211
      self.add_rule(2,0,1,2,1,1,2,1,1,self.s.east+self.s.edge)
      # 210
      # 211
      # 211
      self.add_rule(2,1,0,2,1,1,2,1,1,self.s.east+self.s.edge)
      # 002
      # 112
      # 112
      self.add_rule(0,0,2,1,1,2,1,1,2,self.s.stop)
      # 102
      # 112
      # 112
      self.add_rule(1,0,2,1,1,2,1,1,2,self.s.stop)
      # 002
      # 112
      # 102
      self.add_rule(0,0,2,1,1,2,1,0,2,self.s.stop)
      # 012
      # 112
      # 112
      self.add_rule(0,1,2,1,1,2,1,1,2,self.s.stop)
      # 012
      # 112
      # 102
      self.add_rule(0,1,2,1,1,2,1,0,2,self.s.stop)

   def add_rule(self,nw,nn,ne,ww,cc,ee,sw,ss,se,rule):
      #
      # add a CA rule, with rotations
      #
      s = CA_states()
      #
      # add the rule
      #
      state = \
         (nw <<  0) + (nn <<  2) + (ne <<  4) + \
         (ww <<  6) + (cc <<  8) + (ee << 10) + \
         (sw << 12) + (ss << 14) + (se << 16)
      self.table[state] = rule
      #
      # rotate 90 degrees
      # 
      state = \
         (sw <<  0) + (ww <<  2) + (nw <<  4) + \
         (ss <<  6) + (cc <<  8) + (nn << 10) + \
         (se << 12) + (ee << 14) + (ne << 16)
      if (rule == s.east):
         self.table[state] = s.south
      elif (rule == s.south):
         self.table[state] = s.west
      elif (rule == s.west):
         self.table[state] = s.north
      elif (rule == s.north):
         self.table[state] = s.east
      elif (rule == (s.east+s.edge)):
         self.table[state] = s.south+s.edge
      elif (rule == (s.south+s.edge)):
         self.table[state] = s.west+s.edge
      elif (rule == (s.west+s.edge)):
         self.table[state] = s.north+s.edge
      elif (rule == (s.north+s.edge)):
         self.table[state] = s.east+s.edge
      elif (rule == s.corner):
         self.table[state] = s.corner
      elif (rule == s.stop):
         self.table[state] = s.stop
      #
      # rotate 180 degrees
      # 
      state = \
         (se <<  0) + (ss <<  2) + (sw <<  4) + \
         (ee <<  6) + (cc <<  8) + (ww << 10) + \
         (ne << 12) + (nn << 14) + (nw << 16)
      if (rule == s.east):
         self.table[state] = s.west
      elif (rule == s.south):
         self.table[state] = s.north
      elif (rule == s.west):
         self.table[state] = s.east
      elif (rule == s.north):
         self.table[state] = s.south
      elif (rule == (s.east+s.edge)):
         self.table[state] = s.west+s.edge
      elif (rule == (s.south+s.edge)):
         self.table[state] = s.north+s.edge
      elif (rule == (s.west+s.edge)):
         self.table[state] = s.east+s.edge
      elif (rule == (s.north+s.edge)):
         self.table[state] = s.south+s.edge
      elif (rule == s.corner):
         self.table[state] = s.corner
      elif (rule == s.stop):
         self.table[state] = s.stop
      #
      # rotate 270 degrees
      # 
      state = \
         (ne <<  0) + (ee <<  2) + (se <<  4) + \
         (nn <<  6) + (cc <<  8) + (ss << 10) + \
         (nw << 12) + (ww << 14) + (sw << 16)
      if (rule == s.east):
         self.table[state] = s.north
      elif (rule == s.south):
         self.table[state] = s.east
      elif (rule == s.west):
         self.table[state] = s.south
      elif (rule == s.north):
         self.table[state] = s.west
      elif (rule == (s.east+s.edge)):
         self.table[state] = s.north+s.edge
      elif (rule == (s.south+s.edge)):
         self.table[state] = s.east+s.edge
      elif (rule == (s.west+s.edge)):
         self.table[state] = s.south+s.edge
      elif (rule == (s.north+s.edge)):
         self.table[state] = s.west+s.edge
      elif (rule == s.corner):
         self.table[state] = s.corner
      elif (rule == s.stop):
         self.table[state] = s.stop

def evaluate_state(arr):
   #
   # assemble the state bit strings
   #
   (ny, nx) = shape(arr)
   s = CA_states()
   nn = concatenate(([s.edge+zeros(nx,uint32)],arr[:(ny-1)]))
   ss = concatenate((arr[1:],[s.edge+zeros(nx,uint32)]))
   ww = concatenate((reshape(s.edge+zeros(ny,uint32),(ny,1)),arr[:,:(nx-1)]),1)
   ee = concatenate((arr[:,1:],reshape(s.edge+zeros(ny,uint32),(ny,1))),1)
   cc = arr
   nw = concatenate(([s.edge+zeros(nx,uint32)],ww[:(ny-1)]))
   ne = concatenate(([s.edge+zeros(nx,uint32)],ee[:(ny-1)]))
   sw = concatenate((ww[1:],[s.edge+zeros(nx,uint32)]))
   se = concatenate((ee[1:],[s.edge+zeros(nx,uint32)]))
   state = (nw <<  0) + (nn <<  2) + (ne <<  4) + \
            (ww <<  6) + (cc <<  8) + (ee << 10) + \
            (sw << 12) + (ss << 14) + (se << 16)
   return state

def vectorize_toolpaths(arr):
   #
   # convert lattice toolpath directions to vectors
   #
   s = CA_states()
   toolpaths = []
   max_dist = float(string_vector_error.get())
   start_sites = (arr == (s.north+s.edge)) | (arr == (s.south+s.edge)) | \
      (arr == (s.east+s.edge)) | (arr == (s.west+s.edge))
   num_start_sites = sum(sum(1.0*start_sites))
   path_sites = (arr == s.north) | (arr == s.south) | (arr == s.east) | \
      (arr == s.west)
   num_path_sites = sum(sum(1.0*path_sites))
   remaining_sites = num_start_sites + num_path_sites
   while (remaining_sites != 0):
      #print remaining_sites
      if (num_start_sites > 0):
         #
         # begin segment on a start state
         #
         if (argmax(start_sites[0,:],axis=0) != 0):
            x = argmax(start_sites[0,:],axis=0)
            y = 0
         elif (argmax(start_sites[:,0],axis=0) != 0):
            x = 0
            y = argmax(start_sites[:,0],axis=0)
         elif (argmax(start_sites[-1,:],axis=0) != 0):
            x = argmax(start_sites[-1,:],axis=0)
            y = cad.ny-1
         elif (argmax(start_sites[:,-1],axis=0) != 0):
            x = cad.nx-1
            y = argmax(start_sites[:,-1],axis=0)
         else:
            print "error: internal start"
            sys.exit()
         #print "start from ",x,y
      else:
         #
         # no start states; begin segment on upper-left boundary point
         #
         maxcols = argmax(path_sites,axis=1)
         y = argmax(argmax(path_sites,axis=1))
         x = maxcols[y]
         arr[y][x] += s.edge
         #print "segment from ",x,y
      segment = [point(x,y)]
      vector = [point(x,y)]
      while 1:
         #
         # follow path
         #
         y = vector[-1].y
         x = vector[-1].x
         state = arr[y][x]
         #
         # if start state, set stop
         #
         if (state == (s.north + s.edge)):
            state = s.north
            arr[y][x] = s.stop
         elif (state == (s.south + s.edge)):
            state = s.south
            arr[y][x] = s.stop
         elif (state == (s.east + s.edge)):
            state = s.east
            arr[y][x] = s.stop
         elif (state == (s.west + s.edge)):
            state = s.west
            arr[y][x] = s.stop
         #print "x,y,state,arr: ",x,y,state,arr[y][x]
         #
         # move if a valid direction
         #
         if (state == s.north):
            direction = "north"
            #print "north"
            ynew = y - 1
            xnew = x
         elif (state == s.south):
            direction = "south"
            #print "south"
            ynew = y + 1
            xnew = x
         elif (state == s.east):
            direction = "east"
            #print "east"
            ynew = y
            xnew = x + 1
         elif (state == s.west):
            direction = "west"
            #print "west"
            ynew = y
            xnew = x - 1
         elif (state == s.corner):
            #print "corner"
            if (direction == "east"):
               #print "south"
               xnew = x
               ynew = y + 1
            elif (direction == "west"):
               #print "north"
               xnew = x
               ynew = y - 1
            elif (direction == "north"):
               #print "east"
               ynew = y
               xnew = x + 1
            elif (direction == "south"):
               #print "west"
               ynew = y
               xnew = x - 1
         else:
            #
            # not a valid direction, terminate segment on previous point
            #
            print "unexpected path termination at",x,y
            #sys.exit()
            segment.append(point(x,y))
            toolpaths.append(segment)
            arr[y][x] = s.interior
            break
         #print "xnew,ynew,snew",xnew,ynew,arr[ynew][xnew]
         #
         # check if stop reached
         #
         if (arr[ynew][xnew] == s.stop):
            #print "stop at ",xnew,ynew
            segment.append(point(xnew,ynew))
            toolpaths.extend([segment])
            if (state != s.corner):
               arr[y][x] = s.interior
            arr[ynew][xnew] = s.interior
            break
         #
         # find max transverse distance from vector to new point
         #
         dmax = 0
         dx = xnew - vector[0].x
         dy = ynew - vector[0].y
         norm = sqrt(dx**2 + dy**2)
         nx = dy / norm
         ny = -dx / norm
         for i in range(len(vector)):
            dx = vector[i].x - vector[0].x
            dy = vector[i].y - vector[0].y
            d = abs(nx*dx + ny*dy)
            if (d > dmax):
               dmax = d
         #
         # start new vector if transverse distance > max_dist
         #
         if (dmax >= max_dist):
            #print "max at ",x,y
            segment.append(point(x,y))
            vector = [point(x,y)]
         #
         # otherwise add point to vector
         #
         else:
            #print "add ",xnew,ynew
            vector.append(point(xnew,ynew))
            if ((arr[y][x] != s.corner) & (arr[y][x] != s.stop)):
               arr[y][x] = s.interior
      start_sites = (arr == (s.north+s.edge)) | (arr == (s.south+s.edge)) | \
         (arr == (s.east+s.edge)) | (arr == (s.west+s.edge))
      num_start_sites = sum(sum(1.0*start_sites))
      path_sites = (arr == s.north) | (arr == s.south) | (arr == s.east) | \
         (arr == s.west)
      num_path_sites = sum(sum(1.0*path_sites))
      remaining_sites = num_start_sites + num_path_sites
   #
   # reverse segment order, to start from inside to out
   #
   newpaths = []
   for segment in range(len(toolpaths)):
      newpaths.append(toolpaths[-1-segment])
   root.update()
   return newpaths

def evaluate():
   #
   # evaluate .cad program/image
   #
   if (len(widget_cad_text.get("1.0",END)) > 1):
      #
      # .cad
      #
      cad.zlist = []
      cad_text_string = widget_cad_text.get("1.0",END)
      exec cad_text_string in globals()
      widget_function_text.config(state=NORMAL)
      widget_function_text.delete("1.0",END)
      widget_function_text.insert("1.0",cad.function)
      widget_function_text.config(state=DISABLED)
   if (cad.image_r.size > 1):
      #
      # image 
      #
      cad.xmin = float(string_image_xmin.get())
      xwidth = float(string_image_xwidth.get())
      cad.xmax = cad.xmin + xwidth
      cad.ymin = float(string_image_ymin.get())
      yheight = float(string_image_yheight.get())
      cad.ymax = cad.ymin + yheight
      cad.image_min = float(string_image_min.get())
      cad.image_max = float(string_image_max.get())
      cad.zmin = float(string_image_zmin.get())
      cad.zmax = float(string_image_zmax.get())
      cad.nz = int(string_image_nz.get())
      cad.inches_per_unit = float(string_image_units.get())

def render(view='xyzr'):
   render_stop_flag = 0
   cad.stop = 0
   #
   # if .cad doesn't call render, delete windows and add stop button
   #
   if (find(widget_cad_text.get("1.0",END),"render(") == -1):
      string_msg.set("render ...")
      widget_stop.pack()
      delete_windows()
   #
   # initialize variables
   #
   cad.toolpaths = []
   rx = pi*cad.rx/180.
   rz = pi*cad.rz/180.
   r = rule_table()
   s = CA_states()
   #
   # evaluate coordinate arrays
   #
   Xarray = outer(ones((cad.ny,1)),cad.xmin+(cad.xmax-cad.xmin)*arange(cad.nx)/(cad.nx-1.0))
   Yarray = outer(cad.ymin+(cad.ymax-cad.ymin)*arange(cad.ny-1,-1,-1)/(cad.ny-1.0),ones((1,cad.nx)))
   if (cad.zlist == []):
      if ((cad.nz == 1) & (cad.image_r.size != 1)):
         cad.zlist = [cad.zmax]
         cad.view('xy')
      elif (cad.nz == 1):
         cad.zlist = [cad.zmin]
         cad.view('xy')
      else:
         cad.zlist = cad.zmin + (cad.zmax-cad.zmin)*arange(cad.nz)/(cad.nz-1.0)
         cad.view('xyzr')
   else:
      cad.nz = len(cad.zlist)
      cad.zmin = cad.zlist[0]
      cad.zmax = cad.zlist[-1]
   #
   # draw orthogonal views
   #
   X = Xarray
   Y = Yarray
   accum_r = zeros((cad.ny,cad.nx),uint32)
   accum_g = zeros((cad.ny,cad.nx),uint32)
   accum_b = zeros((cad.ny,cad.nx),uint32)
   im.intensity_yz = zeros((cad.ny,cad.nz),uint32)
   im.intensity_xz = zeros((cad.nz,cad.nx),uint32)
   im.intensity_xyz = zeros((cad.nz,cad.nx),uint32)
   for layer in range(cad.nz):
      #
      # check render stop button
      #
      if (cad.stop == 1):
         break
      #
      # xy view
      #
      Z = cad.zlist[layer]
      string_msg.set("render z = %.3f"%Z)
      # root.update()
      if (cad.image_r.size == 1):
         #
         # .cad
         #
         array_r = eval(cad.function)
         array_g = array_r
         array_b = array_r
         if ((cad.zmax == cad.zmin) | (cad.nz == 1)):
            zi = array([255],uint32)
         else:
            zi = array([55.0 + 200.0*layer/(cad.nz-1.0)],uint32)
         accum_r = where(((zi*array_r) > accum_r),(zi*array_r),accum_r)
         accum_g = where(((zi*array_g) > accum_g),(zi*array_g),accum_g)
         accum_b = where(((zi*array_b) > accum_b),(zi*array_b),accum_b)
         im.intensity_xy = (1 << 16)*accum_b + (1 << 8)*accum_g + (1 << 0)*accum_r
      else:
         #
         # bitmap
         #
         array_r = (cad.image_r[0,] >= (cad.image_min + (cad.image_max-cad.image_min)*(Z-cad.zmin)/float(cad.zmax-cad.zmin)))
         array_g = (cad.image_g[0,] >= (cad.image_min + (cad.image_max-cad.image_min)*(Z-cad.zmin)/float(cad.zmax-cad.zmin)))
         array_b = (cad.image_b[0,] >= (cad.image_min + (cad.image_max-cad.image_min)*(Z-cad.zmin)/float(cad.zmax-cad.zmin)))
         image_z = int(cad.image_min + (cad.image_max-cad.image_min)*(Z-cad.zmin)/float(cad.zmax-cad.zmin))
         intensity_r = where((cad.image_r[0,] <= image_z),cad.image_r[0,],image_z)
         intensity_g = where((cad.image_g[0,] <= image_z),cad.image_g[0,],image_z)
         intensity_b = where((cad.image_b[0,] <= image_z),cad.image_b[0,],image_z)
         im.intensity_xy = (1 << 16)*intensity_b + (1 << 8)*intensity_g + (1 << 0)*intensity_r
      im.xy = Image.fromarray(im.intensity_xy,mode="RGBX")
      im.xy_draw = ImageDraw.Draw(im.xy)
      im.xy = im.xy.resize((cad.nxplot(),cad.nyplot()))
      images.xy = ImageTk.PhotoImage(im.xy)
      canvas_xy.create_image(cad.nplot/2,cad.nplot/2,image=images.xy)
      # root.update()
      #
      # find toolpaths if needed
      #
      ncontours = int(string_num_contours.get())
      if (ncontours == -1):
         ncontours = 2**20 # a big number
      cad.toolpaths.append([])
      """
      if (ncontours != 0):
         #
         # grassfire convolve (to come)
         #
         interior = (array_r | array_g | array_b)
         print shape(X[interior])
         conv_array = interior
      """
      for contour in range(ncontours):
         #
         # check render stop button
         #
         if (cad.stop == 1):
            break
         #
         # convolve tool for contour
         #
         string_msg.set(" convolve tool ... ")
         #
         # FFT convolve
         #
         # root.update()
         tool_rad = float(string_tool_dia.get())/2.0
         tool_dia = float(string_tool_dia.get())
         tool_overlap = float(string_tool_overlap.get())
         kernel_rad = tool_rad + contour*tool_overlap*tool_dia
         ikernel_rad = 1 + int(cad.nx*kernel_rad/(cad.xmax-cad.xmin))
         if (ikernel_rad > (((cad.nx/2),(cad.ny/2))[(cad.ny/2) > (cad.nx/2)])):
            break
         kx = 1+outer(ones((2*ikernel_rad,1)),arange(2*ikernel_rad))
         ky = 1+outer(arange(2*ikernel_rad),ones((1,2*ikernel_rad)))
         k = (((kx-ikernel_rad)**2 + (ky-ikernel_rad)**2) < ikernel_rad**2).astype('uint32')
         interior = (array_r == s.interior).astype('uint32')
         #tstart = time.time()
         conv = scipy.signal.signaltools.fftconvolve(interior,k,mode='same')
         conv = where(conv > 0.01,s.interior,0)
         conv_array = conv + (conv != s.interior)*array_r
         #tend = time.time()
         #print 'convolve:',tend-tstart
         #
         # use CA rule table to find edge directions
         #
         string_msg.set("  follow edges ... ")
         # root.update()
         state = evaluate_state(conv_array)
         toolpath = r.table[state]
         tool_array = toolpath + (toolpath == s.empty)*conv_array
         tool_intensity = \
              ((0 << 16) +   (0 << 8) +   (0 << 0))*(tool_array == s.empty).astype('uint32') +\
            ((255 << 16) + (255 << 8) + (255 << 0))*(tool_array == s.interior).astype('uint32') +\
            ((  0 << 16) + (  0 << 8) + (255 << 0))*(tool_array == s.north).astype('uint32') +\
            ((  0 << 16) + (255 << 8) + (  0 << 0))*(tool_array == s.south).astype('uint32') +\
            ((255 << 16) + (  0 << 8) + (  0 << 0))*(tool_array == s.east).astype('uint32') +\
            ((  0 << 16) + (255 << 8) + (255 << 0))*(tool_array == s.west ).astype('uint32') +\
            ((128 << 16) + (  0 << 8) + (128 << 0))*(tool_array == s.stop).astype('uint32')

         #
         # show CA
         #
         """
         im.xy = Image.fromarray(tool_intensity,mode="RGBX")
         im.xy = im.xy.resize((cad.nplot,cad.nplot))
         images.xy = ImageTk.PhotoImage(im.xy)
         canvas_xy.create_image(cad.nplot/2,cad.nplot/2,image=images.xy)
         """
         #
         # vectorize contour
         #
         #tstart = time.time()
         string_msg.set("    vectorize ...    ")
         # root.update()
         new_paths = vectorize_toolpaths(tool_array)
         if (len(new_paths) == 0):
            break
         cad.toolpaths[layer].extend(new_paths)
         #tend = time.time()
         #print 'vector:',tend-tstart
         #
         # draw toolpath
         #
         im.xy_draw = ImageDraw.Draw(im.xy)
         for segment in range(len(cad.toolpaths[layer])):
            x = cad.nxplot()*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx)
            y = cad.nyplot()*(cad.toolpaths[layer][segment][0].y+0.5)/float(cad.ny)
            for vertex in range(1,len(cad.toolpaths[layer][segment])):
               xnew = cad.nxplot()*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx)
               ynew = cad.nyplot()*(cad.toolpaths[layer][segment][vertex].y+0.5)/float(cad.ny)
               im.xy_draw.line([x,y,xnew,ynew],fill="#ffa0a0",width=1)
               x = xnew
               y = ynew
         #
         # show xy toolpath view
         #
         images.xy = ImageTk.PhotoImage(im.xy)
         canvas_xy.create_image(cad.nplot/2,cad.nplot/2,image=images.xy)
         #
         # add send_to button
         #
         string_send_to_time.set("")
         send_to_frame.pack()
         # root.update()
      #
      # draw labels
      #
      for label in range(len(cad.labels)):
         x = cad.nplot/2. + cad.nxplot()*(cad.labels[label].x-(cad.xmax+cad.xmin)/2.0)/(cad.xmax-cad.xmin)
         y = cad.nplot/2. - cad.nyplot()*(cad.labels[label].y-(cad.ymax+cad.ymin)/2.0)/(cad.ymax-cad.ymin)
         string = cad.labels[label].text
         size = cad.labels[label].size
         color = cad.labels[label].color
         anch = cad.labels[label].anchor
         canvas_xy.create_text(x,y,text=string,font=('arial',size,'bold'),fill=color,anchor=anch,justify=CENTER)
      #
      # draw origin
      #
      x0 = cad.nplot/2. + cad.nxplot()*(0-(cad.xmax+cad.xmin)/2.)/(cad.xmax-cad.xmin)
      y0 = cad.nplot/2. - cad.nyplot()*(0-(cad.ymax+cad.ymin)/2.)/(cad.ymax-cad.ymin)
      dxy = .025*cad.nplot
      canvas_xy.create_line([x0-dxy,y0,x0+dxy,y0],fill="green")
      canvas_xy.create_line([x0,y0-dxy,x0,y0+dxy],fill="green")
      #
      # yz view
      #
      if (cad.views == 'xyzr'):
         accum_yz_r = zeros(cad.ny,uint32)
         accum_yz_g = zeros(cad.ny,uint32)
         accum_yz_b = zeros(cad.ny,uint32)
         for vertex in range(cad.nx):
            xi = array([55.0 + 200.0*vertex/(cad.nx-1.0)],uint32)
            slice_r = array_r[:,vertex]
            slice_g = array_g[:,vertex]
            slice_b = array_b[:,vertex]
            accum_yz_r = where(((xi*slice_r) >= accum_yz_r),(xi*slice_r),accum_yz_r)
            accum_yz_g = where(((xi*slice_g) >= accum_yz_g),(xi*slice_g),accum_yz_g)
            accum_yz_b = where(((xi*slice_b) >= accum_yz_b),(xi*slice_b),accum_yz_b)
         im.intensity_yz[:,layer] = (1 << 16)*accum_yz_b + (1 << 8)*accum_yz_g + (1 << 0)*accum_yz_r
         im.yz = Image.fromarray(im.intensity_yz,mode="RGBX")
         im.yz = im.yz.transpose(Image.FLIP_LEFT_RIGHT)
         im.yz = im.yz.resize((cad.nzplot(),cad.nyplot()))
         images.yz = ImageTk.PhotoImage(im.yz)
         canvas_yz.create_image(cad.nplot/2,cad.nplot/2,image=images.yz)
         #
         # draw origin
         #
         z0 = cad.nplot/2. - cad.nzplot()*(0-(cad.zmax+cad.zmin)/2.)/(cad.zmax-cad.zmin)
         y0 = cad.nplot/2. - cad.nyplot()*(0-(cad.ymax+cad.ymin)/2.)/(cad.ymax-cad.ymin)
         canvas_yz.create_line([z0-dxy,y0,z0+dxy,y0],fill="green")
         canvas_yz.create_line([z0,y0-dxy,z0,y0+dxy],fill="green")
      #
      # xz view
      #
      if (cad.views == 'xyzr'):
         accum_xz_r = zeros(cad.nx,uint32)
         accum_xz_g = zeros(cad.nx,uint32)
         accum_xz_b = zeros(cad.nx,uint32)
         for vertex in range(cad.ny):
            yi = array([55.0+200.0*vertex/(cad.ny-1.0)],uint32)
            slice_r = array_r[vertex,:]
            slice_g = array_g[vertex,:]
            slice_b = array_b[vertex,:]
            accum_xz_r = where(((yi*slice_r) >= accum_xz_r),(yi*slice_r),accum_xz_r)
            accum_xz_g = where(((yi*slice_g) >= accum_xz_g),(yi*slice_g),accum_xz_g)
            accum_xz_b = where(((yi*slice_b) >= accum_xz_b),(yi*slice_b),accum_xz_b)
         im.intensity_xz[(cad.nz-1-layer),:] = (1 << 16)*accum_xz_b + (1 << 8)*accum_xz_g + (1 << 0)*accum_xz_r
         im.xz = Image.fromarray(im.intensity_xz,mode="RGBX")
         im.xz = im.xz.resize((cad.nxplot(),cad.nzplot()))
         images.xz = ImageTk.PhotoImage(im.xz)
         canvas_xz.create_image(cad.nplot/2,cad.nplot/2,image=images.xz)
         #
         # draw origin
         #
         x0 = cad.nplot/2. + cad.nxplot()*(0-(cad.xmax+cad.xmin)/2.)/(cad.xmax-cad.xmin)
         z0 = cad.nplot/2. - cad.nzplot()*(0-(cad.zmax+cad.zmin)/2.)/(cad.zmax-cad.zmin)
         canvas_xz.create_line([x0-dxy,z0,x0+dxy,z0],fill="green")
         canvas_xz.create_line([x0,z0-dxy,x0,z0+dxy],fill="green")
      #
      # draw it
      #
      root.update()
   #
   # rotated view
   #
   if ((cad.views == 'xyzr') & (cad.image_r.size == 1)):
      accum = zeros((cad.ny,cad.nx),uint32)
      for z in cad.zlist:
         #
         # check render stop button
         #
         if (cad.stop == 1):
            break
         string_msg.set("render z = %.3f"%z)
         dY = cos(rx)*(Yarray-(cad.ymax+cad.ymin)/2.0) - sin(rx)*(z-(cad.zmax+cad.zmin)/2.0)
         Z = (cad.zmax+cad.zmin)/2.0 + sin(rx)*(Yarray-(cad.ymax+cad.ymin)/2.0) + cos(rx)*(z-(cad.zmax+cad.zmin)/2.0)
         X = (cad.xmax+cad.xmin)/2.0 + cos(rz)*(Xarray-(cad.xmax+cad.xmin)/2.0) - sin(rz)*dY
         Y = (cad.ymax+cad.ymin)/2.0 + sin(rz)*(Xarray-(cad.xmax+cad.xmin)/2.0) + cos(rz)*dY
         arr = eval(cad.function)
         if (cad.zmax == cad.zmin):
            zi = array([255],uint32)
         else:
            zi = array([55.0 + 200.0*(z-cad.zmin)/(cad.zmax-cad.zmin)],uint32)
         accum = where(((zi*arr) > accum),(zi*arr),accum)
         im.intensity_xyz = ((1 << 16) + (1 << 8) + (1 << 0)) * accum
         im.xyz = Image.fromarray(im.intensity_xyz,mode="RGBX")
         im.xyz = im.xyz.resize((cad.nxplot(),cad.nyplot()))
         images.xyz = ImageTk.PhotoImage(im.xyz)
         canvas_xyz.create_image(cad.nplot/2,cad.nplot/2,image=images.xyz)
         root.update()
   #
   # return
   #
   cad.zwrite = cad.zlist
   cad.zlist = []
   widget_stop.pack_forget()
   string_msg.set("done")
   root.update()
   return

def draw_toolpath():
   im.xy = Image.new("RGBX",(cad.nxplot(),cad.nyplot()),'white')
   im.xy_draw = ImageDraw.Draw(im.xy)
   for layer in range(len(cad.toolpaths)):
      for segment in range(len(cad.toolpaths[layer])):
         x = cad.nxplot()*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx)
         y = cad.nyplot()*(cad.toolpaths[layer][segment][0].y+0.5)/float(cad.ny)
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            xnew = cad.nxplot()*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx)
            ynew = cad.nyplot()*(cad.toolpaths[layer][segment][vertex].y+0.5)/float(cad.ny)
            im.xy_draw.line([x,y,xnew,ynew],fill="black")
            x = xnew
            y = ynew
   images.xy = ImageTk.PhotoImage(im.xy)
   canvas_xy.create_image(cad.nplot/2,cad.nplot/2,image=images.xy)

def delete_windows():
   im.xy = Image.new("RGBX",(cad.nplot,cad.nplot),'black')
   images.xy = ImageTk.PhotoImage(im.xy)
   canvas_xy.create_image(cad.nplot/2,cad.nplot/2,image=images.xy)
   im.yz = Image.new("RGBX",(cad.nplot,cad.nplot),'black')
   images.yz = ImageTk.PhotoImage(im.yz)
   canvas_yz.create_image(cad.nplot/2,cad.nplot/2,image=images.yz)
   im.xz = Image.new("RGBX",(cad.nplot,cad.nplot),'black')
   images.xz = ImageTk.PhotoImage(im.xz)
   canvas_xz.create_image(cad.nplot/2,cad.nplot/2,image=images.xz)
   im.xyz = Image.new("RGBX",(cad.nplot,cad.nplot),'black')
   images.xyz = ImageTk.PhotoImage(im.xyz)
   canvas_xyz.create_image(cad.nplot/2,cad.nplot/2,image=images.xyz)
   root.update()

def select_cad():
   image_x_frame.pack_forget()
   image_y_frame.pack_forget()
   image_z_frame.pack_forget()
   image_intensity_frame.pack_forget()
   image_units_frame.pack_forget()
   image_invert_frame.pack_forget()
   cad_input_frame.pack_forget()
   widget_cad_text.delete("1.0",END)
   widget_cad_text.insert("1.0",cad_template)
   editor_frame.pack()
   cad.image = array(0)
   cad_input_frame.pack()
   cad.toolpaths = []
   string_num_contours.set('0')
   widget_cad_save.pack(side='left')
   delete_windows()

def select_image():
   editor_frame.pack_forget()
   cad_input_frame.pack_forget()
   image_x_frame.pack()
   image_y_frame.pack()
   image_z_frame.pack()
   image_intensity_frame.pack()
   image_units_frame.pack()
   image_invert_frame.pack()
   cad_input_frame.pack()
   cad.toolpaths = []
   string_num_contours.set('0')
   widget_cad_save.pack_forget()
   delete_windows()

def input_open():
   filename = askopenfilename()
   string_input_file.set(filename)
   if (find(filename,'.cad') != -1):
      cad_load(0)
   elif ((find(filename,'.jpg') != -1) | (find(filename,'.JPG') != -1) |
      (find(filename,'.png') != -1) | (find(filename,'.PNG') != -1) |
      (find(filename,'.gif') != -1) | (find(filename,'.GIF') != -1)):
      widget_cad_text.delete("1.0",END)
      image_load(0)
   else:
      string_msg.set("unsupported input file format")
      root.update()
      
def cad_load(event):
   global cad
   cad = cad_variables()
   cam_pack_forget()
   select_cad()
   input_file_name = string_input_file.get()
   input_file = open(input_file_name,'rb')
   cad_text_string = input_file.read()
   widget_cad_text.delete("1.0",END)
   widget_cad_text.insert("1.0",cad_text_string)
   input_file.close()
   cad.toolpaths = []
   cad.image = array(0)
   cad.nz = 1
   string_num_contours.set('0')
   evaluate()
   if (find(widget_cad_text.get("1.0",END),"render(") == -1):
      render()

def image_load(event):
   global cad
   cad = cad_variables()
   cam_pack_forget()
   select_image()
   function_string_frame.pack_forget()
   input_file_name = string_input_file.get()
   input_file = open(input_file_name,'rb')
   input_file.close()
   cad.toolpaths = []
   string_num_contours.set('0')
   image = Image.open(input_file_name)
   num_layers = 1
   while 1: # check number of layers
      try:
         image.seek(image.tell()+1)
         num_layers += 1
      except:
         break
   image = Image.open(input_file_name)
   if image.mode != "RGBX":
      image = image.convert("RGBX")
   (cad.nx,cad.ny) = image.size
   info = image.info
   if ('dpi' in info):
      (xdpi,ydpi) = info['dpi']
   else:
      xdpi = cad.nx
      ydpi = xdpi
   string_image_nx.set(" nx = "+str(cad.nx))
   string_image_ny.set(" ny = "+str(cad.ny))
   cad.nz = 1
   string_image_nz.set(str(cad.nz))
   cad.xmin = 0
   string_image_xmin.set('0')
   cad.xmax = cad.nx/float(xdpi)
   string_image_xwidth.set(str(cad.xmax-cad.xmin))
   cad.ymin = 0
   string_image_ymin.set('0')
   cad.ymax = cad.ny/float(ydpi)
   string_image_yheight.set(str(cad.ymax-cad.ymin))
   cad.zmin = -.005
   string_image_zmin.set('-0.05')
   cad.zmax = 0.05
   string_image_zmax.set('0.05')
   cad.inches_per_unit = 1.0
   string_image_units.set('25.4')
   data = zeros((num_layers,cad.nx*cad.ny,3),uint32)
   data[0,] = array(image.convert("RGB").getdata(),uint32)
   for layer in range(1,num_layers):
      image.seek(image.tell()+1)
      data[layer,] = array(image.convert("RGB").getdata(),uint32)
   cad.image_r = array(data[:,:,0],uint32)
   cad.image_r = cad.image_r.reshape((num_layers,cad.ny,cad.nx))
   cad.image_g = array(data[:,:,1],uint32)
   cad.image_g = cad.image_g.reshape((num_layers,cad.ny,cad.nx))
   cad.image_b = array(data[:,:,2],uint32)
   cad.image_b = cad.image_b.reshape((num_layers,cad.ny,cad.nx))
   cad.image_min = 1
   string_image_min.set(str(cad.image_min))
   cad.image_max = 255
   string_image_max.set(str(cad.image_max))
   evaluate()
   render()

def invert_image(event):
   cad.image_r = 255 - cad.image_r
   cad.image_g = 255 - cad.image_g
   cad.image_b = 255 - cad.image_b
   evaluate()
   render()

def cad_save(event):
   input_file_name = string_input_file.get()
   input_file = open(input_file_name,'wb')
   cad_text_string = widget_cad_text.get("1.0",END)
   input_file.write(cad_text_string)
   input_file.close()
   string_msg.set(input_file_name+" saved")
   root.update()

def render_button(event):
   cam_pack_forget()
   cad.cam = ''
   if (cad.image_r.size == 1):
      function_string_frame.pack()
   cad.toolpaths = []
   string_num_contours.set('0')
   evaluate()
   if (find(widget_cad_text.get("1.0",END),"render(") == -1):
      render()

def render_stop(event):
   cad.stop = 1
   widget_stop.pack_forget()
      
def cam(event):
   function_string_frame.pack_forget()
   cam_file_frame.pack()
   string_num_contours.set('1')
   root.update()

def contour(event):
   evaluate()
   if (find(widget_cad_text.get("1.0",END),"render(") == -1):
      render()

def triangulate(event):
   #
   # triangulate for STL
   #
   # evaluate .cad
   #
   evaluate()
   #
   # initialize variables
   #
   render_stop_flag = 0
   cad.stop = 0
   widget_stop.pack()
   delete_windows()
   cad.toolpaths = []
   cad.zwrite = []
   cad.x = zeros(0)
   cad.y = zeros(0)
   cad.z = zeros(0)
   ixlr = array([])
   iylrs = array([])
   iylre = array([])
   izlr = array([])
   ixfbs = array([])
   ixfbe = array([])
   iyfb = array([])
   izfb = array([])
   ixtbs = array([])
   ixtbe = array([])
   iytb = array([])
   iztb = array([])
   #
   # evaluate coordinate arrays
   #
   (IY,IX) = indices((cad.ny,cad.nx))
   IY = IY[::-1,:]
   X = cad.xmin+(cad.xmax-cad.xmin)*IX/(cad.nx-1.0)
   Y = cad.ymin+(cad.ymax-cad.ymin)*IY/(cad.ny-1.0)
   cad.zwrite = cad.zmin + (cad.zmax-cad.zmin)*arange(cad.nz)/(cad.nz-1.0)
   #
   # set up drawing images
   #
   im.xy = Image.new("RGBX",(cad.nxplot(),cad.nyplot()),'white')
   im.xy_draw = ImageDraw.Draw(im.xy)
   im.xz = Image.new("RGBX",(cad.nxplot(),cad.nzplot()),'white')
   im.xz_draw = ImageDraw.Draw(im.xz)
   im.yz = Image.new("RGBX",(cad.nzplot(),cad.nyplot()),'white')
   im.yz_draw = ImageDraw.Draw(im.yz)
   #
   # loop over layers
   #
   Z = cad.zwrite[0]
   array0 = eval(cad.function)
   Z = cad.zwrite[1]
   array1 = eval(cad.function)
   for layer in range(2,len(cad.zwrite)):
      #
      # check render stop button
      #
      if (cad.stop == 1):
         break
      #
      # evaluate new layer
      #
      Z = cad.zwrite[layer]
      string_msg.set("triangulate z = %.3f"%Z)
      root.update()
      array2 = eval(cad.function)
      #
      # find left faces and merge y
      #
      elements = hstack((reshape((array1[:,0] == True),(cad.ny,1)),((array1[:,1:] == True) & (array1[:,:-1] == False))))
      starts = vstack((((elements[:-1,:] == True) & (elements[1:,:] == False)),reshape((elements[-1,:] == True),(1,cad.nx))))
      ends = vstack((reshape((elements[0,:] == True),(1,cad.nx)),((elements[1:,:] == True) & (elements[:-1,:] == False))))
      IY_t = transpose(IY) # for starts and ends to be read in same row
      IX_t = transpose(IX)
      starts_t = transpose(starts)
      ends_t = transpose(ends)
      ixlr = append(ixlr,IX_t[starts_t])
      iylrs = append(iylrs,IY_t[starts_t])
      iylre = append(iylre,1+IY_t[ends_t])
      izlr = append(izlr,(layer-1)*ones(len(IX_t[starts_t])))
      #
      # find right faces and merge y
      #
      elements = hstack((((array1[:,1:] == False) & (array1[:,:-1] == True)),reshape((array1[:,1] == True),(cad.ny,1))))
      starts = vstack((((elements[:-1,:] == True) & (elements[1:,:] == False)),reshape((elements[-1,:] == True),(1,cad.nx))))
      ends = vstack((reshape((elements[0,:] == True),(1,cad.nx)),((elements[1:,:] == True) & (elements[:-1,:] == False))))
      IY_t = transpose(IY) # for starts and ends to be read in same row
      IX_t = transpose(IX)
      starts_t = transpose(starts)
      ends_t = transpose(ends)
      ixlr = append(ixlr,1+IX_t[starts_t])
      iylre = append(iylre,IY_t[starts_t])
      iylrs = append(iylrs,1+IY_t[ends_t])
      izlr = append(izlr,(layer-1)*ones(len(IX_t[starts_t])))
      #
      # find front faces and merge x
      #
      elements = vstack((((array1[:-1,:] == True) & (array1[1:,:] == False)),reshape((array1[0,:] == True),(1,cad.nx))))
      starts = hstack((reshape((elements[:,0] == True),(cad.ny,1)),((elements[:,1:] == True) & (elements[:,:-1] == False))))
      ends = hstack((((elements[:,:-1] == True) & (elements[:,1:] == False)),reshape((elements[:,-1] == True),(cad.ny,1))))
      ixfbs = append(ixfbs,IX[starts])
      ixfbe = append(ixfbe,1+IX[ends])
      iyfb = append(iyfb,IY[starts])
      izfb = append(izfb,(layer-1)*ones(len(IX[starts])))
      #
      # find back faces and merge x
      #
      elements = vstack((reshape((array1[-1,:] == True),(1,cad.nx)),((array1[1:,:] == True) & (array1[:-1,:] == False))))
      starts = hstack((reshape((elements[:,0] == True),(cad.ny,1)),((elements[:,1:] == True) & (elements[:,:-1] == False))))
      ends = hstack((((elements[:,:-1] == True) & (elements[:,1:] == False)),reshape((elements[:,-1] == True),(cad.ny,1))))
      ixfbe = append(ixfbe,IX[starts])
      ixfbs = append(ixfbs,1+IX[ends])
      iyfb = append(iyfb,1+IY[starts])
      izfb = append(izfb,(layer-1)*ones(len(IX[starts])))
      #
      # find top faces and merge x
      #
      elements = ((array2 == False) & (array1 == True))
      starts = hstack((reshape((elements[:,0] == True),(cad.ny,1)),((elements[:,1:] == True) & (elements[:,:-1] == False))))
      ends = hstack((((elements[:,:-1] == True) & (elements[:,1:] == False)),reshape((elements[:,-1] == True),(cad.ny,1))))
      ixtbs = append(ixtbs,IX[starts])
      ixtbe = append(ixtbe,1+IX[ends])
      iytb = append(iytb,IY[starts])
      iztb = append(iztb,layer*ones(len(IX[starts])))
      #
      # find bottom faces and merge x
      #
      elements = ((array0 == False) & (array1 == True))
      starts = hstack((reshape((elements[:,0] == True),(cad.ny,1)),((elements[:,1:] == True) & (elements[:,:-1] == False))))
      ends = hstack((((elements[:,:-1] == True) & (elements[:,1:] == False)),reshape((elements[:,-1] == True),(cad.ny,1))))
      ixtbe = append(ixtbe,IX[starts])
      ixtbs = append(ixtbs,1+IX[ends])
      iytb = append(iytb,IY[starts])
      iztb = append(iztb,(layer-1)*ones(len(IX[starts])))
      #
      # push array stack
      #
      array0 = array1
      array1 = array2
   #
   # z merge front/back faces
   #
   index = lexsort(keys=(izfb,ixfbe,ixfbs,iyfb))
   merge = (iyfb[index[1:]] == iyfb[index[:-1]]) & \
             (ixfbe[index[1:]] == ixfbe[index[:-1]]) & \
             (ixfbs[index[1:]] == ixfbs[index[:-1]]) & \
             ((izfb[index[1:]] - izfb[index[:-1]]) == 1)
   merge = append(False,merge).astype(bool_)
   starts = ((merge[1:] == True) & (merge[:-1] == False))
   starts = append(starts,False).astype(bool_)
   ends = ((merge[1:] == False) & (merge[:-1] == True))
   if (merge[-1] == True):
      ends = append(ends,True)
   else:
      ends = append(ends,False)
   ends = ends.astype(bool_)
   xs = ixfbs[index][starts | ~merge]
   xe = ixfbe[index][starts | ~merge]
   y = iyfb[index][starts | ~merge]
   zs = izfb[index][starts | ~merge]
   ze = izfb[index][ends | ~(merge | starts)]+1
   cad.x = ravel(transpose(vstack((xs,xe,xs,xs,xe,xe))))
   cad.y = ravel(transpose(vstack((y,y,y,y,y,y))))
   cad.z = ravel(transpose(vstack((zs,ze,ze,zs,zs,ze))))
   #
   # z merge left/right faces
   #
   index = lexsort(keys=(izlr,iylre,iylrs,ixlr))
   merge = (ixlr[index[1:]] == ixlr[index[:-1]]) & \
             (iylre[index[1:]] == iylre[index[:-1]]) & \
             (iylrs[index[1:]] == iylrs[index[:-1]]) & \
             ((izlr[index[1:]] - izlr[index[:-1]]) == 1)
   merge = append(False,merge).astype(bool_)
   starts = ((merge[1:] == True) & (merge[:-1] == False))
   starts = append(starts,False).astype(bool_)
   ends = ((merge[1:] == False) & (merge[:-1] == True))
   if (merge[-1] == True):
      ends = append(ends,True)
   else:
      ends = append(ends,False)
   ends = ends.astype(bool_)
   x = ixlr[index][starts | ~merge]
   ys = iylrs[index][starts | ~merge]
   ye = iylre[index][starts | ~merge]
   zs = izlr[index][starts | ~merge]
   ze = izlr[index][ends | ~(merge | starts)]+1
   cad.x = append(cad.x,ravel(transpose(vstack((x,x,x,x,x,x)))))
   cad.y = append(cad.y,ravel(transpose(vstack((ys,ye,ys,ys,ye,ye)))))
   cad.z = append(cad.z,ravel(transpose(vstack((zs,ze,ze,zs,zs,ze)))))
   #
   # y merge top/bottom faces
   #
   index = lexsort(keys=(iytb,ixtbe,ixtbs,iztb))
   merge = (iztb[index[1:]] == iztb[index[:-1]]) & \
             (ixtbe[index[1:]] == ixtbe[index[:-1]]) & \
             (ixtbs[index[1:]] == ixtbs[index[:-1]]) & \
             ((iytb[index[1:]] - iytb[index[:-1]]) == 1)
   merge = append(False,merge).astype(bool_)
   starts = ((merge[1:] == True) & (merge[:-1] == False))
   starts = append(starts,False).astype(bool_)
   ends = ((merge[1:] == False) & (merge[:-1] == True))
   if (merge[-1] == True):
      ends = append(ends,True)
   else:
      ends = append(ends,False)
   ends = ends.astype(bool_)
   xs = ixtbs[index][starts | ~merge]
   xe = ixtbe[index][starts | ~merge]
   ys = iytb[index][starts | ~merge]
   ye = iytb[index][ends | ~(merge | starts)]+1
   z = iztb[index][starts | ~merge]
   cad.x = append(cad.x,ravel(transpose(vstack((xs,xe,xs,xs,xe,xe)))))
   cad.y = append(cad.y,ravel(transpose(vstack((ys,ye,ye,ys,ys,ye)))))
   cad.z = append(cad.z,ravel(transpose(vstack((z,z,z,z,z,z)))))
   #
   # draw triangulation
   #
   widget_stop.pack_forget()
   string_msg.set("draw ...")
   root.update()
   N = len(cad.x)
   for i in range(0,N,3):
      string_msg.set("draw triangle %d/%d"%(i/3,N/3))
      root.update()
      x0 = cad.nxplot()*(cad.x[i]+0.5)/float(cad.nx)
      y0 = cad.nyplot()*(cad.ny-cad.y[i]+0.5)/float(cad.ny)
      z0 = cad.nzplot()*(cad.nz-cad.z[i]+0.5)/float(cad.nz)
      x1 = cad.nxplot()*(cad.x[i+1]+0.5)/float(cad.nx)
      y1 = cad.nyplot()*(cad.ny-cad.y[i+1]+0.5)/float(cad.ny)
      z1 = cad.nzplot()*(cad.nz-cad.z[i+1]+0.5)/float(cad.nz)
      x2 = cad.nxplot()*(cad.x[i+2]+0.5)/float(cad.nx)
      y2 = cad.nyplot()*(cad.ny-cad.y[i+2]+0.5)/float(cad.ny)
      z2 = cad.nzplot()*(cad.nz-cad.z[i+2]+0.5)/float(cad.nz)
      im.xy_draw.line([x0,y0,x1,y1,x2,y2,x0,y0],fill="black")
      im.xz_draw.line([x0,z0,x1,z1,x2,z2,x0,z0],fill="black")
      im.yz_draw.line([z0,y0,z1,y1,z2,y2,z0,y0],fill="black")
   images.xy = ImageTk.PhotoImage(im.xy)
   images.xz = ImageTk.PhotoImage(im.xz)
   images.yz = ImageTk.PhotoImage(im.yz)
   canvas_xy.create_image(cad.nplot/2,cad.nplot/2,image=images.xy)
   canvas_xz.create_image(cad.nplot/2,cad.nplot/2,image=images.xz)
   canvas_yz.create_image(cad.nplot/2,cad.nplot/2,image=images.yz)
   im.xyz = Image.new("RGBX",(cad.nplot,cad.nplot),'white')
   images.xyz = ImageTk.PhotoImage(im.xyz)
   canvas_xyz.create_image(cad.nplot/2,cad.nplot/2,image=images.xyz)
   string_msg.set("done")
   root.update()

def flash(event):
   #
   # convert to Gerber flashes
   #
   # evaluate .cad
   #
   evaluate()
   #
   # initialize variables
   #
   render_stop_flag = 0
   cad.stop = 0
   widget_stop.pack()
   delete_windows()
   cad.toolpaths = []
   cad.zwrite = []
   cad.x = zeros(0)
   cad.y = zeros(0)
   cad.z = zeros(0)
   ixs = array([])
   ixe = array([])
   iy = array([])
   iz = array([])
   #
   # evaluate coordinate arrays
   #
   (IY,IX) = indices((cad.ny,cad.nx))
   IY = IY[::-1,:]
   IZ = arange(cad.nz)
   X = cad.xmin+(cad.xmax-cad.xmin)*IX/(cad.nx-1.0)
   Y = cad.ymin+(cad.ymax-cad.ymin)*IY/(cad.ny-1.0)
   if (cad.zwrite == []):
      if (cad.nz > 1):
         cad.zwrite = cad.zmin + (cad.zmax-cad.zmin)*arange(cad.nz)/(cad.nz-1.0)
      else:
         cad.zwrite = [cad.zmin]
   #
   # set up drawing image
   #
   im.xy = Image.new("RGBX",(cad.nxplot(),cad.nyplot()),'white')
   im.xy_draw = ImageDraw.Draw(im.xy)
   #
   # loop over layers
   #
   for layer in range(len(cad.zwrite)):
      #
      # check render stop button
      #
      if (cad.stop == 1):
         break
      #
      # evaluate layer
      #
      Z = cad.zwrite[layer]
      string_msg.set("convert z = %.3f"%Z)
      root.update()
      elements = eval(cad.function)
      #
      # merge x
      #
      starts = hstack((reshape((elements[:,0] == TRUE),(cad.ny,1)),((elements[:,1:] == TRUE) & (elements[:,:-1] == FALSE))))
      ends = hstack((((elements[:,:-1] == TRUE) & (elements[:,1:] == FALSE)),reshape((elements[:,-1] == TRUE),(cad.ny,1))))
      ixs = append(ixs,IX[starts])
      ixe = append(ixe,1+IX[ends])
      iy = append(iy,IY[starts])
      iz = append(iz,IZ[layer-1]*ones(len(IX[starts])))
   #
   # merge y
   #
   index = lexsort(keys=(iy,ixe,ixs,iz))
   merge = (iz[index[1:]] == iz[index[:-1]]) & \
             (ixe[index[1:]] == ixe[index[:-1]]) & \
             (ixs[index[1:]] == ixs[index[:-1]]) & \
             ((iy[index[1:]] - iy[index[:-1]]) == 1)
   merge = append(FALSE,merge).astype(bool_)
   starts = ((merge[1:] == TRUE) & (merge[:-1] == FALSE))
   starts = append(starts,FALSE).astype(bool_)
   ends = ((merge[1:] == FALSE) & (merge[:-1] == TRUE))
   if (merge[-1] == TRUE):
      ends = append(ends,TRUE)
   else:
      ends = append(ends,FALSE)
   ends = ends.astype(bool_)
   xs = ixs[index][starts | ~merge]
   xe = ixe[index][starts | ~merge]
   ys = iy[index][starts | ~merge]
   ye = iy[index][ends | ~(merge | starts)]+1
   cad.x = ravel(transpose(vstack((xs,xe))))
   cad.y = ravel(transpose(vstack((ys,ye))))
   #
   # draw flashes
   #
   widget_stop.pack_forget()
   cad.view('xy')
   string_msg.set("draw ...")
   root.update()
   N = len(cad.x)
   for i in range(0,N,2):
      string_msg.set("draw flash %d/%d"%(i/4,N/4))
      root.update()
      x0 = cad.nxplot()*(cad.x[i]+0.5)/float(cad.nx)
      y0 = cad.nyplot()*(cad.ny-cad.y[i]+0.5)/float(cad.ny)
      x1 = cad.nxplot()*(cad.x[i]+0.5)/float(cad.nx)
      y1 = cad.nyplot()*(cad.ny-cad.y[i+1]+0.5)/float(cad.ny)
      x2 = cad.nxplot()*(cad.x[i+1]+0.5)/float(cad.nx)
      y2 = cad.nyplot()*(cad.ny-cad.y[i+1]+0.5)/float(cad.ny)
      x3 = cad.nxplot()*(cad.x[i+1]+0.5)/float(cad.nx)
      y3 = cad.nyplot()*(cad.ny-cad.y[i]+0.5)/float(cad.ny)
      im.xy_draw.line([x0,y0,x1,y1,x2,y2,x3,y3,x0,y0],fill="black")
   images.xy = ImageTk.PhotoImage(im.xy)
   canvas_xy.create_image(cad.nplot/2,cad.nplot/2,image=images.xy)
   string_msg.set("done")
   root.update()

def select_epi():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.epi')
   cad.cam = 'epi'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   laser_frame1.pack()
   if ((cad.nz > 1) | (cad.image_r.size > 1)):
      laser_frame2.pack()
   laser_frame3.pack()
   string_laser_rate.set("2500")
   string_laser_power.set("90")
   string_laser_speed.set("50")
   string_laser_min_power.set("10")
   string_laser_max_power.set("100")
   string_tool_dia.set("0.01")
   root.update()

def select_camm():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.camm')
   cad.cam = 'camm'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   cut_frame.pack()
   string_cut_force.set("45")
   string_cut_velocity.set("2")
   string_tool_dia.set("0.01")
   root.update()

def select_ps():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.ps')
   cad.cam = 'ps'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   fill_frame.pack()
   string_tool_dia.set("0.0")
   root.update()

def select_ord():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.ord')
   cad.cam = 'ord'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   string_tool_dia.set("0.01")
   waterjet_frame.pack()
   string_lead_in.set("0.05")
   string_quality.set("-3")
   root.update()

def select_g():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.gcode')
   cad.cam = 'g'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   string_tool_dia.set("0.0156")
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   string_g_feed_rate.set("20")
   string_g_spindle_speed.set("5000")
   string_g_tool.set("1")
   integer_g_cool.set("0")
   g_frame.pack()
   root.update()

def select_rml():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.rml')
   cad.cam = 'rml'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   speed_frame.pack()
   rml_move_frame.pack()
   string_tool_dia.set("0.0156")
   string_xy_speed.set("4")
   string_z_speed.set("4")
   string_rml_x_move.set("1")
   string_rml_y_move.set("1")
   root.update()

def select_sbp():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.sbp')
   cad.cam = 'sbp'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   jog_frame.pack()
   speed_frame.pack()
   string_tool_dia.set("0.125")
   string_xy_speed.set("1.1")
   string_z_speed.set("1.1")
   string_jog_xy_speed.set("7")
   string_jog_z_speed.set("7")
   string_jog_z.set(".25")
   root.update()

def select_oms():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.oms')
   cad.cam = 'oms'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   excimer_frame.pack()
   string_pulse_period.set("10000")
   string_tool_dia.set("0.001")
   string_cut_vel.set("0.1")
   string_cut_accel.set("5.0")
   root.update()

def select_dxf():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.dxf')
   cad.cam = 'dxf'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   string_tool_dia.set("0.0")
   root.update()

def select_uni():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.uni')
   cad.cam = 'uni'
   cam_pack_forget()
   cam_file_frame.pack()
   cam_vector_frame.pack()
   cam_dia_frame.pack()
   cam_contour_frame.pack()
   laser_frame1.pack()
   if ((cad.nz > 1) | (cad.image_r.size > 1)):
      laser_frame2.pack()
   string_laser_rate.set("500")
   string_laser_power.set("60")
   string_laser_speed.set("15")
   string_tool_dia.set("0.01")
   string_laser_min_power.set("10")
   string_laser_max_power.set("100")
   string_vector_error.set('1.1')
   root.update()

def select_jpg():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.jpg')
   cad.cam = 'jpg'
   cam_pack_forget()
   cam_file_frame.pack()
   root.update()

def select_png():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.png')
   cad.cam = 'png'
   cam_pack_forget()
   cam_file_frame.pack()
   root.update()

def select_stl():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.stl')
   cad.cam = 'stl'
   cam_pack_forget()
   cam_file_frame.pack()
   STL_frame.pack()
   root.update()

def select_gerber():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.grb')
   cad.cam = 'grb'
   cam_pack_forget()
   cam_file_frame.pack()
   Gerber_frame.pack()
   root.update()

def select_excellon():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.drl')
   cad.cam = 'drl'
   cam_pack_forget()
   cam_file_frame.pack()
   Excellon_frame.pack()
   root.update()

def select_ca():
   input_file_name = string_input_file.get()
   string_cam_file.set(input_file_name[0:-4]+'.ca')
   cad.cam = 'ca'
   cam_pack_forget()
   cam_file_frame.pack()
   root.update()

def cam_pack_forget():
   cam_file_frame.pack_forget()
   cam_vector_frame.pack_forget()
   cam_dia_frame.pack_forget()
   cam_contour_frame.pack_forget()
   laser_frame1.pack_forget()
   laser_frame2.pack_forget()
   laser_frame3.pack_forget()
   cut_frame.pack_forget()
   speed_frame.pack_forget()
   jog_frame.pack_forget()
   rml_move_frame.pack_forget()
   waterjet_frame.pack_forget()
   excimer_frame.pack_forget()
   STL_frame.pack_forget()
   Gerber_frame.pack_forget()
   Excellon_frame.pack_forget()
   fill_frame.pack_forget()
   g_frame.pack_forget()
   send_to_frame.pack_forget()

def save_cam(event):
   #
   # write toolpath
   #
   if (cad.cam == "epi"):
      write_epi()
   elif (cad.cam == "camm"):
      write_camm()
   elif (cad.cam == "ps"):
      write_ps()
   elif (cad.cam == "ord"):
      write_ord()
   elif (cad.cam == "g"):
      write_G()
   elif (cad.cam == "rml"):
      write_rml()
   elif (cad.cam == "sbp"):
      write_sbp()
   elif (cad.cam == "oms"):
      write_oms()
   elif (cad.cam == "dxf"):
      write_dxf()
   elif (cad.cam == "uni"):
      write_uni()
   elif (cad.cam == "jpg"):
      write_jpg()
   elif (cad.cam == "png"):
      write_png()
   elif (cad.cam == "stl"):
      write_stl()
   elif (cad.cam == "grb"):
      write_gerber()
   elif (cad.cam == "drl"):
      write_excellon()
   elif (cad.cam == "ca"):
      write_ca()
   else:
      string_msg.set("unsupported output file format")
      root.update()

def write_epi():
   #
   # Epilog lasercutter output
   # todo: try 1200 DPI
   #
   units = 600*cad.inches_per_unit
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   if (integer_laser_autofocus.get() == 0):
      #
      # init with autofocus off
      #
      file.write("%-12345X@PJL JOB NAME="+string_cam_file.get()+"\r\nE@PJL ENTER LANGUAGE=PCL\r\n&y0A&l0U&l0Z&u600D*p0X*p0Y*t600R*r0F&y50P&z50S*r6600T*r5100S*r1A*rC%1BIN;XR"+string_laser_rate.get()+";YP"+string_laser_power.get()+";ZS"+string_laser_speed.get()+";")
   else:
      #
      # init with autofocus on
      #
      file.write("%-12345X@PJL JOB NAME="+string_cam_file.get()+"\r\nE@PJL ENTER LANGUAGE=PCL\r\n&y1A&l0U&l0Z&u600D*p0X*p0Y*t600R*r0F&y50P&z50S*r6600T*r5100S*r1A*rC%1BIN;XR"+string_laser_rate.get()+";YP"+string_laser_power.get()+";ZS"+string_laser_speed.get()+";")
   power = float(string_laser_power.get())
   min_power = float(string_laser_min_power.get())
   max_power = float(string_laser_max_power.get())
   for layer in range(len(cad.toolpaths)):
      if ((len(cad.zwrite) > 1) & (len(cad.toolpaths[layer]) > 0)):
         fraction = (cad.zwrite[layer]-cad.zwrite[0])/(cad.zwrite[-1]-cad.zwrite[0])
         layer_power = min_power + fraction*(max_power-min_power)
         file.write("YP%f;"%layer_power)
      for segment in range(len(cad.toolpaths[layer])):
         x = int(units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx)))
         y = int(units*(-cad.ymin - ((cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][0].y)+0.5)/float(cad.ny))))
         file.write("PU"+str(x)+","+str(y)+";")
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            x = int(units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx)))
            y = int(units*(-cad.ymin - ((cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex].y)+0.5)/float(cad.ny))))
            file.write("PD"+str(x)+","+str(y)+";")
   file.write("%0B%1BPUE%-12345X@PJL EOJ \r\n")
   file.close()
   draw_toolpath()
   string_msg.set("wrote %s"%filename)
   root.update()

def write_camm():
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   units = 1016*cad.inches_per_unit
   file.write("PA;PA;!ST1;!FS"+string_cut_force.get()+";VS"+string_cut_velocity.get()+";")
   for layer in range(len(cad.toolpaths)):
      for segment in range(len(cad.toolpaths[layer])):
         x = int(units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx)))
         y = int(units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][0].y)+0.5)/float(cad.ny)))
         file.write("PU"+str(x)+","+str(y)+";")
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            x = int(units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx)))
            y = int(units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex].y)+0.5)/float(cad.ny)))
            file.write("PD"+str(x)+","+str(y)+";")
   file.write("PU0,0;")
   file.close()
   draw_toolpath()
   string_msg.set("wrote %s"%filename)
   root.update()

def write_ps():
   #
   # Postscript output
   #
   units = cad.inches_per_unit
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   file.write("%! cad.py output\n")
   file.write("%%%%BoundingBox: 0 0 %.3f %.3f\n"%
      (72.0*(cad.xmax-cad.xmin),72.0*(cad.ymax-cad.ymin)))
   file.write("/m {moveto} def\n")
   file.write("/l {lineto} def\n")
   file.write("72 72 scale\n")
   file.write(".005 setlinewidth\n")
   file.write("%f %f translate\n"%(0.5,0.5))
   for layer in range(len(cad.toolpaths)):
      for segment in range(len(cad.toolpaths[layer])):
         x = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx))
         y = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][0].y)+0.5)/float(cad.ny))
         file.write("%f %f m\n"%(x,y))
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            x = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx))
            y = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex].y)+0.5)/float(cad.ny))
            file.write("%f %f l\n"%(x,y))
         if (integer_fill.get() == 0):
            file.write("stroke\n")
         else:
            file.write("fill\n")
   file.write("showpage\n")
   file.close()
   draw_toolpath()
   string_msg.set("wrote %s"%filename)
   root.update()

def write_ord():
   #
   # OMAX waterjet output
   #
   units = cad.inches_per_unit
   lead_in = float(string_lead_in.get())
   quality = int(string_quality.get())
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   xlead = []
   ylead = []
   for layer in range(len(cad.toolpaths)):
      for segment in range(len(cad.toolpaths[layer])):
         #
         # calculate and write lead-in
         #
         x0 = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx))
         y0 = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][0].y)+0.5)/float(cad.ny))
         x1 = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][1].x+0.5)/float(cad.nx))
         y1 = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][1].y)+0.5)/float(cad.ny))
         dx = x1 - x0
         dy = y1 - y0
         norm_x = -dy
         norm_y = dx
         norm = sqrt(norm_x**2 + norm_y**2)
         norm_x = norm_x/norm
         norm_y = norm_y/norm
         xlead.append(x0 + norm_x*lead_in)
         ylead.append(y0 + norm_y*lead_in)
         file.write("%f, %f, 0, %d\n"%(xlead[segment],ylead[segment],quality))
         #
         # loop over segment
         #
         for vertex in range(len(cad.toolpaths[layer][segment])):
            x = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx))
            y = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex].y)+0.5)/float(cad.ny))
            file.write("%f, %f, 0, %d\n"%(x,y,quality))
         #
         # write lead-out
         #
         file.write("%f, %f, 0, 0\n"%(x0,y0))
         file.write("%f, %f, 0, 0\n"%(xlead[segment],ylead[segment]))
   file.close()
   #
   # draw toolpath with lead-in/out
   #
   im.xy = Image.new("RGBX",(cad.nxplot(),cad.nyplot()),'white')
   im.xy_draw = ImageDraw.Draw(im.xy)
   for layer in range(len(cad.toolpaths)):
      for segment in range(len(cad.toolpaths[layer])):
         x = cad.nxplot()*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx)
         y = cad.nyplot()*(cad.toolpaths[layer][segment][0].y+0.5)/float(cad.ny)
         xl = cad.nxplot()*(xlead[segment]-cad.xmin)/(cad.xmax-cad.xmin)
         yl = cad.nyplot()-cad.nyplot()*(ylead[segment]-cad.ymin)/(cad.ymax-cad.ymin)
         im.xy_draw.line([xl,yl,x,y],fill="black")
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            xnew = cad.nxplot()*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx)
            ynew = cad.nyplot()*(cad.toolpaths[layer][segment][vertex].y+0.5)/float(cad.ny)
            im.xy_draw.line([x,y,xnew,ynew],fill="black")
            x = xnew
            y = ynew
   images.xy = ImageTk.PhotoImage(im.xy)
   canvas_xy.create_image(cad.nplot/2,cad.nplot/2,image=images.xy)
   string_msg.set("wrote %s"%filename)
   root.update()

def distance(x1, y1, x2, y2):
   return sqrt((x1-x2)**2+(y1-y2)**2)

def write_G():
   #
   # G code output
   #
   units = cad.inches_per_unit
   zup = units*cad.zmax
   feed_rate = float(string_g_feed_rate.get())
   spindle_speed = float(string_g_spindle_speed.get())
   coolant = integer_g_cool.get()
   tool = int(string_g_tool.get())
   if (cad.nz == 1):
      cad.zwrite = [cad.zmin]
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   file.write("""(---------------------------------------------------------------)
(---------------------------------------------------------------)
(Start of sheet header)
G21 (metric ftw)
G90 (absolute mode)
G92 X0 Y0 Z0 (zero all axes)
G92 Z0.00 F150.00 (go up to printing level)
M106 (pen down)
G4 P120 (wait 120ms)
M300 S50 (pen up)
G4 P120 (wait 120ms)
M18 (disengage drives)
M01 (Was registration test successful?)
(while drives are disengaged, adjustments can be made to position)
M17 (engage drives if YES, and continue)
(End of sheet header)\n""")
   dxy = 0
   dz = 0
   xold = 0
   yold = 0
   for layer in range(len(cad.zwrite)-1,-1,-1):
      zdown = units*cad.zwrite[layer]
      #
      # follow toolpaths CCW, for CW tool motion
      #
      unsorted_segments = cad.toolpaths[layer]
      sorted_segments = []
      if len(unsorted_segments) > 0:
         sorted_segments.append(unsorted_segments.pop(0)) #starts with the first path in the list
      else:
         print "empty path --- strange"

      while len(unsorted_segments) > 0:
         #find closest start to the the last sorted segment start
         min_dist = 99999
         min_dist_index = None
         for i in range(len(unsorted_segments)):
            dist = distance(sorted_segments[-1][0].x, sorted_segments[-1][0].y,
                            unsorted_segments[i][0].x, unsorted_segments[i][0].y)
            if dist < min_dist:
               min_dist = dist
               min_dist_index = i

         #print "min_dist: %d index: %d" % (min_dist, min_dist_index)
         sorted_segments.append(unsorted_segments.pop(min_dist_index))

      for segment in range(len(sorted_segments)):
      
         x = units*(cad.xmin + (cad.xmax-cad.xmin)*(sorted_segments[segment][0].x+0.5)/float(cad.nx))
         y = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-sorted_segments[segment][0].y)+0.5)/float(cad.ny))
         file.write("G1 X%0.4f "%x+"Y%0.4f "%y+"Z%0.4f"%zup+" F2000.00\n") # rapid motion
         file.write("G1 Z%0.4f "%zdown+" F300.00\n") # linear motion
         dxy += sqrt((xold-x)**2+(yold-y)**2)
         xold = x
         yold = y
         dz += zup-zdown
         for vertex in range(1,len(sorted_segments[segment])):
            x = units*(cad.xmin + (cad.xmax-cad.xmin)*(sorted_segments[segment][vertex].x+0.5)/float(cad.nx))
            y = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-sorted_segments[segment][vertex].y)+0.5)/float(cad.ny))
            file.write("G1 X%0.4f "%x+"Y%0.4f"%y+" F2000.00\n")
            dxy += sqrt((xold-x)**2+(yold-y)**2)
            xold = x
            yold = y
   file.write("""(Start of sheet footer.)
M107
G4 P120 (wait 120ms)
G0 X0 Y0 Z15 F3500.00 (go to position for retrieving platform -- increase Z to Z25 or similar if you have trouble avoiding tool)
G4 P300 (wait 300ms)
M01 (Have you retrieved the print?)
(machine halts until 'okay')
G4 P120 (if yes continue, pause 120ms before ... )
G0 Z0 F3500.00 (return to start position of current sheet)
G4 P300 (wait 300ms)
M18 (disengage drives)
(End of sheet footer)

M01 (Printing on the next sheet?)
(yes, if dropping the default .1 mm to next sheet; no, if you will print again on same sheet)
G0 Z-0.10 F3500.00 (drop 0.1mm to next sheet)

(Paste in further sheets below)
(---------------------------------------------------------------)
(---------------------------------------------------------------)
""")
   file.close()
   print "Path length: %f" % dxy
   time = (dxy/feed_rate + dz/feed_rate)
   string_send_to_time.set(" estimated time: %.1f minutes"%time)
   draw_toolpath()
   string_msg.set("wrote %s"%filename)
   root.update()

def write_rml():
   #
   # Roland Modela output
   #
   units = 1016*cad.inches_per_unit # 40/mm
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   file.write("PA;PA;VS"+string_xy_speed.get()+";!VZ"+string_z_speed.get()+";!MC1;")
   zup = cad.zmax
   izup = int(units*zup)
   if (cad.nz == 1):
      cad.zwrite = [cad.zmin]
   xy_speed = float(string_xy_speed.get()) # mm/s
   z_speed = float(string_z_speed.get()) # mm/s
   dxy = 0
   dz = 0
   xold = 0
   yold = 0
   for layer in range(len(cad.zwrite)-1,-1,-1):
      zdown = cad.zwrite[layer]
      izdown = int(units*zdown)
      file.write("!PZ"+str(izdown)+","+str(izup)+";")
      #
      # follow toolpaths CCW, for CW tool motion
      #
      for segment in range(len(cad.toolpaths[layer])):      
         x = int(units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx)))
         y = int(units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][0].y)+0.5)/float(cad.ny)))
         file.write("PU"+str(x)+","+str(y)+";")
         dxy += sqrt((xold-x)**2+(yold-y)**2)
         xold = x
         yold = y
         dz += izup-izdown
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            x = int(units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx)))
            y = int(units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex].y)+0.5)/float(cad.ny)))
            file.write("PD"+str(x)+","+str(y)+";")
            dxy += sqrt((xold-x)**2+(yold-y)**2)
            xold = x
            yold = y
   file.write("PU"+str(x)+","+str(y)+";!MC0;")
   #
   # file padding hack for end-of-file buffering problems
   #
   for i in range(1000):
      file.write("!MC0;")
   file.close()
   time = ((dxy/40.0)/xy_speed + (dz/40.0)/z_speed)/60.0
   string_send_to_time.set(" estimated time: %.1f minutes"%time)
   draw_toolpath()
   string_msg.set("wrote %s"%filename)
   root.update()

def rml_move(event):
   #
   # move Roland Modela
   #
   units = 1016*cad.inches_per_unit # 40/mm
   x = float(string_rml_x_move.get())
   y = float(string_rml_y_move.get())
   ix = int(units*x)
   iy = int(units*y)
   filename = "move.rml"
   file = open(filename, 'wb')
   file.write("PA;PA;!PZ0,400;VS10;!VZ10;!MC0;PU%d,%d;!MC0;"%(ix,iy))
   file.close()
   send_to_file("move.rml")
   os.remove("move.rml")

def write_sbp():
   #
   # ShopBot output
   #
   units = cad.inches_per_unit
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   file.write("SA\r\n") # set to absolute distances
   file.write("SO,1,1\r\n") # set output number 1 to on
   file.write("pause 2\r\n") # let spindle come up to speed
   xy_speed = units*float(string_xy_speed.get())
   z_speed = units*float(string_z_speed.get())
   file.write("MS %f,%f\r\n"%(xy_speed,z_speed)) # set xy,z speed
   jog_xy_speed = units*float(string_jog_xy_speed.get())
   jog_z_speed = units*float(string_jog_z_speed.get())
   file.write("JS %f,%f\r\n"%(jog_xy_speed,jog_z_speed)) # set jog xy,z speed
   zup = units*float(string_jog_z.get())
   dxy = 0
   dz = 0
   xold = 0
   yold = 0
   for layer in range(len(cad.zwrite)-1,-1,-1):
      zdown = cad.zwrite[layer]
      #
      # follow toolpaths CCW, for CW tool motion
      #
      for segment in range(len(cad.toolpaths[layer])):      
         x = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx))
         y = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][0].y)+0.5)/float(cad.ny))
         file.write("JZ %f\r\n"%zup)
         file.write("J2 %f,%f\r\n"%(x,y))
         file.write("MZ %f\r\n"%zdown)
         dxy += sqrt((xold-x)**2+(yold-y)**2)
         xold = x
         yold = y
         dz += zup-zdown
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            x = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx))
            y = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex].y)+0.5)/float(cad.ny))
            file.write("M2 %f,%f\r\n"%(x,y))
            dxy += sqrt((xold-x)**2+(yold-y)**2)
            xold = x
            yold = y
   file.write("JZ %f\r\n"%zup)
   file.close()
   time = (dxy/xy_speed + dz/z_speed)/60.0
   string_send_to_time.set(" estimated time: %.1f minutes"%time)
   draw_toolpath()
   string_msg.set("wrote %s"%filename)
   root.update()

def write_oms():
   #
   # Resonetics excimer micromachining center output
   #
   units = 25.4*cad.inches_per_unit
   pulseperiod = float(string_pulse_period.get())
   cutvel = float(string_cut_vel.get())
   cutaccel = float(string_cut_accel.get())
   slewvel = 1
   slewaccel = 5
   settle = 100
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   file.write("AA LP0,0,0,0,0\n") # set origin
   file.write("PP%d\n"%pulseperiod) # set pulse period
   for layer in range(len(cad.toolpaths)):
      for segment in range(len(cad.toolpaths[layer])):      
         x = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx))
         y = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][0].y)+0.5)/float(cad.ny))
         file.write("VL%.1f,%.1f\n"%(slewvel,slewvel))
         file.write("AC%.1f,%.1f\n"%(slewaccel,slewaccel))
         file.write("MA%f,%f\n"%(x,y))
         file.write("VL%.1f,%.1f\n"%(cutvel,cutvel))
         file.write("AC%.1f,%.1f\n"%(cutaccel,cutaccel))
         file.write("WT%d\n"%settle) # wait to settle
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            x = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx))
            y = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex].y)+0.5)/float(cad.ny))
            file.write("CutAbs %f,%f\n"%(x,y))
   file.write("END\n")
   file.close()
   draw_toolpath()
   string_msg.set("wrote %s"%filename)
   root.update()

def write_dxf():
   #
   # DXF output
   #
   units = cad.inches_per_unit
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   file.write("999\nDXF written by cad.py\n")
   file.write("0\nSECTION\n")
   file.write("2\nHEADER\n")
   file.write("9\n$EXTMIN\n")
   file.write("10\n%f\n"%cad.xmin)
   file.write("20\n%f\n"%cad.ymin)
   file.write("9\n$EXTMAX\n")
   file.write("10\n%f\n"%cad.xmax)
   file.write("20\n%f\n"%cad.ymax)
   file.write("0\nENDSEC\n")
   file.write("0\nSECTION\n")
   file.write("2\nTABLES\n")
   file.write("0\nTABLE\n")
   file.write("2\nLTYPE\n70\n1\n")
   file.write("0\nLTYPE\n")
   file.write("2\nCONTINUOUS\n")
   file.write("70\n64\n3\n")
   file.write("Solid line\n")
   file.write("72\n65\n73\n0\n40\n0.000000\n")
   file.write("0\nENDTAB\n")
   file.write("0\nTABLE\n2\nLAYER\n70\n1\n")
   file.write("0\nLAYER\n2\ndefault\n70\n64\n62\n7\n6\n")
   file.write("CONTINUOUS\n0\nENDTAB\n")
   file.write("0\nENDSEC\n")
   file.write("0\nSECTION\n")
   file.write("2\nBLOCKS\n")
   file.write("0\nENDSEC\n")
   file.write("0\nSECTION\n")
   file.write("2\nENTITIES\n")
   for layer in range(len(cad.toolpaths)):
      for segment in range(len(cad.toolpaths[layer])):
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            x0 = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex-1].x+0.5)/float(cad.nx))
            y0 = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex-1].y)+0.5)/float(cad.ny))
            x1 = units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx))
            y1 = units*(cad.ymin + (cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex].y)+0.5)/float(cad.ny))
            file.write("0\nLINE\n")
            file.write("10\n%f\n"%x0)
            file.write("20\n%f\n"%y0)
            file.write("11\n%f\n"%x1)
            file.write("21\n%f\n"%y1)
   file.write("0\nENDSEC\n")
   file.write("0\nEOF\n")
   file.close()
   draw_toolpath()
   string_msg.set("wrote %s"%filename)
   root.update()

def write_uni():
   #
   # Universal lasercutter output
   #
   units = 1000*cad.inches_per_unit
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   file.write("Z") # initialize
   file.write("t%s~;"%filename) # title
   file.write("IN;DF;PS0;DT~") # initialize
   ppibyte = int(float(string_laser_rate.get())/10)
   file.write("s%c"%ppibyte) # PPI
   speed_hibyte = int(648*float(string_laser_speed.get()))/256
   speed_lobyte = int(648*float(string_laser_speed.get()))%256
   file.write("v%c%c"%(speed_hibyte,speed_lobyte)) # speed
   power = float(string_laser_power.get())
   min_power = float(string_laser_min_power.get())
   max_power = float(string_laser_max_power.get())
   power_hibyte = (320*int(power))/256
   power_lobyte = (320*int(power))%256
   file.write("p%c%c"%(power_hibyte,power_lobyte)) # power
   file.write("a%c"%2) # air assist on high
   for layer in range(len(cad.toolpaths)):
      if ((len(cad.zwrite) > 1) & (len(cad.toolpaths[layer]) > 0)):
         fraction = (cad.zwrite[layer]-cad.zwrite[0])/(cad.zwrite[-1]-cad.zwrite[0])
         layer_power = min_power + fraction*(max_power-min_power)
         power_hibyte = (320*int(layer_power))/256
         power_lobyte = (320*int(layer_power))%256
         file.write("p%c%c"%(power_hibyte,power_lobyte)) # power
      for segment in range(len(cad.toolpaths[layer])):
         x = int(units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][0].x+0.5)/float(cad.nx)))
         y = int(units*(cad.ymin + ((cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][0].y)+0.5)/float(cad.ny))))
         file.write("PU;PA"+str(x)+","+str(y)+";PD;")
         for vertex in range(1,len(cad.toolpaths[layer][segment])):
            x = int(units*(cad.xmin + (cad.xmax-cad.xmin)*(cad.toolpaths[layer][segment][vertex].x+0.5)/float(cad.nx)))
            y = int(units*(cad.ymin + ((cad.ymax-cad.ymin)*((cad.ny-cad.toolpaths[layer][segment][vertex].y)+0.5)/float(cad.ny))))
            file.write("PA"+str(x)+","+str(y)+";")
   file.write("e") # end of file
   file.close()
   draw_toolpath()
   string_msg.set("wrote %s"%filename)
   root.update()

def write_jpg():
   #
   # JPG image output
   #
   if (cad.views == "xy"):
      filename = string_cam_file.get()
      im.xy = Image.fromarray(im.intensity_xy,mode="RGBX")
      im_rgb_xy = im.xy.convert("RGB")
      dpi = int(cad.nx/float(cad.xmax-cad.xmin))
      im_rgb_xy.save(filename,dpi=(dpi,dpi))
      string_msg.set("wrote %s"%filename)
   elif (cad.views == "xyzr"):
      border = 5
      filename = string_cam_file.get()
      im.xy = Image.fromarray(im.intensity_xy,mode="RGBX")
      im.xz = Image.fromarray(im.intensity_xz,mode="RGBX")
      im.yz = Image.fromarray(im.intensity_yz,mode="RGBX")
      im.yz = im.yz.transpose(Image.FLIP_LEFT_RIGHT)
      im.xyz = Image.fromarray(im.intensity_xyz,mode="RGBX")
      (nx,ny) = im.xy.size
      ny = (nx*cad.nyplot())/cad.nxplot()
      nz = (nx*cad.nzplot())/cad.nxplot()
      im.xy = im.xy.resize((nx,ny))
      im.yz = im.yz.resize((nz,ny))
      im.xz = im.xz.resize((nx,nz))
      im.xyz = im.xyz.resize((nx,ny))
      im_rgb_xy = im.xy.convert("RGB")
      im_rgb_xz = im.xz.convert("RGB")
      im_rgb_yz = im.yz.convert("RGB")
      im_rgb_xyz = im.xyz.convert("RGB")
      img = Image.new("RGB",(nx+border+nx,ny+border+ny),"white")
      img.paste(im_rgb_xy,(0,0))
      img.paste(im_rgb_xz,(0,border+ny))
      img.paste(im_rgb_yz,(border+nx,0))
      img.paste(im_rgb_xyz,(border+nx,border+ny))
      img.save(filename)
      string_msg.set("wrote %s"%filename)
   else:
      string_msg.set("unknown view")

def write_png():
   #
   # PNG image output
   #
   if (cad.views == "xy"):
      filename = string_cam_file.get()
      im.xy = Image.fromarray(im.intensity_xy,mode="RGBX")
      im_rgb_xy = im.xy.convert("RGB")
      dpi = int(cad.nx/float(cad.xmax-cad.xmin))
      im_rgb_xy.save(filename,dpi=(dpi,dpi))
      string_msg.set("wrote %s"%filename)
   elif (cad.views == "xyzr"):
      border = 5
      filename = string_cam_file.get()
      im.xy = Image.fromarray(im.intensity_xy,mode="RGBX")
      im.xz = Image.fromarray(im.intensity_xz,mode="RGBX")
      im.yz = Image.fromarray(im.intensity_yz,mode="RGBX")
      im.yz = im.yz.transpose(Image.FLIP_LEFT_RIGHT)
      im.xyz = Image.fromarray(im.intensity_xyz,mode="RGBX")
      (nx,ny) = im.xy.size
      ny = (nx*cad.nyplot())/cad.nxplot()
      nz = (nx*cad.nzplot())/cad.nxplot()
      im.xy = im.xy.resize((nx,ny))
      im.yz = im.yz.resize((nz,ny))
      im.xz = im.xz.resize((nx,nz))
      im.xyz = im.xyz.resize((nx,ny))
      im_rgb_xy = im.xy.convert("RGB")
      im_rgb_xz = im.xz.convert("RGB")
      im_rgb_yz = im.yz.convert("RGB")
      im_rgb_xyz = im.xyz.convert("RGB")
      img = Image.new("RGB",(nx+border+nx,ny+border+ny),"white")
      img.paste(im_rgb_xy,(0,0))
      img.paste(im_rgb_xz,(0,border+ny))
      img.paste(im_rgb_yz,(border+nx,0))
      img.paste(im_rgb_xyz,(border+nx,border+ny))
      img.save(filename)
      string_msg.set("wrote %s"%filename)
   else:
      string_msg.set("unknown view")

def write_stl():
   #
   # STL output
   #
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   units = cad.inches_per_unit
   x = cad.xmin+(cad.xmax-cad.xmin)*(cad.x+0.5)/float(cad.nx)
   y = cad.ymin+(cad.ymax-cad.ymin)*(cad.y+0.5)/float(cad.ny)
   z = cad.zmin+(cad.zmax-cad.zmin)*(cad.z+0.5)/float(cad.nz)
   #
   # header
   #
   file.write('cad.py')
   file.write('a'*74)
   #
   # length
   #
   N = len(cad.x)
   file.write(struct.pack('L',N/3))
   #
   # triangles
   #
   for i in range(0,N,3):
      string_msg.set("write triangle %d/%d"%(i/3,N/3))
      root.update()
      #
      # normals
      #
      file.write(struct.pack('f',0))
      file.write(struct.pack('f',0))
      file.write(struct.pack('f',0))
      #
      # vertices
      #
      file.write(struct.pack('f',x[i]*units))
      file.write(struct.pack('f',y[i]*units))
      file.write(struct.pack('f',z[i]*units))
      file.write(struct.pack('f',x[i+1]*units))
      file.write(struct.pack('f',y[i+1]*units))
      file.write(struct.pack('f',z[i+1]*units))
      file.write(struct.pack('f',x[i+2]*units))
      file.write(struct.pack('f',y[i+2]*units))
      file.write(struct.pack('f',z[i+2]*units))
      #
      # padding
      #
      file.write(struct.pack('xx'))
   file.close()
   string_msg.set("wrote %s"%filename)
   root.update()

def write_gerber():
   #
   # Gerber (RS-274X) output
   #
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   units = cad.inches_per_unit
   #
   # write parameters
   #
   file.write("%FSLAX24Y24*%\n") # leading zeros omitted, absolute coordinates, 2.4
   file.write("%MOIN*%\n") # inches units
   file.write("%OFA0B0*%\n") # no offset
   #
   # find and write apertures
   #
   ixs = cad.x[::2]
   xs = cad.xmin+(cad.xmax-cad.xmin)*(ixs+0.5)/float(cad.nx)
   ixe = cad.x[1::2]
   xe = cad.xmin+(cad.xmax-cad.xmin)*(ixe+0.5)/float(cad.nx)
   idx = ixe - ixs
   dx = xe - xs
   iys = cad.y[::2]
   ys = cad.ymin+(cad.ymax-cad.ymin)*(iys+0.5)/float(cad.ny)
   iye = cad.y[1::2]
   ye = cad.ymin+(cad.ymax-cad.ymin)*(iye+0.5)/float(cad.ny)
   idy = iye - iys
   dy = ye - ys
   mins = where((idx < idy),idx,idy)
   uniques = unique(mins)
   apertures = (cad.xmax-cad.xmin)*uniques/float(cad.nx)
   index = searchsorted(uniques,mins)
   for i in range(len(uniques)):
      file.write("%%ADD%dR,%.4fX%.4f*%%\n"%(i+10,apertures[i],apertures[i]))
   #
   # write flashes
   #
   coords = arange(len(mins))
   for i in range(len(uniques)):
      file.write("D%d*\n"%(i+10))
      coord = coords[index == i]
      delta = apertures[i]/2.
      ixs = (10000*(xs+delta)).astype(int32)
      ixe = (10000*(xe-delta)).astype(int32)
      iys = (10000*(ys+delta)).astype(int32)
      iye = (10000*(ye-delta)).astype(int32)
      for j in range(len(coord)):
         n = coord[j]
         if (idx[n] == idy[n]):
            #
            # flash
            #
            file.write('X%dY%dD03*\n'%(ixs[n],iys[n]))
         elif (idx[n] > idy[n]):
            #
            # stroke horizontal
            #
            file.write('X%dY%dD02*\n'%(ixs[n],iys[n]))
            file.write('X%dY%dD01*\n'%(ixe[n],iys[n]))
         else:
            #
            # stroke vertical
            #
            file.write('X%dY%dD02*\n'%(ixs[n],iys[n]))
            file.write('X%dY%dD01*\n'%(ixs[n],iye[n]))
   file.write("M02*\n") # end of file
   file.close()
   string_msg.set("wrote %s (RS-274X)"%filename)
   root.update()

def write_excellon():
   #
   # Excellon (RS-) output
   #
   """
%  	Rewind and Stop
X#Y# 	Move and Drill
T# 	Tool Selection
M30 	End of Program
M00 	End of Program
R#X#Y# 	Repeat Hole
G05, G81 	Select Drill Mode
G90 	Absolute Mode
G91 	Incremental Mode
G92 X#Y# 	Set Zero
G93 X#Y# 	Set Zero
M48 	Program Header to first "%"
M72 	English-Imperial Mode

   """
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   units = cad.inches_per_unit
   #
   # write parameters
   #
   file.write("%FSLAX24Y24*%\n") # leading zeros omitted, absolute coordinates, 2.4
   file.write("%MOIN*%\n") # inches units
   file.write("%OFA0B0*%\n") # no offset
   #
   # find and write apertures
   #
   ixs = cad.x[::2]
   xs = cad.xmin+(cad.xmax-cad.xmin)*(ixs+0.5)/float(cad.nx)
   ixe = cad.x[1::2]
   xe = cad.xmin+(cad.xmax-cad.xmin)*(ixe+0.5)/float(cad.nx)
   idx = ixe - ixs
   dx = xe - xs
   iys = cad.y[::2]
   ys = cad.ymin+(cad.ymax-cad.ymin)*(iys+0.5)/float(cad.ny)
   iye = cad.y[1::2]
   ye = cad.ymin+(cad.ymax-cad.ymin)*(iye+0.5)/float(cad.ny)
   idy = iye - iys
   dy = ye - ys
   mins = where((idx < idy),idx,idy)
   uniques = unique(mins)
   apertures = (cad.xmax-cad.xmin)*uniques/float(cad.nx)
   index = searchsorted(uniques,mins)
   for i in range(len(uniques)):
      file.write("%%ADD%dR,%.4fX%.4f*%%\n"%(i+10,apertures[i],apertures[i]))
   #
   # write flashes
   #
   coords = arange(len(mins))
   for i in range(len(uniques)):
      file.write("D%d*\n"%(i+10))
      coord = coords[index == i]
      delta = apertures[i]/2.
      ixs = (10000*(xs+delta)).astype(int32)
      ixe = (10000*(xe-delta)).astype(int32)
      iys = (10000*(ys+delta)).astype(int32)
      iye = (10000*(ye-delta)).astype(int32)
      for j in range(len(coord)):
         n = coord[j]
         if (idx[n] == idy[n]):
            #
            # flash
            #
            file.write('X%dY%dD03*\n'%(ixs[n],iys[n]))
         elif (idx[n] > idy[n]):
            #
            # stroke horizontal
            #
            file.write('X%dY%dD02*\n'%(ixs[n],iys[n]))
            file.write('X%dY%dD01*\n'%(ixe[n],iys[n]))
         else:
            #
            # stroke vertical
            #
            file.write('X%dY%dD02*\n'%(ixs[n],iys[n]))
            file.write('X%dY%dD01*\n'%(ixs[n],iye[n]))
   file.write("M02*\n") # end of file
   file.close()
   string_msg.set("wrote %s (RS-274X)"%filename)
   root.update()

def write_ca():
   #
   # CA output
   #
   filename = string_cam_file.get()
   file = open(filename, 'wb')
   file.write(chr(0xB9)) # magic number 0xB9
   file.write(chr(ca.nx/256)) # x size
   file.write(chr(ca.nx%256)) #
   file.write(chr(ca.ny/256)) # y size
   file.write(chr(ca.ny%256)) #
   file.write(chr(4)) # LED sub-array x
   file.write(chr(2)) # LED sub-array y
   for y in range(ca.nx):
      for x in range(ca.nx):
         if (ca.in1[y,x] == ca.E):
            config = 0
         elif (ca.in1[y,x] == ca.NE):
            config = 1
         elif (ca.in1[y,x] == ca.N):
            config = 2
         elif (ca.in1[y,x] == ca.NW):
            config = 3
         elif (ca.in1[y,x] == ca.W):
            config = 4
         elif (ca.in1[y,x] == ca.SW):
            config = 5
         elif (ca.in1[y,x] == ca.S):
            config = 6
         elif (ca.in1[y,x] == ca.SE):
            config = 7
         elif (ca.in1[y,x] == ca.empty): # XOR W W for empty
            config = 4
         if (ca.in2[y,x] == ca.E):
            config += 0
         elif (ca.in2[y,x] == ca.NE):
            config += (1 << 3)
         elif (ca.in2[y,x] == ca.N):
            config += (2 << 3)
         elif (ca.in2[y,x] == ca.NW):
            config += (3 << 3)
         elif (ca.in2[y,x] == ca.W):
            config += (4 << 3)
         elif (ca.in2[y,x] == ca.SW):
            config += (5 << 3)
         elif (ca.in2[y,x] == ca.S):
            config += (6 << 3)
         elif (ca.in2[y,x] == ca.SE):
            config += (7 << 3)
         elif (ca.in2[y,x] == ca.empty): # XOR W W for empty
            config += (4 << 3)
         if (ca.gates[y,x] == ca.AND):
            config += 0
         elif (ca.gates[y,x] == ca.OR):
            config += (1 << 6)
         elif (ca.gates[y,x] == ca.XOR):
            config += (2 << 6)
         elif (ca.gates[y,x] == ca.NAND):
            config += (3 << 6)
         elif (ca.gates[y,x] == ca.empty): # XOR W W for empty
            config += (2 << 6)
         file.write(chr(config))
   for y in range(ca.ny):
      for x in range((ca.nx/8)):
         state = \
              (ca.states[y,8*x+0] << 7) \
            + (ca.states[y,8*x+1] << 6) \
            + (ca.states[y,8*x+2] << 5) \
            + (ca.states[y,8*x+3] << 4) \
            + (ca.states[y,8*x+4] << 3) \
            + (ca.states[y,8*x+5] << 2) \
            + (ca.states[y,8*x+6] << 1) \
            + (ca.states[y,8*x+7] << 0)
         file.write(chr(state))
      if ((ca.nx%8) != 0):
         x = cad.nx/8
         state = 0
         for i in range((ca.nx%8)):
            state += (ca.states[y,8*x+i] << (7-i))
         file.write(chr(state))
   file.close()
   string_msg.set("wrote %s"%filename)
   root.update()

def msg_xy(event):
   x = (cad.xmin+cad.xmax)/2. + (cad.xmax-cad.xmin)*(1+event.x-cad.nplot/2.)/float(cad.nxplot())
   y = (cad.ymin+cad.ymax)/2. + (cad.ymin-cad.ymax)*(1+event.y-cad.nplot/2.)/float(cad.nyplot())
   string_msg.set("x = %.2f  y = %.2f"%(x,y))

def msg_yz(event):
   if (cad.nz > 1):
      y = (cad.ymin+cad.ymax)/2. + (cad.ymin-cad.ymax)*(1+event.y-cad.nplot/2.)/float(cad.nyplot())
      z = (cad.zmin+cad.zmax)/2. + (cad.zmin-cad.zmax)*(1+event.x-cad.nplot/2.)/float(cad.nzplot())
      string_msg.set("y = %.2f  z = %.2f"%(y,z))
   else:
      string_msg.set("")

def msg_xz(event):
   if (cad.nz > 1):
      x = (cad.xmin+cad.xmax)/2. + (cad.xmax-cad.xmin)*(1+event.x-cad.nplot/2.)/float(cad.nxplot())
      z = (cad.zmin+cad.zmax)/2. + (cad.zmin-cad.zmax)*(1+event.y-cad.nplot/2.)/float(cad.nzplot())
      string_msg.set("x = %.2f  z = %.2f"%(x,z))
   else:
      string_msg.set("")

def msg_nomsg(event):
   string_msg.set("")

def image_min_x(event):
   cad.xmin = float(string_image_xmin.get())
   xwidth = float(string_image_xwidth.get())
   cad.xmax = cad.xmin + xwidth
   root.update()

def image_min_y(event):
   cad.ymin = float(string_image_ymin.get())
   yheight = float(string_image_yheight.get())
   cad.ymax = cad.ymin + yheight
   root.update()

def image_scale_x(event):
   yheight = float(string_image_yheight.get())
   xwidth = yheight*cad.nx/float(cad.ny)
   cad.xmax = cad.xmin + xwidth
   string_image_xwidth.set(str(xwidth))
   root.update()

def image_scale_y(event):
   xwidth = float(string_image_xwidth.get())
   yheight = xwidth*cad.ny/float(cad.nx)
   cad.ymax = cad.ymin + yheight
   string_image_yheight.set(str(yheight))
   root.update()

def send_to(event):
   save_cam(0)
   cam_file_name = string_cam_file.get()
   send_to_file(cam_file_name)

def send_to_file(cam_file_name):
   cad_path = os.path.dirname(sys.argv[0])
   if (sys.argv[0] == "cad.py"):
      cfg_path = "cad.cfg"
   else:
      cfg_path = os.path.dirname(sys.argv[0])+"/cad.cfg"
   try:
      config_file = open(cfg_path, 'r')
   except:
      string_msg.set(cfg_path+" not found")
      root.update()
      return()
   dot = find(cam_file_name,".")
   while 1:
      new_dot = find(cam_file_name,".",dot+1)
      if (new_dot == -1):
         break
      else:
         dot = new_dot
   suffix = cam_file_name[dot+1:]
   while 1:
      line = config_file.readline()
      if (find(line,suffix) == 0):
         string_msg.set("sending "+cam_file_name+" ...")
         root.update()
         quote1 = find(line,"'")
         quote2 = find(line,"'",quote1+1)
         cmd = line[(quote1+1):quote2]
         if (os.name == 'nt'):
            cam_file_name = replace(cam_file_name,'/','\\')
         cmd = replace(cmd,'file','"'+cam_file_name+'"')
         os.system(cmd)
         string_msg.set(cam_file_name+" sent")
         root.update()
         config_file.close()
         root.update()
         return()
      elif (line == ""):
         string_msg.set(suffix+" driver not defined in "+cfg_path)
         config_file.close()
         root.update()
         return()

def resize_window(event):
   #
   # resize drawing windows
   #
   cad.nplot = int(string_window_size.get())
   cad.view(cad.views)
   render()

def resize_editor(event):
   #
   # resize editing windows
   #
   cad.editor_height = int(string_editor_height.get())
   widget_cad_text.config(height=cad.editor_height)
   cad.editor_width = int(string_editor_width.get())
   widget_cad_text.config(width=cad.editor_width)
   widget_function_text.config(width=cad.editor_width)
   root.update()

def reload():
   #
   # reload input file
   #
   filename = string_input_file.get()
   if (find(filename,'.cad') != -1):
      cad_load(0)
   elif ((find(filename,'.jpg') != -1) | (find(filename,'.JPG') != -1) |
      (find(filename,'.png') != -1) | (find(filename,'.PNG') != -1) |
      (find(filename,'.gif') != -1) | (find(filename,'.GIF') != -1)):
      widget_cad_text.delete("1.0",END)
      image_load(0)
   else:
      string_msg.set("unsupported input file format")
      root.update()

#
# set up GUI
#
root = Tk()
root.title('cad.py')
#
# message frame
#
msg_frame = Frame(root)
string_msg = StringVar()
widget_msg = Label(msg_frame, textvariable = string_msg)
widget_msg.pack(side='right')
Label(msg_frame, text=" ").pack(side='right')
widget_stop = Button(msg_frame, text='stop', borderwidth=2)
widget_stop.bind('<Button-1>',render_stop)
msg_frame.grid(row=0,column=0)
#
# size frame
#
size_frame = Frame(root)
Label(size_frame, text="window size: ").pack(side='left')
string_window_size = StringVar()
string_window_size.set(str(cad.nplot))
widget_window_size = Entry(size_frame, width=4, bg='white', textvariable=string_window_size)
widget_window_size.bind('<Return>',resize_window)
widget_window_size.pack(side='left')
Label(size_frame, text="   editor width: ").pack(side='left')
string_editor_width = StringVar()
string_editor_width.set(str(cad.editor_width))
widget_editor_width = Entry(size_frame, width=3, bg='white', textvariable=string_editor_width)
widget_editor_width.bind('<Return>',resize_editor)
widget_editor_width.pack(side='left')
Label(size_frame, text=" height: ").pack(side='left')
string_editor_height = StringVar()
string_editor_height.set(str(cad.editor_height))
widget_editor_height = Entry(size_frame, width=3, bg='white', textvariable=string_editor_height)
widget_editor_height.bind('<Return>',resize_editor)
widget_editor_height.pack(side='left')
size_frame.grid(row=0,column=1)
#
# view frame
#
view_frame2 = Frame(root)
view_frame3 = Frame(root)
canvas_xy = Canvas(view_frame3)
canvas_xz = Canvas(view_frame3)
canvas_yz = Canvas(view_frame3)
canvas_xyz = Canvas(view_frame3)
cad.view('xyzr')
#
# I/O frame
#
io_frame = Frame(root)
io_frame.grid(row=2,column=1,sticky=N)
#cad_frame.bind('<Motion>',msg_nomsg)
   #
   # input frame
   #
input_frame = Frame(io_frame)
input_frame.pack()
      #
      # .cad editor
      #
editor_frame = Frame(input_frame)
widget_text_yscrollbar = Scrollbar(editor_frame)
widget_cad_text = Text(editor_frame, bg='white', bd=5, width=cad.editor_width, height=cad.editor_height, yscrollcommand=widget_text_yscrollbar.set)
widget_cad_text.grid(row=1,column=1)
widget_text_yscrollbar.grid(row=1,column=2,sticky=N+S)
widget_text_yscrollbar.config(command=widget_cad_text.yview)
widget_cad_text.bind('<Motion>',msg_nomsg)
editor_frame.pack()
      #
      # input file
      #
cad_input_frame = Frame(input_frame)
widget_input_file = Button(cad_input_frame, text="input:",command=input_open)
widget_input_file.pack(side='left')
string_input_file = StringVar()
string_input_file.set('out.cad')
widget_cad = Entry(cad_input_frame, width=17, bg='white', textvariable=string_input_file)
widget_cad.pack(side='left')
Label(cad_input_frame, text=" ").pack(side='left')
widget_cad_save = Button(cad_input_frame, text="save")
widget_cad_save.bind('<Button-1>',cad_save)
widget_cad_save.pack(side='left')
Label(cad_input_frame, text=" ").pack(side='left')
widget_reload = Button(cad_input_frame, text="reload",command=reload)
widget_reload.pack(side='left')
cad_input_frame.pack()
      #
      # image x
      #
image_x_frame = Frame(input_frame)
Label(image_x_frame, text="x min: ").pack(side='left')
string_image_xmin = StringVar()
widget_image_xmin = Entry(image_x_frame, width=6, bg='white', textvariable=string_image_xmin)
widget_image_xmin.bind('<Return>',image_min_x)
widget_image_xmin.pack(side='left')
Label(image_x_frame, text="   x width: ").pack(side='left')
string_image_xwidth = StringVar()
widget_image_xwidth = Entry(image_x_frame, width=6, bg='white', textvariable=string_image_xwidth)
widget_image_xwidth.bind('<Return>',image_scale_y)
widget_image_xwidth.pack(side='left')
string_image_nx = StringVar()
Label(image_x_frame, textvariable = string_image_nx).pack(side='left')
      #
      # image y
      #
image_y_frame = Frame(input_frame)
Label(image_y_frame, text="y min: ").pack(side='left')
string_image_ymin = StringVar()
widget_image_ymin = Entry(image_y_frame, width=6, bg='white', textvariable=string_image_ymin)
widget_image_ymin.bind('<Return>',image_min_y)
widget_image_ymin.pack(side='left')
Label(image_y_frame, text="  y height: ").pack(side='left')
string_image_yheight = StringVar()
widget_image_yheight = Entry(image_y_frame, width=6, bg='white', textvariable=string_image_yheight)
widget_image_yheight.bind('<Return>',image_scale_x)
widget_image_yheight.pack(side='left')
string_image_ny = StringVar()
Label(image_y_frame, textvariable = string_image_ny).pack(side='left')
      #
      # image z
      #
image_z_frame = Frame(input_frame)
Label(image_z_frame, text="z min: ").pack(side='left')
string_image_zmin = StringVar()
widget_image_zmin = Entry(image_z_frame, width=6, bg='white', textvariable=string_image_zmin)
widget_image_zmin.pack(side='left')
Label(image_z_frame, text="   z max: ").pack(side='left')
string_image_zmax = StringVar()
widget_image_zmax = Entry(image_z_frame, width=6, bg='white', textvariable=string_image_zmax)
widget_image_zmax.pack(side='left')
Label(image_z_frame, text="   nz: ").pack(side='left')
string_image_nz = StringVar()
widget_image_nz = Entry(image_z_frame, width=6, bg='white', textvariable=string_image_nz)
widget_image_nz.pack(side='left')
      #
      # image intensity
      #
image_intensity_frame = Frame(input_frame)
Label(image_intensity_frame, text="intensity min: ").pack(side='left')
string_image_min = StringVar()
widget_image_min = Entry(image_intensity_frame, width=6, bg='white', textvariable=string_image_min)
widget_image_min.pack(side='left')
Label(image_intensity_frame, text="   intensity max: ").pack(side='left')
string_image_max = StringVar()
widget_image_max = Entry(image_intensity_frame, width=6, bg='white', textvariable=string_image_max)
widget_image_max.pack(side='left')
   #
   # image units
   #   
image_units_frame = Frame(input_frame)
Label(image_units_frame, text="inches per unit: ").pack(side='left')
string_image_units = StringVar()
widget_image_units = Entry(image_units_frame, width=6, bg='white', textvariable=string_image_units)
widget_image_units.pack(side='left')
      #
      # image invert
      #
image_invert_frame = Frame(input_frame)
Label(image_invert_frame, text=" ").pack(side='left')
widget_image_invert = Button(image_invert_frame, text="invert image")
widget_image_invert.pack(side='left')
widget_image_invert.bind('<Button-1>',invert_image)
   #
   # output frame
   #
output_frame = Frame(io_frame)
output_frame.pack()
      #
      # controls
      #
control_frame = Frame(output_frame)
widget_render = Button(control_frame, text="render")
widget_render.bind('<Button-1>',render_button)
widget_render.pack(side='left')
Label(control_frame, text=" ").pack(side='left')
canvas_logo = Canvas(control_frame, width=26, height=26, background="white")
canvas_logo.create_oval(2,2,8,8,fill="red",outline="")
canvas_logo.create_rectangle(11,2,17,8,fill="blue",outline="")
canvas_logo.create_rectangle(20,2,26,8,fill="blue",outline="")
canvas_logo.create_rectangle(2,11,8,17,fill="blue",outline="")
canvas_logo.create_oval(10,10,16,16,fill="red",outline="")
canvas_logo.create_rectangle(20,11,26,17,fill="blue",outline="")
canvas_logo.create_rectangle(2,20,8,26,fill="blue",outline="")
canvas_logo.create_rectangle(11,20,17,26,fill="blue",outline="")
canvas_logo.create_rectangle(20,20,26,26,fill="blue",outline="")
canvas_logo.pack(side='left')
control_text = " cad.py (%s) "%DATE
Label(control_frame, text=control_text).pack(side='left')
widget_cam = Button(control_frame, text="cam")
widget_cam.bind('<Button-1>',cam)
widget_cam.pack(side='left')
Label(control_frame, text=" ").pack(side='left')
widget_quit = Button(control_frame, text="quit", command='exit')
widget_quit.pack(side='left')
control_frame.pack()
      #
      # function string
      #
function_string_frame = Frame(output_frame)
Label(function_string_frame, text="function:").grid(row=1,column=1)
widget_function_yscrollbar = Scrollbar(function_string_frame)
widget_function_text = Text(function_string_frame, bg='white', bd=5, width=cad.editor_width, height=12, yscrollcommand=widget_function_yscrollbar.set, state=DISABLED)
widget_function_text.grid(row=2,column=1)
widget_function_yscrollbar.grid(row=2,column=2,sticky=N+S)
widget_function_yscrollbar.config(command=widget_function_text.yview)
function_string_frame.pack()
      #
      # CAM file
      #
cam_file_frame = Frame(output_frame)
widget_cam_menu_button = Menubutton(cam_file_frame,text="output format", relief=RAISED)
widget_cam_menu_button.pack(side='left')
widget_cam_menu = Menu(widget_cam_menu_button)
widget_cam_menu.add_command(label='.epi (Epilog)',command=select_epi)
widget_cam_menu.add_command(label='.camm (CAMM)',command=select_camm)
widget_cam_menu.add_command(label='.rml (Modela)',command=select_rml)
widget_cam_menu.add_command(label='.sbp (ShopBot)',command=select_sbp)
widget_cam_menu.add_command(label='.gcode (Gcode)',command=select_g)
widget_cam_menu.add_command(label='.ps (Postscript)',command=select_ps)
widget_cam_menu.add_command(label='.ord (OMAX)',command=select_ord)
widget_cam_menu.add_command(label='.oms (Resonetics)',command=select_oms)
widget_cam_menu.add_command(label='.grb (Gerber)',command=select_gerber)
widget_cam_menu.add_command(label='.drl (Excellon)',command=select_excellon)
widget_cam_menu.add_command(label='.stl (STL)',command=select_stl)
widget_cam_menu.add_command(label='.dxf (DXF)',command=select_dxf)
widget_cam_menu.add_command(label='.jpg (JPG)',command=select_jpg)
widget_cam_menu.add_command(label='.png (PNG)',command=select_png)
widget_cam_menu.add_command(label='.ca (CA)',command=select_ca)
widget_cam_menu.add_command(label='.uni (Universal)',command=select_uni)
widget_cam_menu.add_command(label='.epb (Epilog bitmap)',state=DISABLED)
widget_cam_menu_button['menu'] = widget_cam_menu
Label(cam_file_frame, text=" output file: ").pack(side='left')
string_cam_file = StringVar()
widget_cam_file = Entry(cam_file_frame, width=12, bg='white', textvariable=string_cam_file)
widget_cam_file.pack(side='left')
Label(cam_file_frame, text=" ").pack(side='left')
widget_cam_save = Button(cam_file_frame, text="save")
widget_cam_save.bind('<Button-1>',save_cam)
widget_cam_save.pack(side='left')
      #
      # vectorization
      #
cam_vector_frame = Frame(output_frame)
Label(cam_vector_frame, text="maximum vector fit error (lattice units): ").pack(side='left')
string_vector_error = StringVar()
string_vector_error.set('.75')
widget_vector_error = Entry(cam_vector_frame, width=6, bg='white', textvariable=string_vector_error)
widget_vector_error.pack(side='left')
      #
      # tool
      #
cam_dia_frame = Frame(output_frame)
Label(cam_dia_frame, text="tool diameter: ").pack(side='left')
string_tool_dia = StringVar()
string_tool_dia.set('0')
widget_tool_dia = Entry(cam_dia_frame, width=6, bg='white', textvariable=string_tool_dia)
widget_tool_dia.pack(side='left')
Label(cam_dia_frame, text=" tool overlap: ").pack(side='left')
string_tool_overlap = StringVar()
string_tool_overlap.set('0.5')
widget_tool_overlap = Entry(cam_dia_frame, width=6, bg='white', textvariable=string_tool_overlap)
widget_tool_overlap.pack(side='left')
      #
      # contour
      #
cam_contour_frame = Frame(output_frame)
Label(cam_contour_frame, text=" # contours (-1 for max): ").pack(side='left')
string_num_contours = StringVar()
string_num_contours.set('0')
widget_num_contours = Entry(cam_contour_frame, width=6, bg='white', textvariable=string_num_contours)
widget_num_contours.pack(side='left')
Label(cam_contour_frame, text=" ").pack(side='left')
widget_cam_contour = Button(cam_contour_frame, text="contour")
widget_cam_contour.pack(side='left')
widget_cam_contour.bind('<Button-1>',contour)
      #
      # laser power
      #
laser_frame1 = Frame(output_frame)
Label(laser_frame1, text=" power:").pack(side='left')
string_laser_power = StringVar()
Entry(laser_frame1, width=6, bg='white', textvariable=string_laser_power).pack(side='left')
Label(laser_frame1, text=" speed:").pack(side='left')
string_laser_speed = StringVar()
Entry(laser_frame1, width=6, bg='white', textvariable=string_laser_speed).pack(side='left')
Label(laser_frame1, text=" rate: ").pack(side='left')
string_laser_rate = StringVar()
Entry(laser_frame1, width=6, bg='white', textvariable=string_laser_rate).pack(side='left')
      #
      # power range
      #
laser_frame2 = Frame(output_frame)
Label(laser_frame2, text=" min power:").pack(side='left')
string_laser_min_power = StringVar()
Entry(laser_frame2, width=6, bg='white', textvariable=string_laser_min_power).pack(side='left')
Label(laser_frame2, text="%  max power:").pack(side='left')
string_laser_max_power = StringVar()
Entry(laser_frame2, width=6, bg='white', textvariable=string_laser_max_power).pack(side='left')
Label(laser_frame2, text="%").pack(side='left')
      #
      # autofocus
      #
laser_frame3 = Frame(output_frame)
integer_laser_autofocus = IntVar()
widget_autofocus = Checkbutton(laser_frame3, text="Auto Focus", variable=integer_laser_autofocus).pack(side='left')
      #
      # cutting
      #
cut_frame = Frame(output_frame)
Label(cut_frame, text="force: ").pack(side='left')
string_cut_force = StringVar()
Entry(cut_frame, width=6, bg='white', textvariable=string_cut_force).pack(side='left')
Label(cut_frame, text=" velocity:").pack(side='left')
string_cut_velocity = StringVar()
Entry(cut_frame, width=6, bg='white', textvariable=string_cut_velocity).pack(side='left')
      #
      # speed
      #
speed_frame = Frame(output_frame)
Label(speed_frame, text="xy speed:").pack(side='left')
string_xy_speed = StringVar()
Entry(speed_frame, width=4, bg='white', textvariable=string_xy_speed).pack(side='left')
Label(speed_frame, text=" z speed:").pack(side='left')
string_z_speed = StringVar()
Entry(speed_frame, width=4, bg='white', textvariable=string_z_speed).pack(side='left')
      #
      # jog
      #
jog_frame = Frame(output_frame)
Label(jog_frame, text="jog xy speed:").pack(side='left')
string_jog_xy_speed = StringVar()
Entry(jog_frame, width=4, bg='white', textvariable=string_jog_xy_speed).pack(side='left')
Label(jog_frame, text=" z speed:").pack(side='left')
string_jog_z_speed = StringVar()
Entry(jog_frame, width=4, bg='white', textvariable=string_jog_z_speed).pack(side='left')
Label(jog_frame, text=" z:").pack(side='left')
string_jog_z = StringVar()
Entry(jog_frame, width=4, bg='white', textvariable=string_jog_z).pack(side='left')
      #
      # RML move
      #
rml_move_frame = Frame(output_frame)
Label(rml_move_frame, text="x: ").pack(side='left')
string_rml_x_move = StringVar()
Entry(rml_move_frame, width=6, bg='white', textvariable=string_rml_x_move).pack(side='left')
Label(rml_move_frame, text=" y: ").pack(side='left')
string_rml_y_move = StringVar()
Entry(rml_move_frame, width=6, bg='white', textvariable=string_rml_y_move).pack(side='left')
Label(rml_move_frame, text=" ").pack(side='left')
widget_rml_move = Button(rml_move_frame, text="move")
widget_rml_move.pack(side='left')
widget_rml_move.bind('<Button-1>',rml_move)
      #
      # G codes
      #
g_frame = Frame(output_frame)
Label(g_frame, text=" feed rate:").pack(side="left")
string_g_feed_rate = StringVar()
Entry(g_frame, width=6, textvariable=string_g_feed_rate).pack(side="left")
Label(g_frame, text=" spindle speed:").pack(side="left")
string_g_spindle_speed = StringVar()
Entry(g_frame, width=6, textvariable=string_g_spindle_speed).pack(side="left")
Label(g_frame, text=" tool:").pack(side="left")
string_g_tool = StringVar()
Entry(g_frame, width=3, textvariable=string_g_tool).pack(side="left")
integer_g_cool = IntVar()
widget_g_cool = Checkbutton(g_frame, text="coolant", variable=integer_g_cool)
widget_g_cool.pack(side="left")
      #
      # waterjet
      #
waterjet_frame = Frame(output_frame)
Label(waterjet_frame,text="lead-in/out: ").pack(side='left')
string_lead_in = StringVar()
widget_lead_in = Entry(waterjet_frame, width=4, bg='white', textvariable=string_lead_in)
widget_lead_in.pack(side='left')
Label(waterjet_frame,text="quality: ").pack(side='left')
string_quality = StringVar()
widget_quality = Entry(waterjet_frame, width=4, bg='white', textvariable=string_quality)
widget_quality.pack(side='left')
      #
      # excimer
      #
excimer_frame = Frame(output_frame)
Label(excimer_frame,text="period (usec): ").pack(side='left')
string_pulse_period = StringVar()
widget_pulse_period = Entry(excimer_frame, width=5, bg='white', textvariable=string_pulse_period)
widget_pulse_period.pack(side='left')
Label(excimer_frame,text="velocity: ").pack(side='left')
string_cut_vel = StringVar()
widget_cut_vel = Entry(excimer_frame, width=4, bg='white', textvariable=string_cut_vel)
widget_cut_vel.pack(side='left')
Label(excimer_frame,text="acceleration: ").pack(side='left')
string_cut_accel = StringVar()
widget_cut_accel = Entry(excimer_frame, width=4, bg='white', textvariable=string_cut_accel)
widget_cut_accel.pack(side='left')
      #
      # STL
      #
STL_frame = Frame(output_frame)
widget_STL_triangulate = Button(STL_frame, text="triangulate")
widget_STL_triangulate.pack(side='left')
widget_STL_triangulate.bind('<Button-1>',triangulate)
      #
      # Gerber
      #
Gerber_frame = Frame(output_frame)
widget_Gerber_convert = Button(Gerber_frame, text="convert")
widget_Gerber_convert.pack(side='left')
widget_Gerber_convert.bind('<Button-1>',flash)
      #
      # Excellon
      #
Excellon_frame = Frame(output_frame)
widget_Excellon_convert = Button(Excellon_frame, text="convert")
widget_Excellon_convert.pack(side='left')
widget_Excellon_convert.bind('<Button-1>',flash)
      #
      # filling
      #
fill_frame = Frame(output_frame)
integer_fill = IntVar()
widget_fill = Checkbutton(fill_frame, text="fill polygons", variable=integer_fill).pack(side='left')
      #
      # send to
      #
send_to_frame = Frame(output_frame)
widget_send_to = Button(send_to_frame, text="send to machine")
widget_send_to.bind('<Button-1>',send_to)
widget_send_to.pack(side='left')
string_send_to_time = StringVar()
string_send_to_time.set("")
Label(send_to_frame,textvariable=string_send_to_time).pack(side='left')

#
# define .cad template
#
cad_template = """#
# .cad template
#

#
# define shapes and transformation
#
# circle(x0, y0, r)
# cylinder(x0, y0, z0, z1, r)
# cone(x0, y0, z0, z1, r0)
# sphere(x0, y0, z0, r)
# torus(x0, y0, z0, r0, r1)
# rectangle(x0, x1, y0, y1)
# cube(x0, x1, y0, y1, z0, z1)
# right_triangle(x0, y0, h)
# triangle(x0, y0, x1, y1, x2, y2) (points in clockwise order)
# pyramid(x0, x1, y0, y1, z0, z1)
# function(Z_of_XY)
# functions(upper_Z_of_XY,lower_Z_of_XY)
# add(part1, part2)
# subtract(part1, part2)
# intersect(part1, part2)
# move(part,dx,dy)
# translate(part,dx,dy,dz)
# rotate(part, angle)
# rotate_x(part, angle)
# rotate_y(part, angle)
# rotate_z(part, angle)
# rotate_90(part)
# rotate_180(part)
# rotate_270(part)
# reflect_x(part)
# reflect_y(part)
# reflect_z(part)
# reflect_xy(part)
# reflect_xz(part)
# reflect_yz(part)
# scale_x(part, x0, sx)
# scale_y(part, y0, sy)
# scale_z(part, z0, sz)
# scale_xy(part, x0, y0, sxy)
# scale_xyz(part, x0, y0, z0, sxyz)
# coscale_x_y(part, x0, y0, y1, angle0, angle1, amplitude, offset)
# coscale_x_z(part, x0, z0, z1, angle0, angle1, amplitude, offset)
# coscale_xy_z(part, x0, y0, z0, z1, angle0, angle1, amplitude, offset)
# taper_x_y(part, x0, y0, y1, s0, s1)
# taper_x_z(part, x0, z0, z1, s0, s1)
# taper_xy_z(part, x0, y0, z0, z1, s0, s1)
# shear_x_y(part, y0, y1, dx0, dx1)
# shear_x_z(part, z0, z1, dx0, dx1)
# (more to come)

def circle(x0, y0, r):
   part = "(((X-x0)**2 + (Y-y0)**2) <= r**2)"
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'r',str(r))
   return part

def cylinder(x0, y0, z0, z1, r):
   part = "(((X-x0)**2 + (Y-y0)**2 <= r**2) & (Z >= z0) & (Z <= z1))"
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'z0',str(z0))
   part = replace(part,'z1',str(z1))
   part = replace(part,'r',str(r))
   return part

def cone(x0, y0, z0, z1, r0):
   part = cylinder(x0, y0, z0, z1, r0)
   part = taper_xy_z(part, x0, y0, z0, z1, 1.0, 0.0)
   return part

def sphere(x0, y0, z0, r):
   part = "(((X-x0)**2 + (Y-y0)**2 + (Z-z0)**2) <= r**2)"
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'z0',str(z0))
   part = replace(part,'r',str(r))
   return part

def torus(x0, y0, z0, r0, r1):
   part = "(((r0 - sqrt((X-x0)**2 + (Y-y0)**2))**2 + (Z-z0)**2) <= r1**2)"
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'z0',str(z0))
   part = replace(part,'r0',str(r0))
   part = replace(part,'r1',str(r1))
   return part

def rectangle(x0, x1, y0, y1):
   part = "((X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1))"
   part = replace(part,'x0',str(x0))
   part = replace(part,'x1',str(x1))
   part = replace(part,'y0',str(y0))
   part = replace(part,'y1',str(y1))
   return part

def cube(x0, x1, y0, y1, z0, z1):
   part = "((X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1) & (Z >= z0) & (Z <= z1))"
   part = replace(part,'x0',str(x0))
   part = replace(part,'x1',str(x1))
   part = replace(part,'y0',str(y0))
   part = replace(part,'y1',str(y1))
   part = replace(part,'z0',str(z0))
   part = replace(part,'z1',str(z1))
   return part

def right_triangle(x0, y0, h):
   part = "((X > x0) & (X < x0 + h - (Y-y0)) & (Y > y0))"
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'h',str(h))
   return part

def triangle(x0, y0, x1, y1, x2, y2): # points in clockwise order
   part = "((((y1-y0)*(X-x0)-(x1-x0)*(Y-y0)) >= 0) & (((y2-y1)*(X-x1)-(x2-x1)*(Y-y1)) >= 0) & (((y0-y2)*(X-x2)-(x0-x2)*(Y-y2)) >= 0))"
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'x1',str(x1))
   part = replace(part,'y1',str(y1))
   part = replace(part,'x2',str(x2))
   part = replace(part,'y2',str(y2))
   return part

def pyramid(x0, x1, y0, y1, z0, z1):
   part = cube(x0, x1, y0, y1, z0, z1)
   part = taper_xy_z(part, (x0+x1)/2., (y0+y1)/2., z0, z1, 1.0, 0.0)
   return part

def function(Z_of_XY):
   part = '(Z <= '+Z_of_XY+')'
   return part

def functions(upper_Z_of_XY,lower_Z_of_XY):
   part = '(Z <= '+upper_Z_of_XY+') & (Z >= '+lower_Z_of_XY+')'
   return part

def add(part1, part2):
   part = "part1 | part2"
   part = replace(part,'part1',part1)
   part = replace(part,'part2',part2)
   return part

def subtract(part1, part2):
   part = "(part1) & ~(part2)"
   part = replace(part,'part1',part1)
   part = replace(part,'part2',part2)
   return part

def intersect(part1, part2):
   part = "(part1) & (part2)"
   part = replace(part,'part1',part1)
   part = replace(part,'part2',part2)
   return part

def move(part,dx,dy):
   part = replace(part,'X','(X-'+str(dx)+')')
   part = replace(part,'Y','(Y-'+str(dy)+')')
   return part   

def translate(part,dx,dy,dz):
   part = replace(part,'X','(X-'+str(dx)+')')
   part = replace(part,'Y','(Y-'+str(dy)+')')
   part = replace(part,'Z','(Z-'+str(dz)+')')
   return part   

def rotate(part, angle):
   angle = angle*pi/180
   part = replace(part,'X','(cos(angle)*X+sin(angle)*y)')
   part = replace(part,'Y','(-sin(angle)*X+cos(angle)*y)')
   part = replace(part,'y','Y')
   part = replace(part,'angle',str(angle))
   return part

def rotate_x(part, angle):
   angle = angle*pi/180
   part = replace(part,'Y','(cos(angle)*Y+sin(angle)*z)')
   part = replace(part,'Z','(-sin(angle)*Y+cos(angle)*z)')
   part = replace(part,'z','Z')
   part = replace(part,'angle',str(angle))
   return part

def rotate_y(part, angle):
   angle = angle*pi/180
   part = replace(part,'X','(cos(angle)*X+sin(angle)*z)')
   part = replace(part,'Z','(-sin(angle)*X+cos(angle)*z)')
   part = replace(part,'z','Z')
   part = replace(part,'angle',str(angle))
   return part

def rotate_z(part, angle):
   angle = angle*pi/180
   part = replace(part,'X','(cos(angle)*X+sin(angle)*y)')
   part = replace(part,'Y','(-sin(angle)*X+cos(angle)*y)')
   part = replace(part,'y','Y')
   part = replace(part,'angle',str(angle))
   return part

def rotate_90(part):
   part = reflect_xy(part)
   part = reflect_y(part)
   return part

def rotate_180(part):
   part = reflect_xy(part)
   part = reflect_y(part)
   part = reflect_xy(part)
   part = reflect_y(part)
   return part

def rotate_270(part):
   part = reflect_xy(part)
   part = reflect_y(part)
   part = reflect_xy(part)
   part = reflect_y(part)
   part = reflect_xy(part)
   part = reflect_y(part)
   return part

def reflect_x(part):
   part = replace(part,'X','(-X)')
   return part

def reflect_y(part):
   part = replace(part,'Y','(-Y)')
   return part

def reflect_z(part):
   part = replace(part,'Z','(-Z)')
   return part

def reflect_xy(part):
   part = replace(part,'X','temp')
   part = replace(part,'Y','X')
   part = replace(part,'temp','Y')
   return part

def reflect_xz(part):
   part = replace(part,'X','temp')
   part = replace(part,'Z','X')
   part = replace(part,'temp','Z')
   return part

def reflect_yz(part):
   part = replace(part,'Y','temp')
   part = replace(part,'Z','Y')
   part = replace(part,'temp','Z')
   return part

def scale_x(part, x0, sx):
   part = replace(part,'X','(x0 + (X-x0)/sx)')
   part = replace(part,'x0',str(x0))
   part = replace(part,'sx',str(sx))
   return part

def scale_y(part, y0, sy):
   part = replace(part,'Y','(y0 + (Y-y0)/sy)')
   part = replace(part,'y0',str(y0))
   part = replace(part,'sy',str(sy))
   return part

def scale_z(part, z0, sz):
   part = replace(part,'Z','(z0 + (Z-z0)/sz)')
   part = replace(part,'z0',str(z0))
   part = replace(part,'sz',str(sz))
   return part

def scale_xy(part, x0, y0, sxy):
   part = replace(part,'X','(x0 + (X-x0)/sxy)')
   part = replace(part,'Y','(y0 + (Y-y0)/sxy)')
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'sxy',str(sxy))
   return part

def scale_xyz(part, x0, y0, z0, sxyz):
   part = replace(part,'X','(x0 + (X-x0)/sxyz)')
   part = replace(part,'Y','(y0 + (Y-y0)/sxyz)')
   part = replace(part,'Z','(z0 + (Z-z0)/sxyz)')
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'z0',str(z0))
   part = replace(part,'sxyz',str(sxyz))
   return part

def coscale_x_y(part, x0, y0, y1, angle0, angle1, amplitude, offset):
   phase0 = pi*angle0/180.
   phase1 = pi*angle1/180.
   part = replace(part,'X','(x0 + (X-x0)/(offset + amplitude*cos(phase0 + (phase1-phase0)*(Y-y0)/(y1-y0))))')
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'y1',str(y1))
   part = replace(part,'phase0',str(phase0))
   part = replace(part,'phase1',str(phase1))
   part = replace(part,'amplitude',str(amplitude))
   part = replace(part,'offset',str(offset))
   return part

def coscale_x_z(part, x0, z0, z1, angle0, angle1, amplitude, offset):
   phase0 = pi*angle0/180.
   phase1 = pi*angle1/180.
   part = replace(part,'X','(x0 + (X-x0)/(offset + amplitude*cos(phase0 + (phase1-phase0)*(Z-z0)/(z1-z0))))')
   part = replace(part,'x0',str(x0))
   part = replace(part,'z0',str(z0))
   part = replace(part,'z1',str(z1))
   part = replace(part,'phase0',str(phase0))
   part = replace(part,'phase1',str(phase1))
   part = replace(part,'amplitude',str(amplitude))
   part = replace(part,'offset',str(offset))
   return part

def coscale_xy_z(part, x0, y0, z0, z1, angle0, angle1, amplitude, offset):
   phase0 = pi*angle0/180.
   phase1 = pi*angle1/180.
   part = replace(part,'X','(x0 + (X-x0)/(offset + amplitude*cos(phase0 + (phase1-phase0)*(Z-z0)/(z1-z0))))')
   part = replace(part,'Y','(y0 + (Y-y0)/(offset + amplitude*cos(phase0 + (phase1-phase0)*(Z-z0)/(z1-z0))))')
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'z0',str(z0))
   part = replace(part,'z1',str(z1))
   part = replace(part,'phase0',str(phase0))
   part = replace(part,'phase1',str(phase1))
   part = replace(part,'amplitude',str(amplitude))
   part = replace(part,'offset',str(offset))
   return part

def taper_x_y(part, x0, y0, y1, s0, s1):
   part = replace(part,'X','(x0 + (X-x0)*(y1-y0)/(s1*(Y-y0) + s0*(y1-Y)))')
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'y1',str(y1))
   part = replace(part,'s0',str(s0))
   part = replace(part,'s1',str(s1))
   return part

def taper_x_z(part, x0, z0, z1, s0, s1):
   part = replace(part,'X','(x0 + (X-x0)*(z1-z0)/(s1*(Z-z0) + s0*(z1-Z)))')
   part = replace(part,'x0',str(x0))
   part = replace(part,'z0',str(z0))
   part = replace(part,'z1',str(z1))
   part = replace(part,'s0',str(s0))
   part = replace(part,'s1',str(s1))
   return part

def taper_xy_z(part, x0, y0, z0, z1, s0, s1):
   part = replace(part,'X','(x0 + (X-x0)*(z1-z0)/(s1*(Z-z0) + s0*(z1-Z)))')
   part = replace(part,'Y','(y0 + (Y-y0)*(z1-z0)/(s1*(Z-z0) + s0*(z1-Z)))')
   part = replace(part,'x0',str(x0))
   part = replace(part,'y0',str(y0))
   part = replace(part,'z0',str(z0))
   part = replace(part,'z1',str(z1))
   part = replace(part,'s0',str(s0))
   part = replace(part,'s1',str(s1))
   return part

def shear_x_y(part, y0, y1, dx0, dx1):
   part = replace(part,'X','(X - dx0 - (dx1-dx0)*(Y-y0)/(y1-y0))')
   part = replace(part,'y0',str(y0))
   part = replace(part,'y1',str(y1))
   part = replace(part,'dx0',str(dx0))
   part = replace(part,'dx1',str(dx1))
   return part

def shear_x_z(part, z0, z1, dx0, dx1):
   part = replace(part,'X','(X - dx0 - (dx1-dx0)*(Z-z0)/(z1-z0))')
   part = replace(part,'z0',str(z0))
   part = replace(part,'z1',str(z1))
   part = replace(part,'dx0',str(dx0))
   part = replace(part,'dx1',str(dx1))
   return part

def coshear_x_z(part, z0, z1, angle0, angle1, amplitude, offset):
   phase0 = pi*angle0/180.
   phase1 = pi*angle1/180.
   part = replace(part,'X','(X - offset - amplitude*cos(phase0 + (phase1-phase0)*(Z-z0)/(z1-z0)))')
   part = replace(part,'z0',str(z0))
   part = replace(part,'z1',str(z1))
   part = replace(part,'phase0',str(phase0))
   part = replace(part,'phase1',str(phase1))
   part = replace(part,'amplitude',str(amplitude))
   part = replace(part,'offset',str(offset))
   return part

#
# define part
#

d = .5
teapot = cylinder(0,0,-d,d,d)
teapot = coscale_xy_z(teapot,0,0,-d,d,-90,90,.5,.75)

handle = torus(0,0,0,3.5*d/5.,d/10.)
handle = reflect_xz(handle)
handle = reflect_xy(handle)
handle = scale_x(handle,0,.75)
handle = scale_y(handle,0,3)
handle = translate(handle,-6*d/5.,0,0)
teapot = add(teapot,handle)

spout = torus(2.1*d,-.2*d,0,1.1*d,.2*d)
spout = reflect_yz(spout)
spout = intersect(spout,cube(-3*d,1.8*d,-3*d,3*d,0,3*d))
teapot = add(teapot,spout)

interior = cylinder(0,0,.1-d,.1+d,d-.1)
interior = coscale_xy_z(interior,0,0,-d,d,-90,90,.5,.75)
teapot = subtract(teapot,interior)

spout_interior = torus(2.1*d,-.2*d,0,1.1*d,.15*d)
spout_interior = reflect_yz(spout_interior)
spout_interior = intersect(spout_interior,cube(-3*d,1.8*d,-3*d,3*d,0,3*d))
teapot = subtract(teapot,spout_interior)

part = teapot

part = subtract(part,cube(0,3*d,-3*d,0,-3*d,3*d))

#
# define limits and parameters
#

width = 2.5
x0 = 0
y0 = 0
z0 = 0
cad.xmin = x0-width/2. # min x to render
cad.xmax = x0+width/2. # max x to render
cad.ymin = y0-width/2. # min y to render
cad.ymax = y0+width/2. # max y to render
#cad.zmin = z0-width/4. # min z to render
#cad.zmax = z0+width/4. # max x to render
cad.zmin = z0-width/4. # min z to render
cad.zmax = z0+width/4. # max x to render
cad.rx = 30 # x view rotation (degrees)
cad.rz = 20 # z view rotation (degrees)
dpi = 100 # rendering resolution
cad.nx = int(dpi*(cad.xmax-cad.xmin)) # x points to render
cad.ny = int(dpi*(cad.ymax-cad.ymin)) # y points to render
cad.nz = int(dpi*(cad.zmax-cad.zmin)) # z points to render
cad.inches_per_unit = 1.0 # use inch units

#
# assign part to cad.function
#

cad.function = part

"""

#
# check config file for window parameters
#

cad_path = os.path.dirname(sys.argv[0])
if (sys.argv[0] == "cad.py"):
   cfg_path = "cad.cfg"
else:
   cfg_path = os.path.dirname(sys.argv[0])+"/cad.cfg"
try:
   config_file = open(cfg_path, 'r')
   string_msg.set("found "+cfg_path)
   while 1:
      line = config_file.readline()
      if (find(line,"window size:") == 0):
         string_window_size.set(int(line[12:]))
      elif (find(line,"editor width:") == 0):
         string_editor_width.set(int(line[13:]))
      elif (find(line,"editor height:") == 0):
         string_editor_height.set(int(line[14:]))
      elif (line == ""):
         break
   config_file.close()
   resize_editor(0)
except:
   string_msg.set(cfg_path+" not found")

#
# read input file if on command line, otherwise use template
#

if len(sys.argv) == 2:
   filename = sys.argv[1]
   string_input_file.set(filename)
   if (find(filename,'.cad') != -1):
      cad_load(0)
   elif ((find(filename,'.jpg') != -1) | (find(filename,'.JPG') != -1) |
      (find(filename,'.png') != -1) | (find(filename,'.PNG') != -1) |
      (find(filename,'.gif') != -1) | (find(filename,'.GIF') != -1)):
      widget_cad_text.delete("1.0",END)
      image_load(0)
   else:
      string_msg.set("unsupported input file format")
      root.update()
else:
   widget_cad_text.insert("1.0",cad_template)

#
# start GUI
#

root.mainloop()
