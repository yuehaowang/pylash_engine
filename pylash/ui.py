from PySide2 import QtGui, QtWidgets
from .core import Object, stage, removeItemsInList, getColor
from .display import Sprite, DisplayObject, RadialGradientColor, LinearGradientColor, Graphics, TextField, TextFormatWeight
from .events import Event, MouseEvent, EventDispatcher, LoopEvent


__author__ = "Yuehao Wang"


class ButtonState(object):
	ENABLED = "enabled_state"
	NORMAL = "normal_state"
	OVER = "over_state"
	DOWN = "down_state"
	DISABLED = "disabled_state"

	def __init__(self):
		raise Exception("ButtonState cannot be instantiated.")


class Button(Sprite):
	def __init__(self, normalState = Sprite(), overState = None, downState = None, disabledState = None):
		super(Button, self).__init__()

		self.__stateList = []

		self.addState(ButtonState.NORMAL, normalState)
		self.addState(ButtonState.OVER, overState)
		self.addState(ButtonState.DOWN, downState)
		self.addState(ButtonState.DISABLED, disabledState)

		self.__preMouseEnabled = self.mouseEnabled
		self.__preUseHandCursor = True
		self.state = ButtonState.NORMAL
		self.useHandCursor = True

		self.addEventListener(MouseEvent.MOUSE_OVER, self.__onMouseOver)
		self.addEventListener(MouseEvent.MOUSE_DOWN, self.__onMouseDown)
		self.addEventListener(MouseEvent.MOUSE_OUT, self.__onMouseOutOrUp)
		self.addEventListener(MouseEvent.MOUSE_UP, self.__onMouseOutOrUp)

	@property
	def state(self):
		return self.__state

	@state.setter
	def state(self, value):
		if value == ButtonState.DISABLED:
			if not self.__state == ButtonState.DISABLED:
				self.__preMouseEnabled = self.mouseEnabled
				self.__preUseHandCursor = self.useHandCursor

			self.mouseEnabled = False
			self.useHandCursor = False
		else:
			self.mouseEnabled = self.__preMouseEnabled
			self.useHandCursor = self.__preUseHandCursor

		self.__state = value

		if value == ButtonState.ENABLED:
			value = ButtonState.NORMAL

		for o in self.__stateList:
			obj = o["displayObject"]

			if isinstance(o, dict) and isinstance(obj, DisplayObject):
				if o["state"] == value:
					obj.visible = True
				else:
					obj.visible = False

	def __onMouseDown(self, e):
		if not self.getDisplayObject(ButtonState.DOWN):
			return

		self.state = ButtonState.DOWN

	def __onMouseOver(self, e):
		if not self.getDisplayObject(ButtonState.OVER):
			return

		self.state = ButtonState.OVER

	def __onMouseOutOrUp(self, e):
		self.state = ButtonState.NORMAL

	def addState(self, state, displayObject):
		if not isinstance(displayObject, DisplayObject):
			return

		self.__stateList.append({
			"state" : state,
			"displayObject" : displayObject
		})

		displayObject.visible = False
		self.addChild(displayObject)

	def removeState(self, state, displayObject):
		def condition(o):
			obj = o["displayObject"]

			return (isinstance(o, dict) and isinstance(obj, DisplayObject) and o["state"] == state and obj.objectIndex == displayObject.objectIndex)

		targetList = removeItemsInList(self.__stateList, condition)

		for o in targetList:
			if isinstance(o["displayObject"], DisplayObject):
				o["displayObject"].remove()

	def getDisplayObject(self, state):
		stateList = self.__stateList

		for o in stateList:
			if state == o["state"]:
				return o["displayObject"]

		return None


class LoadingSample(Sprite):
	def __init__(self, background):
		super(LoadingSample, self).__init__()

		if not isinstance(background, DisplayObject):
			background = Sprite()

		self.background = background
		self.addChild(self.background)

		self.progressBar = Sprite()
		self.addChild(self.progressBar)

	def setProgress(self, value):
		pass


class LoadingSample1(LoadingSample):
	def __init__(self, **opt):
		bg = None

		if "background" in opt:
			bg = opt["background"]

		super(LoadingSample1, self).__init__(bg)
		
		if not "background" in opt:
			self.background.graphics.beginFill("black")
			self.background.graphics.drawRect(0, 0, stage.width, stage.height)
			self.background.graphics.endFill()

		if not "vacantColor" in opt:
			opt["vacantColor"] = "white"

		if not "numberWidth" in opt:
			opt["numberWidth"] = stage.width * 0.1

		if not "numberHeight" in opt:
			opt["numberHeight"] = opt["numberWidth"] / 0.6

		self.__blockWidth = opt["numberWidth"] / 3
		self.__blockHeight = opt["numberHeight"] / 5
		self.progressBarWidth = self.__blockHeight * 7.5
		self.progressBarTotalHeight = self.__blockHeight * 5

		if not "progressColor" in opt:
			opt["progressColor"] = RadialGradientColor(self.__blockWidth * 7.5, self.__blockHeight * 2.5, self.__blockWidth * 7.5)
			opt["progressColor"].addColorStop(0, "red")
			opt["progressColor"].addColorStop(0.3, "orange")
			opt["progressColor"].addColorStop(0.4, "yellow")
			opt["progressColor"].addColorStop(0.5, "green")
			opt["progressColor"].addColorStop(0.8, "blue")
			opt["progressColor"].addColorStop(1, "violet")

		self.progressColor = opt["progressColor"]
		self.vacantColor = opt["vacantColor"]

		self.progressBar.mask = Graphics()

		self.__numberList = [
			[
				[1, 1, 1],
				[1, 0, 1],
				[1, 0, 1],
				[1, 0, 1],
				[1, 1, 1]
			],
			[
				[1, 1, 0],
				[0, 1, 0],
				[0, 1, 0],
				[0, 1, 0],
				[1, 1, 1]
			],
			[
				[1, 1, 1],
				[0, 0, 1],
				[1, 1, 1],
				[1, 0, 0],
				[1, 1, 1]
			],
			[
				[1, 1, 1],
				[0, 0, 1],
				[1, 1, 1],
				[0, 0, 1],
				[1, 1, 1]
			],
			[
				[1, 0, 1],
				[1, 0, 1],
				[1, 1, 1],
				[0, 0, 1],
				[0, 0, 1]
			],
			[
				[1, 1, 1],
				[1, 0, 0],
				[1, 1, 1],
				[0, 0, 1],
				[1, 1, 1]
			],
			[
				[1, 1, 1],
				[1, 0, 0],
				[1, 1, 1],
				[1, 0, 1],
				[1, 1, 1]
			],
			[
				[1, 1, 1],
				[0, 0, 1],
				[0, 0, 1],
				[0, 0, 1],
				[0, 0, 1]
			],
			[
				[1, 1, 1],
				[1, 0, 1],
				[1, 1, 1],
				[1, 0, 1],
				[1, 1, 1]
			],
			[
				[1, 1, 1],
				[1, 0, 1],
				[1, 1, 1],
				[0, 0, 1],
				[1, 1, 1]
			]
		]

	def setProgress(self, value):
		ratio = value / 100
		totalHeight = self.progressBarTotalHeight
		right = 0
		startY = totalHeight * (1 - ratio)
		mask = self.progressBar.mask
		blockW = self.__blockWidth
		blockH = self.__blockHeight

		mask.clear()

		for i in str(round(value)):
			numArray = self.__numberList[int(i)]

			for y, row in enumerate(numArray):
				for x, elem in enumerate(row):
					if elem == 1:
						mask.beginFill()
						mask.drawRect(right + x * blockW, y * self.__blockHeight, blockW, self.__blockHeight)
						mask.endFill()

			right += blockW * 4

		mask.beginFill()
		mask.drawCircle(right + blockW / 2, blockW / 2, blockW / 2)
		right += blockW
		mask.moveTo(right + blockW, 0)
		mask.lineTo(right + blockW * 2, 0)
		mask.lineTo(right, blockH * 5)
		mask.lineTo(right - blockW, blockH * 5)
		right += blockW
		mask.drawCircle(right + blockW / 2, totalHeight - blockW / 2, blockW / 2)
		right += blockW
		mask.endFill()

		self.progressBar.graphics.clear()

		self.progressBar.graphics.beginFill(self.vacantColor)
		self.progressBar.graphics.drawRect(0, 0, right, totalHeight)
		self.progressBar.graphics.endFill()

		self.progressBar.graphics.beginFill(self.progressColor)
		self.progressBar.graphics.drawRect(0, startY, right, totalHeight - startY)
		self.progressBar.graphics.endFill()

		self.progressBar.x = (stage.width - right) / 2
		self.progressBar.y = (stage.height - totalHeight) / 2


class LoadingSample2(LoadingSample):
	def __init__(self, **opt):
		bg = None

		if "background" in opt:
			bg = opt["background"]

		super(LoadingSample2, self).__init__(bg)
		
		if not "background" in opt:
			self.background.graphics.beginFill("black")
			self.background.graphics.drawRect(0, 0, stage.width, stage.height)
			self.background.graphics.endFill()

		if not "fontSize" in opt:
			opt["fontSize"] = stage.height * 0.2

		if not "vacantColor" in opt:
			opt["vacantColor"] = "white"

		txt = TextField()
		txt.size = opt["fontSize"]
		txt.text = "Loading..."
		txt.textColor = opt["vacantColor"]
		txt.weight = TextFormatWeight.BOLD
		txt.x = (stage.width - txt.width) / 2
		txt.y = (stage.height - txt.height) / 2 + 30
		self.progressBar.addChild(txt)

		self.progressBarTotalWidth = txt.width
		self.progressBarHeight = txt.height

		if not "progressColor" in opt:
			opt["progressColor"] = RadialGradientColor(txt.width / 2, txt.height / 2, txt.width / 2)
			opt["progressColor"].addColorStop(0, "red")
			opt["progressColor"].addColorStop(0.3, "orange")
			opt["progressColor"].addColorStop(0.4, "yellow")
			opt["progressColor"].addColorStop(0.5, "green")
			opt["progressColor"].addColorStop(0.8, "blue")
			opt["progressColor"].addColorStop(1, "violet")

		self.progressColor = opt["progressColor"]

		self.__coverTxt = TextField()
		self.__coverTxt.x = txt.x
		self.__coverTxt.y = txt.y
		self.__coverTxt.weight = txt.weight
		self.__coverTxt.size = opt["fontSize"]
		self.__coverTxt.text = txt.text
		self.__coverTxt.textColor = opt["progressColor"]
		self.__coverTxt.mask = Graphics()
		self.progressBar.addChild(self.__coverTxt)

		self.__coverTxt.mask.beginFill()
		self.__coverTxt.mask.drawRect(0, 0, 0, 0)
		self.__coverTxt.mask.endFill()

		self.label = TextField()
		self.label.text = "0%"
		self.label.textColor = "blue"
		self.label.size = 40
		self.label.x = (stage.width - self.label.width) / 2
		self.label.y = (stage.height - self.label.height) / 2 - 60
		self.addChild(self.label)
	
	def setProgress(self, value):
		ratio = value / 100
		totalWidth = self.progressBarTotalWidth

		self.label.text = "%s%%" % round(value)
		self.label.x = (stage.width - self.label.width) / 2

		self.__coverTxt.mask.clear()
		self.__coverTxt.mask.beginFill()
		self.__coverTxt.mask.drawRect(0, 0, totalWidth * ratio, self.progressBarHeight)
		self.__coverTxt.mask.endFill()
		

class LoadingSample3(LoadingSample):
	def __init__(self, **opt):
		bg = None

		if "background" in opt:
			bg = opt["background"]

		super(LoadingSample3, self).__init__(bg)

		if not "background" in opt:
			self.background.graphics.beginFill("#CCCCCC")
			self.background.graphics.drawRect(0, 0, stage.width, stage.height)
			self.background.graphics.endFill()

		if not "progressColor" in opt:
			opt["progressColor"] = "#00A2E8"

		if not "borderColor" in opt:
			opt["borderColor"] = "gray"

		self.progressColor = opt["progressColor"]
		self.progressBarTotalWidth = stage.width * 0.6
		self.progressBarHeight = 20

		self.progressBar.graphics.beginFill()
		self.progressBar.graphics.lineStyle(3, opt["borderColor"])
		self.progressBar.graphics.drawRoundRect(0, 0, self.progressBarTotalWidth, self.progressBarHeight, 10)
		self.progressBar.graphics.endFill()

		self.progressBar.x = (stage.width - self.progressBar.width) / 2
		self.progressBar.y = (stage.height - self.progressBar.height) / 2 + 20

		self.__contentLayer = Sprite()
		self.progressBar.addChild(self.__contentLayer)

		self.label = TextField()
		self.label.text = "Loading... 0%"
		self.label.textColor = "#555555"
		self.label.size = 30
		self.label.weight = TextFormatWeight.BOLD
		self.label.x = (stage.width - self.label.width) / 2
		self.label.y = (stage.height - self.label.height) / 2 - 40
		self.addChild(self.label)

		if not "background" in opt:
			self.background.graphics.beginFill("#DEDEDE")
			self.background.graphics.drawRoundRect(self.progressBar.x - 60, self.label.y - 100, self.progressBar.width + 120, 300, 10)
			self.background.graphics.endFill()

	def setProgress(self, value):
		ratio = value / 100
		totalWidth = self.progressBarTotalWidth

		self.label.text = "Loading... %s%%" % round(value)
		self.label.x = (stage.width - self.label.width) / 2

		self.__contentLayer.graphics.clear()
		self.__contentLayer.graphics.beginFill(self.progressColor)
		self.__contentLayer.graphics.drawRoundRect(3, 3, totalWidth * ratio - 6, self.progressBarHeight - 6, 10, 7)
		self.__contentLayer.graphics.endFill()


class ButtonSample(Button):
	def __init__(self, **kw):
		roundBorder = True
		backgroundColor = {"normalState" : "#DDDDDD", "overState" : "#E3E3E3"}
		lineColor = "#CCCCCC"

		if "roundBorder" in kw:
			roundBorder = kw["roundBorder"]

		if "backgroundColor" in kw:
			backgroundColor = kw["backgroundColor"]

			if not "normalState" in backgroundColor:
				backgroundColor["normalState"] = "#DDDDDD"

			if not "overState" in backgroundColor:
				backgroundColor["overState"] = "#E3E3E3"

		if "lineColor" in kw:
			lineColor = kw["lineColor"]

		txt = TextField()

		if "text" in kw:
			txt.text = kw["text"]

		if "textColor" in kw:
			txt.textColor = kw["textColor"]

		if "font" in kw:
			txt.font = kw["font"]

		if "size" in kw:
			txt.size = kw["size"]

		if "weight" in kw:
			txt.weight = kw["weight"]

		btnWidth = txt.width * 1.2
		btnHeight = txt.height * 1.2

		normalState = Sprite()
		normalState.graphics.beginFill(backgroundColor["normalState"])
		normalState.graphics.lineStyle(2, lineColor)
		if roundBorder:
			normalState.graphics.drawRoundRect(0, 0, btnWidth, btnHeight, 5)
		else:
			normalState.graphics.drawRect(0, 0, btnWidth, btnHeight)
		normalState.graphics.endFill()

		overState = Sprite()
		overState.graphics.beginFill(backgroundColor["overState"])
		overState.graphics.lineStyle(2, lineColor)
		if roundBorder:
			overState.graphics.drawRoundRect(0, 0, btnWidth, btnHeight, 5)
		else:
			overState.graphics.drawRect(0, 0, btnWidth, btnHeight)
		overState.graphics.endFill()

		super(ButtonSample, self).__init__(normalState, overState)

		txt.x = txt.width * 0.1
		txt.y = txt.height * 0.1
		self.addChild(txt)


class LineEditEvent(object):
		TYPE = Event("line_edit_input")
		FOCUS_IN = Event("line_edit_focus_in")
		FOCUS_OUT = Event("line_edit_focus_out")

		def __init__(self):
			raise Exception("LineEditEvent cannot be instantiated.")


class LineEdit(Sprite):
	def __init__(self, backgroundLayer = None):
		super(LineEdit, self).__init__()
		
		self.__font = "Arial"
		self.__size = 15
		self.__italic = False
		self.__weight = TextFormatWeight.NORMAL
		self.__preWidth = self.width
		self.__preHeight = self.height
		self.__preX = self.x
		self.__preY = self.y
		self.__preVisible = not self.visible
		self.__textColor = "black"
		self.__widgetFont = QtGui.QFont()
		self.__widgetPalette = QtGui.QPalette()
		self.lineEditWidget = QtWidgets.QLineEdit(stage.canvasWidget)
		self.backgroundLayer = backgroundLayer

		if not isinstance(self.backgroundLayer, DisplayObject):
			self.backgroundLayer = Sprite()
			self.backgroundLayer.graphics.beginFill("white")
			self.backgroundLayer.graphics.lineStyle(2, "gray")
			self.backgroundLayer.graphics.drawRect(0, 0, 200, 40)
			self.backgroundLayer.graphics.endFill()

		self.addChild(self.backgroundLayer)

		self.__initWidget()

		self.addEventListener(LoopEvent.ENTER_FRAME, self.__loop)

	@property
	def text(self):
		return self.lineEditWidget.text()

	@text.setter
	def text(self, v):
		self.lineEditWidget.setText(v)

	@property
	def textColor(self):
		return self.__textColor

	@textColor.setter
	def textColor(self, v):
		self.__textColor = v

		self.__widgetPalette.setColor(QtGui.QPalette.Text, getColor(v))
		self.lineEditWidget.setPalette(self.__widgetPalette)

	@property
	def font(self):
		return self.__font

	@font.setter
	def font(self, v):
		self.__font = v

		self.__widgetFont.setFamily(v)
		self.lineEditWidget.setFont(self.__widgetFont)

	@property
	def size(self):
		return self.__size

	@size.setter
	def size(self, v):
		self.__size = v

		self.__widgetFont.setPixelSize(v)
		self.lineEditWidget.setFont(self.__widgetFont)

	@property
	def weight(self):
		return self.__weight

	@weight.setter
	def weight(self, v):
		self.__weight = v

		self.__widgetFont.setWeight(self.__getFontWeight(v))
		self.lineEditWidget.setFont(self.__widgetFont)

	@property
	def italic(self):
		return self.__italic

	@italic.setter
	def italic(self, v):
		self.__italic = v

		self.__widgetFont.setItalic(v)
		self.lineEditWidget.setFont(self.__widgetFont)
	
	def _onLineEditFocusIn(self, e):
		self.dispatchEvent(LineEditEvent.FOCUS_IN)
		return QtWidgets.QLineEdit.focusInEvent(self.lineEditWidget, e)
	
	def _onLineEditFocusOut(self, e):
		self.dispatchEvent(LineEditEvent.FOCUS_OUT)
		return QtWidgets.QLineEdit.focusOutEvent(self.lineEditWidget, e)

	def __initWidget(self):
		self.__widgetPalette.setColor(QtGui.QPalette.Base, getColor("transparent"))
		self.__widgetPalette.setColor(QtGui.QPalette.Text, getColor(self.textColor))
		self.lineEditWidget.setPalette(self.__widgetPalette)

		self.__widgetFont.setFamily(self.font)
		self.__widgetFont.setPixelSize(self.size)
		self.__widgetFont.setWeight(self.__getFontWeight(self.weight))
		self.__widgetFont.setItalic(self.italic)
		self.lineEditWidget.setFont(self.__widgetFont)

		self.lineEditWidget.setFrame(False)

		self.lineEditWidget.resize(self.width, self.height)
		
		pos = self.getRootCoordinate()
		self.lineEditWidget.move(pos.x, pos.y)

		self.lineEditWidget.textEdited.connect(lambda t: self.dispatchEvent(LineEditEvent.TYPE))
		self.lineEditWidget.focusInEvent = self._onLineEditFocusIn
		self.lineEditWidget.focusOutEvent = self._onLineEditFocusOut
		self.setMargins(5, 0, 5, 0)

	def __getFontWeight(self, v):
		weight = v

		if v == TextFormatWeight.NORMAL:
			weight = QtGui.QFont.Normal
		elif v == TextFormatWeight.BOLD:
			weight = QtGui.QFont.Bold
		elif v == TextFormatWeight.BOLDER:
			weight = QtGui.QFont.Black
		elif v == TextFormatWeight.LIGHTER:
			weight = QtGui.QFont.Light

		return weight

	def __loop(self, e):
		if not self.__preVisible == self.visible:
			if self.visible:
				self.lineEditWidget.show()
			else:
				self.lineEditWidget.hide()

			self.__preVisible = self.visible

		if not (self.__preX == self.x and self.__preY == self.y):
			pos = self.getRootCoordinate()

			self.lineEditWidget.move(pos.x, pos.y)

			self.__preX = self.x
			self.__preY = self.y

		w = self.width
		h = self.height

		if not (self.__preWidth == w and self.__preHeight == h):
			self.lineEditWidget.resize(w, h)

			self.__preWidth = w
			self.__preHeight = h

	def setBackgroundLayer(self, backgroundLayer):
		self.backgroundLayer.remove()

		self.backgroundLayer = backgroundLayer
		self.addChild(self.backgroundLayer)
	
	def setMargins(self, left = 0, top = 0, right = 0, bottom = 0):
		self.lineEditWidget.setTextMargins(left, top, right, bottom)

	def die(self):
		super(LineEdit, self).die()

		self.lineEditWidget.hide()
