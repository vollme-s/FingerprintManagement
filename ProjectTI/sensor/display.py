import ctypes
tft = ctypes.CDLL("/home/pi/FingerprintSensor/libtft.so.1.0")
path = "/home/pi/FingerprintSensor/bmps/"
textfield = 0
imagefield = 0

def init_tft():
	global imagefield 
	global textfield
	tft.openTFT();
	tft.printImage(path+"hintergrund2.bmp3")
	imagefield = tft.makeFrame(64,64,256,83,0,0xFFFF,path+"hintergrund2.bmp3")
	textfield = tft.makeFrame(256,64,0,83,0,0x0,path+"hintergrund2.bmp3")
	tft.setBackligthValue(255)
	tft.repaintbmp(imagefield)
	tft.repaintbmp(textfield)

def close_tft():
	tft.closeTFT()

def repaintall(bmp,string):
	print "imagefield = ",imagefield
	tft.loadNewbmp(path+bmp,imagefield)
	tft.repaintbmp(imagefield)
	tft.repaintbmp(textfield)
	tft.printText(string,textfield)
	
def printscan(string):
	repaintall("scannen.bmp3",string)

def printok(string):
	repaintall("personok.bmp3",string)

def printunaut(string):
	repaintall("personunberechtigt.bmp3",string)
	
def printerr(string):
	repaintall("personfehler.bmp3",string)

def printclock(string):
	repaintall("zeit.bmp3",string)
	
if __name__ == '__main__':
	init_tft()
	printok("zugangsberechtigt")
#	tft.closeTFT()
