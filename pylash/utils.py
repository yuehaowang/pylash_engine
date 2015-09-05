import sys
from PyQt4 import QtGui, QtCore


__author__ = "Yuehao Wang"


class Object(object):
	latestObjectIndex = 0

	def __init__(self):
		Object.latestObjectIndex += 1

		self.objectIndex = Object.latestObjectIndex


class CanvasWidget(QtGui.QWidget):
	def __init__(self):
		super(CanvasWidget, self).__init__()

		self.setMouseTracking(True)

	def paintEvent(self, event):
		stage._onShow()

	def mousePressEvent(self, event):
		from .events import MouseEvent
		
		self.__enterMouseEvent(event, MouseEvent.MOUSE_DOWN.eventType)

	def mouseMoveEvent(self, event):
		from .events import MouseEvent

		self.__enterMouseEvent(event, MouseEvent.MOUSE_MOVE.eventType)

	def mouseReleaseEvent(self, event):
		from .events import MouseEvent

		self.__enterMouseEvent(event, MouseEvent.MOUSE_UP.eventType)

	def mouseDoubleClickEvent(self, event):
		from .events import MouseEvent

		self.__enterMouseEvent(event, MouseEvent.DOUBLE_CLICK.eventType)

	def keyPressEvent(self, event):
		if not event.isAutoRepeat():
			from .events import KeyboardEvent
		
			self.__enterKeyboardEvent(event, KeyboardEvent.KEY_DOWN.eventType)

	def keyReleaseEvent(self, event):
		if not event.isAutoRepeat():
			from .events import KeyboardEvent

			self.__enterKeyboardEvent(event, KeyboardEvent.KEY_UP.eventType)

	def __enterKeyboardEvent(self, event, eventType):
		s = stage

		if not s:
			return

		for o in s.keyboardEventList:
			if o["eventType"] == eventType:
				from .events import Event

				eve = Event(eventType)
				eve.keyCode = event.key()
				eve.keyText = event.text()

				o["listener"](eve)

	def __enterMouseEvent(self, event, eventType):
		e = {"offsetX" : event.x(), "offsetY" : event.y(), "eventType" : eventType, "target" : None}

		stage._enterMouseEvent(e, {"x" : 0, "y" : 0, "scaleX" : 1, "scaleY" : 1})


class Stage(Object):
	def __init__(self):
		super(Stage, self).__init__()
		
		self.parent = "root"
		self.keyboardEventList = []
		self.width = 0
		self.height = 0
		self.speed = 0
		self.app = None
		self.canvasObj = None
		self.canvas = None
		self.frameRate = None
		self.childList = []
		self.backgroundColor = None

	def _setCanvas(self, speed, title, width, height):
		self.canvas = QtGui.QPainter()

		self.canvasObj = CanvasWidget()
		self.canvasObj.setWindowTitle(title)
		self.canvasObj.setFixedSize(width, height)
		self.canvasObj.show()

		self.frameRate = QtCore.QTimer()
		self.frameRate.setInterval(speed)
		self.frameRate.start();

		QtCore.QObject.connect(self.frameRate, QtCore.SIGNAL("timeout()"), self.canvasObj, QtCore.SLOT("update()"))

	def _onShow(self):
		self.canvas.begin(self.canvasObj)

		if self.backgroundColor is not None:
			self.canvas.fillRect(0, 0, self.width, self.height, getColor(self.backgroundColor))
		else:
			self.canvas.eraseRect(0, 0, self.width, self.height)

		self._showDisplayList(self.childList)

		self.canvas.end();

	def _showDisplayList(self, childList):
		for o in childList:
			if hasattr(o, "_show") and hasattr(o._show, "__call__"):
				o._show(self.canvas)

	def _enterMouseEvent(self, event, cd):
		childList = list(self.childList)
		childList.reverse()

		currentCd = {"x" : cd["x"], "y" : cd["y"], "scaleX" : cd["scaleX"], "scaleY" : cd["scaleY"]}

		for o in childList:
			if hasattr(o, "_enterMouseEvent") and hasattr(o._enterMouseEvent, "__call__") and o._enterMouseEvent(event, currentCd):
				break

	def addChild(self, child):
		if child is not None:
			child.parent = self
			
			self.childList.append(child)
		else:
			raise ValueError("parameter 'child' must be a display object.")

	def removeChild(self, child):
		if child is not None:
			self.childList.remove(child)
			
			child.parent = None
		else:
			raise ValueError("parameter 'child' must be a display object.")

	def addEventListener(self, e, listener):
		from .events import KeyboardEvent

		if hasattr(e, "eventType"):
			if e.eventType == KeyboardEvent.KEY_DOWN.eventType or e.eventType == KeyboardEvent.KEY_UP.eventType:
				self.keyboardEventList.append({
					"eventType" : e.eventType,
					"listener" : listener
				})

	def removeEventListener(self, e, listener):
		from .events import KeyboardEvent

		if hasattr(e, "eventType"):
			if e.eventType == KeyboardEvent.KEY_DOWN.eventType or e.eventType == KeyboardEvent.KEY_UP.eventType:
				for i, o in enumerate(self.keyboardEventList):
					if o["eventType"] == e.eventType and o["listener"] == listener:
						self.keyboardEventList.pop(i)

stage = Stage()


class KeyCode(Object):
	def __init__(self):
		Exception("KeyCode cannot be instantiated.")

for o in dir(QtCore.Qt):
	if o.find("Key_") == 0:
		value = getattr(QtCore.Qt, o)
		propertyName = o.upper()

		setattr(KeyCode, propertyName, value)


def init(speed, title, width, height, callback):
	stage.speed = speed
	stage.width = width
	stage.height = height

	stage.app = QtGui.QApplication(sys.argv)

	stage._setCanvas(speed, title, width, height)

	if not hasattr(callback, "__call__"):
		raise ValueError("parameter 'callback' must be a function.")

	callback()

	stage.app.exec_()


def addChild(child):
	stage.addChild(child)


def removeChild(child):
	stage.removeChild(child)

	
def getColor(color):
	if isinstance(color, QtGui.QColor):
		return color
	elif color == "" or color is None:
		return QtCore.Qt.transparent
	else:
		colorObj = QtGui.QColor()
		colorObj.setNamedColor(color)

		return colorObj