#!/usr/bin/python

from Tkinter import *
import tkFont
from wheel_menu_framework import *

root = Tk()
wheel = WheelMenu(0,0)


def point(event):
	wheel.clearWheel(c)
	wheel.changeLoc(event.x, event.y)
	#wheel.drawWheel(c)
	wheel.highlightSide(c,180)

c = Canvas(root, bg="white", width=1000, height= 1000)

c.configure(cursor="crosshair")

c.pack()


texttest = c.create_text(100,100, text = "hello")
print tkFont.families()

c.bind("<Button-1>", point)

root.mainloop()