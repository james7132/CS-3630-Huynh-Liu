import time
# from Scribbler2 import *
from Myro import *

T_WAT = 0.8
T_TRN = 2.35
T_INV = T_TRN * 2
# command constants (power)
P_FWD = .7
P_TRN = .3

# Connect to the scribbler
# Set timeout to 0 to read instantly, non-blocking
def runCommands(log, commands):
    for c in commands:
      start = time.time()
      motors(c[0],c[1])
      while (time.time() - start < c[2]):
        logNow(log, c[0],c[1],0);
        time.sleep(0.1) # Read sensors at 1Hz

def logNow(log, l, r, fname):
    print ("%s %s %s"%(l,r,fname))
    log.write("%s %s %s\n" %(l, r, fname))

fname = "log-%d.txt" % time.time()
log = open(fname, 'w')

#init("COM8")

def picture():
    print('Taking picture.')
    pic_fname = "pic-%d.jpg" % time.time()
    picture = takePicture('gray')
    savePicture(picture, pic_fname)
    logNow(log, 0,0,pic_fname)
    print('Done.')

setIRPower(140)
setForwardness(1)

## Take picture 320
picture()

# Run
commands = []
commands.append([0, 0, T_WAT])           # WAIT
commands.append([P_TRN, -P_TRN, T_TRN])  # TURN RIGHT
commands.append([0, 0, T_WAT])           # WAIT
commands.append([P_FWD, P_FWD, 4.6])     # FWD
commands.append([0, 0, T_WAT])           # WAIT
runCommands(log, commands)

## Take picture 322
picture()

# Run
commands = []
commands.append([0, 0, T_WAT])           # WAIT
commands.append([-P_TRN, P_TRN, T_TRN])  # TURN LEFT
commands.append([0, 0, T_WAT])           # WAIT
runCommands(log, commands)

## Take picture 321
picture()

# Run
commands = []
commands.append([0, 0, T_WAT])           # WAIT
commands.append([-P_TRN, P_TRN, T_TRN])  # TURN LEFT
commands.append([0, 0, T_WAT])           # WAIT
commands.append([-P_TRN, P_TRN, T_TRN])  # TURN LEFT
commands.append([0, 0, T_WAT])           # WAIT
commands.append([P_FWD, P_FWD, 8.5])     # FWD
commands.append([0, 0, T_WAT])           # WAIT
runCommands(log, commands)

## Take picture 323
picture()

# Run
commands = []
commands.append([0, 0, T_WAT])           # WAIT
commands.append([P_TRN, -P_TRN, T_TRN])  # TURN RIGHT
commands.append([0, 0, T_WAT])           # WAIT
commands.append([P_FWD, P_FWD, 2.0])     # FWD
commands.append([0, 0, T_WAT])           # WAIT
commands.append([-P_TRN, P_TRN, T_TRN])  # TURN LEFT
commands.append([0, 0, T_WAT])           # WAIT
runCommands(log, commands)

## Take picture 324
picture()

# Run
commands = []
commands.append([0, 0, T_WAT])           # WAIT
commands.append([-P_TRN, P_TRN, T_TRN])  # TURN LEFT
commands.append([0, 0, T_WAT])           # WAIT
commands.append([-P_TRN, P_TRN, T_TRN])  # TURN LEFT
commands.append([0, 0, T_WAT])           # WAIT
runCommands(log, commands)

## Take picture 325
picture()

# Run
commands = []
commands.append([0, 0, T_WAT])           # WAIT
commands.append([-P_TRN, P_TRN, T_TRN])  # TURN LEFT
commands.append([0, 0, T_WAT])           # WAIT
commands.append([P_FWD, P_FWD, 0.6])     # FWD
commands.append([0, 0, T_WAT])           # WAIT
runCommands(log, commands)

## Take picture 326
picture()

## Close (Do not remove this line)
log.close();
