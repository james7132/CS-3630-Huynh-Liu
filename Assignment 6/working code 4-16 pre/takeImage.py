import time
import System
from Myro import *

def takePhoto():
	pic_fname = "pic-%d.jpg" % time.time()
	print('\tTaking picture:', pic_fname)
	picture = takePicture();
	print('\tPicture taken!')
	logNow(log, 0,0,pic_fname);
	print('\tSaving picture...')
	savePicture(picture, pic_fname)
	print('\tPicture saved!')


print('Connecting to Scribbler...')
init("COM8")
setIRPower(140)
setForwardness(1)

takePhoto()
print('Photo taken!')

log.close()

print('Script finished!')

System.Environment.Exit(0)