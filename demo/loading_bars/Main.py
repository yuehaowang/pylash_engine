# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylash.core import init, addChild, stage
from pylash.loaders import LoadManage
from pylash.events import MouseEvent, LoopEvent
from pylash.display import Sprite, TextField
from pylash.ui import LoadingSample1, LoadingSample2, LoadingSample3, ButtonSample

loopFrameIndex = 0
loopFrameMax = 5
progress = 0

def main():
    controlLayer = Sprite()
    addChild(controlLayer)

    title = TextField()
    title.size = 25
    title.text = "Choose A Loading Bar"
    controlLayer.addChild(title)

    btn1 = ButtonSample(text = "LoadingSample1", size = 30)
    btn1.y = 100
    btn1.addEventListener(MouseEvent.MOUSE_UP, lambda e: addLoadingBar(1))
    controlLayer.addChild(btn1)
    btn2 = ButtonSample(text = "LoadingSample2", size = 30)
    btn2.y = 180
    btn2.addEventListener(MouseEvent.MOUSE_UP, lambda e: addLoadingBar(2))
    controlLayer.addChild(btn2)
    btn3 = ButtonSample(text = "LoadingSample3", size = 30)
    btn3.y = 260
    btn3.addEventListener(MouseEvent.MOUSE_UP, lambda e: addLoadingBar(3))
    controlLayer.addChild(btn3)

    title.x = (controlLayer.width - title.width) / 2
    controlLayer.x = (stage.width - controlLayer.width) / 2
    controlLayer.y = (stage.height - controlLayer.height) / 2

def onFrame(e):
    global loopFrameIndex, loopFrameMax, progress

    if loopFrameIndex < loopFrameMax:
        loopFrameIndex += 1
        return
    else:
        loopFrameIndex = 0

    progress += 1
    e.currentTarget.setProgress(progress)

    if progress >= 100:
        e.currentTarget.remove()

def addLoadingBar(index):
    global loopFrameIndex, progress
    loopFrameIndex = 0
    progress = 0

    loadingBar = None
    if index == 1:
        loadingBar = LoadingSample1()
    elif index == 2:
        loadingBar = LoadingSample2()
    elif index == 3:
        loadingBar = LoadingSample3()
    
    if not loadingBar:
        return
    loadingBar.addEventListener(LoopEvent.ENTER_FRAME, onFrame)
    addChild(loadingBar)

init(1000 / 60, "Loading Bars", 800, 600, main)
