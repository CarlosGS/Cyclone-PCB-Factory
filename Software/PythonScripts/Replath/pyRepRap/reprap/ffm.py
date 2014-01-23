"""
Module for making things out of plastic using a thermoplast extruder
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

import reprap, time

class FFM:
	def __init__(self, extrudeTemp, extrudeSpeed, moveSpeed, zBottomLayer, zIdleHeight, stopReverseMotorTime):
		self.extrudeTemp = extrudeTemp
		self.extrudeSpeed = extrudeSpeed
		self.moveSpeed = moveSpeed
		self.zBottomLayer = zBottomLayer
		self.zIdleHeight = zIdleHeight
		self.stopReverseMotorTime = stopReverseMotorTime
		self.fastSpeed = 200
		
		self.currentLayerHeight = self.zBottomLayer
		reprap.cartesian.setMoveSpeed(self.moveSpeed)
		
	def setExtrudeSpeed(self, speed):
		self.extrudeSpeed = speed
	
	def setExtrudeMoveSpeed(self, speed):
		self.moveSpeed = speed
	#	reprap.cartesian.setMoveSpeed(self.moveSpeed)
	
	# Layer down a line of plastic (Move to start point, lower tool (if not already), deposit plastic in line to end point, stop depositing.)
	def extrudeLine(self, x1, y1, x2, y2):
		if x1 != x2 or y1 != y2:
			reprap.cartesian.seek( (x1, y1, False), speed = self.fastSpeed )
			self.lowerTool()
			reprap.extruder.setMotor(reprap.MOTOR_FORWARD, self.extrudeSpeed)
			reprap.cartesian.seek( (x2, y2, False), speed = self.moveSpeed )
			reprap.extruder.setMotor(reprap.MOTOR_FORWARD, 0)
		
	def reverseMotorStopFlow(self):
		reprap.extruder.setMotor(reprap.MOTOR_BACKWARD, self.extrudeSpeed)
		time.sleep(self.stopReverseMotorTime)
		reprap.extruder.setMotor(reprap.MOTOR_BACKWARD, 0)
	
	# Raise tool to safe moving height
	def raiseTool(self):
		reprap.cartesian.z.seek(self.currentLayerHeight - self.zIdleHeight, speed = self.fastSpeed)
	
	# Lower tool to current layer working height
	def lowerTool(self):
		reprap.cartesian.z.seek(self.currentLayerHeight, speed = self.fastSpeed)
