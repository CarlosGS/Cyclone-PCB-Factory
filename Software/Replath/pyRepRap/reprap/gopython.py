"""
Module for quick Python command line testing.
Import reprap.gopython with a serial SNAP RepRap connected and switched on.
RepRap commands can then be used to control the machine.
Note: This module should be used for testing only. For any applications
using the reprap module import reprap itself.

Example:

import reprap.gopython
reprap.cartesian.seek((100, 200, 20))
reprap.cartesian.homeReset()
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

import reprap

# Initialise serial port, here the first port (0) is used, timeout 60 seconds.
reprap.openSerial( 0, 19200, 60 )
# These devices are present in network, will automatically scan in the future.
reprap.cartesian.x.active = True
reprap.cartesian.y.active = True
reprap.cartesian.z.active = True
reprap.extruder.active = True

reprap.cartesian.x.setNotify()
reprap.cartesian.y.setNotify()
reprap.cartesian.z.setNotify()

reprap.cartesian.setSpeed(220)
reprap.cartesian.setPower( int( 83 * 0.63 ) )
reprap.cartesian.homeReset()



reprap.cartesian.free()
