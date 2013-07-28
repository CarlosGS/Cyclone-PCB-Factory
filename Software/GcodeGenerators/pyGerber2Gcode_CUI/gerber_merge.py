#!/usr/bin/python
# coding: UTF-8

from string import *
from math import *
#from struct import *
import os
import sys
#import datetime
import locale
import re
TINY = 1e-6
SMALL = 1e-3
TEST_POINTS1 =[]
TEST_POINTS2 =[]
TEST_POINT_R = 0.01

PRE_IN_FLAG = -1

class POLYGON:
	def __init__(self, x_min, x_max, y_min, y_max, points, delete):
		self.x_min = x_min
		self.x_max = x_max
		self.y_min = y_min
		self.y_max = y_max
		self.points = points
		self.delete = delete

class LINE:
	def __init__(self, x1, y1, x2, y2, inside, delete):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.inside = inside
		self.delete = delete
def merge_lines(gGCODES):
	print("merge lines ...")
	i = 0
	while i< len(gGCODES)-1:
		if(gGCODES[i].gtype <= 2):
			i += 1
			continue
		dx1 = gGCODES[i].x2-gGCODES[i].x1
		dy1 = gGCODES[i].y2-gGCODES[i].y1
		abs_dx1 = abs(dx1)
		abs_dy1 = abs(dy1)
		w1 = gGCODES[i].mod1
		if gGCODES[i].gtype == 4:
			w1 = gGCODES[i].mod2
		x1min = gGCODES[i].x1
		x1max = gGCODES[i].x2
		if(gGCODES[i].x2<gGCODES[i].x1):
			x1min = gGCODES[i].x2
			x1max = gGCODES[i].x1
		y1min = gGCODES[i].y1
		y1max = gGCODES[i].y2
		if(gGCODES[i].y2<gGCODES[i].y1):
			y1min = gGCODES[i].y2
			y1max = gGCODES[i].y1
		if dx1 != 0:
			a1 = (dy1)/(dx1)
			b1 = gGCODES[i].y1 - a1 * gGCODES[i].x1
		j = i + 1
		#print("i =",i,", j =",j
		while j< len(gGCODES):
			if(gGCODES[j].gtype <= 2):
				j += 1
				continue
			if(gGCODES[i].gtype <= 2):
				#i += 1
				break
			if(abs_dy1 < TINY):	#Line 1 is Horizontal
				if (abs(gGCODES[j].y2-gGCODES[j].y1) < TINY): #Line 2 is Horizontal
					w2 = gGCODES[j].mod1
					if gGCODES[j].gtype == 4:
						w2 = gGCODES[j].mod2
					if abs(gGCODES[i].y1 - gGCODES[j].y1) < TINY:
						#
						x2min = gGCODES[j].x1
						x2max = gGCODES[j].x2
						if(gGCODES[j].x2<gGCODES[j].x1):
							x2min = gGCODES[j].x2
							x2max = gGCODES[j].x1

						if (x2min <= x1min) and (x2max >= x1max) and (w2 >= w1):
							gGCODES[i].gtype = 0
							break
						elif(x1min <= x2min) and (x1max >= x2max) and (w1 >= w2):
							gGCODES[j].gtype = 0
							j += 1
							continue
						elif abs(w1-w2) < TINY:
							if (x1min <= x2min) and (x1max >= x2min):
								if gGCODES[j].gtype == 3:
									gGCODES[j].x2 = x2max
									gGCODES[j].y2 = gGCODES[i].y1
									gGCODES[j].x1 = x1min
									gGCODES[j].y1 = gGCODES[i].y1
									if gGCODES[i].gtype == 4 or (gGCODES[i].gtype == 5 and gGCODES[i].x1 <= gGCODES[i].x2):
										gGCODES[j].gtype = 5
								elif gGCODES[j].gtype == 5:
									if gGCODES[j].x1 <= gGCODES[j].x2:
										gGCODES[j].x1 = x1min
										if gGCODES[i].gtype == 3 or (gGCODES[i].gtype == 5 and gGCODES[i].x1 >= gGCODES[i].x2):
											gGCODES[j].gtype = 3
									else:	#gGCODES[j].x1 > gGCODES[j].x2
										gGCODES[j].x2 = x1min
										if gGCODES[i].gtype == 4 or (gGCODES[i].gtype == 5 and gGCODES[i].x1 <= gGCODES[i].x2):
											gGCODES[j].gtype = 4
											gGCODES[j].mod2 = w2
								elif gGCODES[j].gtype == 4:
									gGCODES[j].x2 = x1min
									gGCODES[j].y2 = gGCODES[i].y1
									gGCODES[j].x1 = x2max
									gGCODES[j].y1 = gGCODES[i].y1
									if gGCODES[i].gtype == 3 or (gGCODES[i].gtype == 5 and gGCODES[i].x1 >= gGCODES[i].x2):
										gGCODES[j].gtype = 5
										gGCODES[j].mod1 = w2
								gGCODES[i].gtype = 0
								break
							elif (x2min <= x1min) and (x2max >= x1min):
								if gGCODES[j].gtype == 3:
									gGCODES[j].x2 = x2min
									gGCODES[j].y2 = gGCODES[i].y1
									gGCODES[j].x1 = x1max
									gGCODES[j].y1 = gGCODES[i].y1
									if gGCODES[i].gtype == 4 or (gGCODES[i].gtype == 5 and gGCODES[i].x1 >= gGCODES[i].x2):
										gGCODES[j].gtype = 5
								elif gGCODES[j].gtype == 5:
									if gGCODES[j].x1 >= gGCODES[j].x2:
										#gGCODES[j].x2 = x2min	
										gGCODES[j].x1 = x1max
										if gGCODES[i].gtype == 3 or (gGCODES[i].gtype == 5 and gGCODES[i].x1 <= gGCODES[i].x2):
											gGCODES[j].gtype = 3
									else:	#gGCODES[j].x1 < gGCODES[j].x2
										gGCODES[j].x2 = x1max
										#gGCODES[j].x1 = x1min
										if gGCODES[i].gtype == 4 or (gGCODES[i].gtype == 5 and gGCODES[i].x1 >= gGCODES[i].x2):
											gGCODES[j].gtype = 4
											gGCODES[j].mod2 = w2
								elif gGCODES[j].gtype == 4:
									gGCODES[j].x2 = x1max
									gGCODES[j].y2 = gGCODES[i].y1
									gGCODES[j].x1 = x2min
									gGCODES[j].y1 = gGCODES[i].y1
									if gGCODES[i].gtype == 3 or (gGCODES[i].gtype == 5 and gGCODES[i].x1 <= gGCODES[i].x2):
										gGCODES[j].gtype = 5
										gGCODES[j].mod1 = w2
								gGCODES[i].gtype = 0
								break
					elif abs(gGCODES[i].y1 - gGCODES[j].y1) <= (w2/2 + w1/2):
						#print(w2/2 + w1/2, gGCODES[i].y1 - gGCODES[j].y1
						#
						x2min = gGCODES[j].x1
						x2max = gGCODES[j].x2
						if(gGCODES[j].x2 < gGCODES[j].x1):
							x2min = gGCODES[j].x2
							x2max = gGCODES[j].x1
						#print("near"
						#if gGCODES[i].gtype == 4 and gGCODES[j].gtype == 4:
						if abs((x1max-x1min) - (x2max-x2min)) < SMALL:	#same length
							#print("same"
							if abs((x1max+x1min)/2 - (x2max+x2min)/2) < SMALL:	#same center
								#print("center"
								tmp_ymin = gGCODES[i].y1 - w1/2
								tmp_ymax = gGCODES[j].y1 + w2/2
								if tmp_ymin > gGCODES[j].y1 - w2/2:
									tmp_ymin = gGCODES[j].y1 - w2/2
								if tmp_ymax < gGCODES[i].y1 + w1/2:
									tmp_ymax = gGCODES[i].y1 + w1/2
								w2 = tmp_ymax - tmp_ymin
								y2min = (tmp_ymax + tmp_ymin)/2
								gGCODES[j].gtype = 4
								gGCODES[j].mod2 = w2
								#gGCODES[j].x2 = x2min
								gGCODES[j].y2 = y2min
								#gGCODES[j].x1 = x2min
								gGCODES[j].y1 = y2min
								gGCODES[i].gtype = 0
								break
				elif abs(gGCODES[j].x2-gGCODES[j].x1) < TINY:	#Line 2 is Vertical
					y2min = gGCODES[j].y1
					y2max = gGCODES[j].y2
					if(gGCODES[j].y2<gGCODES[j].y1):
						y2min = gGCODES[j].y2
						y2max = gGCODES[j].y1
					if (gGCODES[i].y1 >= y2min and gGCODES[i].y1 <= y2max):
						w2 = gGCODES[j].mod1
						if gGCODES[j].gtype == 4:
							w2 = gGCODES[j].mod2
						if (abs(gGCODES[j].x1 - gGCODES[i].x1) < w2):
							if gGCODES[i].gtype == 3:
								gGCODES[i].gtype = 5
						elif (abs(gGCODES[j].x1 - gGCODES[i].x2) < w2):
							if gGCODES[i].gtype == 3:
								gGCODES[i].gtype = 5
								tmpx = gGCODES[i].x2
								tmpy = gGCODES[i].y2
								gGCODES[i].x2 = gGCODES[i].x1
								gGCODES[i].y2 = gGCODES[i].y1
								gGCODES[i].x1 = tmpx
								gGCODES[i].y1 = tmpy
							elif gGCODES[i].gtype == 5:
								gGCODES[i].gtype = 4
								gGCODES[i].mod2 = w1
						j += 1
						continue
			elif(abs_dx1 < TINY):	#Line 1 is Vertical
				if (abs(gGCODES[j].y2-gGCODES[j].y1) < TINY): #Line 2 is Horizontal
					w2 = gGCODES[j].mod1
					if gGCODES[j].gtype == 4:
						w2 = gGCODES[j].mod2
					y2min = gGCODES[j].y1
					y2max = gGCODES[j].y2
					if(gGCODES[j].y2<gGCODES[j].y1):
						y2min = gGCODES[j].y2
						y2max = gGCODES[j].y1
					if (gGCODES[j].y1 >= y1min and gGCODES[j].y1 <= y1max):
						if (abs(gGCODES[i].x1 - gGCODES[j].x1) < w1):
							if gGCODES[j].gtype == 3:
								gGCODES[j].gtype = 5
							#j += 1
							#continue
						elif (abs(gGCODES[i].x1 - gGCODES[j].x2) < w1):
							w2 = gGCODES[j].mod1
							if gGCODES[j].gtype == 4:
								w2 = gGCODES[j].mod2
							if gGCODES[j].gtype == 3:
								gGCODES[j].gtype = 5
								tmpx = gGCODES[j].x2
								tmpy = gGCODES[j].y2
								gGCODES[j].x2 = gGCODES[j].x1
								gGCODES[j].y2 = gGCODES[j].y1
								gGCODES[j].x1 = tmpx
								gGCODES[j].y1 = tmpy
							elif gGCODES[j].gtype == 5:
								gGCODES[j].gtype = 4
								gGCODES[j].mod2 = w2
						j += 1
						continue
				elif abs(gGCODES[j].x2-gGCODES[j].x1) < TINY:	#Line 2 is Vertical
					#Overlap
					w2 = gGCODES[j].mod1
					if gGCODES[j].gtype == 4:
						w2 = gGCODES[j].mod2
					if abs(gGCODES[i].x1 - gGCODES[j].x1) < TINY:
						y2min = gGCODES[j].y1
						y2max = gGCODES[j].y2
						if(gGCODES[j].y2<gGCODES[j].y1):
							y2min = gGCODES[j].y2
							y2max = gGCODES[j].y1
						if (y2min <= y1min) and (y2max >= y1max) and (w2 >= w1):
							gGCODES[i].gtype = 0
							break
						elif(y1min <= y2min) and (y1max >= y2max) and (w1 >= w2):
							gGCODES[j].gtype = 0
							j += 1
							continue
						#elif(y1max <= y2max) and (y2min <= y1max) and abs(w2-w1) < TINY:
						elif abs(w1-w2) < TINY:
							if (y1min <= y2min) and (y1max >= y2min):
								if gGCODES[j].gtype == 3:
									gGCODES[j].x2 = gGCODES[i].x1
									gGCODES[j].y2 = y2max
									gGCODES[j].x1 = gGCODES[i].x1
									gGCODES[j].y1 = y1min
									if gGCODES[i].gtype == 4 or (gGCODES[i].gtype == 5 and gGCODES[i].y1 <= gGCODES[i].y2):
										gGCODES[j].gtype = 5
								elif gGCODES[j].gtype == 5:
									if gGCODES[j].y1 <= gGCODES[j].y2:
										gGCODES[j].y1 = y1min
										if gGCODES[i].gtype == 3 or (gGCODES[i].gtype == 5 and gGCODES[i].y1 >= gGCODES[i].y2):
											gGCODES[j].gtype = 3
									else:	#gGCODES[j].y1 > gGCODES[j].y2
										gGCODES[j].y2 = y1min
										if gGCODES[i].gtype == 4 or (gGCODES[i].gtype == 5 and gGCODES[i].y1 <= gGCODES[i].y2):
											gGCODES[j].gtype = 4
											gGCODES[j].mod2 = w2
								elif gGCODES[j].gtype == 4:
									gGCODES[j].x2 = gGCODES[i].x1
									gGCODES[j].y2 = y1min
									gGCODES[j].x1 = gGCODES[i].x1
									gGCODES[j].y1 = y2max
									if gGCODES[i].gtype == 3 or (gGCODES[i].gtype == 5 and gGCODES[i].y1 >= gGCODES[i].y2):
										gGCODES[j].gtype = 5
										gGCODES[j].mod1 = w2
								gGCODES[i].gtype = 0
								break
							elif (y2min <= y1min) and (y2max >= y1min):
								if gGCODES[j].gtype == 3:
									gGCODES[j].x2 = gGCODES[i].x1
									gGCODES[j].y2 = y2min
									gGCODES[j].x1 = gGCODES[i].x1
									gGCODES[j].y1 = y1max
									if gGCODES[i].gtype == 4 or (gGCODES[i].gtype == 5 and gGCODES[i].y1 >= gGCODES[i].y2):
										gGCODES[j].gtype = 5
								elif gGCODES[j].gtype == 5:
									if gGCODES[j].y1 >= gGCODES[j].y2:
										gGCODES[j].y1 = y1max
										if gGCODES[i].gtype == 3 or (gGCODES[i].gtype == 5 and gGCODES[i].y1 <= gGCODES[i].y2):
											gGCODES[j].gtype = 3
									else:	#gGCODES[j].y1 < gGCODES[j].y2
										gGCODES[j].y2 = y1max
										if gGCODES[i].gtype == 4 or (gGCODES[i].gtype == 5 and gGCODES[i].y1 >= gGCODES[i].y2):
											gGCODES[j].gtype = 4
											gGCODES[j].mod2 = w2
								elif gGCODES[j].gtype == 4:
									gGCODES[j].x2 = gGCODES[i].x1
									gGCODES[j].y2 = y1min
									gGCODES[j].x1 = gGCODES[i].x1
									gGCODES[j].y1 = y2max
									if gGCODES[i].gtype == 3 or (gGCODES[i].gtype == 5 and gGCODES[i].y1 <= gGCODES[i].y2):
										gGCODES[j].gtype = 5
										gGCODES[j].mod1 = w2
								gGCODES[i].gtype = 0
								break
					elif abs(gGCODES[i].x1 - gGCODES[j].x1) < (w2/2 + w1/2):
						#if gGCODES[i].gtype == 4 and gGCODES[j].gtype == 4:
						y2min = gGCODES[j].y1
						y2max = gGCODES[j].y2
						if(gGCODES[j].y2<gGCODES[j].y1):
							y2min = gGCODES[j].y2
							y2max = gGCODES[j].y1
						if abs((y1max-y1min) - (y2max-y2min)) < SMALL:	#same length
							if abs((y1max+y1min)/2 - (y2max+y2min)/2) < SMALL:	#same center
								tmp_xmin = gGCODES[i].x1 - w1/2
								tmp_xmax = gGCODES[j].x1 + w2/2
								if tmp_xmin > gGCODES[j].x1 - w2/2:
									tmp_xmin = gGCODES[j].x1 - w2/2
								if tmp_xmax < gGCODES[i].x1 + w1/2:
									tmp_xmax = gGCODES[i].x1 + w1/2
								w2 = tmp_xmax - tmp_xmin
								x2min = (tmp_xmax + tmp_xmin)/2
								gGCODES[j].gtype = 4
								gGCODES[j].mod2 = w2
								gGCODES[j].x2 = x2min
								#gGCODES[j].y2 = y2max
								gGCODES[j].x1 = x2min
								#gGCODES[j].y1 = y1min
								gGCODES[i].gtype = 0
								break
			j += 1
		i += 1
	return gGCODES
def check_duplication(gGCODES):
	#global gGCODES,TINY
	print("Check overlapping lines ...")
	i = 0

	while i< len(gGCODES)-1:
		if(gGCODES[i].gtype == 0):
			i += 1
			continue
		#m_x1_flag=0
		#m_y1_flag=0
		#xi1=gGCODES[i].x1
		#yi1=gGCODES[i].y1
		#xi2=gGCODES[i].x2
		#yi2=gGCODES[i].y2
		ti=gGCODES[i].gtype
		xi_min=gGCODES[i].x1
		xi_max=gGCODES[i].x2
		yi_min=gGCODES[i].y1
		yi_max=gGCODES[i].y2
		if(gGCODES[i].x1>gGCODES[i].x2):
			xi_min=gGCODES[i].x2
			xi_max=gGCODES[i].x1
			#m_x1_flag=1
		if(gGCODES[i].y1>gGCODES[i].y2):
			yi_min=gGCODES[i].y2
			yi_max=gGCODES[i].y1
			#m_y1_flag=1
		dxi=gGCODES[i].x2-gGCODES[i].x1
		dyi=gGCODES[i].y2-gGCODES[i].y1
		if(abs(dxi) >= TINY):
			ai=dyi/dxi
			bi=gGCODES[i].y1-ai*gGCODES[i].x1
		j = i + 1
		while j< len(gGCODES):
			if(gGCODES[j].gtype == 0):
				j += 1
				continue
			if(gGCODES[i].gtype == 0):
				#j += 1
				break
			#m_x2_flag=0
			#m_y2_flag=0
			xj1=gGCODES[j].x1
			yj1=gGCODES[j].y1
			xj2=gGCODES[j].x2
			yj2=gGCODES[j].y2
			tj=gGCODES[j].gtype
			xj_min=xj1
			xj_max=xj2
			yj_min=yj1
			yj_max=yj2
			if(xj1>xj2):
				xj_min=xj2
				xj_max=xj1
				#m_x2_flag=1
			if(yj1>yj2):
				yj_min=yj2
				yj_max=yj1
				#m_y2_flag=1
			
			if(ti == tj):	#same type
				if(ti == 3 or ti == 4):
					dxj=xj2-xj1
					dyj=yj2-yj1
					if(abs(dxi) >= TINY):
						if(abs(dxj) >= TINY):
							aj=dyj/dxj
							bj=yj1-aj*xj1
							if(abs(aj-ai) < TINY and abs(bj-bi) < TINY):
								#print("a=" + str(ai)
								if(xj_min>=xi_min):
									#print("a"
									if(xj_max<=xi_max):
										#print("aa"
										#overlap
										if(gGCODES[i].mod1 >= gGCODES[j].mod1):
											gGCODES[j].gtype=0
											j += 1
											continue
									elif(xi_max >= xj_min):	# xj_max > xi_max
										if(gGCODES[i].mod1 == gGCODES[j].mod1):
											#print("ab i=" +str(i) + ", j=" + str(j)
											gGCODES[j].gtype=0
											#gGCODES[i].x1 = xi_min
											#gGCODES[i].y1 = gGCODES[i].y1
											if(gGCODES[i].x1>gGCODES[i].x2):	#if xi_min = gGCODES[i].x2
												gGCODES[i].x1 = xi_min
												gGCODES[i].y1 = gGCODES[i].y2
											gGCODES[i].x2 = xj_max
											gGCODES[i].y2 = yj2
											xi_max = xj_max
											if(xj1>xj2):	#if xj_max = xj1
												gGCODES[i].y2 = yj1
											#j += 1
											#continue
								elif(xj_min<=xi_min):
									#print("b"
									if(xj_max>=xi_max):
										#print("ba"
										#overlap
										if(gGCODES[i].mod1 <= gGCODES[j].mod1):
											gGCODES[i].gtype=0
											break
									elif(xj_max >= xi_min):	# xj_max < xi_max
										if(gGCODES[i].mod1 == gGCODES[j].mod1):
											#print("bb i=" +str(i) + ", j=" + str(j)
											gGCODES[j].gtype=0
											#print("x1=" +str(gGCODES[i].x1) +", y1=" +str(gGCODES[i].y1) +", x2=" +str(gGCODES[i].x2) +", y2=" +str(gGCODES[i].y2)
											#gGCODES[i].x2 = xi_max
											#gGCODES[i].y2 = gGCODES[i].y2
											#if(m_x1_flag):	#if xi_max = gGCODES[i].x1
											if(gGCODES[i].x2 <= gGCODES[i].x1):
												#gGCODES[i].x2 = xi_max
												gGCODES[i].x2 = gGCODES[i].x1
												gGCODES[i].y2 = gGCODES[i].y1
											gGCODES[i].x1 = xj_min
											gGCODES[i].y1 = gGCODES[j].y1
											#xi_min = xj_min
											if(xj1>xj2):	#if xi_min = xj2
												gGCODES[i].y1 = gGCODES[j].y2
											xi_min = xj_min
											#print("x1=" +str(gGCODES[i].x1) +", y1=" +str(gGCODES[i].y1) +", x2=" +str(gGCODES[i].x2) +", y2=" +str(gGCODES[i].y2)
											#j += 1
											#continue
					else:	#dxi==0
						if(dxj==0 and gGCODES[i].x1==xj1):
							if(yj_min>=yi_min):
								if(yj_max<=yi_max):
									if(gGCODES[i].mod1 >= gGCODES[j].mod1):
										#overlap
										gGCODES[j].gtype=0
										#j += 1
										#continue
								elif(yi_max > yj_min):
									if(gGCODES[i].mod1 == gGCODES[j].mod1):
										gGCODES[j].gtype=0
										#gGCODES[i].x1 = gGCODES[i].x1
										gGCODES[i].y1 = yi_min
										if(gGCODES[i].y1>gGCODES[i].y2):	#yi_min = gGCODES[i].y2
											gGCODES[i].x1 = gGCODES[i].x2
											#gGCODES[i].y1 = yi_min
										gGCODES[i].x2 = gGCODES[j].x2
										gGCODES[i].y2 = yj_max
										if(yj1>yj2):
											gGCODES[i].x2 = gGCODES[j].x1
										#j += 1
										#continue
							elif(yj_min<=yi_min):
								if(yj_max>=yi_max):
									if(gGCODES[i].mod1 <= gGCODES[j].mod1):
										#overlap
										gGCODES[i].gtype=0
										break
								elif(yj_max > yi_min):
									if(gGCODES[i].mod1 == gGCODES[j].mod1):
										#gGCODES[i].x2 = GCODES[i].x2
										gGCODES[i].y2 = yi_max
										if(gGCODES[i].y1>gGCODES[i].y2):
											gGCODES[i].x2 = gGCODES[i].x1
											#gGCODES[i].y2 = yi_max
										gGCODES[i].x1 = GCODES[j].x1
										gGCODES[i].y1 = yj_min
										if(yj1>yj2):
											gGCODES[i].x1 = GCODES[j].x2
											#gGCODES[i].y1 = yj_min
			else:	#ti != tj
				if(ti == 2):
					if(tj == 3 or tj == 4):
						#print("rect ti"
						if(gGCODES[j].x1 == gGCODES[j].x2 and gGCODES[i].x1 == gGCODES[j].x1):	#Vertical
							#print("ti check x"
							if(gGCODES[i].mod1 == gGCODES[j].mod1):
								#print("ti check x mod1"
								#line = [gGCODES[i].x1,gGCODES[i].y1-gGCODES[i].mod2/2,gGCODES[i].x1,gGCODES[i].y1+gGCODES[i].mod2/2]
								x1=gGCODES[i].x1
								y1=gGCODES[i].y1-gGCODES[i].mod2/2
								x2=gGCODES[i].x1
								y2=gGCODES[i].y1+gGCODES[i].mod2/2
								xa=gGCODES[j].x1
								ya=gGCODES[j].y1
								xb=gGCODES[j].x2
								yb=gGCODES[j].y2
								ovflag = check_overlap(x1,y1,x2,y2,xa,ya,xb,yb,1)
								if(ovflag):	#Vertical 1-4	
									if(ovflag == 1):
										gGCODES[j].gtype=0
									if(ovflag == 3):
										gGCODES[i].gtype=0
									print("ti overlap =" + str(ovflag))
									#print(line_joint(x1,y1,x2,y2,xa,ya,xb,yb,ovflag)
									tx1,ty1,tx2,ty2=line_joint(x1,y1,x2,y2,xa,ya,xb,yb,ovflag)
									if(tj == 4):	#Rect
										print("Rect-Rect")
										gGCODES[j].gtype = 0
										gGCODES[i].gtype = 4
										gGCODES[i].x1 = tx1
										gGCODES[i].y1 = ty1
										gGCODES[i].x2 = tx2
										gGCODES[i].y2 = ty2
									elif(tj == 3):
										print("rect-cir")
										gGCODES[j].gtype = 0
										gGCODES[i].gtype = 5
										gGCODES[i].mod1 =gGCODES[j].mod1
										gGCODES[i].x1 = tx1
										gGCODES[i].y1 = ty1
										gGCODES[i].x2 = tx2
										gGCODES[i].y2 = ty2
										if(ovflag == 4):
											gGCODES[i].x1 = tx2
											gGCODES[i].y1 = ty2
											gGCODES[i].x2 = tx1
											gGCODES[i].y2 = ty1
						if(gGCODES[j].y1 == gGCODES[j].y2 and gGCODES[i].y1 == gGCODES[j].y1):	#Horizontal
							#print("ti check y"
							if(gGCODES[i].mod2 == gGCODES[j].mod1):
								#print("ti check y mod1"
								#line = [gGCODES[i].x1-gGCODES[i].mod1/2,gGCODES[i].y1,gGCODES[i].x1+gGCODES[i].mod1/2,gGCODES[i].y1]
								x1=gGCODES[i].x1-gGCODES[i].mod1/2
								y1=gGCODES[i].y1
								x2=gGCODES[i].x1+gGCODES[i].mod1/2
								y2=gGCODES[i].y1
								xa=gGCODES[j].x1
								ya=gGCODES[j].y1
								xb=gGCODES[j].x2
								yb=gGCODES[j].y2
								ovflag = check_overlap(x1,y1,x2,y2,xa,ya,xb,yb,0)
								if(ovflag):	#Horizontal 5-8
									if(ovflag == 5):
										gGCODES[j].gtype=0
									if(ovflag == 7):
										gGCODES[i].gtype=0	
									print("ti overlap =" + str(ovflag))
									tx1,ty1,tx2,ty2=line_joint(x1,y1,x2,y2,xa,ya,xb,yb,ovflag)
									
									if(tj == 4):	#Rect
										print("Rect-Rect")
										gGCODES[j].gtype = 0
										gGCODES[i].gtype = 4
										gGCODES[i].x1 = tx1
										gGCODES[i].y1 = ty1
										gGCODES[i].x2 = tx2
										gGCODES[i].y2 = ty2
									elif(tj == 3):
										print("rect-cir")
										gGCODES[j].gtype = 0
										gGCODES[i].gtype = 5
										gGCODES[i].mod1 =gGCODES[j].mod1
										gGCODES[i].x1 = tx1
										gGCODES[i].y1 = ty1
										gGCODES[i].x2 = tx2
										gGCODES[i].y2 = ty2
										if(ovflag == 8):
											gGCODES[i].x1 = tx2
											gGCODES[i].y1 = ty2
											gGCODES[i].x2 = tx1
											gGCODES[i].y2 = ty1
				if(tj == 2):
					if(ti == 3 or ti == 4):
						#print("rect tj"
						if(gGCODES[i].x1 == gGCODES[i].x2 and gGCODES[i].x1 == gGCODES[j].x1):	#Vertical
							#print("ti check x"
							if(gGCODES[i].mod1 == gGCODES[j].mod1):
								#print("ti check x mod1"
								#line = [gGCODES[i].x1,gGCODES[i].y1-gGCODES[i].mod2/2,gGCODES[i].x1,gGCODES[i].y1+gGCODES[i].mod2/2]
								x1=gGCODES[j].x1
								y1=gGCODES[j].y1-gGCODES[j].mod2/2
								x2=gGCODES[j].x1
								y2=gGCODES[j].y1+gGCODES[j].mod2/2
								xa=gGCODES[i].x1
								ya=gGCODES[i].y1
								xb=gGCODES[i].x2
								yb=gGCODES[i].y2
								ovflag = check_overlap(x1,y1,x2,y2,xa,ya,xb,yb,1)
								if(ovflag):	#Vertical 1-4	
									if(ovflag == 1):
										gGCODES[j].gtype=0
									if(ovflag == 3):
										gGCODES[i].gtype=0
									print("tj overlap =" + str(ovflag))
									#print(line_joint(x1,y1,x2,y2,xa,ya,xb,yb,ovflag)
									tx1,ty1,tx2,ty2=line_joint(x1,y1,x2,y2,xa,ya,xb,yb,ovflag)
									if(tj == 4):	#Rect
										print("Rect-Rect")
										gGCODES[j].gtype = 0
										gGCODES[i].gtype = 4
										gGCODES[i].x1 = tx1
										gGCODES[i].y1 = ty1
										gGCODES[i].x2 = tx2
										gGCODES[i].y2 = ty2
									elif(tj == 3):
										print("rect-cir")
										gGCODES[j].gtype = 0
										gGCODES[i].gtype = 5
										gGCODES[i].mod1 =gGCODES[j].mod1
										gGCODES[i].x1 = tx1
										gGCODES[i].y1 = ty1
										gGCODES[i].x2 = tx2
										gGCODES[i].y2 = ty2
										if(ovflag == 4):
											gGCODES[i].x1 = tx2
											gGCODES[i].y1 = ty2
											gGCODES[i].x2 = tx1
											gGCODES[i].y2 = ty1
						if(gGCODES[i].y1 == gGCODES[i].y2 and gGCODES[i].y1 == gGCODES[j].y1):	#Horizontal
							#print("ti check y"
							if(gGCODES[i].mod1 == gGCODES[j].mod2):

								x1=gGCODES[j].x1-gGCODES[j].mod1/2
								y1=gGCODES[j].y1
								x2=gGCODES[j].x1+gGCODES[j].mod1/2
								y2=gGCODES[j].y1
								xa=gGCODES[i].x1
								ya=gGCODES[i].y1
								xb=gGCODES[i].x2
								yb=gGCODES[i].y2
								ovflag = check_overlap(x1,y1,x2,y2,xa,ya,xb,yb,0)
								if(ovflag):	#Horizontal 5-8
									if(ovflag == 5):
										gGCODES[j].gtype=0
									if(ovflag == 7):
										gGCODES[i].gtype=0	
									print("tj overlap =" + str(ovflag))
									tx1,ty1,tx2,ty2=line_joint(x1,y1,x2,y2,xa,ya,xb,yb,ovflag)
									
									if(tj == 4):	#Rect
										print("Rect-Rect")
										gGCODES[j].gtype = 0
										gGCODES[i].gtype = 4
										gGCODES[i].x1 = tx1
										gGCODES[i].y1 = ty1
										gGCODES[i].x2 = tx2
										gGCODES[i].y2 = ty2
									elif(tj == 3):
										print("rect-cir")
										gGCODES[j].gtype = 0
										gGCODES[i].gtype = 5
										gGCODES[i].mod1 =gGCODES[j].mod1
										gGCODES[i].x1 = tx1
										gGCODES[i].y1 = ty1
										gGCODES[i].x2 = tx2
										gGCODES[i].y2 = ty2
										if(ovflag == 8):
											gGCODES[i].x1 = tx2
											gGCODES[i].y1 = ty2
											gGCODES[i].x2 = tx1
											gGCODES[i].y2 = ty1
			j += 1
		i +=1
	return gGCODES
def line_joint(x1,y1,x2,y2,xa,ya,xb,yb,ovflag):
	if(ovflag == 2):	#Vertical 2
		ox1=x1
		oy1=y1
		oy2=yb
		ox2=x2
		if(y1>y2):
			oy1=y2
		if(ya>yb):
			oy2=ya
	elif(ovflag == 4):	#Vertical 4
		ox1=x1
		ox2=x2
		oy1=ya
		oy2=y2
		if(y1>y2):
			oy2=y1
		if(ya>yb):
			oy1=yb
	elif(ovflag == 6):	#Horizontal
		ox1=x1
		ox2=xb
		oy1=y1
		oy2=y2
		if(x1>x2):
			ox1=x2
		if(xa>xb):
			ox2=xa
	elif(ovflag == 8):	#Horizontal
		ox1=xa
		ox2=x2
		oy1=y1
		oy2=y2
		if(x1>x2):
			ox2=x1
		if(xa>xb):
			ox1=xb
	else:
		return (0,0,0,0)
	return (ox1,oy1,ox2,oy2)

def check_overlap(x1,y1,x2,y2,xa,ya,xb,yb,sw):
	if(sw):	#Vertical
		if(y2 < y1):	#x2 < x1
			tmpy = y1
			y1 = y2
			y2 = tmpy
		if(yb < ya):	#xb < xa
			tmpy = ya
			ya = yb
			yb = tmpy
		if(y1 <= ya and y2 >= ya):
			if(y2 >= yb):
				# line 2 is in line1
				return 1
			elif(y2 < yb):
				return 2
		elif(y1 <= yb and y2 >= yb):
			return 4
		elif(y1 > ya and y2 < yb):
			return 3
		else:
			return 0
	else:	#Horizontal
		if(x2 < x1):	#x2 < x1
			tmpx = x1
			x1 = x2
			x2 = tmpx
		if(xb < xa):	#xb < xa
			tmpx = xa
			xa = xb
			xb = tmpx
		if(x1 <= xa and x2 >= xa):
			if(x2 >= xb):
				# line 2 is in line1
				return 5
			elif(x2 < xb):
				return 6
		elif(x1 <= xb and x2 >= xb):
			return 8
		elif(x1 > xa and x2 < xb):
			return 7
		else:
			return 0

def merge(gPOLYGONS, LINE, gLINES,gLINES2):
	#global gPOLYGONS, gLINES,PRE_IN_FLAG,gLINES2
	global PRE_IN_FLAG
	gLINES = []
	gLINES2 = []
	for poly1 in gPOLYGONS:
		PRE_IN_FLAG = -1
		out_points=[]
		if(poly1.delete):
			continue
		x_max=poly1.x_max
		x_min=poly1.x_min
		y_max=poly1.y_max
		y_min=poly1.y_min
		start_line_id=len(gLINES)
		#polygon2line(poly1.points,0)
		#global gLINES,gLINES2
		i = 0
		while i< len(poly1.points)-2:
			gLINES.append(LINE(poly1.points[i],poly1.points[i+1],poly1.points[i+2],poly1.points[i+3],0,0))
			i += 2
		end_line_id=len(gLINES)
		for poly2 in gPOLYGONS:
			if(poly2.delete):
				continue
			if(poly1 == poly2):
				continue
			if(x_max < poly2.x_min or x_min > poly2.x_max):
				continue
			if(y_max < poly2.y_min or y_min > poly2.y_max):
				continue

			i = 0
			while i< len(poly2.points)-2:
				gLINES2.append(LINE(poly2.points[i],poly2.points[i+1],poly2.points[i+2],poly2.points[i+3],0,0))
				i += 2
			end_line_id2=len(gLINES2)
			k = start_line_id
			while k < end_line_id:
				CrossAndIn(k,poly2.points,gLINES, LINE)
				k += 1
			end_line_id = len(gLINES)

	for poly3 in gPOLYGONS:
		#del all polygons
		poly3.delete = 1
	gPOLYGONS = line_merge(gPOLYGONS, gLINES)
	print("End merge polygons")
	return gPOLYGONS

def line_merge(gPOLYGONS, gLINES):
	for line1 in gLINES:
		if(line1.inside or line1.delete):
			continue
		tmp_points = [line1.x1, line1.y1, line1.x2, line1.y2]
		line1.delete = 1
		for line2 in gLINES:
			if(line2.inside or line2.delete):
				continue
			if(len(tmp_points) > 3):
				dist1 = calc_dist(tmp_points[0],tmp_points[1],line2.x2, line2.y2)
				dist2 = calc_dist(tmp_points[len(tmp_points)-2],tmp_points[len(tmp_points)-1], line2.x1, line2.y1)
				if(dist2 < TINY):
					tmp_points = tmp_points + [line2.x2, line2.y2]
					line2.delete = 1
				elif(dist1 < TINY):
					tmp_points = [line2.x1, line2.y1] + tmp_points
					line2.delete = 1
		gPOLYGONS.append(POLYGON(line1.x1, line1.x2, line1.y1, line1.y2,tmp_points,0))
	merge_polygons(gPOLYGONS)
	return gPOLYGONS

def merge_polygons(gPOLYGONS):
	#global gPOLYGONS
	print("      Start merge lines 2")
	for poly1 in gPOLYGONS:
		if(poly1.delete):
			continue
		tmp_points1 = poly1.points
		for poly2 in gPOLYGONS:
			if(poly2.delete or poly1==poly2):
				continue
			tmp_points2 = poly2.points
			dist1 = calc_dist(tmp_points1[0],tmp_points1[1],tmp_points2[len(tmp_points2)-2],tmp_points2[-1])
			dist2 = calc_dist(tmp_points1[len(tmp_points1)-2],tmp_points1[-1],tmp_points2[0],tmp_points2[1])
			if(dist2 < TINY):
				del tmp_points2[0:2]
				tmp_points1 = tmp_points1 + tmp_points2
				poly2.delete = 1
			elif(dist1 < TINY and dist2 > TINY):
				tmp_points2.pop()
				tmp_points2.pop()
				tmp_points1 = tmp_points2 + tmp_points1
				poly2.delete = 1
		poly1.points = tmp_points1
	#disp_test_points()

def IsLineOverlap(x1,y1,x2,y2,xa,ya,xb,yb):
	global TINY
	#print("check overlap"
	dx1 = x2-x1
	#dy1 = y2-y1
	dx2 = xb-xa
	#dy2 = yb-ya
	if(abs(dx1)  < TINY):	#Vertical
		dx2 = xb-xa
		if(abs(dx2) < TINY):	#Vertical
			if(abs(x1-xa) < TINY):
				if (ya - y1)*(ya - y2) <=0 or (yb - y1)*(yb - y2) <=0:
						return 1
	else:
		if(abs(dx2) > TINY):	#not Vertical
			dy1 = y2-y1
			dy2 = yb-ya
			a1 = (dy1)/(dx1)
			#b1 = y1-a1*x1
			a2 = (dy2)/(dx2)
			#b2 = ya-a2*xa
			if(abs(a1-a2) < TINY):
				b1 = y1-a1*x1
				b2 = ya-a2*xa
				#print("same angle " + str(a1 )+ ", b1=" + str(b1)+ ", b2=" + str(b2) + ", b2-b1=" + str(abs(b2-b1)) +", y1=" +str(y1) + ", ya=" + str(ya)
				if(abs(b2-b1) < TINY):	#Horizontal
					#print("same b " + str(b1)
					if (xa - x1)*(xa - x2) <= 0 or (xb - x1)*(xb - x2):
						return 1
	return 0

def GetLineDist(line1,line2):
	global TINY
	dx = line1.x2-line1.x1
	dy = line1.y2-line1.y1
	a = dx * dx + dy * dy
	if(a < TINY):
		dist1 = calc_dist(line1.x1,line1.y1,line2.x1,line2.y1)
		dist2 = calc_dist(line1.x1,line1.y1,line2.x2,line2.y2)
	else:
		b1 = dx * (line1.x1-line2.x1) + dy * (line1.y1-line2.y1)
		b2 = dx * (line1.x1-line2.x2) + dy * (line1.y1-line2.y2)
		t1 =  - (b1 / a)
		t2 =  - (b2 / a)
		if(t1 < 0.0):
			t1 = 0.0
		if(t1 > 1.0):
			t1 = 1.0
		if(t2 < 0.0):
			t2 = 0.0
		if(t2 > 1.0):
			t2 = 1.0
		x1 = t1 * dx + line1.x1
		y1 = t1 * dy + line1.y1
		x2 = t2 * dx + line1.x2
		y2 = t2 * dy + line1.y2
		dist1 = calc_dist(x1,y1,line2.x1,line2.y1)
		dist2 = calc_dist(x2,y2,line2.x2,line2.y2)

	if(abs(dist1-dist2) < TINY):
		return dist1
	else:
		if(dist1 >= dist2):
			return dist1
		else:
			return dist2
def CrossAndIn(line_id,spoints, gLINES, LINE):
	#global gLINES, gCCOUNT1, gCCOUNT2,TEST_POINTS1,TEST_POINTS2
	global gCCOUNT1, gCCOUNT2,TEST_POINTS1,TEST_POINTS2
	#check in or out
	#print(line_id
	if(gLINES[line_id].inside):
		return 0
	xa = gLINES[line_id].x1
	ya = gLINES[line_id].y1
	xb = gLINES[line_id].x2
	yb = gLINES[line_id].y2
	cross_count1 = 0
	cross_count2 = 0
	cross_points = []
	cross_nums = []
	cross_num = 0
	cross_flag = 0
	tmp_flag = 0
	return_flag = 0
	ovflag = 0
	si = 0
	while si< len(spoints)-2:
		xp1=spoints[si]
		yp1=spoints[si+1]
		xp2=spoints[si+2]
		yp2=spoints[si+3]
		if(IsLineOverlap(xa,ya,xb,yb,xp1,yp1,xp2,yp2)):
				ovflag = 1
		(cross_flag,cross_x,cross_y)=find_cross_point(xa,ya,xb,yb,xp1,yp1,xp2,yp2)
		cross_num+=cross_flag
		if(cross_flag):
			#print("cross"
			cross_points.extend([cross_x,cross_y])
			cross_nums.append(si)

		if ((ya <= yp1) and (ya > yp2)) or ((ya > yp1) and (ya <= yp2)):
			#Cross?
			if ((xa <= xp1) and (xa <= xp2)) or ((xa > xp1) and (xa > xp2)):
				if(xa <= xp1):
					#Cross
					if(ya <= yp1):#
						cross_count1 -=1
					else:
						cross_count1 += 1
			elif(yp2 != yp1):#
				if(xa <= (xp1+(xp2-xp1)*(ya-yp1)/(yp2-yp1))):#
					if(ya <= yp1):#
						cross_count1 -= 1
					else:
						cross_count1 += 1



		if ((yb <= yp1) and (yb > yp2)) or ((yb > yp1) and (yb <= yp2)):
			#Cross?
			if ((xb <= xp1) and (xb <= xp2)) or ((xb > xp1) and (xb > xp2)):
				if(xb <= xp1):
					#Cross
					if(yb <= yp1):#
						cross_count2 -= 1
					else:
						cross_count2 += 1
			elif(yp2 != yp1):#
				if(xb <= (xp1+(xp2-xp1)*(yb-yp1)/(yp2-yp1))):#
					if(yb <= yp1):#
						cross_count2 -= 1
					else:
						cross_count2 += 1

		si += 2
	#end while
	if(line_id == 1):
		TEST_POINTS1.append([xa,ya])
		TEST_POINTS1.append([xp1,yp1])
		TEST_POINTS2.append([xb,yb])
		TEST_POINTS2.append([xp2,yp2])
	in_flag1 = 0
	if(cross_count1):#
		in_flag1 = 1
	in_flag2 = 0
	if(cross_count2):#
		in_flag2 = 1
	PRE_IN_FLAG = in_flag2


	if(cross_num>1):
		cross_points = sort_points_by_dist(xa,ya,cross_points)
		#print(calc_dist(gLINES[line_id].x1,gLINES[line_id].y1,cross_points[0],cross_points[1])
		if(calc_dist(gLINES[line_id].x1,gLINES[line_id].y1,cross_points[0],cross_points[1])<=0.0):
			#print("the cross point is same as p1 in_flag1=" + str(in_flag1) + "in_flag2=" + str(in_flag2)
			if(in_flag1 != in_flag2):
				gLINES[line_id].inside = 1
			else:
				gLINES[line_id].inside = in_flag1
			tmp_flag = in_flag1
			tmp_x=gLINES[line_id].x1
			tmp_y=gLINES[line_id].y1
		else:
			gLINES[line_id].x2 = cross_points[0]
			gLINES[line_id].y2 = cross_points[1]
			gLINES[line_id].inside = in_flag1
			tmp_x=cross_points[0]
			tmp_y=cross_points[1]
		tmp_flag=1
		if(in_flag1):
			tmp_flag=0
		i = 2
		while i < len(cross_points)-2:
			gLINES.append(LINE(tmp_x,tmp_y,cross_points[i],cross_points[i+1],tmp_flag,0))
			tmp_flag = 1
			if(in_flag1):
				tmp_flag = 0
			tmp_x=cross_points[i]
			tmp_y=cross_points[i+1]
			i += 2
		#end while
		if(calc_dist(cross_points[len(cross_points)-2],cross_points[len(cross_points)-1],xb,yb)>0.0):
			gLINES.append(LINE(cross_points[len(cross_points)-2],cross_points[len(cross_points)-1],xb,yb,in_flag2,0))
	
	elif(cross_num==1):
		if(in_flag1 == in_flag2):
			#in in
			gLINES[line_id].inside=in_flag1
			#print("in-in or Out-OUT:flag="+str(in_flag1)+ ", id=" +str(line_id)
		else:
			#in out
			if(ovflag <=0):
				gLINES[line_id].x2 = cross_points[0]
				gLINES[line_id].y2 = cross_points[1]
				gLINES[line_id].inside = in_flag1
				gLINES.append(LINE(cross_points[0],cross_points[1],xb,yb,in_flag2,0))
			else:
				#overlap
				gLINES[line_id].x2 = cross_points[0]
				gLINES[line_id].y2 = cross_points[1]
				gLINES[line_id].inside = 0
				gLINES.append(LINE(cross_points[0],cross_points[1],xb,yb,0,0))
	else:
		gLINES[line_id].inside = in_flag1

	if(cross_num > 0) or (in_flag1 or in_flag2):
		return 1

	return 0
def sort_points_by_dist(x,y,points):
	return_points=[]
	return_pos=[]
	pre_dist=calc_dist(x,y,points[0],points[1])
	i = 0
	while i < len(points):
		if(pre_dist > calc_dist(x,y,points[i],points[i+1])):
			tmp_x = points[i]
			tmp_y = points[i+1]
			points[i] = points[i-2]
			points[i+1] = points[i-1]
			points[i-2] = tmp_x
			points[i-1] = tmp_y
		i += 2
	return points
def calc_dist(x1,y1,x2,y2):
	return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def find_cross_point(x1,y1,x2,y2,xa,ya,xb,yb):
	#flag = 0

	if(x1 ==  x2):
		if(xa == xb):
			return (0,0,0)
		else:
			aa=(yb-ya)/(xb-xa)
			ba=ya-aa*xa
			x=x1
			y=aa*x+ba
	else:
		a1=(y2-y1)/(x2-x1)
		b1=y1-a1*x1
		if(xa == xb):
			x=xa
			y=a1*x+b1
		else:
			aa=(yb-ya)/(xb-xa)
			ba=ya-aa*xa
			if(a1 == aa):
				return (0,0,0)
			else:
				x=(ba-b1)/(a1-aa)
				y=a1*x+b1

	x_max = x2
	x_min = x1
	if(x1 > x2):
		x_max = x1
		x_min = x2
	if(x_min-TINY <= x and x_max+TINY >= x):
		xa_max = xb
		xa_min = xa
		if(xa > xb):
			xa_max=xa
			xa_min=xb
		if(xa_min-TINY <= x and xa_max+TINY>=x):
			y_max = y2
			y_min = y1
			if(y1 > y2):
				y_max=y1
				y_min=y2
			if(y_min-TINY <= y and y_max+TINY >= y):
				ya_max = yb
				ya_min = ya
				if(ya >  yb):
					ya_max = ya
					ya_min = yb
				if(ya_min-TINY <= y and ya_max+TINY >= y):
					return (1,x,y)
	return (0,0,0)

