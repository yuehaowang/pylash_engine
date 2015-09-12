import sys, threading
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

		for o in s._keyboardEventList:
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
		self.width = 0
		self.height = 0
		self.speed = 0
		self.app = None
		self.canvasWidget = None
		self.canvas = None
		self.timer = None
		self.childList = []
		self.backgroundColor = None
		self._keyboardEventList = []

	def _setCanvas(self, speed, title, width, height):
		self.speed = speed
		self.width = width
		self.height = height

		self.canvas = QtGui.QPainter()

		self.canvasWidget = CanvasWidget()
		self.canvasWidget.setWindowTitle(title)
		self.canvasWidget.setFixedSize(width, height)
		self.canvasWidget.show()

		self.timer = QtCore.QTimer()
		self.timer.setInterval(speed)
		self.timer.start();

		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.canvasWidget, QtCore.SLOT("update()"))

	def _onShow(self):
		self.canvas.begin(self.canvasWidget)

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
		childList = self.childList[:: -1]

		currentCd = {"x" : cd["x"], "y" : cd["y"], "scaleX" : cd["scaleX"], "scaleY" : cd["scaleY"]}

		for o in childList:
			if hasattr(o, "_enterMouseEvent") and hasattr(o._enterMouseEvent, "__call__") and o._enterMouseEvent(event, currentCd):
				break

	def setFrameRate(self, speed):
		if not self.timer:
			return

		self.speed = speed
		self.timer.setInterval(speed)

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
				self._keyboardEventList.append({
					"eventType" : e.eventType,
					"listener" : listener
				})

	def removeEventListener(self, e, listener):
		from .events import KeyboardEvent

		if hasattr(e, "eventType"):
			if e.eventType == KeyboardEvent.KEY_DOWN.eventType or e.eventType == KeyboardEvent.KEY_UP.eventType:
				for i, o in enumerate(self._keyboardEventList):
					if o["eventType"] == e.eventType and o["listener"] == listener:
						self._keyboardEventList.pop(i)

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
	elif not color:
		return QtCore.Qt.transparent
	else:
		colorObj = QtGui.QColor()
		colorObj.setNamedColor(color)

		return colorObj