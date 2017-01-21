from PyQt4 import QtWebKit, QtCore, QtGui
from PyQt4.phonon import Phonon
from .utils import stage
from .events import EventDispatcher, Event, MediaEvent


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


class Media(EventDispatcher, QtGui.QWidget):
	ignoreLoadingError = False

	TYPE_SOUND = "type_sound"

	def __init__(self, type, url = None):
		EventDispatcher.__init__(self)
		QtGui.QWidget.__init__(self)

		self.setParent(stage.canvasWidget)
		self.show()

		self.__mediaSource = None
		self.mediaNode = None
		self.mediaObject = Phonon.MediaObject(self)
		self.__playing = False
		self.loop = False
		self.loopTimes = None
		self.__loopIndex = 0
		self.__startTime = 0

		if type == Media.TYPE_SOUND:
			self.mediaNode = Phonon.AudioOutput(Phonon.MusicCategory, self)

		if self.mediaNode:
			Phonon.createPath(self.mediaObject, self.mediaNode)

		self.mediaObject.stateChanged.connect(self.__onStateChanged)
		self.mediaObject.aboutToFinish.connect(self.__onAboutToFinish)
		
		if url:
			self.load(url)

	@property
	def playing(self):
		return self.__playing
	
	@property
	def length(self):
		return self.mediaObject.totalTime()

	@property
	def currentTime(self):
		return self.length - self.mediaObject.remainingTime()

	@property
	def volume(self):
		if hasattr(self, "mediaNode"):
			return self.mediaNode.volume()
		else:
			return 0

	@volume.setter
	def volume(self, v):
		if hasattr(self, "mediaNode"):
			return self.mediaNode.setVolume(v)

	@QtCore.pyqtSlot(int, int)
	def __onStateChanged(self, newState, oldState):
		if oldState == Phonon.LoadingState and self.__mediaSource:
			if (not self.__mediaSource or newState == Phonon.ErrorState) and not Media.ignoreLoadingError:
				raise Exception("%s cannot load data in the path you give." % self.__class__.__name__)

			e = Event(Event.COMPLETE)
			e.target = self.__mediaSource
			self.dispatchEvent(e)

			self.__mediaSource = None

			return

		if newState == Phonon.PlayingState:
			self.dispatchEvent(MediaEvent.PLAY)
		elif newState == Phonon.PausedState:
			self.dispatchEvent(MediaEvent.PAUSE)
		elif newState == Phonon.StoppedState:
			self.dispatchEvent(MediaEvent.STOP)

	@QtCore.pyqtSlot()
	def __onAboutToFinish(self):
		if self.loop:
			loopPlaying = True

			if self.loopTimes:
				self.__loopIndex += 1

				if self.__loopIndex >= self.loopTimes:
					loopPlaying = False

			if loopPlaying:
				self.mediaObject.seek(self.__startTime)

	def load(self, url):
		if isinstance(url, Phonon.MediaSource):
			self.__mediaSource = url
		else:
			self.__mediaSource = Phonon.MediaSource(url)
		
		self.__mediaSource.setAutoDelete(True)
		self.mediaObject.setCurrentSource(self.__mediaSource)

		self.mediaObject.stop()

	def play(self, start = 0):
		self.__playing = True
		self.__startTime = start
		self.__loopIndex = 0

		self.mediaObject.seek(start)
		self.mediaObject.play()

	def pause(self):
		self.__playing = False

		self.mediaObject.pause()

	def resume(self):
		self.__playing = True

		self.mediaObject.seek(self.currentTime)
		self.mediaObject.play()

	def stop(self):
		self.__playing = False
		self.__startTime = 0
		self.__loopIndex = 0

		self.mediaObject.stop()

	def close(self):
		self.__playing = False
		self.__startTime = 0
		self.__loopIndex = 0

		self.mediaObject.clear()
		

class Sound(Media):
	def __init__(self, url = None):
		super(Sound, self).__init__(Media.TYPE_SOUND, url)