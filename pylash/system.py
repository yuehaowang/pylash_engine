import threading, time
from .utils import Object, stage
from .display import Loader
from .events import Event


__author__ = "Yuehao Wang"


class LoadManage(Object):
	__resultList = {}
	__loadListLength = 0
	__loadIndex = 0
	__onUpdate = None
	__onComplete = None
	__isLoadComplete = False
	delay = 50

	def __init__():
		raise Exception("LoadManage cannot be instantiated.")

	def _show(c):
		self = LoadManage

		if self.__isLoadComplete and hasattr(self.__onComplete, "__call__") and self.__resultList:
			self.__onComplete(dict(self.__resultList))

			self.__isLoadComplete = False

	def load(loadList, onUpdate = None, onComplete = None):
		LoadManage.__resultList = {}
		LoadManage.__loadIndex = 0
		LoadManage.__loadListLength = len(loadList)
		LoadManage.__onUpdate = onUpdate
		LoadManage.__onComplete = onComplete

		def startLoad():
			for o in loadList:
				path = o["path"]

				loader = Loader()

				if "name" in o:
					loader.name = o["name"]

				loader.addEventListener(Event.COMPLETE, LoadManage.loadComplete)

				if "path" in o:
					loader.load(o["path"])

		loadThread = threading.Thread(target = startLoad)
		loadThread.start()

	def loadComplete(e):
		self = LoadManage
		name = e.currentTarget.name

		self.__resultList[name] = e.target

		self.__loadIndex += 1

		if hasattr(self.__onUpdate, "__call__"):
			self.__onUpdate(self.__loadIndex * 100 / self.__loadListLength)

		time.sleep(self.delay / 1000)

		if self.__loadIndex >= self.__loadListLength:
			self.__isLoadComplete = True

stage.childList.append(LoadManage)