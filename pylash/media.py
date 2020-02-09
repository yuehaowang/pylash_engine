from PySide2 import QtCore, QtMultimedia, QtMultimediaWidgets, QtGui
from .core import stage
from .display import DisplayObject
from .events import EventDispatcher, Event


__author__ = "Yuehao Wang"


class MediaEvent(object):
	SIZE_CHANGED = Event("media_size_changed")
	LOOP = Event("media_loop")
	COMPLETE = Event("media_complete")

	def __init__(self):
		raise Exception("MediaEvent cannot be instantiated.")


class Media(EventDispatcher):
	LOOP_FOREVER = -1

	TYPE_SOUND = "media_sound"
	TYPE_VIDEO = "media_video"

	def __init__(self, mediaType, source):
		super(Media, self).__init__()

		self.mediaType = mediaType
		self.loopCount = 1
		self._loopIndex = 0
		self.source = source

		self.source.stop()
		self.source.stateChanged.connect(
			lambda state: self._onSourceStateChanged(state)
		)
	
	def _onSourceStateChanged(self, state):
		if state == QtMultimedia.QMediaPlayer.State.StoppedState:
			if self.source.mediaStatus() == QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia:
				self._loopIndex += 1

				if self.loopCount == self.LOOP_FOREVER or self._loopIndex < self.loopCount:
					self.source.setPosition(0)
					self.source.play()
					self.dispatchEvent(MediaEvent.LOOP)
				else:
					self.source.stop()
					self.dispatchEvent(MediaEvent.COMPLETE)
	
	def play(self):
		self.source.play()

	def pause(self):
		self.source.pause()

	def stop(self):
		self._loopIndex = 0
		self.source.stop()
	
	@property
	def position(self):
		return self.source.position()

	@position.setter
	def position(self, v):
		return self.source.setPosition(v)

	@property
	def duration(self):
		return self.source.duration()
	
	@property
	def playing(self):
		return self.source.state() == QtMultimedia.QMediaPlayer.State.PlayingState
	
	@property
	def volume(self):
		return self.source.volume()

	@volume.setter
	def volume(self, v):
		return self.source.setVolume(v)
		

class Sound(Media):
	def __init__(self, source):
		super(Sound, self).__init__(Media.TYPE_SOUND, source)

		self.source.setAudioRole(QtMultimedia.QAudio.GameRole)


class Video(Media, DisplayObject):
	def __init__(self, source):
		Media.__init__(self, Media.TYPE_VIDEO, source)
		DisplayObject.__init__(self)

		self._videoGraphicsItem = QtMultimediaWidgets.QGraphicsVideoItem()
		self._videoGraphicsItem.setAspectRatioMode(QtCore.Qt.IgnoreAspectRatio)
		self._videoGraphicsItem._nativeSizeChangedSlot = lambda size: self._onVideoNativeSizeChanged(size)
		self._videoGraphicsItem.nativeSizeChanged.connect(self._videoGraphicsItem._nativeSizeChangedSlot)
		self.source.setVideoOutput(self._videoGraphicsItem)

	def _onVideoNativeSizeChanged(self, size):
		QtCore.QObject.disconnect(
			self._videoGraphicsItem,
			QtCore.SIGNAL("nativeSizeChanged()"),
			self._videoGraphicsItem._nativeSizeChangedSlot
		)

		self._videoGraphicsItem.setSize(size)
		self.dispatchEvent(MediaEvent.SIZE_CHANGED)

	def _getOriginalWidth(self):
		w = self._videoGraphicsItem.nativeSize().width()
		return w if w > 0 else 0

	def _getOriginalHeight(self):
		h = self._videoGraphicsItem.nativeSize().height()
		return h if h > 0 else 0
	
	def _loopDraw(self, c):
		self._videoGraphicsItem.paint(c, None, None)
