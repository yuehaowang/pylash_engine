# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from GameLayer import GameLayer

from pylash.utils import init, addChild, removeChild, stage
from pylash.display import Sprite, Bitmap, BitmapData
from pylash.text import TextField, TextFormatWeight
from pylash.system import LoadManage
from pylash.events import MouseEvent
from pylash.ui import LoadingSample2

dataList = {}
beginningLayer = None
gameLayer = None
loadingPage = None

def main():
	global loadingPage

	# save the file path which needs to be loaded
	loadList = [
		{"name" : "bg", "path" : "./images/bg.jpg"}
	]

	# create loading page
	loadingPage = LoadingSample2()
	addChild(loadingPage)

	# load file
	LoadManage.load(loadList, loadingPage.setProgress, gameInit)

def gameInit(result):
	global beginningLayer, dataList, loadingPage

	loadingPage.remove()

	# save the data which is loaded
	dataList = result

	# create a Sprite object
	beginningLayer = Sprite()
	# push the Sprite object into display list to show
	addChild(beginningLayer)

	# add background
	bg = Bitmap(BitmapData(dataList["bg"], 330, 300))
	beginningLayer.addChild(bg)

	# add some text fields
	title = TextField()
	title.text = "Find Character"
	title.font = "Microsoft YaHei"
	title.size = 60
	title.weight = TextFormatWeight.BOLD
	title.x = (stage.width - title.width) / 2
	title.y = 150
	beginningLayer.addChild(title)

	hintTxt = TextField()
	hintTxt.text = "Tap to Start The Game"
	hintTxt.font = "Microsoft YaHei"
	hintTxt.size = 30
	hintTxt.x = (stage.width - hintTxt.width) / 2
	hintTxt.y = 300
	beginningLayer.addChild(hintTxt)

	engineTxt = TextField()
	engineTxt.text = "- Powered by Pylash -"
	engineTxt.font = "Microsoft YaHei"
	engineTxt.size = 20
	engineTxt.italic = True
	engineTxt.x = (stage.width - engineTxt.width) / 2
	engineTxt.y = 400
	beginningLayer.addChild(engineTxt)

	# add event that game will start when you click
	beginningLayer.addEventListener(MouseEvent.MOUSE_UP, startGame)

def startGame(e):
	global beginningLayer, gameLayer

	beginningLayer.remove()

	gameLayer = GameLayer(dataList["bg"])
	addChild(gameLayer)

init(30, "Find Character", 700, 600, main)