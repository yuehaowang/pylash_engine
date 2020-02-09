# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylash.core import init, addChild
from pylash.loaders import LoadManage
from pylash.display import BitmapData, Bitmap
from pylash.ui import LoadingSample3
from pylash.media import Sound

loadingBar = None

def main():
	global loadingBar

	loadList = [
		{"name" : "bgm", "path" : "./sample.wav"},
		{"name" : "1", "path" : "./1.jpg"},
		{"name" : "2", "path" : "./2.jpg"},
		{"name" : "3", "path" : "./3.jpg"},
		{"name" : "4", "path" : "./4.jpg"}
	]

	loadingBar = LoadingSample3()
	addChild(loadingBar)
	
	LoadManage.load(loadList, loadingBar.setProgress, demoInit)

def demoInit(result):
	global loadingBar

	loadingBar.remove()

	imageList = [BitmapData(result["1"]), BitmapData(result["2"]), BitmapData(result["3"]), BitmapData(result["4"])]

	for i, bmpd in enumerate(imageList):
		bmp = Bitmap(bmpd)
		bmp.scaleX = bmp.scaleY = 0.3
		bmp.x += i * 140
		bmp.y += i * 150
		addChild(bmp)

	sound = Sound(result["bgm"])
	sound.loopCount = Sound.LOOP_FOREVER
	sound.play()

init(1000 / 60, "LoadManage demo", 1000, 800, main)