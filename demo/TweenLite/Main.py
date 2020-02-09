# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylash.core import init, addChild
from pylash.loaders import LoadManage
from pylash.display import BitmapData, Bitmap
from pylash.ui import LoadingSample2
from pylash.transitions import TweenLite, Easing

loadingBar = None

def main():
	global loadingBar

	loadList = [
		{"name" : "1", "path" : "./1.png"},
		{"name" : "2", "path" : "./2.png"},
		{"name" : "3", "path" : "./3.png"}
	]

	loadingBar = LoadingSample2()
	addChild(loadingBar)

	LoadManage.load(loadList, loadingBar.setProgress, demoInit)

def demoInit(result):
	global loadingBar

	loadingBar.remove()

	dataList = result

	bmp1 = Bitmap(BitmapData(dataList["1"]))
	bmp1.x = 530
	bmp1.y = 30
	addChild(bmp1)

	bmp2 = Bitmap(BitmapData(dataList["2"]))
	bmp2.x = 530
	bmp2.y = 230
	addChild(bmp2)

	bmp3 = Bitmap(BitmapData(dataList["3"]))
	bmp3.x = 530
	bmp3.y = 460
	addChild(bmp3)

	TweenLite.to(bmp1, 3, {
		"x" : 30,
		"alpha" : 0.5,
		"ease" : Easing.Sine.easeOut
	})

	TweenLite.to(bmp2, 3, {
		"x" : 50,
		"rotation" : 360,
		"ease" : Easing.Back.easeIn
	})

	TweenLite.to(bmp3, 3, {
		"x" : 250,
		"y" : 700,
		"scaleX" : -1,
		"scaleY" : -1,
		"ease" : Easing.Quad.easeIn
	}).to(bmp3, 2, {
		"delay" : 1,
		"scaleY" : 1,
		"y" : 460
	})

init(1000 / 60, "TweenLite demo", 800, 750, main)