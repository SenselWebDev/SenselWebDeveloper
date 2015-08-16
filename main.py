
from lib.SenselGestureFramework.sensel_framework_simple import *
from Tkinter import *
import wheel_menu_framework
import threading
# from pymitter import EventEmitter

RENDER_DELAY = 1

SCREEN_WIDTH = 1150
SCREEN_HEIGHT = 600

class Objects(object):
	"""Objects that will need to be rendered"""
	def __init__(self):
		self.data = []
		self.cursors = []
		self.actionText = ""
		self.grid_ids = []
	def addObject(self, obj):
		self.data.append(obj)

	def undo(self):
		print("UNIMPLEMENTED")

	def redo(self):
		print("UNIMPLEMENTED")

class Circle(object):
	"""docstring for Circle"""
	def __init__(self, (x, y), radius = 5):
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
			#last_location = gesture.tracked_locations[len(gesture.tracked_locations) - 1]
			arg.cursors = []
			if(len(gesture.xy_contacts) > 0):
				for c in gesture.xy_contacts:
					arg.cursors.append(Circle(c))
		if(gesture.contact_points == 3):
			if(gesture.state == GestureState.ENDED):
				arg.actionText = ""
			else:
				print(gesture.bestdirection)
				if(gesture.bestdirection == Direction.DOWN):
					arg.undo()
					arg.actionText = "UNDO"
				elif(gesture.bestdirection == Direction.UP):
					arg.redo()
					arg.actionText = "REDO"
		elif(gesture.contact_points == 2 and (gesture.weight_class == WeightClass.MEDIUM or gesture.weight_class == WeightClass.LARGE)):
			print("Context Menu Triggerred")

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

		self.canvas = Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
		self.canvas.pack()

		self.objects = objects
		
		self.canvas.after(RENDER_DELAY, self.render)
		self.actionTextElement = None

	def render(self):

		self.canvas.delete("all")

		#print(self.objects.data)
		for o in self.objects.data:
			o.render(self.canvas)

		# Draw the cursor
		if(len(self.objects.cursors) > 0):
			#print str(self.objects.cursor.x) + " " + str(self.objects.cursor.y) + " " + str(self.objects.cursor.radius)
			for c in self.objects.cursors:
				c.render(self.canvas)

		# Draw the action text
		actionText = self.objects.actionText
		if(not actionText == ""):
			print(actionText + " ")
			if(not self.actionTextElement == None):
				print(self.actionTextElement.get(1.0,END)[:-1])
			if(self.actionTextElement == None):# or self.actionTextElement.get(1.0,END)[:-1] == actionText):
				
				canvas_id = self.canvas.create_text(35, SCREEN_HEIGHT - 10)
				self.canvas.itemconfig(canvas_id, text=actionText)
				self.canvas.itemconfig(canvas_id, font=("courier", 20))

		self.canvas.after(RENDER_DELAY, self.render)

if __name__ == '__main__':

	objects = Objects()

	t = SenselWorkerThread(objects)
	t.start()

	# Setup the screen
	app = App(objects)

	app.root.mainloop()





	

