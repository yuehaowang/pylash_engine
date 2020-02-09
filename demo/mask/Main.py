# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylash.core import init, addChild
from pylash.loaders import LoadManage
from pylash.display import Bitmap, BitmapData, Shape, Sprite

def main():
	loadList = [
		{"name" : "avatar", "path" : "./avatar.jpg"},
        {"name" : "girl", "path" : "./girl.jpg"}
	]

	LoadManage.load(loadList, None, demoInit)

def demoInit(result):
    m1 = Shape()
    m1.graphics.beginFill()
    m1.graphics.drawRect(50, 50, 100, 100)
    m1.graphics.drawCircle(25, 25, 25)
    m1.graphics.moveTo(200, 25)
    m1.graphics.lineTo(150, 125)
    m1.graphics.lineTo(250, 150)
    m1.graphics.closePath()
    m1.graphics.drawRect(40, 175, 150, 150)
    m1.graphics.drawCircle(250, 225, 50)

    img1 = Bitmap(BitmapData(result["avatar"]))
    img1.mask = m1
    addChild(img1)

    img1_bg = Bitmap(BitmapData(result["avatar"]))
    img1_bg.alpha = 0.3
    addChild(img1_bg)


    m2 = Shape()
    m2.graphics.beginFill()
    m2.graphics.drawRect(100, 100, 200, 200)
    m2.graphics.drawCircle(200, 200, 50)

    img2 = Bitmap(BitmapData(result["girl"]))
    img2.x = 320
    img2.mask = m2
    addChild(img2)

    img2_bg = Bitmap(BitmapData(result["girl"]))
    img2_bg.x = 320
    img2_bg.alpha = 0.3
    addChild(img2_bg)

init(1000 / 60, "Mask", 640, 320, main)
