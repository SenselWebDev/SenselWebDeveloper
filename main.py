
from lib.SenselGestureFramework.sensel_framework_simple import *
from Tkinter import *
from wheel_menu_framework import *
import threading
# from pymitter import EventEmitter

RENDER_DELAY = 1

SCREEN_WIDTH = 1150
SCREEN_HEIGHT = 600

NUM_COLUMNS = 16
CELL_DIMN = SCREEN_WIDTH/NUM_COLUMNS
GRID_COLOR = "grey"
GRID_WIDTH = 1.5
GRID_PADDING = 0

def snapPoint((x, y)):

	return (x, y)

def getDegreesFromDirection(direction):
	angle = None
	if(direction == Direction.RIGHT):
		angle = 0
	elif(direction == Direction.UP):
		angle = 90
	elif(direction == Direction.LEFT):
		angle = 180
	else:
		angle = 270
	return angle

class Objects(object):
	"""Objects that will need to be rendered"""
	def __init__(self):
		self.data = []
		self.ui_data = []
		self.cursors = []
		self.avg_location = None
		self.actionText = ""
		#self.grid_ids = []
		self.context_menu = None
		self.bestdirection = None
		self.grid_visible = False
		self.boxselection = [None, None]

	def addObject(self, obj):
		self.data.append(obj)

	def undo(self):
		# pop the previous object, save to temp storage and re-render
		print("UNIMPLEMENTED")

	def redo(self):
		# If element exists in temp storage, add to object queue and re-render
		print("UNIMPLEMENTED")

class Circle(object):
	"""docstring for Circle"""
	def __init__(self, (x, y), radius = 5, color="darkgrey"):
		super(Circle, self).__init__()
		self.x = x
		self.y = y
		self.color = color
		self.radius = radius

	def render(self, canvas):
		#print("Circle!")
		# emitter.emit('circle')
		canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill=self.color, outline=self.color)
		
class Line(object):
	"""docstring for Circle"""
	def __init__(self, (x, y), (x2, y2), color="#FF0066"):
		super(Line, self).__init__()
		self.x = x
		self.y = y
		self.x2 = x2
		self.y2 = y2
		self.color = color

	def render(self, canvas):
		canvas.create_line(self.x, self.y, self.x2, self.y2, fill=self.color, width=2)
		

class SenselEventLoop(SenselGestureHandler):
	"""docstring for SenselEventLoop"""
	def __init__(self, arg):
		super(SenselEventLoop, self).__init__(arg)

	def gestureEvent(self, gesture, arg):
		#if(gesture.weight_class == WeightClass.LIGHT):
		# Draw the cursor
		arg.cursors = []
		show_cursors = True
		if(gesture.contact_points == 2 and (gesture.weight_class == WeightClass.MEDIUM or gesture.weight_class == WeightClass.HEAVY)):
			#print("possible trigger")
			if(not gesture.state == GestureState.ENDED):
				show_cursors = False
				if(arg.context_menu == None):
					arg.actionText = "MENU"
					avg_curr_location = gesture.tracked_locations[len(gesture.tracked_locations) - 1]
					arg.context_menu = avg_curr_location
					print("Context Menu Triggerred")
			else:
				arg.actionText = ""
				arg.context_menu = None
				arg.grid_visible = True
		if(arg.grid_visible and gesture.contact_points == 1 and (gesture.weight_class == WeightClass.MEDIUM or gesture.weight_class == WeightClass.HEAVY)):
			arg.ui_data = []
			# Check if the first point has not been picked yet
			second_point = gesture.avg_location
			if(arg.boxselection[0] == None):
				# Set anchor at nearest snap point
				anchor_point = snapPoint(gesture.avg_location)
				arg.boxselection[0] = anchor_point
			# Calculate the second snap point
			anchor_point = snapPoint(gesture.avg_location)
			arg.boxselection[1] = anchor_point
			# Draw line to current position from snap point	to user or to final snap
			arg.ui_data.append(Line(arg.boxselection[0], (arg.boxselection[1][0], arg.boxselection[0][1])))
			arg.ui_data.append(Line(arg.boxselection[0], (arg.boxselection[0][0], arg.boxselection[1][1])))
			arg.ui_data.append(Line((arg.boxselection[1][0], arg.boxselection[0][1]), arg.boxselection[1]))
			arg.ui_data.append(Line((arg.boxselection[0][0], arg.boxselection[1][1]), arg.boxselection[1]))
			
			arg.ui_data.append(Circle(arg.boxselection[0], color="#003300"))
			arg.ui_data.append(Circle(second_point, color="#003300"))


		if(len(gesture.xy_contacts) > 0):
			if(show_cursors):
				for c in gesture.xy_contacts:
					arg.cursors.append(Circle(c))
			arg.avg_location = gesture.avg_location
			#print(self.avg_location)
			arg.bestdirection = gesture.bestdirection
		if(gesture.contact_points == 3):
			if(gesture.state == GestureState.ENDED):
				arg.actionText = ""
			else:
				#print(gesture.bestdirection)
				if(gesture.bestdirection == Direction.DOWN):
					arg.undo()
					arg.actionText = "UNDO"
				elif(gesture.bestdirection == Direction.UP):
					arg.redo()
					arg.actionText = "REDO"

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

		self.canvas = Canvas(self.root, width=SCREEN_WIDTH - 20, height=SCREEN_HEIGHT)
		self.canvas.pack()

		self.objects = objects
		
		self.canvas.after(RENDER_DELAY, self.render)
		self.actionTextElement = None

		self.wheel = None

	def showGrid(self):
		# Draw Horizontal Lines
		for y in range(-GRID_PADDING, SCREEN_HEIGHT + 2*GRID_PADDING, CELL_DIMN):
			line_id = self.canvas.create_line(0, y, SCREEN_WIDTH, y, fill=GRID_COLOR, width=GRID_WIDTH)
			#self.objects.grid_ids.append(line_id)
		# Draw Vertical Lines
		for x in range(-GRID_PADDING, SCREEN_WIDTH + 2*GRID_PADDING, SCREEN_WIDTH/NUM_COLUMNS):
			line_id = self.canvas.create_line(x, 0, x, SCREEN_HEIGHT, fill=GRID_COLOR, width=GRID_WIDTH)
			#self.objects.grid_ids.append(line_id)

	def hideGrid(self):
		for gridline_id in self.objects.grid_ids:
			self.canvas.delete(gridline_id)

	def render(self):

		self.canvas.delete("all")

		# Render the grid
		if(self.objects.grid_visible):
			self.showGrid()

		# Render created objects
		for o in self.objects.data:
			o.render(self.canvas)

		# Render UI Data
		for o in self.objects.ui_data:
			o.render(self.canvas)

		# Draw the action text
		actionText = self.objects.actionText
		if(not actionText == ""):
			if(not self.actionTextElement == None):
				print(self.actionTextElement.get(1.0,END)[:-1])
			if(self.actionTextElement == None):# or self.actionTextElement.get(1.0,END)[:-1] == actionText):
				
				canvas_id = self.canvas.create_text(35, SCREEN_HEIGHT - 10)
				self.canvas.itemconfig(canvas_id, text=actionText)
				self.canvas.itemconfig(canvas_id, font=("courier", 20))

		# Draw the Context Menu
		cm = self.objects.context_menu
		if(cm):
			if(self.wheel):
				self.wheel.clearWheel(self.canvas)
			self.wheel = WheelMenu(0, 0) 
			self.wheel.changeLoc(cm[0], cm[1])
			self.wheel.drawWheel(self.canvas)
			# If the selection is far enough from the center
			if(self.objects.avg_location):
				dist = euclideanDist(cm, self.objects.avg_location)
				if(dist >= SMALL_WHEEL_SIDE):
					self.wheel.highlightSide(self.canvas, getDegreesFromDirection(self.objects.bestdirection))

		# Draw the cursor
		if(len(self.objects.cursors) > 0):
			#print str(self.objects.cursor.x) + " " + str(self.objects.cursor.y) + " " + str(self.objects.cursor.radius)
			for c in self.objects.cursors:
				c.render(self.canvas)

		self.canvas.after(RENDER_DELAY, self.render)

if __name__ == '__main__':

	objects = Objects()

	t = SenselWorkerThread(objects)
	t.start()

	# Setup the screen
	app = App(objects)

	app.root.mainloop()





	

