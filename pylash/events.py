from .utils import Object, removeItemsInList


__author__ = "Yuehao Wang"


class Event(Object):
	COMPLETE = "complete"
	ENTER_FRAME = "enter_frame"

	def __init__(self, eventType):
		super(Event, self).__init__()

		self.eventType = eventType
		self.currentTarget = None
		self.target = None


class MouseEvent(object):
	MOUSE_DOWN = Event("mouse_down")
	MOUSE_UP = Event("mouse_up")
	MOUSE_MOVE = Event("mouse_move")
	MOUSE_OVER = Event("mouse_over")
	MOUSE_OUT = Event("mouse_out")
	DOUBLE_CLICK = Event("mouse_dbclick")

	def __init__():
		raise Exception("MouseEvent cannot be instantiated.")


class KeyboardEvent(object):
	KEY_DOWN = Event("key_down")
	KEY_UP = Event("key_up")

	def __init__():
		raise Exception("KeyboardEvent cannot be instantiated.")


class AnimationEvent(object):
	CHANGE_FRAME = Event("animation_change_frame")
	STOP = Event("animation_stop")
	START = Event("animation_start")

	def __init__():
		raise Exception("AnimationEvent cannot be instantiated.")


class RankingSystemEvent(object):
	SUCCEED_IN_ADDING_RECORD = Event("ranking_system_succeed_in_adding_record")
	FAIL_TO_ADD_RECORD = Event("ranking_system_fail_to_add_record")
	FAIL_TO_GET_RECORDS = Event("ranking_system_fail_to_get_records")
	SUCCEED_IN_GETTING_RECORDS = Event("ranking_system_succeed_in_getting_records")

	def __init__(self):
		raise Exception("RankingSystemEvent cannot be instantiated.")


class MediaEvent(object):
	PAUSE = Event("media_pause")
	PLAY = Event("media_play")
	STOP = Event("media_stop")

	def __init__(self):
		raise Exception("RankingSystemEvent cannot be instantiated.")


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
		def condition(o):
			t = o["eventType"]
			l = o["listener"]

			return (l == listener and self.__isEventTypeEqual(e, t))

		removeItemsInList(eventList, condition)

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