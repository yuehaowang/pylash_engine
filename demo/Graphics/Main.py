# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylash.utils import init, addChild
from pylash.display import Sprite, Graphics

def main():
	layer = Sprite()
	layer.x = layer.y = 50
	addChild(layer)

	layer.graphics.beginFill()
	layer.graphics.lineStyle(5, "green", 0.2)
	layer.graphics.drawRect(0, 0, 150, 150)
	layer.graphics.endFill()

	layer.graphics.beginFill()
	layer.graphics.lineStyle(5, "green", 0.8)
	layer.graphics.drawRect(200, 0, 150, 150)
	layer.graphics.endFill()

	layer.graphics.beginFill("lightgreen")
	layer.graphics.lineStyle(5, "green", 0.5)
	layer.graphics.drawRect(400, 0, 150, 150)
	layer.graphics.endFill()


	layer.graphics.beginFill()
	layer.graphics.lineStyle(5, "green", 0.2)
	layer.graphics.drawCircle(75, 275, 75)
	layer.graphics.endFill()

	layer.graphics.beginFill()
	layer.graphics.lineStyle(5, "green", 0.8)
	layer.graphics.drawCircle(275, 275, 75)
	layer.graphics.endFill()

	layer.graphics.beginFill("lightgreen")
	layer.graphics.lineStyle(5, "green", 0.5)
	layer.graphics.drawCircle(475, 275, 75)
	layer.graphics.endFill()


	layer.graphics.beginFill()
	layer.graphics.lineStyle(5, "green", 0.2)
	layer.graphics.moveTo(0, 498)
	layer.graphics.lineTo(75, 400)
	layer.graphics.lineTo(150, 498)
	layer.graphics.lineTo(0, 498)
	layer.graphics.endFill()

	layer.graphics.beginFill()
	layer.graphics.lineStyle(5, "green", 0.8)
	layer.graphics.moveTo(200, 498)
	layer.graphics.lineTo(275, 400)
	layer.graphics.lineTo(350, 498)
	layer.graphics.lineTo(200, 498)
	layer.graphics.endFill()

	layer.graphics.beginFill("lightgreen")
	layer.graphics.lineStyle(5, "green", 0.5)
	layer.graphics.moveTo(400, 498)
	layer.graphics.lineTo(475, 400)
	layer.graphics.lineTo(550, 498)
	layer.graphics.lineTo(400, 498)
	layer.graphics.endFill()

init(1000 / 60, "Graphics demo", 700, 600, main)