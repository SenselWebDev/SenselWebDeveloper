#!/usr/bin/python

from Tkinter import *
import tkFont
from wheel_menu_framework import *
from color_wheel_framework import *
import math

root = Tk()
wheel = WheelMenu(0,0)
colorwheel = ColorWheel(500,500)


def point(event):
	colorwheel.clearWheel(c)
	#wheel.drawWheel(c)
	print colorwheel.getColor(c,event.x, event.y)

c = Canvas(root, bg="white", width=1000, height= 1000)

c.configure(cursor="crosshair")

c.pack()

texttest = c.create_text(100,100, text = "hello")

c.bind("<Button-1>", point)

root.mainloop()