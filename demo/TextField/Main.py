# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylash.core import init, addChild
from pylash.display import TextField, TextFormatWeight

def main():
	t1 = TextField()
	t1.x = t1.y = 50
	t1.size = 30
	t1.text = "Hello World!"
	addChild(t1)

	t2 = TextField()
	t2.x = 50
	t2.y = 150
	t2.text = "Hello Pylash~"
	t2.rotation = 30
	t2.size = 50
	t2.textColor = "#FF4500"
	t2.weight = TextFormatWeight.BOLD
	addChild(t2)

	t3 = TextField()
	t3.x = 300
	t3.y = 130
	t3.text = "Based on Python3, PySide2"
	t3.alpha = 0.7
	t3.size = 40
	t3.textColor = "#0000FF"
	t3.italic = True
	addChild(t3)

init(1000 / 60, "TextField", 800, 430, main)