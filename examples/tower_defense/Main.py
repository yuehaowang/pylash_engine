# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import math, copy
from map_data import mapImageList, terrainList
from characters_data import charactersData
from AttackCharacter import AttackCharacter
from Enemy import Enemy

from pylash.utils import stage, init, addChild
from pylash.system import LoadManage
from pylash.display import Sprite, BitmapData, Bitmap, FPS
from pylash.text import TextField, TextFormatWeight
from pylash.events import MouseEvent, Event
from pylash.ui import LoadingSample2, Button, ButtonState

dataList = {}

stageLayer = None
gameLayer = None
ctrlLayer = None
mapLayer = None
characterLayer = None
fps = None

terrain = copy.deepcopy(terrainList)

isMouseDownAtGameLayer = False
mousePrePosition = None

selectedCharacter = None

startBtn = None

start = False

enemyNum = 0

loopSpeed = 30
loopIndex = 0

money = 200
lives = 10

moneyTxt = None
livesTxt = None

def main():
	# save the file paths which need to be loaded
	loadList = [
		{"name" : "map", "path" : "./images/map.jpg"},
		{"name" : "guanyu_mov", "path" : "./images/guanyu_mov.png"},
		{"name" : "guanyu_atk", "path" : "./images/guanyu_atk.png"},
		{"name" : "soldier1_atk", "path" : "./images/soldier1_atk.png"},
		{"name" : "soldier1_mov", "path" : "./images/soldier1_mov.png"},
		{"name" : "soldier2_mov", "path" : "./images/soldier2_mov.png"},
		{"name" : "xiahoudun_atk", "path" : "./images/xiahoudun_atk.png"},
		{"name" : "xiahoudun_mov", "path" : "./images/xiahoudun_mov.png"},
	]

	# create loading page
	loadingPage = LoadingSample2()
	addChild(loadingPage)

	def loadComplete(result):
		global dataList

		loadingPage.remove()

		dataList = result

		gameInit()

	# load files
	LoadManage.load(loadList, loadingPage.setProgress, loadComplete)

def gameInit():
	global stageLayer, gameLayer, ctrlLayer, mapLayer, characterLayer, fps

	# create some layers
	stageLayer = Sprite()
	addChild(stageLayer)

	gameLayer = Sprite()
	stageLayer.addChild(gameLayer)

	mapLayer = Sprite()
	gameLayer.addChild(mapLayer)

	characterLayer = Sprite()
	characterLayer.mouseChildren = False
	gameLayer.addChild(characterLayer)

	ctrlLayer = Sprite()
	stageLayer.addChild(ctrlLayer)

	# add FPS
	fps = FPS()
	addChild(fps)

	addMap()
	initCtrlLayer()
	addEvents()

def addMap():
	global mapLayer

	for y, row in enumerate(mapImageList):
		for x, v in enumerate(row):
			# get the small image's position in map.jpg
			yIndex = math.floor(v / 10)
			xIndex = v % 10

			# get the small image in map.jpg
			bmpd = BitmapData(dataList["map"], xIndex * 48, yIndex * 48, 48, 48)
			# display the small image
			bmp = Bitmap(bmpd)
			bmp.x = x * 48
			bmp.y = y * 48
			mapLayer.addChild(bmp)

def initCtrlLayer():
	global ctrlLayer, selectedCharacter, startBtn, moneyTxt, livesTxt, money, lives

	def selectCharacter(e):
		global selectedCharacter

		name = e.currentTarget.name

		# create selectedCharacter
		selectedCharacter = Sprite()
		selectedCharacter.name = name
		selectedCharacter.mouseShelter = False
		stageLayer.addChild(selectedCharacter)

		bmp = Bitmap(BitmapData(dataList[name + "_mov"], 0, 0, 48, 48))
		selectedCharacter.addChild(bmp)

		# make selectedCharacter move to mouse's position
		selectedCharacter.x = e.offsetX - selectedCharacter.width / 2
		selectedCharacter.y = e.offsetY - selectedCharacter.height / 2

	# draw the background of the ctrlLayer
	ctrlLayer.graphics.beginFill("#333333")
	ctrlLayer.graphics.lineStyle(3, "#222222")
	ctrlLayer.graphics.drawRect(0, 0, 150, stage.height)
	ctrlLayer.graphics.endFill()

	# list of our characters
	ourList = ["guanyu", "xiahoudun", "soldier1"]

	# show selectors of our characters
	selectorsLayer = Sprite()
	ctrlLayer.addChild(selectorsLayer)

	for i, v in enumerate(ourList):
		selector = Sprite()
		selector.name = v
		selectorsLayer.addChild(selector)

		# the appearance of the character
		bmp = Bitmap(BitmapData(dataList[v + "_mov"], 0, 0, 48, 48))
		selector.addChild(bmp)

		# show the cost of the character
		costTxt = TextField()
		costTxt.text = charactersData[v]["cost"]
		costTxt.textColor = "white"
		costTxt.x = (bmp.width - costTxt.width) / 2
		costTxt.y = bmp.height + 10
		selector.addChild(costTxt)

		selector.y = i * 88

		selector.addEventListener(MouseEvent.MOUSE_DOWN, selectCharacter)

	selectorsLayer.x = (ctrlLayer.width - selectorsLayer.width) / 2
	selectorsLayer.y = 40

	# add lives and money text
	livesTxt = TextField()
	livesTxt.text = "Lives: %s" % lives
	livesTxt.x = (ctrlLayer.width - livesTxt.width) / 2
	livesTxt.y = stage.height - 150
	livesTxt.textColor = "white"
	ctrlLayer.addChild(livesTxt)

	moneyTxt = TextField()
	moneyTxt.text = "Money: %s" % money
	moneyTxt.x = (ctrlLayer.width - moneyTxt.width) / 2
	moneyTxt.y = livesTxt.y + 30
	moneyTxt.textColor = "white"
	ctrlLayer.addChild(moneyTxt)

	# add a button to start game
	def clickStartBtn(e):
		global start, enemyNum

		start = True

		enemyNum = 0

		e.currentTarget.state = ButtonState.DISABLED

	normal = Sprite()
	normal.graphics.beginFill("#666666")
	normal.graphics.lineStyle(3, "#222222")
	normal.graphics.drawRect(0, 0, 100, 60)
	normal.graphics.endFill()

	txt = TextField()
	txt.text = "START"
	txt.textColor = "white"
	txt.size = 20
	txt.x = (normal.width - txt.width) / 2
	txt.y = (normal.height - txt.height) / 2
	normal.addChild(txt)

	over = Sprite()
	over.graphics.beginFill("#888888")
	over.graphics.lineStyle(3, "#222222")
	over.graphics.drawRect(0, 0, 100, 60)
	over.graphics.endFill()

	txt = TextField()
	txt.text = "START"
	txt.textColor = "white"
	txt.size = 20
	txt.x = (over.width - txt.width) / 2
	txt.y = (over.height - txt.height) / 2
	over.addChild(txt)

	disabled = Sprite()
	disabled.graphics.beginFill("#666666")
	disabled.graphics.lineStyle(3, "#222222")
	disabled.graphics.drawRect(0, 0, 100, 60)
	disabled.graphics.endFill()

	txt = TextField()
	txt.text = "START"
	txt.textColor = "#333333"
	txt.size = 20
	txt.x = (disabled.width - txt.width) / 2
	txt.y = (disabled.height - txt.height) / 2
	disabled.addChild(txt)

	startBtn = Button(normal, over, None, disabled)
	startBtn.x = (ctrlLayer.width - startBtn.width) / 2
	startBtn.y = stage.height - 80
	ctrlLayer.addChild(startBtn)

	startBtn.addEventListener(MouseEvent.MOUSE_UP, clickStartBtn)

	ctrlLayer.x = stage.width - ctrlLayer.width

def addEvents():
	global gameLayer, ctrlLayer

	def onMouseDownAtGameLayer(e):
		global isMouseDownAtGameLayer, mousePrePosition

		isMouseDownAtGameLayer = True

		mousePrePosition = {"x" : e.offsetX, "y" : e.offsetY}

	def onMouseMoveAtGameLayer(e):
		global isMouseDownAtGameLayer, mapLayer, mousePrePosition, gameLayer

		if isMouseDownAtGameLayer and mousePrePosition:
			# make the map follow mouse if you hold your mouse pressed
			gameLayer.x += e.offsetX - mousePrePosition["x"]
			gameLayer.y += e.offsetY - mousePrePosition["y"]

			mousePrePosition = {"x" : e.offsetX, "y" : e.offsetY}

			# limit to the area of moving map
			minX = stage.width - 150 - mapLayer.width
			minY = stage.height - mapLayer.height

			if gameLayer.x > 0:
				gameLayer.x = 0
			elif gameLayer.x < minX:
				gameLayer.x = minX

			if gameLayer.y > 0:
				gameLayer.y = 0
			elif gameLayer.y < minY:
				gameLayer.y = minY

	def onMouseUpAtGameLayer(e):
		global isMouseDownAtGameLayer, mousePrePosition, selectedCharacter

		isMouseDownAtGameLayer = False

		mousePrePosition = None

		# if selectedCharacter exist, create our character
		if not selectedCharacter:
			return

		createOurCharacter(selectedCharacter.name, math.floor(e.selfX / 48), math.floor(e.selfY / 48))

		selectedCharacter.remove()

		selectedCharacter = None

	def onMouseMoveAtStageLayer(e):
		if not selectedCharacter:
			return

		# make selectedCharacter follow mouse
		selectedCharacter.x = e.offsetX - selectedCharacter.width / 2
		selectedCharacter.y = e.offsetY - selectedCharacter.height / 2

	def onMouseUpAtCtrlLayer(e):
		global isMouseDownAtGameLayer, mousePrePosition, selectedCharacter

		# make map stop following mouse
		isMouseDownAtGameLayer = False

		mousePrePosition = None

		# if selectedCharacter exist, remove it
		if not selectedCharacter:
			return

		selectedCharacter.remove()

		selectedCharacter = None

	gameLayer.addEventListener(MouseEvent.MOUSE_DOWN, onMouseDownAtGameLayer)
	gameLayer.addEventListener(MouseEvent.MOUSE_MOVE, onMouseMoveAtGameLayer)
	gameLayer.addEventListener(MouseEvent.MOUSE_UP, onMouseUpAtGameLayer)
	
	stageLayer.addEventListener(MouseEvent.MOUSE_MOVE, onMouseMoveAtStageLayer)
	stageLayer.addEventListener(Event.ENTER_FRAME, loop)

	ctrlLayer.addEventListener(MouseEvent.MOUSE_UP, onMouseUpAtCtrlLayer)

def createOurCharacter(name, x, y):
	global characterLayer, money, terrain

	# if our characters cannot stand on the block of the map
	if terrain[y][x] != 0:
		return

	# create our character
	cost = charactersData[name]["cost"]

	if money - cost < 0:
		return

	money -= cost

	refreshMoneyTxt()

	character = AttackCharacter(name, dataList[name + "_mov"], dataList[name + "_atk"], x, y, charactersData[name]["atk"])
	characterLayer.addChild(character)

	terrain[y][x] = -1

	AttackCharacter.ourList.append(character)

def loop(e):
	global characterLayer, loopIndex, loopSpeed, start, enemyNum

	if not start:
		return

	# control the speed of adding enemy
	loopIndex += 1

	if loopIndex < loopSpeed:
		return

	loopIndex = 0

	# control the number of enemy
	if enemyNum >= 15:
		start = False

		return

	# add a enmey
	enemy = Enemy(dataList["soldier2_mov"], 1, 15)
	characterLayer.addChild(enemy)

	Enemy.enemyList.append(enemy)

	enemyNum += 1

	# add customized events
	enemy.addEventListener(Enemy.EVENT_DIE, enemyDie)
	enemy.addEventListener(Enemy.EVENT_ARRIVE, enemyArrive)

def enemyArrive(e):
	global lives, livesTxt, ctrlLayer

	o = e.currentTarget

	Enemy.enemyList.remove(o)

	o.remove()

	lives -= 1

	livesTxt.text = "Lives: %s" % lives
	livesTxt.x = (ctrlLayer.width - livesTxt.width) / 2

	if lives <= 0:
		gameOver()

		return

	recoveryStartBtn()

def enemyDie(e):
	global money, moneyTxt, ctrlLayer

	o = e.currentTarget

	Enemy.enemyList.remove(o)

	o.remove()

	if money <= 999:
		money += 10

		refreshMoneyTxt()

	recoveryStartBtn()

def refreshMoneyTxt():
	global moneyTxt, ctrlLayer

	moneyTxt.text = "Money: %s" % money
	moneyTxt.x = (ctrlLayer.width - moneyTxt.width) / 2

def recoveryStartBtn():
	global startBtn

	if len(Enemy.enemyList) == 0 and startBtn.state == ButtonState.DISABLED and not start:
		startBtn.state = ButtonState.NORMAL

def gameOver():
	global stageLayer, selectedCharacter, start, enemyNum, isMouseDownAtGameLayer

	for o in AttackCharacter.ourList:
		o.animaSet.currentAnimation.removeAllEventListeners()
		o.animaSet.currentAnimation.stop()

	for o in Enemy.enemyList:
		o.animaSet.currentAnimation.removeAllEventListeners()
		o.animaSet.currentAnimation.stop()

	start = False

	stageLayer.mouseEnabled = False
	stageLayer.mouseChildren = False

	if selectedCharacter:
		selectedCharacter.remove()

	selectedCharacter = None

	enemyNum = 0
	isMouseDownAtGameLayer = False

	resultLayer = Sprite()
	addChild(resultLayer)

	# add hint of game over
	hintTxt = TextField()
	hintTxt.textColor = "red"
	hintTxt.text = "Game Over!"
	hintTxt.weight = TextFormatWeight.BOLD
	hintTxt.size = 50
	hintTxt.x = (stage.width - hintTxt.width) / 2
	hintTxt.y = (stage.height - hintTxt.height) / 2 - 40
	resultLayer.addChild(hintTxt)

	# add restart button
	def clickRestartBtn(e):
		global money, lives, loopIndex, stageLayer, fps, terrain

		AttackCharacter.ourList = []
		Enemy.enemyList = []
		
		loopIndex = 0
		money = 200
		lives = 10

		terrain = copy.deepcopy(terrainList)

		stageLayer.remove()
		fps.remove()

		resultLayer.remove()

		gameInit()

	normal = Sprite()
	normal.graphics.beginFill("#666666")
	normal.graphics.lineStyle(3, "#222222")
	normal.graphics.drawRect(0, 0, 130, 60)
	normal.graphics.endFill()

	txt = TextField()
	txt.text = "RESTART"
	txt.textColor = "white"
	txt.size = 20
	txt.x = (normal.width - txt.width) / 2
	txt.y = (normal.height - txt.height) / 2
	normal.addChild(txt)

	over = Sprite()
	over.graphics.beginFill("#888888")
	over.graphics.lineStyle(3, "#222222")
	over.graphics.drawRect(0, 0, 130, 60)
	over.graphics.endFill()

	txt = TextField()
	txt.text = "RESTART"
	txt.textColor = "white"
	txt.size = 20
	txt.x = (over.width - txt.width) / 2
	txt.y = (over.height - txt.height) / 2
	over.addChild(txt)

	restartBtn = Button(normal, over)
	restartBtn.x = (stage.width - restartBtn.width) / 2
	restartBtn.y = stage.height / 2 + 30
	resultLayer.addChild(restartBtn)

	restartBtn.addEventListener(MouseEvent.MOUSE_UP, clickRestartBtn)

init(1000 / 60, "Tower Defense", 726, 480, main)