from math import *

MAX_WHEEL_DIST = 200

def getColorWheel (initx, inity, currx, curry):
	delta_y = curry - inity
	delta_x = currx - initx
	angle = atan2(delta_y, -delta_x)
	angle = angle / (2*pi)
	h = angle
	dist = sqrt(delta_y**2 + delta_x**2)
	dist = min (dist, MAX_WHEEL_DIST) / MAX_WHEEL_DIST
	s = dist
	v = 0.7 # lol 0.7 for no reason
	(r,g,b) = hsv_to_rgb(h,s,v)
	r = r * 255
	g = g * 255
	b = b * 255
	return rgb_to_hex((r,g,b))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb