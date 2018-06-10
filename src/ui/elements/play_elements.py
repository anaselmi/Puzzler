from src.consts import *
from src.ui.elements.element import Element


class LogElement(Element):
    name = LOG
    plt = (D_GREY, BLACK)

    def __init__(self, pos, size=LOG_SIZE, sc_size=SIZE):
        name = LogElement.name
        plt = LogElement.plt
        super().__init__(name, pos, size, sc_size, plt=plt)

    def draw_logs(self, logs):
        x = 0
        self.clear()
        assert(len(logs) < self.height)
        for y, log in enumerate(logs):
            self.draw_log(log, x, y)

    def draw_log(self, log, x, y):
        pass

    def _draw_log(self, x, y, text, color):
        pass
        # self.c.draw_str(x + self.f_w, y + self.f_h, text, color)


class TileElement(Element):
    name = TILE

    def __init__(self, pos, size=TILE_SIZE, sc_size=SIZE):
        name = TileElement.name
        super().__init__(name, pos, size, sc_size)

    # Batch draw calls after camera movement, loading level, etc.
    def draw_tiles(self, tiles):
        pass

    # A tile contains a position, and a base color.
    def draw_tile(self, tile):
        pass

    def draw_char(self, char, pos, color, tile=None, light=None, old_pos=None):
        pass

    def _draw_char(self, char, pos, color):
        pass

    def clear_char(self, pos):
        pass

    def draw_lights(self, lights):
        pass