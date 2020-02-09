from pylash.core import stage
from pylash.display import Sprite, Animation, BitmapData

class Player(Sprite):
	def __init__(self, playerImage):
		super(Player, self).__init__()

		self.direction = None
		self.step = 5
		
		# create bitmap data
		bmpd = BitmapData(playerImage)
		# create frames in animation
		frames = Animation.divideUniformSizeFrames(bmpd.width, bmpd.height, 4, 4)

		# create animation
		self.animation = Animation(bmpd, frames)
		self.animation.speed = 5
		self.animation.play()
		self.addChild(self.animation)

	def loop(self):
		# move towards right
		if self.direction == "right":
			self.x += self.step
			self.animation.currentRow = 2
		# move towards left
		elif self.direction == "left":
			self.x -= self.step
			self.animation.currentRow = 1
		# no movement
		else:
			self.animation.currentRow = 0

		if self.x < 0:
			self.x = 0

		elif self.x > stage.width - self.width:
			self.x = stage.width - self.width