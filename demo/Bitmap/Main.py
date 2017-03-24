# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylash.utils import init, addChild
from pylash.display import Loader, Bitmap, BitmapData

def main():
	loader1 = Loader()
	loader1.load("./1.png")

	bmp1 = Bitmap(BitmapData(loader1.content))
	bmp1.x = bmp1.y = 10
	addChild(bmp1)

	loader2 = Loader()
	loader2.load("./2.png")

	bmp2 = Bitmap(BitmapData(loader2.content))
	bmp2.x = 400
	bmp2.y = 10
	bmp2.rotation = 15
	bmp2.alpha = 0.8
	addChild(bmp2)

init(1000 / 60, "Bitmap", 800, 550, main)