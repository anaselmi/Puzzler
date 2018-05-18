from enum import Enum


class EventStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNDETERMINED = "UNDETERMINED"


class Event:
    def __init__(self):
        self.branches = []
        self.root = None
        self.data = {}
        self.status = EventStatus.UNDETERMINED

    def initialize(self):
        pass

event = Event()
print(event.status)
event.status = EventStatus.PASS
print(event.status)



class TickEvent(Event):
    pass


