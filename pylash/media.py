from PyQt4 import QtWebKit, QtCore
from .utils import stage
from .events import EventDispatcher, Event


__author__ = "Yuehao Wang"


class StageWebView(EventDispatcher):
	def __init__(self):
		super(StageWebView, self).__init__()

		self.__isAddedToParentWidget = False
		
		self.webView = QtWebKit.QWebView()
		
	def loadURL(self, url):
		self.webView.load(QtCore.QUrl(url))

	def show(self):
		if not self.__isAddedToParentWidget:
			self.webView.setParent(stage.canvasWidget)

			self.__isAddedToParentWidget = True

		self.webView.show()

	def hide(self):
		self.webView.hide()

	def setViewPort(self, rect):
		self.webView.move(rect.x, rect.y)
		self.webView.resize(rect.width, rect.height)

	def setScrollBarVisible(self, h = True, v = True):
		p1 = p2 = QtCore.Qt.ScrollBarAsNeeded
		mainFrame = self.webView.page().mainFrame()

		if not h:
			p1 = QtCore.Qt.ScrollBarAlwaysOff

		if not v:
			p2 = QtCore.Qt.ScrollBarAlwaysOff
		
		mainFrame.setScrollBarPolicy(QtCore.Qt.Horizontal, p1)
		mainFrame.setScrollBarPolicy(QtCore.Qt.Vertical, p2)		