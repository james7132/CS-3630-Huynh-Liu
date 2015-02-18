import time
from Scribbler2 import *

# Connect to the scribbler
# Set timeout to 0 to read instantly, non-blocking

fname = "log-%d.txt" % time.time()

s = Scribbler2('COM8', fname)

# command constants (time)
T_WAIT = .6
T_TURN = 1.2
# command constants (power)
P_FWRD = 200
P_TURN = 100

# Set timeout to zero
print ('Connected!')
s.setIRPower(140)
s.setForwardness(1)
# Create a list of commands
commands = []
# Command is a list [cmd, leftMotor, rightMotor, time]
# Setting motors to 200 will drive 
# forward with the fluke facing forward
commands.append([P_FWRD, P_FWRD, 2.1])     # FWD
commands.append([0, 0, T_WAIT])           # WAIT
commands.append([-P_TURN, P_TURN, T_TURN])  # TURN LEFT
commands.append([0, 0, T_WAIT])           # WAIT
commands.append([P_FWRD, P_FWRD, 1.9])     # FWD
commands.append([0, 0, T_WAIT])           # WAIT
commands.append([P_TURN, -P_TURN, T_TURN])  # TURN RIGHT
commands.append([0, 0, T_WAIT])           # WAIT
commands.append([P_FWRD, P_FWRD, 4.4])     # FWD
commands.append([0, 0, T_WAIT])           # WAIT
commands.append([P_TURN, -P_TURN, T_TURN])  # TURN RIGHT
commands.append([0, 0, T_WAIT])           # WAIT
commands.append([P_FWRD, P_FWRD, 3.0])     # FWD
commands.append([0, 0, T_WAIT])           # WAIT
print ("Start!")
for c in commands:
  start = time.time()
  s.setMotors(c[0],c[1])
  while (time.time() - start < c[2]):
    s.getObstacle(1)
    time.sleep(0.1) # Read sensors at 1Hz
s.log.close()


