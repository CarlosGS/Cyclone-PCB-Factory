#!/usr/bin/python

###### Misc functions for Cyclone Host ######

def floats(val): # This is used to convert a float value to a string (avoiding exponent notation)
	return "%.3f" % float(val) # Compatible with Python 2.6
	#return '{:.3f}'.format(float(val)) # It truncates the decimals that aren't used

def isOdd(number):
	if number % 2 == 0:
		return 0 # Even number
	else:
		return 1 # Odd number

