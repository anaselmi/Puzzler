from src.consts import *
import src.ui.elements.element as el


class LogElement(el.Element):
    name = LOG
    plt = D_GREY, BLACK

    def __init__(self, pos, size=LOG_SIZE):
        name = LogElement.name
        plt = LogElement.plt
        frame = el.DEFAULT_FRAME
        super().__init__(name=name, pos=pos, size=size, plt=plt, frame=frame)

    def draw_logs(self, logs):
        x = 0
        self.clear()
        assert(len(logs) < self.win.height)
        for y, log in enumerate(logs):
            self.draw_log(log, x, y)

    def draw_log(self, log, x, y):
        pass

    def _draw_log(self, x, y, text, color):
        pass
        # self.c.draw_str(x + self.f_w, y + self.f_h, text, color)


class TileElement(el.Element):
    # A tile should contain a position, and a base color.

    name = TILE
    plt = PLT_WB

    def __init__(self, pos, size=TILE_SIZE):
        name = TileElement.name
        plt = TileElement.plt
        frame = el.DEFAULT_FRAME
        super().__init__(name=name, pos=pos, size=size, plt=plt, frame=frame)

    # Draw all tiles. Useful after moving the camera, loading the level, etc.
    def draw_tiles(self, tiles):
        pass

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
