

class Renderable:
    def __init__(self, char, fg=None, bg=None, active=True, priority=1, focus=False):
        self.char = char
        self.fg = fg
        self.bg = bg
        self.active = active
        self.priority = priority
        self.focus = focus


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
    def __init__(self, messages=None):
        if not messages:
            self.messages = []
        else:
            self.messages = messages


class Ticking:
    def __init__(self, speed=10, energy=0, energy_cap=200, active=False):
        self.speed = speed
        self.energy = energy
        self.energy_cap = energy_cap
        self.active = active
