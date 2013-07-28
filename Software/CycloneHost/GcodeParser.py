#!/usr/bin/python

# AUTHOR:
#   Carlosgs (http://carlosgs.es)
# LICENSE:
#   Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)
#
# DISCLAIMER:
#   This software is provided "as is", and you use the software at your own risk. Under no
#   circumstances shall Carlosgs be liable for direct, indirect, special, incidental, or
#   consequential damages resulting from the use, misuse, or inability to use this software,
#   even if Carlosgs has been advised of the possibility of such damages.
#
# CREDIT:
#   Based on Etch_Z_adjust.1.8.py from http://www.cnczone.com/forums/pcb_milling/82628-cheap_simple_height-probing.html (multiple authors)

# Begin modules
import os.path
# End modules

def parseGcodeRaw(filePath, etch_definition = 0, close_shapes = 0): # Gcode parser from Etch_Z_adjust.1.8.py (modified by Carlosgs to output toolpaths)
	
	gcode_maxXY = (0,0)
	gcode_minXY = (0,0)
	travel_moves = []
	etch_moves = []
	
	if os.path.isfile(filePath) == False :
		return etch_moves, travel_moves, gcode_minXY, gcode_maxXY
	
	gcode = open(filePath, "r")
	
	# Height to consider etching
	# etch_definition = 0
	
	# Check for max and min values in the gcode file
	is_first_X = True
	is_first_Y = True
	is_first_Z = True
	
	G_dest = 0
	X_dest = 0
	Y_dest = 0
	Z_dest = 10
	F_dest = 10
	
	path = []
	
	def get_num(line,char_ptr,num_chars):
		char_ptr=char_ptr+1
		numstr = ''
		good = '-.0123456789'
		while char_ptr < num_chars:
			digit = line[char_ptr]
			if good.find(digit) != -1:
				numstr = numstr + digit
				char_ptr = char_ptr + 1
			else: break
		return numstr

	def test_X(X_min, X_max):
		if X_dest < X_min : X_min = X_dest
		elif X_dest > X_max : X_max = X_dest
		return X_min, X_max

	def test_Y(Y_min, Y_max):
		if Y_dest < Y_min : Y_min = Y_dest
		elif Y_dest > Y_max : Y_max = Y_dest
		return Y_min, Y_max
	
	def isSame(list1, list2): # Compare two lists, returns True if they have same values
		i = 0
		for val1 in list1:
			val2 = list2[i]
			if val1 != val2:
				return False
			i = i + 1
		return True
	
	etchMove = False
	
	currentLine = 0.0
	lines = gcode.readlines()
	totalLines = len(lines)
	for line in lines:# check each line
		currentLine = currentLine + 1
		#print("({0:.1f}%)".format((currentLine / totalLines)*100), "Reading:", line[:-1])
		
		X_start = X_dest
		Y_start = Y_dest
		Z_start = Z_dest
		
		# check each character
		char_ptr = 0
		num_chars= len(line)
		while char_ptr < num_chars:
			char = line[char_ptr]
			if '(;'.find(char) != -1:
				break
			elif char == 'G' :
				G_dest = int(get_num(line,char_ptr,num_chars))
			elif char == 'X' :
				X_dest = float(get_num(line,char_ptr,num_chars))
			elif char == 'Y' :
				Y_dest = float(get_num(line,char_ptr,num_chars))
			elif char == 'Z' :
				Z_dest = float(get_num(line,char_ptr,num_chars))
			elif char == 'F' :
				F_dest = float(get_num(line,char_ptr,num_chars))
			char_ptr = char_ptr + 1
		
		if G_dest == 0 or G_dest == 1 :
			if Z_dest < etch_definition: # if the line is an etch move, then replace the line with an etch call
				#line = 'O200 call [%.4f] [%.4f] [%.4f] [%.4f]\n' % (X_start, Y_start, X_dest, Y_dest)
				if etchMove == False :
					travel_moves.append(path)
					path = []
					etchMove = True # Set etch mode
					path.append([X_dest,Y_dest,Z_dest,F_dest])
				
				destPoint = [X_dest,Y_dest,Z_dest,F_dest]
				if len(path) == 0 or isSame(destPoint,path[-1]) == False: # Don't add same point twice
					path.append(destPoint)
				
				# and now check for max and min X and Y values
				if is_first_X == True :
					X_min = X_dest
					X_max = X_dest
					is_first_X = False
				else : (X_min, X_max) = test_X(X_min, X_max)
				
				if is_first_Y == True :
					Y_min = Y_dest
					Y_max = Y_dest
					is_first_Y = False
				else : (Y_min, Y_max) = test_Y(Y_min, Y_max)
			else :
				if etchMove == True :
					if close_shapes : # Return to the start point
						path.append(path[0])
					etch_moves.append(path)
					path = []
					etchMove = False # Set travel mode
					path.append([X_dest,Y_dest,Z_dest,F_dest])
				
				destPoint = [X_dest,Y_dest,Z_dest,F_dest]
				if len(path) == 0 or isSame(destPoint,path[-1]) == False: # Don't add same point twice
					path.append(destPoint)
				
		#file_out.append(line)
	
	if is_first_X == False :
		# then there were etch moves so get to work!
		
		gcode_maxXY = [X_max, Y_max]
		gcode_minXY = [X_min, Y_min]
		
		print("Gcode XY min: " + str(gcode_minXY))
		print("Gcode XY max: " + str(gcode_maxXY))
	
	else :
		print("No etch moves found!")
		return etch_moves, travel_moves, [0,0], [0,0]
	gcode.close()
	return etch_moves, travel_moves, gcode_minXY, gcode_maxXY

def optimize(etch_moves_in, origin=[0,0], travel_height = 5): # Optimizes the toolpath using closest neighbour (author: Carlosgs)
	
	etch_moves = []
	travel_moves = []
	
	if len(etch_moves_in) == 0 :
		return etch_moves, travel_moves
	
	travel_moves = []
	
	toolPosition = [origin[0], origin[1], travel_height, 10]
	
	minDistance = 1e9
	
	while len(etch_moves_in) > 0 : # While there are remaining moves
		closest = 1e9
		distance = 1e9
		closestMove_i = 0
		i = 0
		reverse = 0
		for path in etch_moves_in : # Find the one that begins more close to the position of our tool
			firstPoint = path[0]
			distance = (toolPosition[0]-firstPoint[0])**2 + (toolPosition[1]-firstPoint[1])**2 # We only check XY
			if distance < closest :
				closest = distance
				closestMove_i = i
			elif path[-1][2] == path[0][2]: # We also consider that paths can be made in reverse # Only in case there is no Z lift
				firstPoint = path[-1] # We check the last point first
				distance = (toolPosition[0]-firstPoint[0])**2 + (toolPosition[1]-firstPoint[1])**2 # We only check XY
				if distance < closest :
					closest = distance
					closestMove_i = i
					reverse = 1 # Flag set to reverse the path
					#print("Using a reverse path did optimize!")
			i = i + 1
		
		path = etch_moves_in[closestMove_i] # Select the closest that has been found
		if reverse :
			path = path[::-1] # If the closest one was from the end, we reverse the path
			#print("Reverse!")
		
		firstPoint = path[0]
		
		if distance > 0.1**2 : # This will join etching moves closer than 0.1 mm (this avoids repetitive drill lifting)
			travel_moves.append([toolPosition, [firstPoint[0], firstPoint[1], travel_height, firstPoint[3]] ]) # Travel to the initial point of the etching
		else :
			travel_moves.append([toolPosition, firstPoint]) # Travel to the initial point of the etching (without lifting)
			print("Joining etching paths!") # TODO: This needs to join also the paths in etch_moves! otherwise it makes no difference!
		
		if distance < minDistance :
			minDistance = distance
		
		etch_moves.append(path) # Do the etching
		etch_moves_in.pop(closestMove_i) # Remove the move from the list, it has been done!
		
		toolPosition = path[-1] # Set our endpoint as the initial one for the next move
	
	print("Minimum XY travel distance: " + str(minDistance**0.5) )
	
	travel_moves.append([toolPosition, [origin[0], origin[1], travel_height, 10]]) # Return to the origin
	return etch_moves, travel_moves

