from map_data import terrainList

from pylash.display import Sprite, BitmapData, Animation, AnimationSet, AnimationPlayMode, AnimationEvent

class Enemy(Sprite):
	def __init__(self, mov, xInMap, yInMap):
		super(Enemy, self).__init__()

		self.xInMap = xInMap
		self.yInMap = yInMap
		self.x = xInMap * 48
		self.y = yInMap * 48
		# direction that enemy move towards
		self.dir = "up"
		# notice that value of stepLength property must be a divisible number of 48
		self.stepLength = 8
		self.stepIndex = 0
		self.stepNum = 48 / self.stepLength
		self.fullHp = 150
		self.hp = self.fullHp

		self.animaSet = AnimationSet()
		self.addChild(self.animaSet)

		frameList = Animation.divideUniformSizeFrames(48, 96, 1, 2)

		# move down
		bmpd = BitmapData(mov, 0, 0, 48, 96)
		anima = Animation(bmpd, frameList)
		self.animaSet.addAnimation("mov_down", anima)

		# move up
		bmpd = BitmapData(mov, 0, 96, 48, 96)
		anima = Animation(bmpd, frameList)
		self.animaSet.addAnimation("mov_up", anima)

		# move left
		bmpd = BitmapData(mov, 0, 192, 48, 96)
		anima = Animation(bmpd, frameList)
		self.animaSet.addAnimation("mov_left", anima)

		# move right
		bmpd = BitmapData(mov, 0, 192, 48, 96)
		anima = Animation(bmpd, frameList)
		anima.mirroring = True
		self.animaSet.addAnimation("mov_right", anima)

		# uniform treatment of these animations
		for n in self.animaSet.animationList:
			o = self.animaSet.animationList[n]

			o.playMode = AnimationPlayMode.VERTICAL
			o.speed = 3

			o.addEventListener(AnimationEvent.CHANGE_FRAME, self.step)
		
		self.animaSet.changeAnimation("mov_" + self.dir)

		# create hp layer
		self.hpLayer = Sprite()
		self.hpLayer.x = 8
		self.hpLayer.y = -5
		self.addChild(self.hpLayer)

		self.hpLayer.graphics.beginFill("red")
		self.hpLayer.graphics.drawRect(0, 0, 32, 5)
		self.hpLayer.graphics.endFill()

	EVENT_ARRIVE = "event_arrive"
	EVENT_DIE = "event_die"

	enemyList = []

	def step(self, e):
		# make enemy move
		if self.dir == "up":
			self.y -= self.stepLength
		elif self.dir == "down":
			self.y += self.stepLength
		elif self.dir == "left":
			self.x -= self.stepLength
		elif self.dir == "right":
			self.x += self.stepLength

		self.stepIndex += 1

		# when moved to the next small map block...
		if  self.stepIndex >= self.stepNum:
			self.stepIndex = 0

			if self.dir == "up":
				self.yInMap -= 1
			elif self.dir == "down":
				self.yInMap += 1
			elif self.dir == "left":
				self.xInMap -= 1
			elif self.dir == "right":
				self.xInMap += 1

			self.dir = self.searchDirection()

			if self.dir == "arrive":
				return

			self.animaSet.changeAnimation("mov_" + self.dir, 0, 0)

	def searchDirection(self):
		terrain = terrainList
		x = self.xInMap
		y = self.yInMap

		if 0 <= y - 1 and terrain[y - 1][x] == 1 and self.dir != "down":
			return "up"
		elif 0 <= x - 1 and terrain[y][x - 1] == 1 and self.dir != "right":
			return "left"
		elif y + 1 < len(terrain) and terrain[y + 1][x] == 1 and self.dir != "up":
			return "down"
		elif x + 1 < len(terrain[y]) and terrain[y][x + 1] == 1 and self.dir != "left":
			return "right"

		self.dispatchEvent(Enemy.EVENT_ARRIVE)

		return "arrive"

	def beAttacked(self, v):
		self.hp -= v

		# redraw hp
		self.hpLayer.graphics.clear()
		self.hpLayer.graphics.beginFill("red")
		self.hpLayer.graphics.drawRect(0, 0, 32 * (self.hp / self.fullHp), 5)
		self.hpLayer.graphics.endFill()

		if self.hp <= 0:
			self.dispatchEvent(Enemy.EVENT_DIE)