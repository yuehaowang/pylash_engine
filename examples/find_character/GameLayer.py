import sys
import random
from TimeBar import TimeBar

sys.path.insert(0, "../../")
from pylash.utils import stage
from pylash.display import Sprite, Bitmap, BitmapData
from pylash.text import TextField, TextFormatWeight, TextFormatAlign
from pylash.events import MouseEvent

class GameLayer(Sprite):
	def __init__(self, bg):
		super(GameLayer, self).__init__()

		self.blockLayer = None
		self.characters = (("我", "找"), ("王", "玉"), ("籍", "藉"), ("春", "舂"), ("龙", "尤"), ("已", "己"), ("巳", "已"))

		# add background
		bg = Bitmap(BitmapData(bg, 50, 50))
		self.addChild(bg)

		# start game
		self.start()

	def createTimeBar(self):
		self.timeBar = TimeBar()
		self.timeBar.x = stage.width - 70
		self.timeBar.y = (stage.height - self.timeBar.height) / 2
		self.addChild(self.timeBar)

	def startLevel(self, char):
		# get random position of target
		targetX = random.randint(0, 9)
		targetY = random.randint(0, 9)

		self.blockLayer = Sprite()
		self.blockLayer.x = 50
		self.blockLayer.y = 50
		self.blockLayer.alpha = 0.7
		self.addChild(self.blockLayer)

		# create blocks with a character
		for i in range(10):
			for j in range(10):
				block = Sprite()
				block.x = j * 50
				block.y = i * 50
				block.graphics.beginFill("#33CCFF")
				block.graphics.lineStyle(5, "#0066FF")
				block.graphics.drawRect(0, 0, 50, 50)
				block.graphics.endFill()
				self.blockLayer.addChild(block)

				txt = TextField()
				txt.size = 20
				txt.font = "Microsoft YaHei"

				# when this block is target
				if i == targetY and j == targetX:
					txt.text = char[1]

					block.isTarget = True
				# when this block is not target
				else:
					txt.text = char[0]

					block.isTarget = False

				txt.x = (50 - txt.width) / 2
				txt.y = (50 - txt.height) / 2
				block.addChild(txt)

				block.addEventListener(MouseEvent.MOUSE_UP, self.check)

	def check(self, e):
		global gameOver

		b = e.currentTarget

		if b.isTarget:
			self.gameOver("win")
	
	def gameOver(self, flag):
		self.blockLayer.remove()

		if flag == "win":
			self.levelIndex += 1

			if self.levelIndex >= len(self.characters):
				self.addResultLayer("Level Clear!", "Time: %s" % int(self.timeBar.usedTime))

				self.timeBar.remove()
			else:
				self.startLevel(self.characters[self.levelIndex])
		elif flag == "lose":
			self.addResultLayer("Time is Up!", "Level: %s" % (self.levelIndex))

			self.timeBar.remove()

	def addResultLayer(self, *text):
		resultLayer = Sprite()
		self.addChild(resultLayer)

		for i in text:
			txt = TextField()
			txt.font = "Microsoft YaHei"
			txt.text = i
			txt.size = 40
			txt.textAlign = TextFormatAlign.CENTER
			txt.x = stage.width / 2
			txt.y = resultLayer.height + 20
			txt.textColor = "orangered"
			txt.weight = TextFormatWeight.BOLD
			resultLayer.addChild(txt)

		# add a botton used for restart
		restartBtn = Sprite()
		restartBtn.graphics.beginFill("yellow")
		restartBtn.graphics.lineStyle(3, "orangered")
		restartBtn.graphics.drawRect(0, 0, 200, 60)
		restartBtn.graphics.endFill()
		restartBtn.x = (stage.width - restartBtn.width) / 2
		restartBtn.y = resultLayer.height + 50
		resultLayer.addChild(restartBtn)

		restartTxt = TextField()
		restartTxt.font = "Microsoft YaHei"
		restartTxt.text = "Restart"
		restartTxt.textColor = "orangered"
		restartTxt.size = 30
		restartTxt.x = (restartBtn.width - restartTxt.width) / 2
		restartTxt.y = (restartBtn.height - restartTxt.height) / 2
		restartBtn.addChild(restartTxt)

		def restart(e):
			self.start()

			resultLayer.remove()

		restartBtn.addEventListener(MouseEvent.MOUSE_UP, restart)
		
		# make the result layer locate at vertical center
		resultLayer.y = (stage.height - resultLayer.height) / 2

	def start(self):
		self.levelIndex = 0

		# add time bar
		self.createTimeBar()

		# start level 1
		self.startLevel(self.characters[0])