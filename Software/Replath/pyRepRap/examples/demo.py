# Import the reprap  modules
import reprap, time

# Initialise serial port, here the first port (0) is used.
reprap.openSerial( 0, 19200, 60 )

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
reprap.cartesian.setMoveSpeed(220)
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
