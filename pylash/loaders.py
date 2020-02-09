import threading, time, socket
from PySide2 import QtCore, QtGui, QtMultimedia
from .core import Object, stage
from .events import Event, EventDispatcher


__author__ = "Yuehao Wang"


def getExtension(p):
	pList = p.split(".")
	
	return pList[len(pList) - 1]


class LoaderEvent(object):
	COMPLETE = Event("loader_complete")
	ERROR = Event("loader_error")

	def __init__(self):
			raise Exception("LoaderEvent cannot be instantiated.")


class Loader(EventDispatcher):
	def __init__(self):
		super(Loader, self).__init__()
	
		self.content = None
		self.resourceName = None

	def load(self, path):
		pass


class ImageLoader(Loader):
	class _ImageLoaderWorker(QtCore.QObject):
		resultReady = QtCore.Signal(QtGui.QImage)

		def __init__(self, path):
			super(ImageLoader._ImageLoaderWorker, self).__init__()

			self.path = path
		
		def doLoad(self):
			image = QtGui.QImage()
			image.load(self.path)
			self.resultReady.emit(image)

	def __init__(self):
		super(ImageLoader, self).__init__()

		self.content = None
		self._loadingThread = None
	
	def _onLoadWorkerComplete(self, image):
		if self._loadingThread:
			self._loadingThread.started.disconnect()
			self._loadingThread.finished.disconnect()
			self._loadingThread.quit()

		self.content = image

		if image.isNull():
			e = Event(LoaderEvent.ERROR)
			e.target = Exception("ImageLoader: cannot load file in the given path.")
			self.dispatchEvent(e)
		else:
			e = Event(LoaderEvent.COMPLETE)
			e.target = image
			self.dispatchEvent(e)

	def load(self, path):
		self._loadingThread = QtCore.QThread(stage.canvasWidget)
		worker = self._ImageLoaderWorker(path)
		worker.moveToThread(self._loadingThread)
		worker.resultReady.connect(lambda img: self._onLoadWorkerComplete(img))
		self._loadingThread.started.connect(lambda: worker.doLoad())
		self._loadingThread.finished.connect(lambda: worker.deleteLater())
		self._loadingThread.start()


class MediaLoader(Loader):
	def __init__(self):
		super(MediaLoader, self).__init__()

		self.content = None
		self._contentMediaStatusChangedConn = None
		self._contentErrorConn = None
	
	def _onMediaStatusChanged(self, status):
		if status == QtMultimedia.QMediaPlayer.MediaStatus.LoadedMedia:
			QtCore.QObject.disconnect(
				self.content,
				QtCore.SIGNAL("mediaStatusChanged()"),
				self.content._mediaStatusChangedSlot
			)
			QtCore.QObject.disconnect(
				self.content,
				QtCore.SIGNAL("error()"),
				self.content._errorSlot
			)
			
			e = Event(LoaderEvent.COMPLETE)
			e.target = self.content
			self.dispatchEvent(e)

	def _onError(self, err):
		e = Event(LoaderEvent.ERROR)
		e.target = Exception("MediaLoader: cannot load file in the given path (%s)." % self.content.errorString())
		self.dispatchEvent(e)

	def load(self, path):
		fullpath = QtCore.QDir.current().absoluteFilePath(path)
		mediaContent = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fullpath))
		self.content = QtMultimedia.QMediaPlayer(stage.canvasWidget)

		self.content._mediaStatusChangedSlot = lambda status: self._onMediaStatusChanged(status)
		self.content.mediaStatusChanged.connect(self.content._mediaStatusChangedSlot)

		self.content._errorSlot = lambda err: self_onError(err)
		self.content.error.connect(self.content._errorSlot)

		self.content.setMedia(mediaContent)
		self.content.stop()


class LoadManageWorker(Object):
	def __init__(self):
		super(LoadManageWorker, self).__init__()
		
		self._resultList = {}
		self._loadIndex = 0
		self._loadNum = 0
		self._onUpdate = None
		self._onComplete = None

	def load(self, loadList, onUpdate = None, onComplete = None):
		self._loadNum = len(loadList)
		self._onUpdate = onUpdate
		self._onComplete = onComplete

		for o in loadList:
			path = None
			fileType = None

			if "path" in o:
				path = o["path"]
			else:
				raise ValueError("LoadManage.load(loadList, onUpdate = None, onComplete = None): parameter 'loadList' has a wrong item which dosen't have a key named 'path'.")

			if not "type" in o:
				extension = getExtension(path)

				if extension in LoadManage.IMAGE_EXTENSION:
					fileType = "image"
				elif extension in LoadManage.MEDIA_EXTENSION:
					fileType = "media"
			else:
				fileType = o["type"]
			
			if not path:
				continue
			
			if fileType == "image":
				loader = ImageLoader()
			elif fileType == "media":
				loader = MediaLoader()
			else:
				raise ValueError("LoadManage.load(loadList, onUpdate = None, onComplete = None): an item with unsupported file type found in parameter 'loadList'.")
			
			if "name" in o:
				loader.resourceName = o["name"]
			
			loader.addEventListener(LoaderEvent.COMPLETE, self._onLoadOneComplete)
			loader.load(path)

	def _onLoadOneComplete(self, e):
		if e.currentTarget.resourceName:
			self._resultList[e.currentTarget.resourceName] = e.target

		self._loadIndex += 1
		if hasattr(self._onUpdate, "__call__"):
			self._onUpdate(self._loadIndex * 100 / self._loadNum)

		if LoadManage.delay > 0:
			time.sleep(LoadManage.delay / 1000)

		if self._loadIndex >= self._loadNum and hasattr(self._onComplete, "__call__"):
			self._onComplete(self._resultList)


class LoadManage(Object):
	delay = 50
	IMAGE_EXTENSION = ["png", "jpg", "jpeg", "bmp", "gif"]
	MEDIA_EXTENSION = [
		"aif", "cda", "mid", "midi", "mp3", "mpa", "wav", "ogg", "wma", "m4a",
		"avi", "flv", "m4v", "mkv", "mov", "mp4", "mpg", "mpeg", "swf", "vob", "wmv"
	]

	def __init__(self):
		raise Exception("LoadManage cannot be instantiated.")

	@staticmethod
	def load(loadList, onUpdate = None, onComplete = None):
		worker = LoadManageWorker()
		worker.load(loadList, onUpdate, onComplete)
