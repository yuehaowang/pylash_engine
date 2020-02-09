import math, time
from .core import Object, stage, UnityOfDictAndClass


__author__ = "Yuehao Wang"


class Uniform(object):
	def __init__(self):
		raise Exception("Uniform cannot be instantiated.")

	def easeIn(t, b, c, d):
		return b + t * c / d

	def easeOut(t, b, c, d):
		return b + t * c / d

	def easeInOut(t, b, c, d):
		return b + t * c / d


class Quad(object):
	def __init__(self):
		raise Exception("Quad cannot be instantiated.")

	def easeIn(t, b, c, d):
		t /= d

		return c * t * t + b

	def easeOut(t, b, c, d):
		t /= d

		return -c * t * (t - 2) + b

	def easeInOut(t, b, c, d):
		t /= d

		if (t / 2) < 1:
			return c / 2 * t * t + b

		t -= 1
		
		return -c / 2 * (t * (t - 2) - 1) + b
		

class Cubic(object):
	def __init__(self):
		raise Exception("Cubic cannot be instantiated.")

	def easeIn(t, b, c, d):
		t /= d

		return c * t * t * t + b

	def easeOut(t, b, c, d):
		t = t / d - 1

		return c * (t * t * t + 1) + b

	def easeInOut(t, b, c, d):
		t /= d

		if (t / 2) < 1:
			return c / 2 * t * t * t + b
		
		t -= 2

		return c / 2 * (t * t * t + 2) + b


class Quart(object):
	def __init__(self):
		raise Exception("Quart cannot be instantiated.")

	def easeIn(t, b, c, d):
		t /= d

		return c * t * t * t * t + b

	def easeOut(t, b, c, d):
		t = t / d - 1

		return -c * (t * t * t * t - 1) + b

	def easeInOut(t, b, c, d):
		t /= d

		if (t / 2) < 1:
			return c / 2 * t * t * t * t + b
		
		t -= 2

		return -c / 2 * (t * t * t * t - 2) + b


class Quint(object):
	def __init__(self):
		raise Exception("Quint cannot be instantiated.")

	def easeIn(t, b, c, d):
		t /= d

		return c * t * t * t * t * t + b

	def easeOut(t, b, c, d):
		t = t / d - 1

		return c * (t * t * t * t * t + 1) + b

	def easeInOut(t, b, c, d):
		t /= d

		if (t / 2) < 1:
			return c / 2 * t * t * t * t * t + b

		t -= 2

		return c / 2 * (t * t * t * t * t + 2) + b


class Sine(object):
	def __init__(self):
		raise Exception("Sine cannot be instantiated.")

	def easeIn(t, b, c, d):
		return -c * math.cos(t / d * (math.pi / 2)) + c + b

	def easeOut(t, b, c, d):
		return c * math.sin(t / d * (math.pi / 2)) + b

	def easeInOut(t, b, c, d):
		return -c / 2 * (math.cos(math.pi * t / d) - 1) + b


class Strong(object):
	def __init__(self):
		raise Exception("Strong cannot be instantiated.")

	def easeIn(t, b, c, d):
		t /= d

		return c * t * t * t * t * t + b

	def easeOut(t, b, c, d):
		t = t / d - 1

		return c * (t * t * t * t * t + 1) + b

	def easeInOut(t, b, c, d):
		t /= d / 2

		if t < 1:
			return c / 2 * t * t * t * t * t + b

		t -= 2

		return c / 2 * (t * t * t * t * t + 2) + b


class Expo(object):
	def __init__(self):
		raise Exception("Expo cannot be instantiated.")

	def easeIn(t, b, c, d):
		return ((t == 0) and b) or c * math.pow(2, 10 * (t / d - 1)) + b

	def easeOut(t, b, c, d):
		return ((t == d) and b + c) or c * (-math.pow(2, -10 * t / d) + 1) + b

	def easeInOut(t, b, c, d):
		if t == 0:
			return b
		
		if t == d:
			return b + c
		
		t /= d

		if (t / 2) < 1:
			return c / 2 * math.pow(2, 10 * (t - 1)) + b

		t -= 1
		
		return c / 2 * (-math.pow(2, -10 * t) + 2) + b


class Circ(object):
	def __init__(self):
		raise Exception("Circ cannot be instantiated.")

	def easeIn(t, b, c, d):
		t /= d

		return -c * (math.sqrt(1 - t * t) - 1) + b

	def easeOut(t, b, c, d):
		t = t / d - 1

		return c * math.sqrt(1 - t * t) + b

	def easeInOut(t, b, c, d):
		t /= d

		if (t / 2) < 1:
			return -c / 2 * (math.sqrt(1 - t * t) - 1) + b

		t -= 2

		return c / 2 * (math.sqrt(1 - t * t) + 1) + b


class Elastic(object):
	def __init__(self):
		raise Exception("Elastic cannot be instantiated.")

	def easeIn(t, b, c, d, a = None, p = None):
		s = None

		if t == 0:
			return b
		
		t /= d

		if t == 1:
			return b + c
		
		if not p:
			p = d * 0.3
		
		if not a or a < abs(c):
			a = c
			s = p / 4
		else:
			s = p / (2 * math.pi) * math.asin(c / a)

		t -= 1

		return -(a * pow(2, 10 * t) * math.sin((t * d - s) * (2 * math.pi) / p)) + b

	def easeOut(t, b, c, d, a = None, p = None):
		s = None

		if t == 0:
			return b

		t /= d
		
		if t == 1:
			return b + c
		
		if not p:
			p = d * 0.3
		
		if not a or a < abs(c):
			a = c
			s = p / 4
		else:
			s = p / (2 * math.pi) * math.asin(c / a)

		return (a * pow(2, -10 * t) * math.sin((t * d - s) * (2 * math.pi) / p) + c + b)

	def easeInOut(t, b, c, d, a = None, p = None):
		s = None

		if t == 0:
			return b

		t /= d
		
		if t == 1:
			return b + c
		
		if not p:
			p = d * 0.3 * 1.5
		
		if not a or a < abs(c):
			a = c
			s = p / 4
		else:
			s = p / (2 * math.pi) * math.asin(c / a)

		if t < 1:
			t -= 1

			return -0.5 * (a * pow(2, 10 * t) * math.sin((t * d - s) * (2 * math.pi) / p)) + b
			
		t -= 1

		return a * pow(2, -10 * t) * math.sin((t * d - s) * (2 * math.pi) / p) * 0.5 + c + b


class Back(object):
	def __init__(self):
		raise Exception("Back cannot be instantiated.")

	def easeIn(t, b, c, d, s = None):
		if not s:
			s = 1.70158

		t /= d

		return c * t * t * ((s + 1) * t - s) + b

	def easeOut(t, b, c, d, s = None):
		if not s:
			s = 1.70158

		t = t / d - 1
		
		return c * (t * t * ((s + 1) * t + s) + 1) + b

	def easeInOut(t, b, c, d, s = None):
		if not s:
			s = 1.70158

		t /= d

		if (t / 2) < 1:
			s *= 1.525

			return c / 2 * (t * t * ((s + 1) * t - s)) + b
			
		t -= 2
		s *= 1.525

		return c / 2 * (t * t * ((s + 1) * t + s) + 2) + b


class Bounce(object):
	def __init__(self):
		raise Exception("Bounce cannot be instantiated.")

	def easeIn(t, b, c, d):
		return c - Bounce.easeOut(d - t, 0, c, d) + b

	def easeOut(t, b, c, d):
		t /= d

		if t < (1 / 2.75):
			return c * (7.5625 * t * t) + b
		elif t < (2 / 2.75):
			t -= (1.5 / 2.75)

			return c * (7.5625 * t * t + 0.75) + b
		elif t < (2.5 / 2.75):
			t -= (2.25 / 2.75)

			return c * (7.5625 * t * t + 0.9375) + b
		else:
			t -= (2.625 / 2.75)

			return c * (7.5625 * t * t + 0.984375) + b

	def easeInOut(t, b, c, d):
		if t < d / 2:
			return Bounce.easeIn(t * 2, 0, c, d) * 0.5 + b
		
		return Bounce.easeOut(t * 2 - d, 0, c, d) * 0.5 + c * 0.5 + b
		

class Easing(object):
	def __init__(self):
		raise Exception("Easing cannot be instantiated.")

setattr(Easing, "Uniform", Uniform)
setattr(Easing, "Quad", Quad)
setattr(Easing, "Cubic", Cubic)
setattr(Easing, "Quart", Quart)
setattr(Easing, "Quint", Quint)
setattr(Easing, "Sine", Sine)
setattr(Easing, "Strong", Strong)
setattr(Easing, "Expo", Expo)
setattr(Easing, "Circ", Circ)
setattr(Easing, "Elastic", Elastic)
setattr(Easing, "Back", Back)
setattr(Easing, "Bounce", Bounce)


class TweenLiteChild(Object):
	def __init__(self, target, duration, tranVars):
		super(TweenLiteChild, self).__init__()

		self.__toNew = []
		self._initTween(target, duration, tranVars)

	def _initTween(self, target, duration, tranVars):
		if not duration:
			duration = 0.001
		
		self.__target = target
		self.__duration = duration
		self.__vars = tranVars

		if not "delay" in self.__vars:
			self.__vars["delay"] = 0

		self.__delay = self.__vars["delay"]
		del self.__vars["delay"]

		self.__currentTime = 0
		self.__duration *= 1000
		self.__currentTime -= self.__delay * 1000

		self.__varsTo = {}
		self.__varsFrom = {}

		self.stop = False

		if (not "ease" in self.__vars) or (not hasattr(self.__vars["ease"], "__call__")):
			self.__vars["ease"] = Easing.Uniform.easeIn
		
		self.__ease = self.__vars["ease"]
		del self.__vars["ease"]

		if "onComplete" in self.__vars:
			self._onComplete = self.__vars["onComplete"]
			del self.__vars["onComplete"]
		
		if "onUpdate" in self.__vars:
			self._onUpdate = self.__vars["onUpdate"]
			del self.__vars["onUpdate"]
		
		if "onStart" in self.__vars:
			self._onStart = self.__vars["onStart"]
			del self.__vars["onStart"]

		for k in self.__vars:
			if not isinstance(self.__vars.get(k), (int, float)) or not UnityOfDictAndClass.has(self.__target, k) or not isinstance(UnityOfDictAndClass.get(self.__target, k), (int, float)):
				continue

			fromValue = UnityOfDictAndClass.get(self.__target, k)

			self.__varsTo[k] = self.__vars[k]
			self.__varsFrom[k] = fromValue
	
	def pause(self):
		self.stop = True

	def resume(self):
		self.stop = False

	def to(self, target, duration, tranVars):
		if target == None:
			raise TypeError("TweenLiteChild.to(target, duration, tranVars): parameter 'target' cannot be None.")

		if not isinstance(tranVars, dict):
			raise TypeError("TweenLiteChild.to(target, duration, tranVars): parameter 'tranVars' must be a dict object.")

		self.__toNew.append({"target" : target, "duration" : duration, "vars" : tranVars})
		
		return self

	def _tween(self):
		if self.stop:
			return
		
		self.__currentTime += stage.speed

		if self.__currentTime < 0:
			return
		
		for tweenType in self.__varsTo:
			fromValue = self.__varsFrom[tweenType]
			toValue = self.__varsTo[tweenType]
			easeValue = self.__ease(self.__currentTime, fromValue, toValue - fromValue, self.__duration)

			UnityOfDictAndClass.set(self.__target, tweenType, easeValue)
		
		if hasattr(self, "_onStart"):
			self.__dispatchEvent(self._onStart)
			del self._onStart
		
		e = (self.__currentTime >= self.__duration)
		
		if e:
			for tweenType in self.__varsTo:
				UnityOfDictAndClass.set(self.__target, tweenType, self.__varsTo[tweenType])

			if hasattr(self, "_onComplete"):
				self.__dispatchEvent(self._onComplete)
			
			return True
		elif hasattr(self, "_onUpdate"):
			self.__dispatchEvent(self._onUpdate)
		
		return False
		
	def __dispatchEvent(self, f):
		self.__target.__target = self.__target
		self.__target.currentTarget = self

		if hasattr(f, "__call__"):
			f(self.__target)

		del self.__target.currentTarget
		del self.__target.__target
	
	def _keep(self):
		if len(self.__toNew) > 0:
			t = self.__toNew.pop(0)

			if "loop" in self.__vars:
				self.loop = True

			target = UnityOfDictAndClass.get(t, "target")
			duration = UnityOfDictAndClass.get(t, "duration")
			tranVars = UnityOfDictAndClass.get(t, "vars")

			if hasattr(self, "loop") and self.loop:
				vs = dict(tranVars)
				
				self.to(target, duration, vs)
			
			self._initTween(target, duration, tranVars)

			return True
		
		return False

class TweenLite(Object):
	__tweens = []

	def __init__(self):
		super(TweenLite, self).__init__()
		
	def count():
		return len(TweenLite.__tweens)

	def to(target, duration, tranVars):
		if target == None:
			raise TypeError("TweenLite.to(target, duration, tranVars): parameter 'target' cannot be None.")
		
		if not isinstance(tranVars, dict):
			raise TypeError("TweenLite.to(target, duration, tranVars): parameter 'tranVars' must be a dict object.")

		tween = TweenLiteChild({}, 0, {})
		TweenLite.__tweens.append(tween)

		tween.to(target, duration, tranVars)

		return tween

	def remove(tween):
		if not isinstance(tween, TweenLiteChild):
			raise TypeError("TweenLite.remove(tween): parameter 'tween' must not be a TweenLiteChild object.")

		TweenLite.__tweens.remove(tween)

	def removeAll():
		TweenLite.__tweens = []

	def pauseAll():
		tweens = TweenLite.__tweens

		for t in tweens:
			t.pause()

	def resumeAll():
		tweens = TweenLite.__tweens

		for t in tweens:
			t.resume()

	def _show(c):
		self = TweenLite

		if self.count() <= 0:
			return

		toRemoveList = []

		for t in self.__tweens:
			if t and hasattr(t._tween, "__call__") and t._tween():
				toRemoveList.append(t)

				if t._keep():
					self.__add(t)

		for i in toRemoveList:
			self.__tweens.remove(i)

	def __add(tween):
		TweenLite.__tweens.append(tween)

stage.childList.append(TweenLite)
