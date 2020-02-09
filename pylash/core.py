'''
Provides basic and utility classes and functions.
'''


import sys, threading
from PySide2 import QtGui, QtCore, QtWidgets


__author__ = "Yuehao Wang"
__pdoc__ = {}


class Object(object):
	'''
	Base class of other classes in `pylash`, providing fundamental interfaces for `pylash` objects.
	'''
	
	latestObjectIndex = 0
	'''
	The ID number of the last instantiated `pylash` object. It also represents the number of
	instantiated `pylash` objects. Note: it is .

	Type: `int`, read-only
	'''

	def __init__(self):
		self.objectIndex = Object.latestObjectIndex
		'''
		The unique ID number of the object.

		Type: `int`, read-only
		'''

		self.name = "instance" + str(self.objectIndex)
		'''
		The name of the object. Default: `"instance" + str(self.objectIndex)`.

		Type: `str`
		'''

		Object.latestObjectIndex += 1

	def _nonCopyableAttrs(self):
		return ["objectIndex", "name"]
	
	def copyFrom(self, source):
		'''
		Copies all instance attributes from `source` to self. The `source` should have the same
		type with selves, or be an object instantiated from the parent classes of the self class.

		Parameters
		----------
		source : pylash.core.Object
			The source object to be copied from.
		
		'''

		if not source or not isinstance(self, source.__class__):
			raise TypeError("Object.copyFrom(source): cannot copy from the parameter 'source'.")
		
		noncopyable = self._nonCopyableAttrs()
		attrs = source.__dict__
		for attr_name in attrs:
			if attr_name in noncopyable:
				continue
			
			setattr(self, attr_name, attrs[attr_name])


__pdoc__["CanvasWidget.staticMetaObject"] = False

class CanvasWidget(QtWidgets.QWidget):
	'''
	A `QWidget` object which presents the main window, propagates window events, performs
	rendering, etc. In most cases, it is not necessary to use this class.
	'''
	
	def __init__(self):
		super(CanvasWidget, self).__init__()

		self.setMouseTracking(True)
		self.setFocusPolicy(QtCore.Qt.ClickFocus)

	def paintEvent(self, event):
		'''
		Override [QWidget.paintEvent](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QWidget.paintEvent).
		'''
		
		stage._onShow()

	def mousePressEvent(self, event):
		'''
		Override [QWidget.mousePressEvent](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QWidget.mousePressEvent).
		'''
		self.__enterMouseEvent(event, "mouse_down")

	def mouseMoveEvent(self, event):
		'''
		Override [QWidget.mouseMoveEvent](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QWidget.mouseMoveEvent).
		'''
		stage._useHandCursor = False

		self.__enterMouseEvent(event, "mouse_move")

		if stage._useHandCursor:
			self.setCursor(QtCore.Qt.PointingHandCursor)
		else:
			self.setCursor(QtCore.Qt.ArrowCursor)

	def mouseReleaseEvent(self, event):
		'''
		Override [QWidget.mouseReleaseEvent](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QWidget.mouseReleaseEvent).
		'''
		self.__enterMouseEvent(event, "mouse_up")

	def mouseDoubleClickEvent(self, event):
		'''
		Override [QWidget.mouseDoubleClickEvent](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QWidget.mouseDoubleClickEvent).
		'''
		self.__enterMouseEvent(event, "mouse_dbclick")

	def keyPressEvent(self, event):
		'''
		Override [QWidget.keyPressEvent](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QWidget.keyPressEvent).
		'''
		if not event.isAutoRepeat():
			self.__enterKeyboardEvent(event, "key_down")

	def keyReleaseEvent(self, event):
		'''
		Override [QWidget.keyReleaseEvent](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QWidget.keyReleaseEvent).
		'''
		if not event.isAutoRepeat():
			self.__enterKeyboardEvent(event, "key_up")

	def __enterKeyboardEvent(self, event, eventType):
		from .events import Event

		s = stage

		if not s:
			return

		for o in s._keyboardEventList:
			if o["eventType"] == eventType:
				eve = Event(eventType)
				eve.keyCode = event.key()
				eve.keyText = event.text()

				o["listener"](eve)

	def __enterMouseEvent(self, event, eventType):
		e = {"offsetX" : event.x(), "offsetY" : event.y(), "eventType" : eventType, "target" : None}

		stage._enterMouseEvent(e, {"x" : 0, "y" : 0, "scaleX" : 1, "scaleY" : 1})


class Stage(Object):
	'''
	`pylash.core.Stage` provides interfaces to control and configure global settings and operations
	regarding rendering and events. Intuitively, it is a scene where game objects like
	characters, maps, effects, etc. can be presented.
	
	This class is not expected to be instantiated directly. Instead, it is recommended to
	use the global `stage` object, which is a builtin instance of this class and will be
	configured by `pylash.core.init` and other initialization steps.
	'''

	PARENT = "stage_parent_root"
	'''
	An identifier representing the parent of the `stage` object.

	Type: `str`, read-only
	'''

	def __init__(self):
		super(Stage, self).__init__()
		
		self.parent = Stage.PARENT
		'''
		The parent of `stage` object.

		Type: `str`, read-only
		'''
		self.x = 0
		self.y = 0
		self.scaleX = 1
		self.scaleY = 1
		self.rotation = 0
		self.width = 0
		'''
		The width of the game window.

		Type: `int`, read-only
		'''
		self.height = 0
		'''
		The height of the game window.

		Type: `int`, read-only
		'''
		self.speed = 0
		'''
		The repainting rate of the game window. Unit: millisecond.

		Type: `float`, read-only
		'''
		self.app = None
		'''
		The repainting rate of the game window.

		Type: `QApplication`, read-only
		'''
		self.canvasWidget = None
		'''
		The game window widget.

		Type: `pylash.core.CanvasWidget`, read-only
		'''
		self.canvas = None
		'''
		The game window painter.

		Type: `QPainter`, read-only
		'''
		self.timer = None
		'''
		The window repainting timer.

		Type: `QTimer`, read-only
		'''
		self.childList = []
		'''
		The window repainting timer.

		Type: `list` of `pylash.display.DisplayObject`, read-only
		'''
		self.backgroundColor = None
		'''
		The background color of the game window. Default: `None` (no background)

		Type: `str`, `pylash.display.GradientColor`
		'''
		self.useAntialiasing = True
		'''
		Disable/enable antialiasing.

		Type: `bool`
		'''
		self._useHandCursor = False
		self._keyboardEventList = []
	
	def copyFrom(self, source):
		raise Exception("Stage objects cannot be copied from others.")

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
		self.timer.start()

		self.timer.timeout.connect(self.canvasWidget.update)
		
	def _onShow(self):
		self.canvas.begin(self.canvasWidget)

		if self.useAntialiasing:
			self.canvas.setRenderHint(QtGui.QPainter.Antialiasing, True)
		else:
			self.canvas.setRenderHint(QtGui.QPainter.Antialiasing, False)

		if self.backgroundColor is not None:
			self.canvas.fillRect(0, 0, self.width, self.height, getColor(self.backgroundColor))
		else:
			self.canvas.eraseRect(0, 0, self.width, self.height)

		self._showDisplayList(self.childList)

		self.canvas.end()

	def _showDisplayList(self, childList):
		for o in childList:
			if hasattr(o, "_show") and hasattr(o._show, "__call__"):
				o._show(self.canvas)

	def _enterMouseEvent(self, event, cd):
		childList = self.childList[:: -1]

		currentCd = {"x" : cd["x"], "y" : cd["y"], "scaleX" : cd["scaleX"], "scaleY" : cd["scaleY"]}

		for o in childList:
			if hasattr(o, "_enterMouseEvent") and hasattr(o._enterMouseEvent, "__call__") and o._enterMouseEvent(event, currentCd, o._mouseIsOn):
				break

	def setFrameRate(self, speed):
		'''
		Sets the repainting rate of the game. Unit: millisecond.

		Parameters
		----------
		speed : float
			The repainting rate.

		See Also
		--------
		pylash.core.Stage.speed
		'''

		if not self.timer:
			return

		self.speed = speed
		self.timer.setInterval(speed)

	def addChild(self, child):
		'''
		Appends `child` to the `stage`'s display list, then the `child` object will be rendered
		on the game window.

		Parameters
		----------
		child : pylash.display.DisplayObject
			The display object to be added to the stage.
		'''

		if child is not None:
			child.parent = self
			
			self.childList.append(child)
		else:
			raise TypeError("Stage.addChild(child): parameter 'child' must be a display object.")

	def removeChild(self, child):
		'''
		Removes `child` from the `stage`'s display list, then the `child` object will NOT be
		rendered on the game window.

		Parameters
		----------
		child : pylash.display.DisplayObject
			The display object to be removed from the stage.
		'''

		if child is not None:
			self.childList.remove(child)
			
			child.die()
		else:
			raise TypeError("Stage.removeChild(child): parameter 'child' must be a display object.")

	def addEventListener(self, e, listener):
		'''
		Adds an event listener to the `stage` object.

		Parameters
		----------
		e : str or pylash.events.Event
			The event type.
		listener : function
			The listener, i.e. a function invoked when the event is dispatched.
		'''

		from .events import Event

		e = Event(e)
		if hasattr(e, "eventType"):
			if e.eventType == "key_down" or e.eventType == "key_up":
				self._keyboardEventList.append({
					"eventType" : e.eventType,
					"listener" : listener
				})

	def removeEventListener(self, e, listener = None):
		'''
		Removes event listener(s) from the `stage` object. If the `listener` is ignored, all
		event listeners with event type `e` will be removed.

		Parameters
		----------
		e : str or pylash.events.Event
			The event type.
		listener : function, optional
			The listener.
		'''

		from .events import Event
		
		e = Event(e)
		if hasattr(e, "eventType"):
			if e.eventType == "key_down" or e.eventType == "key_up":
				for i, o in enumerate(self._keyboardEventList):
					if o["eventType"] == e.eventType and (listener == None or o["listener"] == listener):
						self._keyboardEventList.pop(i)

stage = Stage()


class KeyCode(object):
	'''
	An enumeration of available key codes. Each class attribute stands for a key code.
	For more detailed meaning of each attribute, please refer to [the related documentation
	of PySide2](https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html#PySide2.QtCore.PySide2.QtCore.Qt.Key).

	Example
	-------
	```
	def keyDown(e):
		if e.keyCode == KeyCode.KEY_RIGHT:
			print("press RIGHT")
		elif e.keyCode == KeyCode.KEY_LEFT:
			print("press LEFT")

	stage.addEventListener(KeyboardEvent.KEY_DOWN, keyDown)
	```

	See Also
	--------
	pylash.core.Stage.addEventListener
	pylash.core.Stage.removeEventListener
	pylash.events.KeyboardEvent
	'''

	def __init__(self):
		Exception("KeyCode cannot be instantiated.")

for o in dir(QtCore.Qt):
	if o.find("Key_") == 0:
		value = getattr(QtCore.Qt, o)
		propertyName = o.upper()

		setattr(KeyCode, propertyName, value)


class UnityOfDictAndClass(object):
	'''
	A static class providing interfaces of unified getting/setting operations on key-value pairs of
	`dict` objects and attributes of other instances.
	'''

	def __init__(self):
		Exception("UnityOfDictAndClass cannot be instantiated.")
	
	@staticmethod
	def set(obj, key, value):
		'''
		If `obj` is a `dict`, `obj[key] = value`. Otherwise, `setattr(obj, key, value)`.

		Parameters
		----------
		obj : dict or object
			The target to set a value.
		key : str
			A `dict` key or an attribute name.
		value : any
			The value that the attribute or key-value pair to store.
		'''

		if isinstance(obj, dict):
			obj[key] = value
		else:
			setattr(obj, key, value)

	@staticmethod
	def get(obj, key):
		'''
		If `obj` is a `dict`, returns `obj[key]`. Otherwise, returns `getattr(obj, key)`. If the `key`
		is not a key or is an undefined attribute in `obj`, returns `None`.

		Parameters
		----------
		obj : dict or object
			The target to retrieve values.
		key : str
			A `dict` key or an attribute name.

		Returns
		-------
		any
			The value that the attribute or key-value pair stores.
		'''

		value = None

		if isinstance(obj, dict):
			if key in obj:
				value = obj[key]
		else:
			if hasattr(obj, key):
				value = getattr(obj, key)

		return value

	@staticmethod
	def has(obj, key):
		'''
		Returns `True` if the `key` is a key or a defined attribute in `obj`. Otherwise, returns `False`.
		
		Parameters
		----------
		obj : dict or object
			The target to check existence of a key-value pair or an attribute.
		key : str
			A `dict` key or an attribute name.

		Returns
		-------
		bool
			Existence of a key-value pair or an attribute.
		'''

		if isinstance(obj, dict):
			return (key in obj)
		else:
			return hasattr(obj, key)


def init(speed, title, width, height, callback):
	'''
	The initialization function of `pylash`. This function will create a game window, set its
	size to \\(width \\times height\\) and window title to `title`. The game window will repaint
	per `speed` milliseconds. After the setup of the game window, `callback` will be
	invoked, which is the entrance function of your game.

	Parameters
	----------
	speed : float
		The window repainting rate. Generally, it is supposed to be \\(1000 / FPS\\).
	title : str
		The window title.
	width : int
		The window's width.
	height : int
		The window's height.
	callback : funtion
		The callback function invoked after the setup of game window.

	Example
	-------
	```
	def main():
		print("Hello, world!")
	
	init(1000 / 60, "Init Test", 100, 100, main)
	```
	'''

	stage.app = QtWidgets.QApplication(sys.argv)

	stage._setCanvas(speed, title, width, height)

	if not hasattr(callback, "__call__"):
		raise TypeError("init(speed, title, width, height, callback): parameter 'callback' must be a function.")

	callback()

	sys.exit(stage.app.exec_())


def addChild(child):
	'''
	Identical to `stage.addChild`.

	Parameters
	----------
	child : pylash.display.DisplayObject
		The display object to be appended to the root display list.

	See Also
	--------
	Stage.addChild
	'''

	stage.addChild(child)


def removeChild(child):
	'''
	Identical to `stage.removeChild`.

	Parameters
	----------
	child : pylash.display.DisplayObject
		The display object to be removed from the root display list.

	See Also
	--------
	Stage.removeChild
	'''

	stage.removeChild(child)


__pdoc__["getColor"] = False

def getColor(color):
	if isinstance(color, QtGui.QColor) or isinstance(color, QtGui.QGradient):
		return color
	elif hasattr(color, "addColorStop"):
		return color.value
	elif not color:
		return QtCore.Qt.transparent
	else:
		if isinstance(color, int):
			color = hex(color)
			
		if color[0 : 2].lower() == "0x":
			color = "#" + color[2 ::]

		colorObj = QtGui.QColor()
		colorObj.setNamedColor(color)

		return colorObj


__pdoc__["removeItemsInList"] = False

def removeItemsInList(theList, condition):
	if not hasattr(condition, "__call__") or not isinstance(theList, list):
		return

	targetList = []

	for o in theList:
		if condition(o):
			targetList.append(o)

	for i in targetList:
		theList.remove(i)

	return targetList
