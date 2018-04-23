

class Renderable:
    def __init__(self, char, pos=(None, None), fg=None, bg=None, active=True, priority=0):
        # Position relative to the screen
        self.x, self.y = pos
        self.char = char
        self.fg = fg
        self.bg = bg
        self.active = active
        self.priority = priority


class Playable:
    def __init__(self, is_player=True):
            self.is_player = is_player


class Velocity:
    def __init__(self, difference=(0, 0)):
        self.dx, self.dy = difference


class Positionable:
    def __init__(self, x, y, pathable=True):
        # Position in actual space
        self.x = x
        self.y = y
        self.pathable = pathable
        self.moved = True


class Describable:
    def __init__(self, name, reference, description):
        self.name = name
        self.reference = reference
        self.description = description


class Messaging:
    def __init__(self, messages):
        self.messages = messages


