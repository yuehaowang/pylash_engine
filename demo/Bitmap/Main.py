# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylash.core import init, addChild
from pylash.loaders import ImageLoader, LoaderEvent
from pylash.display import Bitmap, BitmapData

def displayImg1(e):
	bmp1 = Bitmap(BitmapData(e.target))
	bmp1.x = bmp1.y = 10
	addChild(bmp1)

def displayImg2(e):
	bmp2 = Bitmap(BitmapData(e.currentTarget.content))
	bmp2.x = 400
	bmp2.y = 10
	bmp2.rotation = 15
	bmp2.alpha = 0.8
	addChild(bmp2)

def main():
	loader1 = ImageLoader()
	loader1.addEventListener(LoaderEvent.COMPLETE, displayImg1)
	loader1.load("./1.png")

	loader2 = ImageLoader()
	loader2.addEventListener(LoaderEvent.COMPLETE, displayImg2)
	loader2.load("./2.png")

init(1000 / 60, "Bitmap", 800, 550, main)