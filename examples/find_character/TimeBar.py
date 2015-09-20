import sys
import time

sys.path.insert(0, "../../")
from pylash.utils import stage
from pylash.display import Sprite
from pylash.events import Event

class TimeBar(Sprite):
	def __init__(self):
		super(TimeBar, self).__init__()

		self.totalTime = 60
		self.usedTime = 0
		self.preTime = time.time()
		self.usedTimeColor = "#CC99FF"
		self.leftTimeColor = "#CC00FF"
		self.borderColor = "#6600FF"
		
		self.graphics.beginFill(self.usedTimeColor)
		self.graphics.lineStyle(3, self.borderColor)
		self.graphics.drawRect(0, 0, 20, stage.height * 0.75)
		self.graphics.endFill()

		# add loop event that will be dispatch when the page is redrawn
		self.addEventListener(Event.ENTER_FRAME, self.loop)

	def loop(self, e):
		currentTime = time.time()
		self.usedTime += currentTime - self.preTime
		self.preTime = currentTime

		barHeight = stage.height * 0.75
		# calculate the position at which the left time bar is drawn
		startX = barHeight * (self.usedTime / self.totalTime)

		if (self.usedTime >= self.totalTime):
			if self.parent:
				self.parent.gameOver("lose")

			return

		# redraw the time bar
		self.graphics.clear()

		self.graphics.beginFill(self.usedTimeColor)
		self.graphics.drawRect(0, 0, 20, barHeight)
		self.graphics.endFill()

		self.graphics.beginFill(self.leftTimeColor)
		self.graphics.drawRect(0, startX, 20, barHeight - startX)
		self.graphics.endFill()

		self.graphics.beginFill()
		self.graphics.lineStyle(3, self.borderColor)
		self.graphics.drawRect(0, 0, 20, barHeight)
		self.graphics.endFill()