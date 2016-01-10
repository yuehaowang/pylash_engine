import threading, time, socket


__author__ = "Yuehao Wang"


class RankingServer(object):
	def __init__(self, domain, port):
		super(RankingServer, self).__init__()

		self.rankingFile = "./ranking.txt"
		self.domain = domain
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def start(self, waitingNum = 5):
		self.socket.bind((self.domain, self.port))
		self.socket.listen(waitingNum)

		while True:
			socks, addr = self.socket.accept()

			t = threading.Thread(target = self.__tcpLink, args = (socks, addr))
			t.start()

	def close(self):
		self.socket.close()

	def __tcpLink(self, socks, addr):
		print("Accept new connection from %s:%s..." % addr)

		while True:
			data = socks.recv(1024)
			time.sleep(0.5)

			if not data:
				break

			cmdList = data.decode("utf-8").split(" ")
			cmdName = cmdList[0]
			cmdParam = cmdList[1] if len(cmdList) > 1 else None

			if cmdName == "exit":
				break
			elif cmdName == "setRanking" and cmdParam:
				ranking = self.__setRanking(cmdParam)

				socks.send(("%s" % ranking).encode("utf-8"))
			elif cmdName == "getRanking" and cmdParam:
				ranking = self.__getRanking(cmdParam)

				socks.send(ranking.encode("utf-8"))
			else:
				break

		socks.close()

		print("Connection from %s:%s closed." % addr)

	def __setRanking(self, param):
		paramList = param.split("&")
		valueList = {"uid" : None, "score" : None}

		for o in paramList:
			kv = o.split("=")

			if len(kv) < 2:
				continue

			pn = kv[0]
			pv = kv[1]

			if pn == "uid":
				valueList["uid"] = pv
			elif pn == "score":
				valueList["score"] = pv

		if not valueList["uid"] or not valueList["score"]:
			return "no_ranking"

		lines = self.__readFile()
		currentScore = int(valueList["score"])
		listLen = len(lines)
		ranking = 0

		if listLen > 0:
			ranking = listLen

			for i, li in enumerate(lines):
				if not li:
					continue

				score = int(li.split(";")[1])

				if currentScore > score:
					ranking = i

					break

		lines.insert(ranking, "%s;%s\n" % (valueList["uid"], currentScore))

		self.__writeFile(lines)

		return ranking + 1

	def __getRanking(self, param):
		paramList = param.split("&")
		valueList = {"from" : None, "to" : None}

		for o in paramList:
			kv = o.split("=")

			if len(kv) < 2:
				continue

			pn = kv[0]
			pv = int(kv[1])

			if pn == "from":
				valueList["from"] = int(pv) - 1
			elif pn == "to":
				valueList["to"] = int(pv)

		if valueList["from"] is None or valueList["to"] is None:
			return "no_ranking"

		lines = self.__readFile()
		listLen = len(lines)

		if valueList["to"] >= listLen:
			valueList["to"] = listLen

		if valueList["from"] < 0:
			valueList["from"] = 0

		resultList = lines[valueList["from"]:valueList["to"]]
		result = ""

		for i in resultList:
			result += i

		return result

	def __writeFile(self, l):
		with open(self.rankingFile, "w", encoding = "utf-8") as f:
			f.writelines(l)

	def __readFile(self):
		with open(self.rankingFile, "r", encoding = "utf-8") as f:
			return f.readlines()