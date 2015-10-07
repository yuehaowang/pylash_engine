from Enemy import Enemy

import sys

sys.path.insert(0, "../../")
from pylash.display import Sprite, BitmapData, Animation, AnimationSet, AnimationPlayMode
from pylash.events import AnimationEvent

class AttackCharacter(Sprite):
	def __init__(self, name, mov, atk, xInMap, yInMap, atkValue):
		super(AttackCharacter, self).__init__()

		self.xInMap = xInMap
		self.yInMap = yInMap
		self.x = xInMap * 48
		self.y = yInMap * 48
		self.isAtk = False

		self.atkValue = atkValue
		
		self.dir = "down"

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

		frameList = Animation.divideUniformSizeFrames(64, 256, 1, 4)

		# atk down
		bmpd = BitmapData(atk, 0, 0, 64, 256)
		anima = Animation(bmpd, frameList)
		self.animaSet.addAnimation("atk_down", anima)

		# atk up
		bmpd = BitmapData(atk, 0, 256, 64, 256)
		anima = Animation(bmpd, frameList)
		self.animaSet.addAnimation("atk_up", anima)

		# atk left
		bmpd = BitmapData(atk, 0, 512, 64, 256)
		anima = Animation(bmpd, frameList)
		self.animaSet.addAnimation("atk_left", anima)

		# atk right
		bmpd = BitmapData(atk, 0, 512, 64, 256)
		anima = Animation(bmpd, frameList)
		anima.mirroring = True
		self.animaSet.addAnimation("atk_right", anima)

		# uniform treatment of these animations
		for n in self.animaSet.animationList:
			o = self.animaSet.animationList[n]

			o.playMode = AnimationPlayMode.VERTICAL
			o.speed = 5

			o.addEventListener(AnimationEvent.CHANGE_FRAME, self.step)
			
			# if atk animation...
			if n.find("atk") >= 0:
				o.loopTimes = 1
				o.x -= 8
				o.y -= 8

				o.addEventListener(AnimationEvent.STOP, self.atkOver)

		self.animaSet.changeAnimation("mov_" + self.dir)

	ourList = []

	def step(self, e):
		if not self.isAtk:
			self.attack()

	def attack(self):
		x = self.xInMap
		y = self.yInMap
		targetList = []

		# the attack range of the character:
		# 	o o o
		# 	o x o
		# 	o o o

		# get some targets to attack and turn to these targets
		for o in Enemy.enemyList:
			if o.xInMap == x - 1 and o.yInMap == y:
				self.dir = "left"

				targetList.append(o)
			elif o.xInMap == x - 1 and o.yInMap == y - 1:
				self.dir = "left"

				targetList.append(o)
			elif o.xInMap == x - 1 and o.yInMap == y + 1:
				self.dir = "left"

				targetList.append(o)
			elif o.xInMap == x + 1 and o.yInMap == y:
				self.dir = "right"

				targetList.append(o)
			elif o.xInMap == x + 1 and o.yInMap == y - 1:
				self.dir = "right"

				targetList.append(o)
			elif o.xInMap == x + 1 and o.yInMap == y + 1:
				self.dir = "right"

				targetList.append(o)
			elif o.xInMap == x and o.yInMap == y + 1:
				self.dir = "down"

				targetList.append(o)
			elif o.xInMap == x and o.yInMap == y - 1:
				self.dir = "up"

				targetList.append(o)

		if len(targetList) > 0:
			label = "atk_" + self.dir

			self.animaSet.changeAnimation(label, 0, 0, True)

			self.isAtk = True

			# attack targets
			for t in targetList:
				t.beAttacked(self.atkValue / len(targetList))
		else:
			self.isAtk = False

		return self.isAtk

	def atkOver(self, e):
		if not self.attack():
			self.animaSet.changeAnimation("mov_" + self.dir)