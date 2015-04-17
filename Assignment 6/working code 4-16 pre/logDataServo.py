import time
import os.path
import System
from Myro import *

# Run commands to move the robot
def runCommands(log, commands):
    for c in commands:
      start = time.time()
      motors(c[0],c[1])
      while (time.time() - start < c[2]):
        logNow(log, c[0],c[1],0);
        time.sleep(0.1) # Read sensors at 1Hz

def takePhoto():
	pic_fname = "pic-%d.jpg" % time.time()
	print('\tTaking picture:', pic_fname)
	picture = takePicture();
	print('\tPicture taken!')
	logNow(log, 0,0,pic_fname);
	print('\tSaving picture...')
	savePicture(picture, pic_fname)
	print('\tPicture saved!')
		
# Run commands followed by taking picture        
def runCommand(log, cmd):

	# Move the robot
	commands = [];
	commands.append(cmd);
	commands.append([0,0,0.1]);
	runCommands(log,commands);

# Log motor commands
def logNow(log, l, r, fname):
    log.write("%s %s %s\n" %(l, r, fname))

# write to output log
fname = "motion_log.txt"
if os.path.exists(fname):
	log = open(fname, 'a')
else:
	log = open(fname, 'w')

# read from command log
cmdFile = open('motion_plan.txt', 'r')
commands = cmdFile.readlines()
cmdFile.close()
	
# setup robot
print('Connecting to Scribbler...')
init("COM8")
setIRPower(140)
setForwardness(1)
	
print('Starting motion plan...')
for command in commands:
	cmd = command.split()
	roboCmd = [float(cmd[0]), float(cmd[1]), float(cmd[2])]
	print('Running command:', roboCmd)
	runCommand(log, roboCmd)
print('Motion plan complete.')
takePhoto()

log.close();

print('Script finished!')

System.Environment.Exit(0)