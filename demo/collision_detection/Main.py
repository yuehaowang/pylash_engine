# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

from pylash.core import init, addChild, stage
from pylash.display import Sprite
from pylash.events import MouseEvent
from pylash.geom import Vec2, Polygon, Circle

stageLayer = None
isDragging = False
draggingObj = None

def main():
	global stageLayer

	stageLayer = Sprite()
	stageLayer.graphics.beginFill()
	stageLayer.graphics.drawRect(0, 0, stage.width, stage.height)
	stageLayer.graphics.endFill()
	addChild(stageLayer)

	# add events
	stageLayer.addEventListener(MouseEvent.MOUSE_MOVE, mouseMove)
	stageLayer.addEventListener(MouseEvent.MOUSE_UP, mouseUp)

	# create a circle
	circle = DraggableShape(Circle(0, 0, 60))
	circle.x = circle.y = 150
	stageLayer.addChild(circle)

	# create a square
	square = DraggableShape(Polygon(getPolygonVertices(4, 70)))
	square.x = square.y = 350
	stageLayer.addChild(square)

	# create a pentagon
	pentagon = DraggableShape(Polygon(getPolygonVertices(5, 80)))
	pentagon.x = 150
	pentagon.y = 350
	stageLayer.addChild(pentagon)

	# create a hexagon
	hexagon = DraggableShape(Polygon(getPolygonVertices(6, 90)))
	hexagon.x = 350
	hexagon.y = 150
	stageLayer.addChild(hexagon)

	# create a dodecagon
	dodecagon = DraggableShape(Polygon(getPolygonVertices(12, 100)))
	dodecagon.x = 580
	dodecagon.y = 250
	stageLayer.addChild(dodecagon)

def mouseMove(e):
	global isDragging, draggingObj, stageLayer

	if isDragging and draggingObj != None:
		draggingObj.x = e.offsetX
		draggingObj.y = e.offsetY

		isHit = False

		for o in stageLayer.childList:
			if o.objectIndex != draggingObj.objectIndex and draggingObj.hitTestObject(o):
				isHit = True

				o.draw(DraggableShape.COLOR_2)
			else:
				o.draw(DraggableShape.COLOR_1)

		if isHit:
			draggingObj.draw(DraggableShape.COLOR_2)
		else:
			draggingObj.draw(DraggableShape.COLOR_1)

def mouseUp(e):
	global isDragging, draggingObj

	isDragging = False
	draggingObj = None

def getPolygonVertices(edges, r):
	ca = 0
	aiv = 360 / edges
	ata = math.pi / 180
	res = []

	for k in range(edges):
		x = math.cos(ca * ata) * r
		y = math.sin(ca * ata) * r

		res.append(Vec2(x, y))

		ca += aiv

	return res

# a class for creating a shape with a handle
class DraggableShape(Sprite):
	COLOR_1 = "#333333"
	COLOR_2 = "#FF0000"

	def __init__(self, sh):
		super(DraggableShape, self).__init__()

		self.addShape(sh)
		
		self.shape = sh

		self.handleLayer = Sprite()
		self.handleLayer.graphics.beginFill("#0000FF", 0.6)
		self.handleLayer.graphics.drawCircle(0, 0, 10)
		self.handleLayer.graphics.endFill()
		self.addChild(self.handleLayer)

		self.handleLayer.addEventListener(MouseEvent.MOUSE_DOWN, self.onMouseDown)

		self.draw(DraggableShape.COLOR_1)

	def draw(self, color):
		sh = self.shape

		self.graphics.clear()
		self.graphics.beginFill()
		self.graphics.lineStyle(2, color)

		if isinstance(sh, Circle):
			self.graphics.drawCircle(sh.x, sh.y, sh.r)
		elif isinstance(sh, Polygon):
			vtx = sh.vertices

			self.graphics.moveTo(vtx[0].x, vtx[0].y)

			for v in vtx[1:]:
				self.graphics.lineTo(v.x, v.y)

			self.graphics.closePath()
		
		self.graphics.endFill()

	def onMouseDown(self, e):
		global isDragging, draggingObj

		isDragging = True
		draggingObj = self

init(1000 / 60, "Collision detection", 800, 530, main)