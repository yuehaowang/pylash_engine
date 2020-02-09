# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from pylash.core import init, addChild
from pylash.loaders import MediaLoader, LoaderEvent
from pylash.events import MouseEvent
from pylash.media import Sound, Video, MediaEvent
from pylash.ui import ButtonSample


def initEffSound(e):
	effSound = Sound(e.target)
	effSound.loopCount = 2
	effSound.addEventListener(MediaEvent.LOOP, lambda e: print(
		"Sound Effect Loop. Position: %s, Playing: %s" % (e.currentTarget.position, e.currentTarget.playing)
	))
	effSound.addEventListener(MediaEvent.COMPLETE, lambda e: print(
		"Sound Effect Complete. Position: %s, Playing: %s" % (e.currentTarget.position, e.currentTarget.playing)
	))

	btnPlay = ButtonSample(text="Play Sound Effect")
	btnPlay.x = 100
	btnPlay.y = 100
	btnPlay.addEventListener(MouseEvent.MOUSE_DOWN, lambda e: effSound.play())
	addChild(btnPlay)

def initBgmSound(e):
	bgmSound = Sound(e.target)
	bgmSound.loopCount = Sound.LOOP_FOREVER
	bgmSound.volume = 30
	bgmSound.play()

	btnPlay = ButtonSample(text="Play Bgm")
	btnPlay.x = 100
	btnPlay.y = 140
	btnPlay.addEventListener(MouseEvent.MOUSE_DOWN, lambda e: bgmSound.play())
	addChild(btnPlay)
	btnPause = ButtonSample(text="Pause Bgm")
	btnPause.x = 100
	btnPause.y = 180
	btnPause.addEventListener(MouseEvent.MOUSE_DOWN, lambda e: bgmSound.pause())
	addChild(btnPause)
	btnStop = ButtonSample(text="Stop Bgm")
	btnStop.x = 100
	btnStop.y = 220
	btnStop.addEventListener(MouseEvent.MOUSE_DOWN, lambda e: bgmSound.stop())
	addChild(btnStop)

def initVideo(e):
	video = Video(e.target)
	video.loopCount = 5
	video.x = 350
	video.y = 80
	video.scaleX = 0.3
	video.scaleY = 0.3
	video.play()
	addChild(video)
	video.addEventListener(MediaEvent.SIZE_CHANGED, lambda e: print("Video Size: ", video.width, video.height))
	video.addEventListener(MediaEvent.LOOP, lambda e: print(
		"Video Loop. Position: %s, Playing: %s" % (e.currentTarget.position, e.currentTarget.playing)
	))
	video.addEventListener(MediaEvent.COMPLETE, lambda e: print(
		"Video Complete. Position: %s, Playing: %s" % (e.currentTarget.position, e.currentTarget.playing)
	))

def main():
	loader1 = MediaLoader()
	loader1.addEventListener(LoaderEvent.COMPLETE, initEffSound)
	loader1.load("ring.wav")

	loader2 = MediaLoader()
	loader2.addEventListener(LoaderEvent.COMPLETE, initBgmSound)
	loader2.load("bgm.mp3")

	loader3 = MediaLoader()
	loader3.addEventListener(LoaderEvent.COMPLETE, initVideo)
	loader3.load("sunset.mp4")


init(1000 / 60, "Media", 800, 400, main)
