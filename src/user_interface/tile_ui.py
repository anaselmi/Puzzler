import tdl
import itertools
from src.consts import *
from src.camera import Camera


class TileUI:
    def __init__(self, manager, console, size, destination=(0, 0), fg=WHITE, bg=P_D_GREEN, default_char="."):
        self.manager = manager
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
        self.tiles = None

    def draw(self):
        self._fill()
        for unadjusted_y, row in enumerate(self.tiles):
            for unadjusted_x, tile in enumerate(row):
                x = unadjusted_x
                y = unadjusted_y
                fg = tile.get("fg", ...)
                bg = tile.get("bg", ...)
                char = tile.get("char", self.default_char)
                self.window.draw_char(x, y, char=char, fg=fg, bg=bg)

    def process(self, action):
        pass

    def update(self, tiles):
        self.tiles = tiles

    def _fill(self):
        self.window.draw_rect(0, 0, None, None, None)

    def clear(self):
        self.tiles = None
        self.window.clear(fg=self.fg, bg=self.bg)
