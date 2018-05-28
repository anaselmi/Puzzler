from src.consts import *
from src.user_interface.elements.element import Element


class MapElement(Element):
    name = "map"

    def __init__(self, con, pos, size):
        name = MapElement.name
        super().__init__(name, con, size, pos)
        self.create_frame()

    # Batch draw calls after camera movement, loading level, etc.
    def draw_tiles(self, tiles):
        pass

    # A tile contains a position, and a base color
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
