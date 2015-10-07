# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from Player import Player
from Item import Item

import sys

sys.path.insert(0, "../../")
from pylash.utils import stage, init, addChild, KeyCode
from pylash.system import LoadManage
from pylash.display import Sprite, BitmapData, Bitmap, FPS
from pylash.text import TextField, TextFormatWeight
from pylash.events import MouseEvent, Event, KeyboardEvent
from pylash.ui import LoadingSample1

dataList = {}

stageLayer = None
player = None
itemLayer = None
scoreTxt = None
addItemSpeed = 40
addItemSpeedIndex = 0
score = 0
keyboardEnabled = False

def main():
	# save the file paths which need to be loaded
	loadList = [
		{"name" : "player", "path" : "./images/player.png"},
		{"name" : "bg", "path" : "./images/bg.jpg"},
		{"name" : "item0", "path" : "./images/item0.png"},
		{"name" : "item1", "path" : "./images/item1.png"},
		{"name" : "item2", "path" : "./images/item2.png"},
		{"name" : "item3", "path" : "./images/item3.png"},
		{"name" : "item4", "path" : "./images/item4.png"},
		{"name" : "item5", "path" : "./images/item5.png"},
		{"name" : "item6", "path" : "./images/item6.png"},
		{"name" : "item7", "path" : "./images/item7.png"}
	]

	# create loading page
	loadingPage = LoadingSample1()
	addChild(loadingPage)

	def loadComplete(result):
		loadingPage.remove()

		gameInit(result)

	# load files
	LoadManage.load(loadList, loadingPage.setProgress, loadComplete)

def gameInit(result):
	global dataList, stageLayer

	dataList = result

	# create stage layer
	stageLayer = Sprite()
	addChild(stageLayer)

	# add FPS
	fps = FPS()
	addChild(fps)

	# add background
	bg = Bitmap(BitmapData(dataList["bg"]))
	stageLayer.addChild(bg)

	# add some text fields
	titleTxt = TextField()
	titleTxt.text = "Get Furit"
	titleTxt.size = 70
	titleTxt.textColor = "red"
	titleTxt.x = (stage.width - titleTxt.width) / 2
	titleTxt.y = 100
	stageLayer.addChild(titleTxt)

	hintTxt = TextField()
	hintTxt.text = "Tap to Start the Game!~"
	hintTxt.textColor = "red"
	hintTxt.size = 40
	hintTxt.x = (stage.width - hintTxt.width) / 2
	hintTxt.y = 300
	stageLayer.addChild(hintTxt)

	engineTxt = TextField()
	engineTxt.text = "- Powered by Pylash -"
	engineTxt.textColor = "red"
	engineTxt.size = 20
	engineTxt.weight = TextFormatWeight.BOLD
	engineTxt.italic = True
	engineTxt.x = (stage.width - engineTxt.width) / 2
	engineTxt.y = 500
	stageLayer.addChild(engineTxt)

	# add event that the game will start when you click
	stageLayer.addEventListener(MouseEvent.MOUSE_UP, startGame)

	# add keyboard events to control player
	stage.addEventListener(KeyboardEvent.KEY_DOWN, keyDown)
	stage.addEventListener(KeyboardEvent.KEY_UP, keyUp)

def startGame(e):
	global player, itemLayer, scoreTxt, addItemSpeedIndex, score, keyboardEnabled

	# reset some global variables
	addItemSpeedIndex = 0
	score = 0

	keyboardEnabled = True

	stageLayer.removeAllChildren()
	stageLayer.removeAllEventListeners()

	# add background
	bg = Bitmap(BitmapData(dataList["bg"]))
	stageLayer.addChild(bg)

	# create player
	player = Player(dataList["player"])
	player.x = (stage.width - player.width) / 2
	player.y = 450
	stageLayer.addChild(player)

	# create item layer to contain objects falling from the top
	itemLayer = Sprite()
	stageLayer.addChild(itemLayer)
	# set the hit target to confirm a object which will be checked collision with items
	itemLayer.hitTarget = player

	# add score text field
	scoreTxt = TextField()
	scoreTxt.text = "Score: 0"
	scoreTxt.textColor = "red"
	scoreTxt.size = 30
	scoreTxt.x = scoreTxt.y = 30
	scoreTxt.weight = TextFormatWeight.BOLDER
	stageLayer.addChild(scoreTxt)

	# add events
	stageLayer.addEventListener(MouseEvent.MOUSE_DOWN, onMouseDown)
	stageLayer.addEventListener(MouseEvent.MOUSE_UP, onMouseUp)
	stageLayer.addEventListener(Event.ENTER_FRAME, loop)

def keyDown(e):
	global player

	if not keyboardEnabled or not player:
		return

	if e.keyCode == KeyCode.KEY_RIGHT:
		player.direction = "right"
	elif e.keyCode == KeyCode.KEY_LEFT:
		player.direction = "left"

def keyUp(e):
	global player

	if not keyboardEnabled or not player:
		return

	player.direction = None

def onMouseDown(e):
	global player
	
	if e.offsetX > (stage.width / 2):
		player.direction = "right"
	else:
		player.direction = "left"

def onMouseUp(e):
	global player

	player.direction = None

def loop(e):
	global player, itemLayer, addItemSpeed, addItemSpeedIndex

	player.loop()

	for o in itemLayer.childList:
		o.loop()

	# control the speed of adding a item
	if addItemSpeedIndex < addItemSpeed:
		addItemSpeedIndex += 1

		return

	addItemSpeedIndex = 0

	# get random item
	randomNum = random.randint(0, 7)

	# add a item
	item = Item(dataList["item" + str(randomNum)])
	item.index = randomNum
	item.x = int(random.randint(30, stage.width - 100))
	itemLayer.addChild(item)
	# add ourselves events
	item.addEventListener(Item.EVENT_ADD_SCORE, addScore)
	item.addEventListener(Item.EVENT_GAME_OVER, gameOver)

def addScore(e):
	global score, scoreTxt

	score += 1

	scoreTxt.text = "Score: %s" % score

def gameOver(e):
	global player, scoreTxt, stageLayer, keyboardEnabled

	keyboardEnabled = False

	stageLayer.removeAllEventListeners()

	scoreTxt.remove()
	player.animation.stop()

	resultTxt = TextField()
	resultTxt.text = "Final Score: %s" % score
	resultTxt.size = 40
	resultTxt.weight = TextFormatWeight.BOLD
	resultTxt.textColor = "orangered"
	resultTxt.x = (stage.width - resultTxt.width) / 2
	resultTxt.y = 250
	stageLayer.addChild(resultTxt)

	hintTxt = TextField()
	hintTxt.text = "Double Click to Restart"
	hintTxt.size = 35
	hintTxt.textColor = "red"
	hintTxt.x = (stage.width - hintTxt.width) / 2
	hintTxt.y = 320
	stageLayer.addChild(hintTxt)

	# add double click event to restart
	stageLayer.addEventListener(MouseEvent.DOUBLE_CLICK, startGame)

init(1000 / 60, "Get Fruits", 800, 600, main)