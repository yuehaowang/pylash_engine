import threading
from .utils import Object
from .display import Loader
from .events import Event


__author__ = "Yuehao Wang"


class LoadManage(Object):
	__resultList = {}
	__loadListLength = 0
	__loadIndex = 0
	__onUpdate = None
	__onComplete = None

	def __init__():
		raise Exception("LoadManage cannot be instantiated.")
	
	def load(loadList, onUpdate = None, onComplete = None):
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

		if self.__loadIndex >= self.__loadListLength:
			if hasattr(self.__onComplete, "__call__"):
				self.__onComplete(dict(self.__resultList))