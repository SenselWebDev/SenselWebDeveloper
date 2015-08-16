from Tkinter import *
from math import *
from enum import Enum
from lib.SenselGestureFramework.sensel_framework_simple import Direction
from colorsys import *

WHEEL_SIDE = 200.0
SMALL_COLOR_SIDE = WHEEL_SIDE/2 - 15

def getImages():
	return PhotoImage(file="fontawesome/colorwheel.gif")


class ColorWheel(object):

	def __init__ (self, xloc, yloc):
		self.xloc = xloc
		self.yloc = yloc
		self.TR = 0
		self.color = "#FFFFFF"
		self.images = getImages()

	def changeLoc (self, xloc, yloc):
		self.xloc = xloc
		self.yloc = yloc

	def getColor (self, canv, currx, curry):
		delta_y = curry - self.yloc
		delta_x = currx - self.xloc
		angle = -1*atan2(delta_y, -delta_x) + pi

		angle = angle / (2*pi)
		h = angle
		dist = sqrt(delta_y**2 + delta_x**2)
		dist = min(dist, WHEEL_SIDE) / WHEEL_SIDE
		s = dist
		v = 0.7 # lol 0.7 for no reason
		(r,g,b) = hsv_to_rgb(h,s,v)
		r = r * 255
		g = g * 255
		b = b * 255
		self.color = self.rgb_to_hex((r,g,b))
		self.drawWheel(canv)
		return self.color

	def drawWheel (self, canv):

		self.inner = canv.create_oval(self.xloc - SMALL_COLOR_SIDE, self.yloc + SMALL_COLOR_SIDE, self.xloc + SMALL_COLOR_SIDE, self.yloc - SMALL_COLOR_SIDE,  tags="inner", fill = self.color, outline = "")
		self.wheel = canv.create_image(self.xloc, self.yloc, image=self.images)


	def clearWheel (self, canv):
		try:
			canv.delete(self.wheel)
			canv.delete(self.inner)
		except Exception, e:
			pass


	def moveWheel (self, canv, xloc, yloc):
		clearWheel(self, canv)
		changeLoc(self, self.xloc, self.yloc)		
		drawWheel(self, canv)

	def rgb_to_hex(self, rgb):
		return '#%02x%02x%02x' %rgb

