import threading, time, socket
from .utils import Object, stage
from .display import Loader
from .events import Event, EventDispatcher, RankingSystemEvent


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