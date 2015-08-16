
from lib.SenselGestureFramework.sensel_framework_simple import *
from Tkinter import *
from wheel_menu_framework import *
import threading
from math import *
from image_factory import *
import base64
from converthtml import *
# from pymitter import EventEmitter

data_count = 0

RENDER_DELAY = 1

SCREEN_WIDTH = 1150
SCREEN_HEIGHT = 600
NUM_COLUMNS = 16
CELL_DIMN = SCREEN_WIDTH/NUM_COLUMNS
CELL_HEIGHT = SCREEN_WIDTH/NUM_COLUMNS
GRID_COLOR = "grey"
GRID_WIDTH = 1.5
GRID_PADDING = 0

UNDO_DIST = 100 # Distance to move fingers before calling undo/redo methods

GLOBAL_FONT = "lato"

def snapLoc ((x, y)):
	newX = round(x/CELL_DIMN)*CELL_DIMN
	newY = round(y/CELL_DIMN)*CELL_DIMN
	#print("Snapping " + str((x, y)) + " to " + str((newX, newY)))
	return (newX, newY)

def snapToGrid (xloc, yloc):
	gridCol = round(xloc/CELL_DIMN)
	gridRow = round(yloc/CELL_DIMN)
	return (gridRow, gridCol)

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
		self.imageType = None
		#self.grid_ids = []
		self.context_menu = None
		self.bestdirection = None
		self.grid_visible = False
		self.boxselection = [None, None]
		self.redo_stack = []
		self.data_at_start = None
		self.selected_tb = None # The id of the text box listening to keyboard input

	def addObject(self, obj):
		self.data.append(obj)

	def reundo(self, end_obj_count):
		obj_count = len(self.data)
		obj_diff = int(end_obj_count - obj_count)
		#print(obj_diff)
		if(obj_diff < 0):
			# Perform Undos
			for i in range(0, -obj_diff):
				self.undo()
		elif(obj_diff > 0):
			# Perform Redos
			for i in range(0, obj_diff):
				self.redo()

	def undo(self):
		# pop the previous object, save to temp storage and re-render
		if(len(self.data) > 0):
			obj = self.data.pop()
			self.redo_stack.append(obj)
		#print("UNIMPLEMENTED")

	def redo(self):
		# If element exists in temp storage, add to object queue and re-render
		if(len(self.redo_stack) > 0):
			obj = self.redo_stack.pop()
			self.data.append(obj)
		#print("UNIMPLEMENTED")

	def getElements(self):
		elements = []

		for d in self.data:
			elem = d.getElement()
			if(elem):
				elements.append(elem)

		return elements

class Shape(object):
	def __init__(self):
		global data_count
		print(data_count)
		super(Shape, self).__init__()
		self.uid = data_count
		data_count += 1

	def __eq__(self, other):
		if(not other == None):
			return self.uid == other.uid
		return False

	def changeColor (self, newColor):
		self.color = newColor

	def changeFillColor (self, newFillColor):
		self.fillcolor = newFillColor

	def getElement(self):
		return None

class Circle(Shape):
	"""docstring for Circle"""
	def __init__(self, (x, y), radius = 5, color="darkgrey", fillcolor=None):
		super(Circle, self).__init__()
		self.x = x
		self.y = y
		self.color = color
		self.radius = radius
		self.fillcolor = fillcolor if fillcolor else color
		#print(data_count)

	def render(self, canvas):
		#print("Circle!")
		# emitter.emit('circle')
		canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill=self.fillcolor, outline=self.color)
	

class Rectangle(Shape):
	"""docstring for Rectangle"""
	def __init__(self, (x, y), (x2, y2), color="#666", fillcolor=None, width=3.5):
		super(Rectangle, self).__init__()
		self.x = x
		self.y = y
		self.x2 = x2
		self.y2 = y2
		self.color = color
		self.fillcolor = fillcolor if fillcolor else color
		self.width = 3.5

	def render(self, canvas):
		canvas.create_rectangle(self.x, self.y, self.x2, self.y2, fill=self.fillcolor, outline=self.color, width=self.width)
	
	def getElement(self):
		elem = Element("shape" + str(self.uid), "shape", [snapToGrid(self.x, self.y), snapToGrid(self.x2, self.y2)], None, self.fillcolor)
		return elem

class Line(Shape):
	"""docstring for Line"""
	def __init__(self, (x, y), (x2, y2), color="#FF0066"):
		super(Line, self).__init__()
		self.x = x
		self.y = y
		self.x2 = x2
		self.y2 = y2
		self.color = color

	def render(self, canvas):
		canvas.create_line(self.x, self.y, self.x2, self.y2, fill=self.color, width=3.5)
		
class Image(Shape):
	"""docstring for Image"""
	def __init__(self, (x, y), (x2, y2), url):
		super(Image, self).__init__()
		self.x = x
		self.y = y
		self.x2 = x2
		self.y2 = y2
		self.url = url
		print(self.url)
		# Load image
		u = urllib.urlopen(self.url)
		raw_data = u.read()
		u.close()
		b64_data = base64.encodestring(raw_data)
		self.image = PhotoImage(data=b64_data, height=int(self.y2-self.y), width=int(self.x2-self.x))

	def render(self, canvas):
		canvas.create_image(self.x + (self.x2 - self.x)/2, self.y + (self.y2-self.y)/2, image=self.image)

	def getElement(self):
		elem = Element("img" + str(self.uid), "img", [snapToGrid(self.x, self.y), snapToGrid(self.x2, self.y2)], self.url, None)
		return elem

class TextBox(Shape):
	"""docstring for TextBox"""
	def __init__(self, (x, y), (x2, y2), default_text="Start Typing..", submittable=False, textcolor="#444"):
		super(TextBox, self).__init__()
		self.x = x
		self.y = y
		self.x2 = x2
		self.y2 = y2
		self.text = default_text
		self.default_text = default_text
		self.isplaceholder = True
		self.submittable = submittable
		self.textcolor = textcolor

	def addText(self, char):
		self.text += char
		self.isplaceholder = False

	def remText(self):
		self.text = self.text[0:-1]
		if(len(self.text) == 0):
			self.isplaceholder = True
			self.text = default_text

	def render(self, canvas):
		self.id = canvas.create_text((self.x + self.x2)/2, (self.y + self.y2)/2, width=(self.x2-self.x))
		canvas.itemconfig(self.id, text=self.text)
		canvas.itemconfig(self.id, font=(GLOBAL_FONT, 40))
		canvas.itemconfig(self.id, fill=self.textcolor)

	def getElement(self):
		elem = Element("txt" + str(self.uid), "txt", [snapToGrid(self.x, self.y), snapToGrid(self.x2, self.y2)], self.text, self.textcolor)
		return elem

class SenselEventLoop(SenselGestureHandler):
	"""docstring for SenselEventLoop"""
	def __init__(self, arg):
		super(SenselEventLoop, self).__init__(arg)
		self.deployed = False

	def gestureEvent(self, gesture, arg):
		#if(gesture.weight_class == WeightClass.LIGHT):
		# Draw the cursor
		arg.cursors = []
		show_cursors = True

		# Context Menu Trigger
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
				if(gesture.gesture_type == GestureType.PAN):
					arg.grid_visible = True
					arg.imageType = convertDirectionToAction(gesture.bestdirection)

		# Box Drawing Trigger
		if(arg.grid_visible and gesture.contact_points == 1 and (gesture.weight_class == WeightClass.MEDIUM or gesture.weight_class == WeightClass.HEAVY)):
			arg.ui_data = []
			# Check if the first point has not been picked yet
			second_point = gesture.avg_location
			if(arg.boxselection[0] == None):
				# Set anchor at nearest snap point
				anchor_point = snapLoc(gesture.avg_location)
				arg.boxselection[0] = anchor_point
			# Calculate the second snap point
			anchor_point = snapLoc(gesture.avg_location)
			arg.boxselection[1] = anchor_point

			if(gesture.state == GestureState.ENDED):
				# Trigger Individual Action Menu Item events
				if(not arg.boxselection[0][0] == arg.boxselection[1][0] and not arg.boxselection[0][1] == arg.boxselection[1][1]):
					if(arg.imageType == Action.SHAPE):
						# Draw the rectangle at the box selection
						rect = Rectangle(arg.boxselection[0], arg.boxselection[1])
						arg.data.append(rect)

					elif(arg.imageType == Action.TEXT):
						# Begin listening for keyboard input, write it into a label
						tb = TextBox(arg.boxselection[0], arg.boxselection[1])
						arg.data.append(tb)
						arg.selected_tb = tb

					elif(arg.imageType == Action.IMAGE):
						# Similar to text, open a prompt and fetch image and display
						tb = TextBox(arg.boxselection[0], arg.boxselection[1], "Search Images..", True)
						arg.data.append(tb) # Will swap with the image later
						arg.selected_tb = tb

				arg.grid_visible = False # Toggle the grid to hide next time through the render function
				arg.imageType = None
				arg.boxselection = [None, None]
			else:
				arg.ui_data.append(Rectangle(arg.boxselection[0], arg.boxselection[1], fillcolor="white", color="#F00996"))
				
				arg.ui_data.append(Circle(arg.boxselection[0], color="#CAE5FC", radius=8, fillcolor="white"))
				arg.ui_data.append(Circle(arg.boxselection[0], color="#91C1FC"))
				arg.ui_data.append(Circle(arg.boxselection[1], color="#CAE5FC", radius=8, fillcolor="white"))
				arg.ui_data.append(Circle(arg.boxselection[1], color="#91C1FC"))

		# Cursor Trigger
		if(len(gesture.xy_contacts) > 0):
			if(show_cursors):
				for c in gesture.xy_contacts:
					arg.cursors.append(Circle(c))
			arg.avg_location = gesture.avg_location
			#print(self.avg_location)
			arg.bestdirection = gesture.bestdirection

		# Undo/Redo Trigger
		if(gesture.contact_points == 3):
			if(gesture.state == GestureState.ENDED):
				arg.actionText = ""
			else:
				if(gesture.state == GestureState.STARTED or (gesture.state == GestureState.MOVED and arg.data_at_start == None)):
					arg.data_at_start = len(arg.data) if arg.data else 0
				#print(gesture.bestdirection)
				delta_y = gesture.tracked_locations[-1][1] - gesture.down_y
				undo_count = floor(delta_y / UNDO_DIST) 
				if(undo_count < 0):
					# handle flooring for negatives 
					undo_count += 1
				print(str(gesture.state) + " " + str(delta_y) + " " + str(undo_count) + " " + str(UNDO_DIST))
				print("Originally at " + str(arg.data_at_start) + " now at " + str(arg.data_at_start-undo_count))
				arg.reundo(max(arg.data_at_start-undo_count, 0))

		# Deploy Trigger
		if(gesture.contact_points >= 6):
			if(not self.deployed):
				print("DEPLOYING!")
				elements = arg.getElements()
				path = "~/index.html"
				grid_size = 94
				convertHTML(elements, grid_size, path)
				# On completion, push html file to AWS

				self.deployed = True

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

		# Hook up Keyboard
		self.root.bind_all('<Key>', self.keypress)

		self.canvas = Canvas(self.root, width=SCREEN_WIDTH - 20, height=SCREEN_HEIGHT)
		self.canvas.pack()

		self.objects = objects
		
		self.canvas.after(RENDER_DELAY, self.render)
		self.actionTextElement = None

		self.wheel = None

		self.textbox = None

		self.images = getImages()

	def keypress(self, event):
		if event.keysym == 'Escape':
			self.root.destroy()
		print(event.keycode)
		if(self.objects.selected_tb):
			x = event.char
			print("'" + x + "'")
			if(self.objects.selected_tb.isplaceholder):
				self.objects.selected_tb.text = ""
			# If delete key, delete char
			if(event.keycode == 3342463): # Delete or backspace
				self.objects.selected_tb.remText()
			# Check if enter was pressed 
			elif(self.objects.selected_tb.submittable and event.keycode == 2359309):
				# Trigger a submit of the search
				search_term = self.objects.selected_tb.text
				print(search_term)
				results = gif_search(search_term)
				# Find the best result
				# TODO
				# Swap the text input for the gif
				for i in range(0, len(self.objects.data)):
					if(self.objects.data[len(self.objects.data) - i - 1] == self.objects.selected_tb):
						image = Image((self.objects.selected_tb.x, self.objects.selected_tb.y), (self.objects.selected_tb.x2, self.objects.selected_tb.y2), url=results['data'][0]['images']['original']['url'])
						# Swap the text box for the image
						self.objects.data[len(self.objects.data) - i - 1] = image
						self.objects.selected_tb = None
						self.objects.ui_data = []
			# Add this key to the text for the text box
			else:
				self.objects.selected_tb.addText(x)

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

		# Draw the Image
		imageType = self.objects.imageType
		if(imageType and imageType in self.images.keys()):
			self.canvas.create_image(35, SCREEN_HEIGHT - 40, image=self.images[imageType])

		# Draw the action text
		actionText = self.objects.actionText
		if(not actionText == ""):
			if(not self.actionTextElement == None):
				print(self.actionTextElement.get(1.0,END)[:-1])
			if(self.actionTextElement == None):# or self.actionTextElement.get(1.0,END)[:-1] == actionText):
				
				canvas_id = self.canvas.create_text(35, SCREEN_HEIGHT - 10)
				self.canvas.itemconfig(canvas_id, text=actionText)
				self.canvas.itemconfig(canvas_id, font=(GLOBAL_FONT, 20))

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
	



