"""
This module is an implementation of the SNAP communications protocol and is used for
communications between the PC host and the RepRap machine.
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


import serial, exceptions, threading, time
from __init__ import _RepRapError


SYNC_BYTE = 0x54
PAYLOAD_OFFSET = 5
HDB1_OFFSET = 2

printOutgoing = False
#printOutgoing = True
printIncoming = False
#printIncoming = True

localAddress = 0
serialPort = None


def openSerial( port = 0, rate = 19200, tout = 60 ):
	"""Open serial port for SNAP RepRap communications"""
	global serialPort
	try:
		serialPort = serial.Serial( port, rate, timeout = tout )
	except:
		raise _RepRapError("You do not have permissions to use the serial port, try running as root")


def closeSerial():
	"""Close serial port for SNAP RepRap communications"""
	serialPort.close()


class _SNAPError(exceptions.Exception):
	"""Exception class"""
	def __init__(self, msg):
		self.msg = msg
		return
	
	def __str__(self):
		return "A SNAP error has occured! " + str(self.msg)


class Packet:
	"""SNAP packet class"""
	def __init__(self, DAB = None, SAB = None, ACK = None, NAK = None, dataBytes = None):
		"""Create SNAP packet"""
		self.bytes = []
		self.encoded = False
		
		if DAB != None and SAB != None and ACK != None and NAK != None and dataBytes != None:
			self.SYNC = SYNC_BYTE
			self.DAB = DAB
			self.SAB = SAB
			self.ACK = ACK
			self.NAK = NAK
			self.dataBytes = dataBytes
			self.decoded = True
		else:
			self.SYNC = None
			self.decoded = False
	
	def send(self):
		"""Send SNAP packet over serial conneciton (automatically encodes)"""
		# Encode packet
		self._encode()
		# Clear incoming packet buffer (if we havn't looked at the yet we never will)
		#Receiver.clearPackets()
		# Transimit packet
		self._sendBytes()
		if printOutgoing:
			self.printPacket("Outgoing")
		# Get ack packet and remove from buffer
		ack = getPacket(serialPort)
		
		if not ack._check():
			raise _SNAPError("ACK packet checksum failed")
		ack._decode()
		
		# check that packet is an acknoledgement and that it is from the device we just messaged.
		if ack.ACK == 1 and ack.SAB == self.DAB:		
			return
		else:
			# If somthing is wrong with the ACK, print the packet we sent, the one we recieved, then raise an exception
			self.printPacket("Failed")
			ack.printPacket("Failed ACK")
			if ack.ACK != 1 and ack.SAB == self.DAB:
				raise _SNAPError("ACK expected, packet is not an ACK")
			elif ack.SAB != self.DAB and ack.ACK == 1:
				raise _SNAPError("ACK packet is not from the expected module""")
			else:
				raise _SNAPError("ACK expected, packet is not an ACK and it is from the wrong module (it's all gone very wrong)")
	
	def getReply(self):
		"""Returns the first packet from the receive buffer"""
		rep = getPacket(serialPort)
		if not rep._check():
			raise _SNAPError("reply packet checksum failed")
		return rep
	
	def _encode(self):
		"""Encode attributes into byte list (Packet.bytes)"""
		if not self.decoded:
			raise _SNAPError("Can't encode packet, data is missing")
		self.NDB = len(self.dataBytes)
		self.bytes = []
		self.bytes.insert( 0, 0xFF & self.SYNC )
		self.HDB1 = _makeHDB2(self.ACK, self.NAK)
		self.bytes.insert( 1, 0xFF & self.HDB1 )
		self.HDB2 = _makeHDB1(self.NDB)
		self.bytes.insert( 2, 0xFF & self.HDB2 )
		self.bytes.insert( 3, 0xFF & self.DAB )
		self.bytes.insert( 4, 0xFF & self.SAB )
		
		for d in self.dataBytes:	
			self.bytes.append( 0xFF & d )
		
		checksum = _Checksum()
		for d in self.bytes[1:]:
			checksum.addData(d)
		self.CRC = checksum.getResult()
		self.bytes.append( self.CRC )
		self.encoded = True
	
	def _decode(self):
		"""Decode byte list (Packet.bytes) to attributes"""
		if len(self.bytes) == 0:
			raise _SNAPError("Can't decode and empty packet")
		
		self.SYNC = self.bytes[0]
		self.HDB2 = self.bytes[1]
		self.HDB1 = self.bytes[2]
		self.DAB = self.bytes[3]
		self.SAB = self.bytes[4]
		self.NDB = _breakHDB1(self.HDB1)
		
		self.dataBytes = []
		for d in self.bytes[5:5 + self.NDB]:
			self.dataBytes.append(d)
		
		self.CRC = self.bytes[5 + self.NDB::6 + self.NDB][0]
		numLeftoverBytes = len(self.bytes) - 6 - self.NDB
		self.leftoverBytes = self.bytes[6 + self.NDB:len(self.bytes)]
		if numLeftoverBytes > 0:
			#print "leftover bytes", numLeftoverBytes, self.leftoverBytes
			raise _SNAPError("Decoded packet has " + str(numLeftoverBytes) + " bytes left over")
		self.ACK, self.NAK = _breakHDB2(self.HDB2)
		self.bytes = self.bytes[:6 + self.NDB]
		self.decoded = True
	
	def _check(self):
		"""Returns True if calculated checksum matches checksum attatched to packet, otherwise False"""
		newChecksum = _Checksum()
		for d in self.bytes[1:-1]:
			newChecksum.addData(d)
		testCRC = newChecksum.getResult()
		if testCRC == self.CRC:
			return True
		else:
			return False, testCRC, self.CRC
	
	def checkReply(self, expectedBytes, expectedCommand):
		"""Checks that the correct number of data bytes have been recieved and that the reply is a reply to the sent command"""
		if len( self.dataBytes ) != expectedBytes:
			raise RepRapError("Reply contains wrong number of bytes")
		if self.dataBytes[0] != expectedCommand:
			raise RepRapError("Reply is for wrong command")
		return True
	
	def _sendBytes(self):
		"""Transmit byte list (Packet.bytes) on serial conneciton"""
		if self.encoded == True:
			for d in self.bytes:
				serialPort.write(chr(d))
		else:
			raise _SNAPError("Trying to send a packet that has not been encoded")
	
	#def _addByte(self, byte):
	#	"""Add a byte to the packet, is this obsolete?"""
	#	self.bytes.append(byte)
	
	def _setBytes(self, bytes):
		"""Set Packet.bytes contents"""
		self.bytes = bytes
	
	def printPacket(self, status):
		"""Print contents of packet to screen"""
		if self.decoded == True:
			print "### Start", status, "SNAP Packet ###"
			print "Bytes", self.bytes
			if self.SYNC == 0x54:
				print "...Sync OK"
			else:
				print "...Sync Error"
			print "...Check: ",		self._check()
			print "...DATA",		self.dataBytes
			print "...CRC",			self.CRC
			print "...SAB",			self.SAB
			print "...DAB",			self.DAB
			print "...HDB1",		self.HDB1, ":"
			print "...........NDB",	self.NDB
			print "...HDB2", 		self.HDB2, ":"
			print "...........ACK",	self.ACK
			print "...........NAK",	self.NAK
			print "### End", status, "SNAP Packet ###"
		else:
			raise _SNAPError("Trying to print a packet that has not been decoded")


#this is done again in full decode, but needed here so num bytes to expect is known.
def _getPacketLen(buffer):	
	l = _breakHDB1( buffer[offset_hdb1] )
	return l


def getPacket(ser):
	bytes = []
	# Read in 5 bytes
	while len(bytes) <= 4:
		byte = ser.read()
		if len(byte) > 0:
			# If this is the sync then clear the byte buffer.
			if byte == SYNC_BYTE:
				bytes = []
			bytes.append( ord(byte) )
		else:
			raise _SNAPError("Serial timeout")
	
	# Read the expected packet length from Header Byte 1
	packetLength = _breakHDB1( bytes[HDB1_OFFSET] ) + PAYLOAD_OFFSET + 1
	
	while len(bytes) < packetLength:
		byte = ser.read()
		if len(byte) > 0:
			bytes.append( ord(byte) )
		else:
			raise _SNAPError("Serial timeout")
	
	# We have enough bytes, create packet object
	p = Packet()
	p._setBytes(bytes)
	p._decode()
	p._check()
	
	if printIncoming:
		p.printPacket("Incoming")
	if p.DAB == localAddress:
		return p
	else:
		raise _RepRapError( "Received packet bound for " + str(p.DAB) )



class _Checksum:
	"""Class for checksum calculator"""
	def __init__(self):
		"""Create checksum calculator"""
		self.crc = 0
	
	def addData(self, data): 
		"""Add a byte"""
		#byte i = (byte)(data ^ self.crc)
		i = data ^ self.crc
		self.crc = 0
		if((i & 1) != 0):
			self.crc ^= 0x5e
		if((i & 2) != 0):
			self.crc ^= 0xbc
		if((i & 4) != 0):
			self.crc ^= 0x61
		if((i & 8) != 0):
			self.crc ^= 0xc2
		if((i & 0x10) != 0):
			self.crc ^= 0x9d
		if((i & 0x20) != 0):
			self.crc ^= 0x23
		if((i & 0x40) != 0):
			self.crc ^= 0x46
		if((i & 0x80) != 0):
			self.crc ^= 0x8c
		return data
	
	def getResult(self):
		"""Return the checksum as an integer"""
		return self.crc


def _makeHDB2(ACK, NAK):
	"""Encode Header Byte 2 (HDB2)"""
	SAB = 1			# Length of the Source Address Bytes, in Binary. RepRap currently only accepts source addresses of 1 byte length
	DAB = 1			# Length of the Destination Address Bytes, in Binary. RepRap currently only accepts destinations of 1 byte length
	PFB = 0			# Length of Protocol Flag Bytes. RepRap does not accept any protocol flag bytes, so this must be set to 00
	HDB2val = ((DAB & 0x3) * pow(2,6)) | ((SAB & 0x3) * pow(2,4)) | ((PFB & 0x3) * pow(2,2)) | ((ACK & 0x1) * pow(2,1)) | (NAK & 0x1)
	return HDB2val

def _breakHDB2(HDB2):
	"""Decode Header Byte 2 (HDB2)"""
	ACK = (HDB2 & 0x2) / pow(2,1)
	NAK = (HDB2 & 0x1)
	return ACK, NAK

def _makeHDB1(NDB):
	"""Encode Header Byte 1 (HDB1)"""
	CMD = 0			# Command Mode Bit. Not implemented by RepRap and should be set to 0
	EMD = 0x3		# Currently RepRap only implements 8-bit self.crc. this should be set to 011
	HDB1val = ((CMD & 0x1) * pow(2,7)) | ((EMD & 0x7) * pow(2,4)) | (0xF & NDB)
	return HDB1val

def _breakHDB1(HDB1):
	"""Decode Header Byte 1 (HDB1)"""
	NDB = HDB1 & 0xF
	return NDB



