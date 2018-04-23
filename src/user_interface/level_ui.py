import tdl
import itertools
from src.consts import *


class LevelUI:
    def __init__(self, console, size, destination=(0, 0), fg=WHITE, bg=P_D_GREEN, default_char="."):
        self.console = console
        width, height = size
        self.x, self.y = destination
        self.fg = fg
        self.bg = bg
        self.default_char = default_char
        self.window = tdl.Window(self.console, self.x, self.y, width, height)
        # Width and height aren't assigned to the object to account for initializing window with None
        self.width, self.height = self.window.get_size()
        self.window.set_colors(fg=self.fg, bg=self.bg)

    def draw(self):
        self._fill()
        for y in self.level:
            for x in y:
                fg = x.get("fg")
                bg = x.get("bg")
                char = x.get("char")
                self.window.draw_char(x, y, fg, bg, char)

    def process(self, action):
        return action

    def handle(self, level):
        # There should be a better way of passing level data along, maybe have
        # the process method create the nested list of dictionaries and
        # draw simply access that?
        # possibly be a function that has some level of awareness of current game state
        self.level = level
        pass

    def _fill(self):
        self.window.draw_rect(0, 0, None, None, None)

    def clear(self):
        self.window.clear(fg=self.fg, bg=self.bg)
