import math
from PyQt4 import QtGui
from .utils import Object


__author__ = "Yuehao Wang"


class Point(Object):
	def __init__(self, x = 0, y = 0):
		super(Point, self).__init__()

		if not isinstance(x, (int, float)):
			x = 0
		if not isinstance(y, (int, float)):
			y = 0
		
		self.x = x
		self.y = y

	def __str__(self):
		return "Point(%s, %s)" % (self.x, self.y)

	def distance(p1, p2):
		return Point.distance2(p1.x, p1.y, p2.x, p2.y)

	def distance2(x1, y1, x2, y2):
		x = x1 - x2
		y = y1 - y2

		return math.sqrt(x * x + y * y)

	def interpolate(p1, p2, f):
		return Point(p1.x + (p2.x - p1.x) * (1 - f), p1.y + (p2.y - p1.y) * (1 - f))

	def polar(l, a):
		return Point(l * math.cos(a), l * math.sin(a))

	def length(self):
		return Point.distance2(self.x, self.y, 0, 0)

	def add(self, v):
		return Point(self.x + v.x, self.y + v.y)

	def setTo(self, x, y):
		if not isinstance(x, (int, float)):
			x = 0
		if not isinstance(y, (int, float)):
			y = 0

		self.x = x
		self.y = y

	def copyFrom(self, s):
		self.setTo(s.x, s.y)

	def equals(self, t):
		return self.x == t.x and self.y == t.y

	def normalize(self, t):
		scale = t / self.length()

		self.x *= scale
		self.y *= scale

	def offset(self, dx, dy):
		self.x += dx
		self.y += dy

	def substract(self, v):
		return Point(self.x - v.x, self.y - v.y)


class Rectangle(Object):
	def __init__(self, x = 0, y = 0,  w = 0, h = 0):
		super(Rectangle, self).__init__()

		if not isinstance(x, (int, float)):
			x = 0
		if not isinstance(y, (int, float)):
			y = 0
		if not isinstance(w, (int, float)):
			w = 0
		if not isinstance(h, (int, float)):
			h = 0
		
		self.left = 0
		self.right = 0
		self.top = 0
		self.bottom = 0
		self.__x = x
		self.__y = y
		self.__width = w
		self.__height = h
		self.x = x
		self.y = y
		self.width = w
		self.height = h

	@property
	def x(self):
		return self.__x

	@x.setter
	def x(self, v):
		self.__x = v

		self.left = v
		self.right = v + self.width

	@property
	def y(self):
		return self.__y

	@y.setter
	def y(self, v):
		self.__y = v

		self.top = v
		self.bottom = v + self.height

	@property
	def width(self):
		return self.__width

	@width.setter
	def width(self, v):
		self.__width = v

		self.right = v + self.x

	@property
	def height(self):
		return self.__height

	@height.setter
	def height(self, v):
		self.__height = v

		self.bottom = v + self.y

	def contains(self, x, y):
		return self.x <= x <= self.right and self.y <= y <= self.bottom

	def containsRect(self, rect):
		return rect.x >= self.x and rect.right <= self.right and rect.y >= self.y and rect.bottom <= self.bottom
		
	def equals(self, v):
		return v.x == self.x and v.width == self.width and v.y == self.y and v.height == self.height

	def inflate(self, dx, dy):
		self.width += dx
		self.height += dy

	def intersection(self, t):
		ix = self.x if self.x > t.x else t.x
		iy = self.y if self.y > t.y else t.y
		ax = t.right if self.right > t.right else self.right
		ay = t.bottom if self.bottom > t.bottom else self.bottom

		if ix <= ax and iy <= ay:
			return Rectangle(ix, iy, ax, ay)
		else:
			return Rectangle(0, 0, 0, 0)

	def intersects(self, t):
		ix = self.x if self.x > t.x else t.x
		iy = self.y if self.y > t.y else t.y
		ax = t.right if self.right > t.right else self.right
		ay = t.bottom if self.bottom > t.bottom else self.bottom

		return ix <= ax and iy <= ay

	def isEmpty(self):
		return self.x == 0 and self.y == 0 and self.width == 0 and self.height == 0

	def offset(self, dx, dy):
		self.x += dx
		self.y += dy

	def setEmpty(self):
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0

	def setTo(self, x, y, w, h):
		if not isinstance(x, (int, float)):
			x = 0
		if not isinstance(y, (int, float)):
			y = 0
		if not isinstance(w, (int, float)):
			w = 0
		if not isinstance(h, (int, float)):
			h = 0

		self.x = x
		self.y = y
		self.width = w
		self.height = h

	def union(self, t):
		return Rectangle(t.x if self.x > t.x else self.x, t.y if self.y > t.y else self.y, self.right if self.right > t.right else t.right, self.bottom if self.bottom > t.bottom else t.bottom)


class Matrix(Object):
	def __init__(self, a = None, b = None, c = None, d = None, tx = None, ty = None, u = None, v = None, w = None):
		super(Matrix, self).__init__()

		self.a = 1
		self.b = 0
		self.u = 0
		self.c = 0
		self.d = 1
		self.v = 0
		self.tx = 0
		self.ty = 0
		self.w = 1
		
		self.setTo(a, b, c, d, tx, ty, u, v, w)

	def setTo(self, a = None, b = None, c = None, d = None, tx = None, ty = None, u = None, v = None, w = None):
		if a != None:
			self.a = a

		if b != None:
			self.b = b

		if c != None:
			self.c = c

		if d != None:
			self.d = d

		if tx != None:
			self.tx = tx

		if ty != None:
			self.ty = ty

		if u != None:
			self.u = u

		if v != None:
			self.v = v

		if w != None:
			self.w = w

	def isDentity(self):
		return (self.a == 1 and self.b == 0 and self.c == 0 and self.d == 1 and self.tx == 0 and self.ty == 0 and self.u == 0 and self.v == 0 and self.w == 1)

	def transform(self, c):
		c.setTransform(self.toQTransform(), True)

	def identity(self):
		self.setTo(1, 0, 0, 1, 0, 0, 0, 0, 1)
	
	def rotate(self, q):
		radian = q * math.pi / 180
		cos = math.cos(radian)
		sin = math.sin(radian)
		
		mtx = Matrix(cos, sin, -sin, cos, 0, 0, 0, 0, 1)
		self.add(mtx)

		return self

	def scale(self, sx, sy):
		mtx = Matrix(sx, 0, 0, sy, 0, 0, 0, 0, 1)
		self.add(mtx)
		
		return self

	def translate(self, tx, ty):
		mtx = Matrix(1, 0, 0, 1, tx, ty, 0, 0, 1)
		self.add(mtx)

		return self

	def skew(self, kx, ky):
		mtx = Matrix(1, ky, kx, 1, 0, 0, 0, 0, 1)
		self.add(mtx)

		return self

	def add(self, mtx):
		a = self.a * mtx.a + self.b * mtx.c + self.u * mtx.tx
		b = self.a * mtx.b + self.b * mtx.d + self.u * mtx.ty
		u = self.a * mtx.u + self.b * mtx.v + self.u * mtx.w
		c = self.c * mtx.a + self.d * mtx.c + self.v * mtx.tx
		d = self.c * mtx.b + self.d * mtx.d + self.v * mtx.ty
		v = self.c * mtx.u + self.d * mtx.v + self.v * mtx.w
		tx = self.tx * mtx.a + self.ty * mtx.c + self.w * mtx.tx
		ty = self.tx * mtx.b + self.ty * mtx.d + self.w * mtx.ty
		w = self.tx * mtx.u + self.ty * mtx.v + self.w * mtx.w
		
		self.setTo(a, b, c, d, tx, ty, u, v, w)

	def toArray(self, mtx):
		if isinstance(mtx, list) and len(mtx) == 3:
			m = mtx[0] * self.a + mtx[1] * self.c + mtx[2] * self.tx
			n = mtx[0] * self.b + mtx[1] * self.d + mtx[2] * self.ty
			k = mtx[0] * self.u + mtx[1] * self.v + mtx[2] * self.w
			
			return [m, n, k]
		else:
			a = self.a * mtx.a + self.b * mtx.c + self.u * mtx.tx
			b = self.a * mtx.b + self.b * mtx.d + self.u * mtx.ty
			u = self.a * mtx.u + self.b * mtx.v + self.u * mtx.w
			c = self.c * mtx.a + self.d * mtx.c + self.v * mtx.tx
			d = self.c * mtx.b + self.d * mtx.d + self.v * mtx.ty
			v = self.c * mtx.u + self.d * mtx.v + self.v * mtx.w
			tx = self.tx * mtx.a + self.ty * mtx.c + self.w * mtx.tx
			ty = self.tx * mtx.b + self.ty * mtx.d + self.w * mtx.ty
			w = self.tx * mtx.u + self.ty * mtx.v + self.w * mtx.w
			
			return [a, b, c, d, tx, ty, u, v, w]

	def toList(self, mtx):
		return self.toArray(mtx)

	def toQTransform(self):
		return QtGui.QTransform(self.a, self.b, self.c, self.d, self.tx, self.ty)


class Transform(Object):
	def __init__(self):
		super(Transform, self).__init__()

		self.matrix = None