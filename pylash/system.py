import threading, time, socket
from PyQt4 import QtCore
from .utils import Object, stage
from .display import Loader
from .events import Event, EventDispatcher, RankingSystemEvent
from .media import Sound


__author__ = "Yuehao Wang"


class LoadThread(QtCore.QThread):
	loadOne = QtCore.pyqtSignal(dict)

	def __init__(self, target):
		super(LoadThread, self).__init__()

		self.__target = target

	def run(self):
		self.__target(self)


class LoadManage(Object):
	__resultList = {}
	__loadListLength = 0
	__loadIndex = 0
	__soundIndex = 0
	__onUpdate = None
	__onComplete = None
	__isLoadComplete = False
	__soundObjectList = None
	delay = 50

	def __init__():
		raise Exception("LoadManage cannot be instantiated.")

	def _show(c):
		self = LoadManage

		if self.__isLoadComplete and hasattr(self.__onComplete, "__call__") and self.__resultList:
			self.__onComplete(dict(self.__resultList))

			self.__isLoadComplete = False

			del self.__resultList

	def load(loadList, onUpdate = None, onComplete = None):
		self = LoadManage
		self.__resultList = {}
		self.__loadIndex = 0
		self.__soundIndex = 0
		self.__loadListLength = len(loadList)
		self.__onUpdate = onUpdate
		self.__onComplete = onComplete
		self.__soundObjectList = []

		for o in loadList:
			path = None
			extension = None

			if "path" in o:
				path = o["path"]
			else:
				raise ValueError("LoadManage.load(loadList, onUpdate = None, onComplete = None): parameter 'loadList' has a wrong item which dosen't have a key named 'path'.")

			if not "type" in o:
				extension = self.getExtension(path)

				if extension in ["mp3", "ogg", "wav", "m4a"]:
					o["type"] = "sound"

					self.__soundObjectList.append(Sound())
				else:
					o["type"] = "image"


		def startLoad(thread):
			for o in loadList:
				thread.loadOne.emit(o)

		self.__loadThread = LoadThread(startLoad)
		self.__loadThread.loadOne.connect(self.__loadOneResource)
		self.__loadThread.start()

	@QtCore.pyqtSlot(dict)
	def __loadOneResource(o):
		self = LoadManage
		t = o["type"]
		loader = None

		if t == "sound":
			loader = self.__soundObjectList[self.__soundIndex]

			self.__soundIndex += 1
		elif t == "image":
			loader = Loader()

		if "name" in o:
			loader.name = o["name"]

		loader.addEventListener(Event.COMPLETE, self.__loadComplete)

		loader.load(o["path"])

	def __loadComplete(e):
		self = LoadManage
		name = e.currentTarget.name

		self.__resultList[name] = e.target

		self.__loadIndex += 1

		if hasattr(self.__onUpdate, "__call__"):
			self.__onUpdate(self.__loadIndex * 100 / self.__loadListLength)

		del e.currentTarget

		time.sleep(self.delay / 1000)

		if self.__loadIndex >= self.__loadListLength:
			self.__isLoadComplete = True

			del self.__soundObjectList
			del self.__loadThread

	def getExtension(p):
		pList = p.split(".")
		
		return pList[len(pList) - 1]

stage.childList.append(LoadManage)


class RankingSystem(EventDispatcher):
	NO_RANKING = "no_ranking"

	def __init__(self, domain, port):
		super(RankingSystem, self).__init__()
		
		self.domain = domain
		self.port = port

	def addRecord(self, uid, score):
		if not isinstance(score, (int, float)):
			raise ValueError("RankingSystem.addRecord(uid, score): parameter 'score' must be a number.")

		socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socks.connect((self.domain, self.port))

		socks.send(("setRanking uid=%s&score=%s" % (uid, score)).encode("utf-8"))

		def receive():
			data = socks.recv(1024).decode("utf-8")

			if data == RankingSystem.NO_RANKING:
				RankingSystemEvent.FAIL_TO_ADD_RECORD.data = data

				self.dispatchEvent(RankingSystemEvent.FAIL_TO_ADD_RECORD)

				del RankingSystemEvent.FAIL_TO_ADD_RECORD.data
			else:
				RankingSystemEvent.SUCCEED_IN_ADDING_RECORD.data = int(data)

				self.dispatchEvent(RankingSystemEvent.SUCCEED_IN_ADDING_RECORD)

				del RankingSystemEvent.SUCCEED_IN_ADDING_RECORD.data

			socks.close()

		t = threading.Thread(target = receive)
		t.start()

	def getRecords(self, fro, to):
		if not isinstance(fro, (int, float)):
			raise ValueError("RankingSystem.getRecords(fro, to): parameter 'fro' must be a number.")

		if not isinstance(to, (int, float)):
			raise ValueError("RankingSystem.getRecords(fro, to): parameter 'to' must be a number.")

		socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socks.connect((self.domain, self.port))

		socks.send(("getRanking from=%s&to=%s" % (fro, to)).encode("utf-8"))

		def receive():
			d = socks.recv(1024).decode("utf-8")

			if d == RankingSystem.NO_RANKING:
				RankingSystemEvent.FAIL_TO_GET_RECORDS.data = data

				self.dispatchEvent(RankingSystemEvent.FAIL_TO_GET_RECORDS)

				del RankingSystemEvent.FAIL_TO_GET_RECORDS.data
			else:
				dl = d.split("\n")
				dl.pop()

				if len(dl) <= 0:
					return

				data = []

				for i in dl:
					li = i.split(";")
					
					data.append((li[0], int(li[1])))

				RankingSystemEvent.SUCCEED_IN_GETTING_RECORDS.data = data

				self.dispatchEvent(RankingSystemEvent.SUCCEED_IN_GETTING_RECORDS)

				del RankingSystemEvent.SUCCEED_IN_GETTING_RECORDS.data

			socks.close()

		t = threading.Thread(target = receive)
		t.start()