# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylash.utils import init, addChild
from pylash.system import LoadManage
from pylash.events import MouseEvent
from pylash.display import BitmapData, Bitmap, Sprite, AnimationSet, Animation, AnimationPlayMode
from pylash.ui import LoadingSample2, ButtonSample

loadingBar = None
animaSet = None

def main():
	global loadingBar

	loadList = [
		{"name" : "atk", "path" : "./atk.png"},
		{"name" : "mov", "path" : "./mov.png"}
	]

	loadingBar = LoadingSample2()
	addChild(loadingBar)

	LoadManage.load(loadList, loadingBar.setProgress, demoInit)

def demoInit(result):
	global loadingBar, animaSet

	loadingBar.remove()

	# move image
	mov = result["mov"]
	# atk image
	atk = result["atk"]


	###
	# create animation set to contain a sort of animations
	###
	animaSet = AnimationSet()
	animaSet.x = animaSet.y = 100
	addChild(animaSet)


	###
	# move animation
	###
	# get move animation frame list
	frameList = Animation.divideUniformSizeFrames(48, 96, 1, 2)

	# move down
	bmpd = BitmapData(mov, 0, 0, 48, 96)
	anima = Animation(bmpd, frameList)
	animaSet.addAnimation("move_down", anima)
	# move up
	bmpd = BitmapData(mov, 0, 96, 48, 96)
	anima = Animation(bmpd, frameList)
	animaSet.addAnimation("move_up", anima)
	# move left
	bmpd = BitmapData(mov, 0, 192, 48, 96)
	anima = Animation(bmpd, frameList)
	animaSet.addAnimation("move_left", anima)
	# move right
	bmpd = BitmapData(mov, 0, 192, 48, 96)
	anima = Animation(bmpd, frameList)
	anima.mirroring = True
	animaSet.addAnimation("move_right", anima)


	###
	# attack animation
	###
	# get atk animation frame list
	frameList = Animation.divideUniformSizeFrames(64, 256, 1, 4)

	# atk down
	bmpd = BitmapData(atk, 0, 0, 64, 256)
	anima = Animation(bmpd, frameList)
	animaSet.addAnimation("atk_down", anima)
	# atk up
	bmpd = BitmapData(atk, 0, 256, 64, 256)
	anima = Animation(bmpd, frameList)
	animaSet.addAnimation("atk_up", anima)
	# atk left
	bmpd = BitmapData(atk, 0, 512, 64, 256)
	anima = Animation(bmpd, frameList)
	animaSet.addAnimation("atk_left", anima)
	# atk right
	bmpd = BitmapData(atk, 0, 512, 64, 256)
	anima = Animation(bmpd, frameList)
	anima.mirroring = True
	animaSet.addAnimation("atk_right", anima)

	for n in animaSet.animationList:
		o = animaSet.animationList[n]

		o.playMode = AnimationPlayMode.VERTICAL
		o.speed = 5

		# if atk animation... (because atk animation is bigger than move animation)
		if n.find("atk") >= 0:
			o.x -= 8
			o.y -= 8

	animaSet.changeAnimation("move_down")


	###
	# create buttons
	###
	btnList = [
		"move down", "move up", "move right", "move left",
		"atk down", "atk up", "atk right", "atk left"
	]

	btnLayer = Sprite()
	btnLayer.x = 200
	btnLayer.y = 50
	addChild(btnLayer)

	for i, n in enumerate(btnList):
		btn = ButtonSample(text = n)
		btn.label = n
		btnLayer.addChild(btn)
		btn.addEventListener(MouseEvent.MOUSE_DOWN, onBtnClick)

		btn.x = (0 if (4 - i) > 0 else 1) * 150
		btn.y = (i % 4) * 50

def onBtnClick(e):
	animaSet.changeAnimation(e.currentTarget.label.replace(" ", "_"))

init(1000 / 60, "Animation demo", 600, 400, main)