import tdl
import itertools
from src.ecs.ui import UI
from src.consts import *


class TileUI(UI):
    def __init__(self, console, size, destination):
        fg = P_L_GREEN
        bg = BLACK
        super().__init__(console, size, destination, fg, bg)

        self.default_char = "."
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
