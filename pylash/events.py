from .utils import Object


__author__ = "Yuehao Wang"


class Event(Object):
	COMPLETE = "complete"
	ENTER_FRAME = "enter_frame"

	def __init__(self, eventType):
		super(Event, self).__init__()

		self.eventType = eventType
		self.currentTarget = None
		self.target = None


class MouseEvent(Event):
	MOUSE_DOWN = Event("mouse_down")
	MOUSE_UP = Event("mouse_up")
	MOUSE_MOVE = Event("mouse_move")
	DOUBLE_CLICK = Event("mouse_dbclick")

	def __init__():
		raise Exception("MouseEvent cannot be instantiated.")


class KeyboardEvent(Event):
	KEY_DOWN = Event("key_down")
	KEY_UP = Event("key_up")

	def __init__():
		raise Exception("KeyboardEvent cannot be instantiated.")


class EventDispatcher(Object):
	def __init__(self):
		super(EventDispatcher, self).__init__()
		
		self._eventList = []

	def __isEventTypeEqual(self, e1, t):
		return (isinstance(e1, str) and t.eventType == e1) or (isinstance(e1, Event) and t.eventType == e1.eventType)

	def _addEventListenerInList(self, e, listener, eventList):
		event = e

		if not isinstance(e, Event):
			event = Event(e)

		eventList.append({
			"eventType" : event,
			"listener" : listener
		})

	def _removeAllEventListenersInList(self, eventList):
		eventList = []

	def _removeEventListenerInList(self, e, listener, eventList):
		for i, o in enumerate(eventList):
			t = o["eventType"]
			l = o["listener"]

			if l == listener and self.__isEventTypeEqual(e, t):
				eventList.pop(i)

	def _dispatchEventInList(self, e, eventList):
		for o in eventList:
			t = o["eventType"]
			l = o["listener"]

			if isinstance(e, str) and t.eventType == e:
				if not hasattr(self, "currentTarget") or self.currentTarget is None:
					self.currentTarget = self
				
				if not hasattr(self, "target") or self.target is None:
					self.target = self
				
				self.eventType = e

				l(self)

				del self.currentTarget
				del self.target
				del self.eventType
			elif isinstance(e, Event) and t.eventType == e.eventType:
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