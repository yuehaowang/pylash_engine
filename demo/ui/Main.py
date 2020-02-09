# !/usr/bin/env python3
# -*- coding: utf-8 -*-


from pylash.core import init, addChild, removeChild
from pylash.events import MouseEvent
from pylash.display import Sprite
from pylash.ui import ButtonSample, LineEdit, LineEditEvent

def main():
	btn1 = ButtonSample(text = "Button 1")
	btn1.x = 100
	btn1.y = 50
	btn1.addEventListener(MouseEvent.MOUSE_DOWN, lambda e: print("Click Button 1"))
	addChild(btn1)

	btn2 = ButtonSample(
		text = "Button 2",
		roundBorder = False,
		backgroundColor = {"normalState" : "#00AA00", "overState" : "#00FF00"},
		lineColor = "green",
		size = 30,
		textColor = "#222222"
	)
	btn2.x = 100
	btn2.y = 90
	btn2.addEventListener(MouseEvent.MOUSE_DOWN, lambda e: print("Click Button 2"))
	addChild(btn2)

	lineEdit1 = LineEdit()
	lineEdit1.x = 100
	lineEdit1.y = 150
	addChild(lineEdit1)

	bgLayer = Sprite()
	bgLayer.graphics.beginFill("lightgreen")
	bgLayer.graphics.lineStyle(5, "green", 0.5)
	bgLayer.graphics.drawRect(0, 0, 300, 50)
	bgLayer.graphics.endFill()
	lineEdit2 = LineEdit(bgLayer)
	lineEdit2.text = "Input 2"
	lineEdit2.x = 100
	lineEdit2.y = 200
	lineEdit2.size = 30
	lineEdit2.setMargins(10, 0, 10, 0)
	lineEdit2.addEventListener(LineEditEvent.FOCUS_IN, lambda e: print("Focus in Line Edit 2"))
	lineEdit2.addEventListener(LineEditEvent.FOCUS_OUT, lambda e: print("Focus out Line Edit 2"))
	addChild(lineEdit2)


init(1000 / 60, "UI", 600, 430, main)
