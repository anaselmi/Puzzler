import tdl
import itertools
from src.consts import *
from src.camera import Camera


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
        for y in self.tiles:
            for x in y:
                fg = x.get("fg")
                bg = x.get("bg")
                char = x.get("char")
                self.window.draw_char(x, y, fg, bg, char)

    def process(self, action):
        pass

    def handle(self, tiles):
        self.tiles = tiles

    def _fill(self):
        self.window.draw_rect(0, 0, None, None, None)

    def clear(self):
        self.window.clear(fg=self.fg, bg=self.bg)
