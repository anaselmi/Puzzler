from src.consts import *


class Renderable:
    def __init__(self, char, fg=WHITE, active=True, priority=0):
        self.char = char
        self.fg = fg
        self.active = active
        self.priority = priority
        self.x = None
        self.y = None


class Playable:
    def __init__(self):
        pass


class Velocity:
    def __init__(self, x=0, y=0, loop=True):
        self.x = x
        self.y = y
        self.loop = loop


class Positionable:
    def __init__(self, x, y, tangible=True, pathable=True):
        self.x = x
        self.y = y
        self.tangible = tangible
        self.pathable = pathable
        self.moved = True


class Describable:
    def __init__(self, name, reference, description):
        self.name = name
        self.reference = reference
        self.description = description


