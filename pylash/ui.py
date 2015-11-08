from .utils import Object, stage, removeItemsInList
from .display import Sprite, DisplayObject, RadialGradientColor, Graphics
from .text import TextField, TextFormatWeight
from .events import MouseEvent


__author__ = "Yuehao Wang"


class ButtonState(object):
	ENABLED = "enabled_state"
	NORMAL = "normal_state"
	OVER = "over_state"
	DOWN = "down_state"
	DISABLED = "disabled_state"

	def __init__():
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
			opt["progressColor"].addColorStop(0, "red");  
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
			opt["progressColor"].addColorStop(0, "red");  
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