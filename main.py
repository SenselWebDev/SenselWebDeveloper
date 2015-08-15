
from lib.SenselGestureFramework.sensel_framework_simple import *
from Tkinter import *
import threading

objects = None
root = None
canvas = None

class Objects(object):
	"""Objects that will need to be rendered"""
	def __init__(self):
		self.data = []

	def addObject(self, obj):
		self.data.append(obj)

class Circle(object):
	"""docstring for Circle"""
	def __init__(self, x, y, radius):
		super(Circle, self).__init__()
		self.x = x
		self.y = y
		
		self.radius = radius

	def render(self, canvas):
		print("Circle!")
		canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill="grey")
		

class SenselEventLoop(SenselGestureHandler):
	"""docstring for SenselEventLoop"""
	def __init__(self, arg):
		super(SenselEventLoop, self).__init__(arg)

	def gestureEvent(self, gesture, arg):
		if(gesture.gesture_type == GestureType.TAP and gesture.weight_class == WeightClass.LIGHT):
			# Draw the cursor
			print("Would draw cursor")
			last_location = gesture.tracked_locations[len(gesture.tracked_locations) - 1]
			objects.addObject(Circle(last_location[0], last_location[1], 20))
			render(arg)

class SenselWorkerThread(threading.Thread):
	"""docstring for SenselWorkerThread"""
	def __init__(self, objects):
		# Pass a reference to the objects up as the arg
		super(SenselWorkerThread, self).__init__()
		self.event_loop = SenselEventLoop(objects)

	def run(self):
		self.event_loop.start()
		

def view_setup():
	global root, canvas, objects

	if(root == None): 
		root = Tk()
		root.resizable(0, 0)
		root.title("Hack the Planet: Sensel Website Creator")

	if(canvas == None): 
		canvas = Canvas(root, width=1150, height=600)
		canvas.pack()

	render(objects, canvas)
	
	root.mainloop()

def render(objects, canvas):
	print(objects)
	for o in objects.data:
		print str(o.x) + " " + str(o.y) + " " + str(o.radius)
		o.render(canvas)

if __name__ == '__main__':

	objects = Objects()

	t = SenselWorkerThread(objects)
	t.start()

	# Setup the screen
	view_setup()



	

