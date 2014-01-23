"""
This is the main pyRepRap module for controlling a serial
SNAP RepRap machine.

Import this module and use the internally created objects
reprap.cartesian and reprap.extruder to control the machine.



Example:

# Import the reprap  modules
import reprap, time

# Initialise serial port, here the first port (0) is used.
reprap.openSerial( 0, 19200, 1 )

# These devices are present in network, will automatically scan in the future.
reprap.cartesian.x.active = True
reprap.cartesian.y.active = True
reprap.cartesian.z.active = True
reprap.extruder.active = True

# Set axies to notify arrivals
reprap.cartesian.x.setNotify()
reprap.cartesian.y.setNotify()
reprap.cartesian.z.setNotify()

# Set stepper speed to 220 (out of 255)
reprap.cartesian.setSpeed(220)
# Set power to 83%
reprap.cartesian.setPower(83)

# The module is now ready to recieve commands #

# Send all axies to home position. Wait until arrival.
reprap.cartesian.homeReset()

# When using seek with no waitArrival = True/False argument, it defaults to true
# Seek to X1000, Y1000
reprap.cartesian.seek( (1000, 1000, None) )

# Pause
time.sleep(2)

# Seek to X500, Y1000
reprap.cartesian.seek( (500, 1000, None) )

time.sleep(2)

# Seek to X1000, Y500
reprap.cartesian.seek( (1000, 500, None) )

time.sleep(2)

# Seek to X100, Y100
reprap.cartesian.seek( (100, 100, None) )

# Send all axies to home position. Wait until arrival.
reprap.cartesian.homeReset()

# Shut off power to all motors.
reprap.cartesian.free()


"""

# Python module properties
__author__ = "Stefan Blanke (greenarrow) (greenarrow@users.sourceforge.net)"
__credits__ = ""
__license__ = "GPL 3.0"
__version__ = "2.0"
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

# Import modules
import snap, time, serial, math, exceptions

# Enable / Diable debug
printDebug = False
#printDebug = True

# SNAP Control Commands - Taken from PIC code #
# extruder commands #
CMD_VERSION       =  0
CMD_FORWARD       =  1
CMD_REVERSE       =  2
CMD_SETPOS        =  3
CMD_GETPOS        =  4
CMD_SEEK          =  5
CMD_FREE          =  6
CMD_NOTIFY        =  7
CMD_ISEMPTY       =  8
CMD_SETHEAT       =  9
CMD_GETTEMP       = 10
CMD_SETCOOLER     = 11
CMD_PWMPERIOD     = 50
CMD_PRESCALER     = 51
CMD_SETVREF       = 52
CMD__setTempScaler = 53
CMD_GETDEBUGINFO  = 54
CMD_GETTEMPINFO   = 55
# stepper commands #
CMD_VERSION			=   0
CMD_FORWARD			=   1
CMD_REVERSE			=   2
CMD_SETPOS			=   3
CMD_GETPOS			=   4
CMD_SEEK			=   5
CMD_FREE			=   6
CMD_NOTIFY			=   7
CMD_SYNC			=   8
CMD_CALIBRATE		=   9
CMD_GETRANGE		=  10
CMD_DDA				=  11
CMD_FORWARD1		=  12
CMD_BACKWARD1		=  13
CMD_SETPOWER		=  14
CMD_GETSENSOR		=  15
CMD_HOMERESET		=  16
CMD_GETMODULETYPE	= 255
# DDA sync modes #
SYNC_NONE	= 0		# no sync (default)
SYNC_SEEK	= 1		# synchronised seeking
SYNC_INC	= 2		# inc motor on each pulse
SYNC_DEC	= 3		# dec motor on each pulse

# Motor direction modes
MOTOR_FORWARD = 1
MOTOR_BACKWARD = 2

# Unit types
UNITS_MM = 1
UNITS_STEPS = 2
UNITS_INCHES = 3	# Not implemented TODO

# Local address of host PC. This will always be 0.
snap.localAddress = 0


class _RepRapError(exceptions.Exception):
	"""RepRap Exception"""
	def __init__(self, msg):
		self.msg = msg
		return
	
	def __str__(self):
		return "A RepRap error has occured! " + str(self.msg)


def openSerial( port = 0, rate = 19200, timeout = 1 ):
	"""Open serial port for SNAP RepRap communications"""
	snap.openSerial(port = port, rate = rate, tout = timeout)


def closeSerial():
	"""Close serial port for SNAP RepRap communications"""
	snap.closeSerial()


def _bytes2int(LSB, MSB):
	"""Convert two 8 bit bytes to one integer"""
	return int( (0x100 * int(MSB) ) | int(LSB) )


def _int2bytes(val):
	"""Convert integer to two 8 bit bytes"""
	MSB = int( ( int(val) & 0xFF00) / 0x100 )
	LSB = int( int(val) & 0xFF )
	return LSB, MSB


def scanNetwork():
	"""Scan reprap network for devices (incomplete) - this will be used by autoconfig functions when complete"""
	devices = []
	for remoteAddress in range(2, 6):									# For every address in range. full range will be 255
		print "Trying address " + str(remoteAddress)
		p = snap.Packet( remoteAddress, snap.localAddress, 0, 1, [CMD_GETMODULETYPE] )	# Create snap packet requesting module type
		#p = snap.Packet( remoteAddress, snap.localAddress, 0, 1, [CMD_VERSION] )
		p.send()											# Send snap packet, if sent ok then await reply
		rep = p.getReply()
		print "dev", remoteAddress
		#devices.append( { 'address':remoteAddress, 'type':rep.dataBytes[1], 'subType':rep.dataBytes[2] } )	# If device replies then add to device list.
		time.sleep(0.5)
	for d in devices:
		#now get versions
		print "device", d


def testComms():
	"""Test that serial communications are working properly with simple loopback (incomplete)"""
	p = snap.Packet( snap.localAddress, snap.localAddress, 0, 1, [255, 0] ) 	#start sync
	p.send()
	notif = _getNotification( serialPort )
	if notif.dataBytes[0] == 255:
		return True
	return False


def _getNotification(serialPort):
	"""Return notification packet"""
	return snap.getPacket()


class extruderClass:
	"""Used to control a RepRap thermoplast extruder.
	An instance is automatically created in the reprap module, so for
	basic use just use reprap.extruder rather than defining a new one
	"""
	def __init__(self):
		"""Create an extruder instance. An instance is automatically create at reprap.extruder."""
		self.address = 8
		self.active = False
		self.requestedTemperature = 0
		self.vRefFactor = 7			# Default in java (middle)
		self.hb = 20				# Variable Preference
		self.hm = 1.66667			# Variable Preference
		self.absZero = 273.15		# Static, K
		self.rz = 29000				# Variable Preference
		self.beta = 3480			# Variable Preference
		self.vdd = 5.0				# Static, volts
		self.cap = 0.0000001		# Variable Preference
	
	def _getModuleType(self):
		"""Returns module type as an integer.
		note: do pics not support this yet? I can't see it in code and get no reply from pic"""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_GETMODULETYPE] )	# Create SNAP packet requesting module type
		p.send()
		rep = p.getReply()
		rep.checkReply(2, CMD_GETMODULETYPE)
		data = rep.dataBytes
		return data[1]
	
	def getVersion(self):
		"""Returns (major, minor) firmware version as a two integer tuple."""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_VERSION] )
		p.send()
		rep = p.getReply()
		rep.checkReply(3, CMD_VERSION)
		data = rep.dataBytes
		return data[1], data[2]
	
	def setMotor(self, direction, speed):
		"""Set motor direction (reprap.MOTOR_BACKWARD or reprap.MOTOR_FORWARD) and speed (0-255)"""
		if int(direction) > 0 and int(direction) < 3 and int(speed) >= 0 and int(speed <= 0xFF):
			p = snap.Packet( self.address, snap.localAddress, 0, 1, [int(direction), int(speed)] ) ##no command being sent, whats going on?
			p.send()
		else:
			raise RepRapError("Invalid direction or speed value")
	
	def _calculateResistance(self, picTemp, calibrationPicTemp):
		"""Calculate resistance from pic timer value"""
		# TODO remove hard coded constants
		# TODO should use calibration value instead of first principles
		
		scale = 1 << (self.tempScaler+1)
		# calculate clock in hertz
		clock = 4000000.0 / (4.0 * scale)
		
		# calculate vRef in volts
		vRef = 0.25 * self.vdd + self.vdd * self.vRefFactor / 32.0
		
		# calculate time in seconds
		T = picTemp / clock
		# calc resistance in ohms
		resistance = -T / (math.log(1 - vRef / self.vdd) * self.cap)
		return resistance

	def _calculateTemperature(self, resistance):
		"""Calculate temerature from resistance"""
		return (1.0 / (1.0 / self.absZero + math.log(resistance/self.rz) / self.beta)) - self.absZero;
	
	def _rerangeTemperature(self, rawHeat):
		"""Adjust temperature range"""
		notDone = False
		if (rawHeat == 255 and self.vRefFactor > 0):
			self.vRefFactor -= 1
			# extruder re-ranging temperature (faster)
			self._setTempRange()
		elif (rawHeat < 64 and self.vRefFactor < 15):
			self.vRefFactor += 1
			# extruder re-ranging temperature (slower)
			self._setTempRange()
		else:
			notDone = True
		return notDone
	
	def _setTempRange(self):
		"""Set tempertaure range"""
		# We will send the vRefFactor to the PIC.  At the same
		# time we will send a suitable temperature scale as well.
		# To maximize the range, when vRefFactor is high (15) then
		# the scale is minimum (0).
		
		#extruder vRefFactor set to " + vRefFactor
		self.tempScaler = 7 - (self.vRefFactor >> 1);
		self._setVoltageReference(self.vRefFactor)
		self._setTempScaler(self.tempScaler)
		if (self.requestedTemperature != 0):
			self.setTemp(self.requestedTemperature, False)
			# should we be re-calling this function to make sure temp request is updated (rather than just calling it once. are we?)
	
	def _getRawTemp(self):
		"""Get raw temperature pic timer value"""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_GETTEMP] )
		p.send()
		rep = p.getReply()
		rep.checkReply(3, CMD_GETTEMP)
		data = rep.dataBytes
		#rawTemp, calibration
		return data[1], data[2]
	
	def getTemp(self):
		"""Returns current extruder temperature in degrees Celsius as an integer"""
		self._autoTempRange()
		rawHeat, calibration = self._getRawTemp()
		while rawHeat == 255 or rawHeat == 0:
			time.sleep(0.1)
			self._autoTempRange()
		res = self._calculateResistance( rawHeat, calibration )
		temp = self._calculateTemperature(res)
		#print rawHeat, res, temp
		return round(temp, 1)	#there is no point returning more points than this
		
	def setTemp(self, temperature):
		"""Set the extruder target temperature (degrees Celsius)"""
		self.requestedTemperature = temperature
		#if(math.abs(self.requestedTemperature - extrusionTemp) > 5):
		#	print " extruder temperature set to " + self.requestedTemperature + "C, which is not the standard temperature (" + extrusionTemp + "C).")
		# Aim for 10% above our target to ensure we reach it.  It doesn't matter
		# if we go over because the power will be adjusted when we get there.  At
		# the same time, if we aim too high, we'll overshoot a bit before we
		# can react.
		
		# Tighter temp constraints under test 10% -> 3% (10-1-8)
		temperature0 = temperature * 1.03
		
		# A safety cutoff will be set at 20% above requested setting
		# Tighter temp constraints added by eD 20% -> 6% (10-1-8)
		temperatureSafety = temperature * 1.06
		
		# Calculate power output from hm, hb.  In general, the temperature
		# we achieve is power * hm + hb.  So to achieve a given temperature
		# we need a power of (temperature - hb) / hm
		
		# If we reach our temperature, rather than switching completely off
		# go to a reduced power level.
		power0 = int( round(((0.9 * temperature0) - self.hb) / self.hm) )
		if power0 < 0: power0 = 0
		if power0 > 255: power0 = 255

		# Otherwise, this is the normal power level we will maintain
		power1 = int( round((temperature0 - self.hb) / self.hm) )
		if power1 < 0: power1 = 0
		if power1 > 255: power1 = 255

		# Now convert temperatures to equivalent raw PIC temperature resistance value
		# Here we use the original specified temperature, not the slight overshoot
		resistance0 = self._calculateResistanceForTemperature(temperature)
		resistanceSafety = self._calculateResistanceForTemperature(temperatureSafety)

		# Determine equivalent raw value
		t0 = self._calculatePicTempForResistance(resistance0)
		if t0 < 0: t0 = 0
		if t0 > 255: t0 = 255
		t1 = self._calculatePicTempForResistance(resistanceSafety)
		if t1 < 0: t1 = 0
		if t1 > 255: t1 = 255
		
		if (temperature == 0):
			self._setHeat( 0, 0, 0, 0 )
		else:
			self._setHeat( power0, power1, t0, t1 )

	def _calculateResistanceForTemperature(self, temperature):
		return self.rz * math.exp(self.beta * (1/(temperature + self.absZero) - 1/self.absZero))

	def _calculatePicTempForResistance(self, resistance):
		scale = 1 << (self.tempScaler+1)
		clock = 4000000.0 / (4.0 * scale)	#// hertz		
		vRef = 0.25 * self.vdd + self.vdd * self.vRefFactor / 32.0	#// volts
		T = -resistance * (math.log(1 - vRef / self.vdd) * self.cap)
		picTemp = T * clock
		return int( round(picTemp) )
	
	def _autoTempRange(self):
		"""Automatically find the suitable temperature range"""
		rawHeat, calibration = self._getRawTemp()
		unChanged = self._rerangeTemperature(rawHeat)
		while not unChanged:
			rawHeat, calibration = self._getRawTemp()
			unChanged = self._rerangeTemperature(rawHeat)
			time.sleep(0.1)
	
	def _setVoltageReference(self, val):
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_SETVREF, int(val)] )
		p.send()
	
	def _setTempScaler(self, val):
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD__setTempScaler, int(val)] )
		p.send()
	
	def _setHeat(self, lowHeat, highHeat, tempTarget, tempMax):
		print "Setting heater with params, ", "lowHeat", lowHeat, "highHeat", highHeat, "tempTarget", tempTarget, "tempMax", tempMax
		tempTargetMSB, tempTargetLSB = _int2bytes( tempTarget )
		tempMaxMSB ,tempMaxLSB = _int2bytes( tempMax )
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_SETHEAT, int(lowHeat), int(highHeat), tempTargetMSB, tempTargetLSB, tempMaxMSB, tempMaxLSB] )	# assumes MSB first (don't know this!)
		p.send()
	
	def setCooler(self, speed):
		"""Set the speed (0-255) of the cooling fan"""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_SETCOOLER, int(speed)] )
		p.send()
	
	def freeMotor(self):
		"""Power off the extruder motor"""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_FREE] )
		p.send()

extruder = extruderClass()



class axisClass:
	"""Used to control a RepRap axis.
	X, Y & Z instances are automatically created in the reprap module,
	so for basic use just use reprap.cartesian.x, reprap.cartesian.y
	& reprap.cartesian.z  rather than defining new ones.
	
	Most of the time the functions in reprap.cartesian will be 
	sufficient. E.g. to move just one axis you can use:
	reprap.cartesian.seek((200, None, None))
	"""
	def __init__(self, address):
		"""Create an axis instance with address (1-255). Instances for the three axies are automatically created and can be accessed via reprap.cartesian.x, reprap.cartesian.y & reprap.cartesian.z
		These instances are pre-configured with the correct addresses and alow the use of whole machine reprap.cartesian commands."""
		self.address = address
		# when scanning network, set this, then in each func below, check alive before doing anything TODO
		self.active = False
		self.limit = 0
		self.speed = None
		self.stepsPerMM = None
		self.units = None
	
	def forward1(self):
		"""Move axis one step forward
		Return the completed state as a bool."""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_FORWARD1] ) 
		p.send()
	
	def backward1(self):
		"""Move axis one step backward"""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_BACKWARD1] ) 
		p.send()
	
	def forward(self, speed = None):
		"""Spin axis forward at given speed (0-255)
		If no speed is specified then a value must have been previously set with axisClass.setSpeed()"""
		if speed == None:
			speed = self.speed
			if speed == None:
				raise _RepRapError("Axis speed not set")
		if speed >=0 and speed <= 0xFF:
			p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_FORWARD, int(speed)] ) 
			p.send()
		else:
			raise RepRapError("Invalid speed value")
	
	def backward(self, speed = None):
		"""Spin axis backward at given speed (0-255)
		If no speed is specified then a value must have been previously set with axisClass.setSpeed()"""
		# If speed is not specified use stored (or default)
		if speed == None:
			speed = self.speed
			if speed == None:
				raise _RepRapError("Axis speed not set")
		if speed >=0 and speed <= 0xFF:
			p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_REVERSE, int(speed)] ) 
			p.send()
		else:
			raise RepRapError("Invalid speed value")
	
	def getSensors(self):
		"""Debug only. Returns raw PIC port bytes)"""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_GETSENSOR] )
		p.send()
		rep = p.getReply()
		rep.checkReply(3, CMD_GETSENSOR)
		data = rep.dataBytes
		print data[1], data[2]
	
	def getPos(self):
		"""Return the axis postition as an integer (steps)."""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_GETPOS] )
		p.send()
		rep = p.getReply()
		rep.checkReply(3, CMD_GETPOS)
		data = rep.dataBytes
		pos = _bytes2int( data[1], data[2] )
		return pos
	
	def setPos(self, pos):
		"""set current position (integer) (set variable, not physical position. units as steps)"""
		if pos >=0 and pos <= 0xFFFF:
			posMSB ,posLSB = _int2bytes( pos )
			p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_SETPOS, posMSB, posLSB] )
			p.send()
		else:
			raise RepRapError("Invalid position value")
	
	def free(self):
		"""Power off coils on stepper"""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_FREE] ) 
		p.send()
	
	def seek(self, pos, speed = None, waitArrival = True, units = None):
		"""Seek to axis location pos. If waitArrival is True, funtion waits until seek is compete to return"""
		
		# If no speed is specified use value set for axis, if this doesn't exist raise exception
		if speed == None:
			speed = self.speed
			if speed == None:
				raise _RepRapError("Axis speed not set")
		
		# If no units area specified use units set for axis, if this doesn't exist use steps
		if units == None:
			units = self.units
			if units == None:
				units = UNITS_STEPS
		
		# Convert units into steps
		if units == UNITS_STEPS:
			pass
		elif units == UNITS_MM:
			newX = int( float(newX) * self.stepsPerMM )
			newY = int( float(newY) * self.stepsPerMM )
		elif units == UNITS_INCHES:
			newX = int( float(newX) * self.stepsPerMM * 25.4 )
			newX = int( float(newY) * self.stepsPerMM * 25.4 )
		else:
			raise _RepRapError("Invalid units")
		
		# Check that position is withing limits and speed is valid
		if (pos <= self.limit or self.limit == 0) and pos >=0 and pos <= 0xFFFF and speed >=0 and speed <= 0xFF:
			posMSB ,posLSB = _int2bytes( pos )
			p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_SEEK, int(speed), posMSB ,posLSB] ) 
			p.send()
			if waitArrival:
				notif = p.getReply()
				if not notif.dataBytes[0] == CMD_SEEK:
					raise _RepRapError("Expected seek notification")
		else:
			raise RepRapError("Invalid speed or position value")
	
	def homeReset(self, speed = None, waitArrival = True):
		"""Go to 0 position. If waitArrival is True, funtion waits until reset is compete to return"""
		if speed == None:
			speed = self.speed
			if speed == None:
				raise _RepRapError("Axis speed not set")
		if speed >= 0 and speed <= 0xFF:
			p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_HOMERESET, int(speed)] ) 
			p.send()
			if waitArrival:
				notif = p.getReply()
				if not notif.dataBytes[0] == CMD_HOMERESET:
					raise _RepRapError("Expected home reset notification")
		else:
			raise RepRapError("Invalid speed value")
	
	def setNotify(self):
		"""Set axis to notify on arrivals"""
		p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_NOTIFY, snap.localAddress] ) 	# set notifications to be sent to host
		p.send()
	
	def _setSync( self, syncMode ):
		"""Set sync mode"""
		if syncMode >= 0 and syncMode <= 0xFF:
			p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_SYNC, int(syncMode)] )
			p.send()
		else:
			raise RepRapError("Invalid sync mode")
	
	def _DDA( self, seekTo, slaveDelta, speed = False, waitArrival = True):
		"""Set DDA mode"""
		if not speed:
			speed = self.speed
		if (seekTo <= self.limit or self.limit == 0) and seekTo >=0 and seekTo <= 0xFFFF and slaveDelta >=0 and slaveDelta <= 0xFFFF and speed >=0 and speed <= 0xFF:
			masterPosMSB, masterPosLSB = _int2bytes( seekTo )
			slaveDeltaMSB, slaveDeltaLSB = _int2bytes( slaveDelta )
			p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_DDA, int(speed), masterPosMSB ,masterPosLSB, slaveDeltaMSB, slaveDeltaLSB] ) 	#start sync
			p.send()
			if waitArrival:
				notif = p.getReply()
				if not notif.dataBytes[0] == CMD_DDA:
					raise _RepRapError("Expected DDA notification")
	
	def setPower( self, power ):
		"""Set stepper motor power (0-100%)"""
		power = int( float(power) * 0.63 )
		if power >=0 and power <=0x3F:
			p = snap.Packet( self.address, snap.localAddress, 0, 1, [CMD_SETPOWER, int( power * 0.63 )] ) # This is a value from 0 to 63 (6 bits)
			p.send()
		else:
			raise RepRapError("Invalid power value")
	
	def setSpeed(self, speed):
		"""Set axis move speed (0-255)"""
		if speed >= 0 and speed <= 0xFF:
			self.speed = speed
		else:
			raise RepRapError("Invalid speed value")
	
	def setStepsPerMM(self, spmm):
		"""Set axis steps per millimeter"""
		self.stepsPerMM = float(spmm)
	
	def setUnits(self, units):
		"""Set axis units (reprap.UNITS_STEPS/reprap.UNITS_MM/reprap.UNITS_INCHES)"""
		if self.stepsPerMM == None:
			raise _RepRapError("Only reprap.UNITS_STEPS can be used without specifying steps per mm. use setStepsPerMM().")
		else:
			self.units = units


class _syncAxis:
	"""Class to hold axis info so master and slave on sync move can be swapped over."""
	def __init__( self, axis, seekTo, delta, direction ):
		self.axis = axis
		self.seekTo = seekTo
		self.delta = delta
		self.direction = direction
		
		if self.direction > 0:
			self.syncMode = SYNC_INC
		else:
			self.syncMode = SYNC_DEC

class cartesianClass:
	"""Main cartesian robot class"""
	def __init__(self):
		"""Create a cartesian instance. An instances is automatically created and can be accessed via reprap.cartesian
		You will only need to create another one in you want to control more than one machine at the same time."""
		
		self.units = None
		
		# initiate axies with addresses
		self.x = axisClass(2)
		self.y = axisClass(3)
		self.z = axisClass(4)
	
	def homeReset(self, speed = None, waitArrival = True):
		"""Reset all axies to the home position with speed (0-255) and wait until arrival (boolean)
		WARNING : Reseting all axies at the same time is unstable. suggest using waitArrival = True option."""
		if not waitArrival:
			print "WARNING : Reseting all axies at the same time is unstable. suggest using waitArrival = True option."
		#z is done first so we don't break anything we just made
		if self.z.homeReset( speed = speed, waitArrival = waitArrival ):
			print "Z Reset"
		if self.x.homeReset( speed = speed, waitArrival = waitArrival ):
			print "X Reset"
		if self.y.homeReset( speed = speed, waitArrival = waitArrival ):
			print "Y Reset"
		
		# TODO add a way to collect all three notifications (in whatever order) then check they are all there. this will allow symultanious axis movement and use of waitArrival
		# This requires snap receiver to search packets rather than just returning oldest one. probably need to do this anyway
	
	def seek(self, pos, speed = None, waitArrival = True, units = None):
		"""Seek to a position ( tuple (x, y, z) ) with speed (0-255) and and wait until arrival (boolean)
		Seek will automatically select between a standard seek and a syncronised seek when it is required
		When waitArrival is True, funtion does not return until all seeks are compete"""
		
		if speed == None:
			speed = self.speed
			if speed == None:
				raise _RepRapError("Cartesian speed not set or specified")
		
		if units == None:
			units = self.units
			if units == None:
				units = UNITS_STEPS
		
		curX, curY, curZ = self.x.getPos(), self.y.getPos(), self.z.getPos()
		x, y, z = pos
		#print "seek from", curX, curY, curZ, "to", x, y, z
		# Check that we are moving withing limits, and 
		if (x == None or x <= self.x.limit or self.x.limit == 0) and (y == None or y <= self.y.limit or self.y.limit == 0) and (z == None or z <= self.z.limit or self.z.limit == 0):
			if printDebug: print "seek from [", curX, curY, curZ, "] to [", x, y, z, "]"
			# Check if we need to do a standard seek or a DDA seek
			if x == curX or y == curY or x == None or y == None:
				if printDebug: print "    standard seek"
				if x != None and x != curX:				
					self.x.seek( x, speed, waitArrival, units )			#setting these to true breaks waitArrival convention. need to rework waitArrival and possibly have each axis storing it's arrival flag and pos as variables?
				if y != None and y != curY:
					self.y.seek( y, speed, waitArrival, units )
			elif x != None and y != None:
				if printDebug: print "    sync seek"
				self._syncSeek( pos, curX, curY, speed, waitArrival, units )
			if z != None and z != curZ:
				#self.z.seek( z, speed, True ) # why was this forced?
				self.z.seek( z, speed, waitArrival, units )
			return True
		else:
			print "Trying to print outside of limit, aborting seek"
			return False
	
	def _syncSeek(self, pos, curX, curY, speed, waitArrival, units):
		"""perform syncronised x/y movement. This is called by seek when needed."""
		newX, newY, nullZ = pos
		if units == UNITS_STEPS:
			pass
		elif units == UNITS_MM:
			newX = int( float(newX) * self.stepsPerMM )
			newY = int( float(newY) * self.stepsPerMM )
		elif units == UNITS_INCHES:
			newX = int( float(newX) * self.stepsPerMM * 25.4 )
			newX = int( float(newY) * self.stepsPerMM * 25.4 )
		else:
			raise _RepRapError("Invalid units")
		
		deltaX = abs( curX - newX )		# calc delta movements
		deltaY = abs( curY - newY )
		#print "syncseek deltas", deltaX, deltaY
		directionX = ( curX - newX ) / -deltaX	# gives direction -1 or 1
		directionY = ( curY - newY ) / -deltaY	
		
		master = _syncAxis( self.x, newX, deltaX, directionX )	# create two swapable data structures, set x as master, y as slave
		slave = _syncAxis( self.y, newY, deltaY, directionY )
		
		if slave.delta > master.delta:		# if y has the greater movement then make y master
			slave, master = master, slave
			if printDebug: print "    switching to y master"
		if printDebug: print "    masterPos", master.seekTo, "slaveDelta", slave.delta
		slave.axis._setSync( slave.syncMode )
		master.axis._DDA( master.seekTo, slave.delta, speed, True )	#why was this forced? # because we have to wait before we tell the slave axis to leave sync mode!
		#master.axis._DDA( master.seekTo, slave.delta, speed, waitArrival )
		time.sleep(0.01)	# TODO this is really bad, can we remove?
		slave.axis._setSync( SYNC_NONE )
		if printDebug: print "    sync seek complete"
	
	def getPos(self):
		"""Return the current positions of all three axies as a tuple (x, y, z) in steps"""
		return self.x.getPos(), self.y.getPos(), self.z.getPos()
	
	def stop(self):
		"""Stop all motors (but retain current)"""
		self.x.forward(0)
		self.y.forward(0)
		self.z.forward(0)
	
	def free(self):
		"""Free all motors (no current on coils)"""
		self.x.free()
		self.y.free()
		self.z.free()
	
	def setPower(self, power):
		"""Set stepper power (0-100)"""
		self.x.setPower(power)
		self.y.setPower(power)
		self.z.setPower(power)
	
	#def lockout():
	#keep sending power down commands to all board every second
	
	def setSpeed(self, speed):
		"""Set axies move speed (0-255)"""
		self.speed = speed
		self.x.setSpeed(speed)
		self.y.setSpeed(speed)
		self.z.setSpeed(speed)
	
	def setStepsPerMM(self, spmm):
		"""Set axies steps per millimeter"""
		self.stepsPerMM = float(spmm)
		self.x.stepsPerMM(spmm)
		self.z.stepsPerMM(spmm)
		self.z.stepsPerMM(spmm)
	
	def setUnits(self, units):
		"""Set axies units (reprap.UNITS_STEPS/reprap.UNITS_MM/reprap.UNITS_INCHES)"""
		self.units = units
		self.x.setUnits(units)
		self.y.setUnits(units)
		self.z.setUnits(units)


cartesian = cartesianClass()



