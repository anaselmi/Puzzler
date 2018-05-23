

class Renderable:
    def __init__(self, char, fg=None, bg=None, active=True, priority=1, focus=False):
        self.char = char
        self.fg = fg
        self.bg = bg
        self.active = active
        self.priority = priority
        self.focus = focus


class Controllable:
    def __init__(self, player):
        self.action = {}
        self.player = player


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


class Logging:
    def __init__(self, log=None):
        if log is None:
            log = []
        self.log = log


class Active:
    pass


class Ticking:
    def __init__(self, speed=1, energy=0):
        self.speed = speed
        self.energy = energy
