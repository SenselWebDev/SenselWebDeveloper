
from lib.SenselGestureFramework.sensel_framework_simple import *

class SenselEventLoop(SenselGestureHandler):
	"""docstring for SenselEventLoop"""
	def __init__(self):
		super(SenselEventLoop, self).__init__()

	def gestureEvent(self, gesture):
		if(gesture.state == GestureState.STARTED):
			print("! Started gesture: " + str(gesture) + " @ " + str(time.time()))
		#elif(gesture.state == GestureState.MOVED):
			#print("Gesture moved")
		elif(gesture.state == GestureState.ENDED):
			print("! Gesture ended: " + str(gesture) + " @ " + str(time.time()))

if __name__ == '__main__':
	event_loop = SenselEventLoop()
	event_loop.start()

