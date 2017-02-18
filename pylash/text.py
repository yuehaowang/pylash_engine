from PyQt4 import QtGui, QtCore
from .display import DisplayObject
from .utils import Object, getColor, stage


__author__ = "Yuehao Wang"


class TextFormatAlign(object):
	RIGHT = "right"
	LEFT = "left"
	CENTER = "center"
	START = "start"
	END = "end"

	def __init__(self):
		raise Exception("TextFormatAlign cannot be instantiated.")


class TextFormatBaseline(object):
	ALPHABETIC = "alphabetic"
	BOTTOM = "bottom"
	MIDDLE = "middle"
	HANGING = "hanging"
	TOP = "top"

	def __init__(self):
		raise Exception("TextFormatBaseline cannot be instantiated.")


class TextFormatWeight(object):
	NORMAL = "normal"
	BOLD = "bold"
	BOLDER = "bolder"
	LIGHTER = "lighter"

	def __init__(self):
		raise Exception("TextFormatWeight cannot be instantiated.")


class TextField(DisplayObject):
	def __init__(self):
		super(TextField, self).__init__()

		self.text = ""
		self.font = "Arial"
		self.size = 15
		self.textColor = "#000000"
		self.backgroundColor = None
		self.italic = False
		self.weight = TextFormatWeight.NORMAL
		self.textAlign = TextFormatAlign.LEFT
		self.textBaseline = TextFormatBaseline.TOP
		
	def _getOriginalWidth(self):
		font = self.__getFont()
		fontMetrics = QtGui.QFontMetrics(font)

		return fontMetrics.width(str(self.text))

	def _getOriginalHeight(self):
		font = self.__getFont()
		fontMetrics = QtGui.QFontMetrics(font)

		return fontMetrics.height()

	def __getFont(self):
		weight = self.weight

		if self.weight == TextFormatWeight.NORMAL:
			weight = QtGui.QFont.Normal
		elif self.weight == TextFormatWeight.BOLD:
			weight = QtGui.QFont.Bold
		elif self.weight == TextFormatWeight.BOLDER:
			weight = QtGui.QFont.Black
		elif self.weight == TextFormatWeight.LIGHTER:
			weight = QtGui.QFont.Light

		font = QtGui.QFont()
		font.setFamily(self.font)
		font.setPixelSize(self.size)
		font.setWeight(weight)
		font.setItalic(self.italic)

		return font

	def __getTextStartX(self):
		w = self._getOriginalWidth()

		if self.textAlign == TextFormatAlign.END or self.textAlign == TextFormatAlign.RIGHT:
			return -w
		elif self.textAlign == TextFormatAlign.CENTER:
			return -w / 2
		else:
			return 0

	def __getTextStartY(self):
		h = self._getOriginalHeight()

		if self.textBaseline == TextFormatBaseline.ALPHABETIC or self.textBaseline == TextFormatBaseline.MIDDLE:
			return -h
		elif self.textBaseline == TextFormatBaseline.MIDDLE:
			return -h / 2
		else:
			return 0

	def _loopDraw(self, c):
		font = self.__getFont()
		flags = QtCore.Qt.AlignCenter
		startX = self.__getTextStartX()
		startY = self.__getTextStartY()
		width = self._getOriginalWidth()
		height = self._getOriginalHeight()

		pen = QtGui.QPen()
		pen.setBrush(QtGui.QBrush(getColor(self.textColor)))

		if self.backgroundColor:
			brush = QtGui.QBrush()
			brush.setColor(getColor(self.backgroundColor))
			brush.setStyle(QtCore.Qt.SolidPattern)
			c.setBrush(brush)

			c.setPen(getColor("transparent"))

			c.drawRect(startX, startY, width, height)

		c.setFont(font)
		c.setPen(pen)
		c.drawText(startX, startY, width, height, flags, str(self.text))