from Tkinter import *
import math
from PIL import ImageTk
from enum import Enum
from lib.SenselGestureFramework.sensel_framework_simple import Direction

WHEEL_SIDE = 200.0
SMALL_WHEEL_SIDE = WHEEL_SIDE/5
LINE_L = WHEEL_SIDE*math.sqrt(2)/4

BACK_COLOR = "#97D6FF"
HIGH_COLOR = "#90FF74"
LINE_COLOR = "#FFFFFF"
LINE_WIDTH = 3

class Action(Enum):
	IMAGE = 0
	SHAPE = 1
	TEXT = 2

def getImages():
	return {
		Action.IMAGE: PhotoImage(file="fontawesome/pic.gif").subsample(12, 12),
		Action.SHAPE: PhotoImage(file="fontawesome/square.gif").subsample(12, 12),
		Action.TEXT: PhotoImage(file="fontawesome/text.gif").subsample(12, 12)
	}

def convertDirectionToAction(direction):
	returnValue = None
	if(direction == Direction.UP):
		returnValue = Action.TEXT
	elif(direction == Direction.LEFT):
		returnValue = Action.IMAGE
	elif(direction == Direction.RIGHT):
		returnValue = Action.SHAPE
	return returnValue


class WheelMenu(object):

	def __init__ (self, xloc, yloc):
		self.xloc = xloc
		self.yloc = yloc
		self.TR = 0
		self.highlight = 0
		self.images = getImages()

	def changeLoc (self, xloc, yloc):
		self.xloc = xloc
		self.yloc = yloc

	def drawWheel (self, canv):
		print LINE_L
		self.circ = canv.create_oval(self.xloc - WHEEL_SIDE/2, self.yloc + WHEEL_SIDE/2, self.xloc + WHEEL_SIDE/2, self.yloc - WHEEL_SIDE/2,  tags="circle", fill = BACK_COLOR, outline = "")
		self.TR = canv.create_line(self.xloc - LINE_L, self.yloc - LINE_L, self.xloc + LINE_L, self.yloc + LINE_L, fill = LINE_COLOR, tags="TRline", width = LINE_WIDTH)
		self.TL = canv.create_line(self.xloc + LINE_L, self.yloc - LINE_L, self.xloc - LINE_L, self.yloc + LINE_L, fill = LINE_COLOR, tags="TLline", width = LINE_WIDTH)
		self.inner = canv.create_oval(self.xloc - SMALL_WHEEL_SIDE, self.yloc + SMALL_WHEEL_SIDE, self.xloc + SMALL_WHEEL_SIDE, self.yloc - SMALL_WHEEL_SIDE,  tags="inner", fill = "white", outline = "")
		self.drawImages(canv)
		
	def highlightSide (self, canv, side):		
		self.circ = canv.create_oval(self.xloc - WHEEL_SIDE/2, self.yloc + WHEEL_SIDE/2, self.xloc + WHEEL_SIDE/2, self.yloc - WHEEL_SIDE/2,  tags="circle", fill = BACK_COLOR, outline = "")
		self.highlight = canv.create_arc(self.xloc - WHEEL_SIDE/2, self.yloc + WHEEL_SIDE/2, self.xloc + WHEEL_SIDE/2, self.yloc - WHEEL_SIDE/2,  tags="circle", fill = HIGH_COLOR, outline = "", start = side-45, extent = 90)
		self.TR = canv.create_line(self.xloc - LINE_L, self.yloc - LINE_L, self.xloc + LINE_L, self.yloc + LINE_L, fill = LINE_COLOR, tags="TRline", width = LINE_WIDTH)
		self.TL = canv.create_line(self.xloc + LINE_L, self.yloc - LINE_L, self.xloc - LINE_L, self.yloc + LINE_L, fill = LINE_COLOR, tags="TLline", width = LINE_WIDTH)
		self.inner = canv.create_oval(self.xloc - SMALL_WHEEL_SIDE, self.yloc + SMALL_WHEEL_SIDE, self.xloc + SMALL_WHEEL_SIDE, self.yloc - SMALL_WHEEL_SIDE,  tags="inner", fill = "white", outline = "")
		self.drawImages(canv)

	def drawImages(self, canvas):
		# Draw shapes on each quadrant
		canvas.create_image(self.xloc-WHEEL_SIDE/2 + 30, self.yloc, image=self.images[Action.IMAGE])
		canvas.create_image(self.xloc+WHEEL_SIDE/2 - 30, self.yloc, image=self.images[Action.SHAPE])
		canvas.create_image(self.xloc, self.yloc-WHEEL_SIDE/2 + 30, image=self.images[Action.TEXT])

	def clearWheel (self, canv):
		if self.TR:
			print "ah"
			canv.delete(self.TR)
			canv.delete(self.TL)
			canv.delete(self.circ)
			canv.delete(self.inner)
		if self.highlight:
			canv.delete(self.highlight)

	def moveWheel (self, canv, xloc, yloc):
		clearWheel(self, canv)
		changeLoc(self, self.xloc, self.yloc)		
		drawWheel(self, canv)