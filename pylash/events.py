from .core import Object, removeItemsInList


__author__ = "Yuehao Wang"


class Event(Object):
	def __init__(self, e):
		super(Event, self).__init__()

		if isinstance(e, Event):
			self.copyFrom(e)
		elif isinstance(e, str):
			self.eventType = e
			self.currentTarget = None
			self.target = None
		else:
			raise TypeError("Event.__init__(e): parameter 'e' is either a str or an Event object.")


class LoopEvent(object):
	ENTER_FRAME = Event("loop_enter_frame")
	EXIT_FRAME = Event("loop_exit_frame")


class MouseEvent(object):
	MOUSE_DOWN = Event("mouse_down")
	MOUSE_UP = Event("mouse_up")
	MOUSE_MOVE = Event("mouse_move")
	MOUSE_OVER = Event("mouse_over")
	MOUSE_OUT = Event("mouse_out")
	DOUBLE_CLICK = Event("mouse_dbclick")

	def __init__(self):
		raise Exception("MouseEvent cannot be instantiated.")


class KeyboardEvent(object):
	KEY_DOWN = Event("key_down")
	KEY_UP = Event("key_up")

	def __init__(self):
		raise Exception("KeyboardEvent cannot be instantiated.")


class EventDispatcher(Object):
	def __init__(self):
		super(EventDispatcher, self).__init__()
		
		self._eventList = []

	def __isEventTypeEqual(self, e1, e2):
		e1 = Event(e1)
		e2 = Event(e2)
		return e1.eventType == e2.eventType

	def _addEventListenerInList(self, e, listener, eventList):
		eventList.append({
			"eventType" : e,
			"listener" : listener
		})

	def _removeEventListenerInList(self, e, listener, eventList):
		def condition(o):
			t = o["eventType"]
			l = o["listener"]

			return (l == listener and self.__isEventTypeEqual(e, t))

		removeItemsInList(eventList, condition)

	def _dispatchEventInList(self, e, eventList):
		for o in eventList:
			t = o["eventType"]
			l = o["listener"]

			if self.__isEventTypeEqual(e, t):
				e = Event(e)

				if e.currentTarget is None:
					e.currentTarget = self
				if e.target is None:
					e.target = self

				l(e)

	def _hasEventListenerInList(self, e, listener, eventList):
		for o in eventList:
			t = o["eventType"]
			l = o["listener"]

			if l == listener:
				if self.__isEventTypeEqual(e, t):
					return True
				else:
					return False

			return False

	def addEventListener(self, e, listener):
		self._addEventListenerInList(e, listener, self._eventList)

	def removeEventListener(self, e, listener):
		self._removeEventListenerInList(e, listener, self._eventList)

	def removeAllEventListeners(self):
		self._eventList = []

	def dispatchEvent(self, e):
		self._dispatchEventInList(e, self._eventList)

	def hasEventListener(self, e, listener):
		return self._hasEventListenerInList(e, listener, self._eventList)
