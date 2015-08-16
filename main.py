
from lib.SenselGestureFramework.sensel_framework_simple import *
from Tkinter import *
import threading
# from pymitter import EventEmitter

RENDER_DELAY = 1

class Objects(object):
	"""Objects that will need to be rendered"""
	def __init__(self):
		self.data = []
		self.cursor = None

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
		#print("Circle!")
		# emitter.emit('circle')
		canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill="darkgrey", outline="darkgrey")
		

class SenselEventLoop(SenselGestureHandler):
	"""docstring for SenselEventLoop"""
	def __init__(self, arg):
		super(SenselEventLoop, self).__init__(arg)

	def gestureEvent(self, gesture, arg):
		if(gesture.weight_class == WeightClass.LIGHT):
			# Draw the cursor
			print("Would draw cursor")
			last_location = gesture.tracked_locations[len(gesture.tracked_locations) - 1]
			arg.cursor = Circle(last_location[0], last_location[1], 5)
			# Emit event to re-render 
			#render(arg[0], arg[1])

class SenselWorkerThread(threading.Thread):
	"""docstring for SenselWorkerThread"""
	def __init__(self, arg):
		# Pass a reference to the objects up as the arg
		super(SenselWorkerThread, self).__init__()
		self.event_loop = SenselEventLoop(arg)

	def run(self):
		self.event_loop.start()
		
class App(object):
	"""docstring for App"""
	def __init__(self, objects):
		super(App, self).__init__()

		self.root = Tk()
		self.root.resizable(0, 0)
		self.root.title("Hack the Planet: Sensel Website Creator")

		self.canvas = Canvas(self.root, width=1150, height=600)
		self.canvas.pack()

		self.objects = objects
		
		self.canvas.after(RENDER_DELAY, self.render)

	def render(self):

		self.canvas.delete("all")

		#print(self.objects.data)
		for o in self.objects.data:
			o.render(self.canvas)

		# Draw the cursor
		if(self.objects.cursor):
			print str(self.objects.cursor.x) + " " + str(self.objects.cursor.y) + " " + str(self.objects.cursor.radius)
			self.objects.cursor.render(self.canvas)

		self.canvas.after(RENDER_DELAY, self.render)

if __name__ == '__main__':

	objects = Objects()

	t = SenselWorkerThread(objects)
	t.start()

	# Setup the screen
	app = App(objects)

	app.root.mainloop()





	

