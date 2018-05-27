import tdl

from src.game.processors.processors import LoggingProcessor, RenderProcessor
from src.user_interface.elements.map_element import MapElement
from src.user_interface.elements.log_element import MessageElement


# TODO: Rename ui windows to elements
class PlayUI:
    def __init__(self, size):
        self.width, self.height = size
        self.console = tdl.Console(self.width, self.height)
        self.elements = []
        log_element_height = int(self.height / 5)
        map_element_height = self.height - log_element_height
        self._create_map_element(size=(None, map_element_height), destination=(0, 0))
        self._create_log_element(size=(None, None), destination=(0, map_element_height))

    def _create_log_element(self, size, destination):
        self.log_element = MessageElement(self.console, size=size, destination=destination)
        self.elements.append(self.log_element)

    def _create_map_element(self, size, destination):
        self.map_element = MapElement(self.console, size=size, destination=destination)
        self.elements.append(self.map_element)

    def render(self, console):
        self.map_element.draw()
        console.blit(self.console)

    def handle(self, command, level):
        self._update_map_element(level)

    def update(self):
        pass

    def _update_map_element(self, level):
        render_processor = level.get_processor(RenderProcessor)
        map_ui_size = self.map_element.window.get_size()
        tiles = self._reset_tiles(map_ui_size)
        entities = render_processor.get_entities()
        for ent, (rend_component, pos_component) in entities:
            pos = pos_component.x, pos_component.y
            if pos is None:
                continue
            x, y = pos
            try:
                tile = tiles[y][x]
            except IndexError:
                continue
            char = rend_component.char
            tile["char"] = char
            fg = rend_component.fg
            tile["fg"] = fg
            bg = rend_component.bg
            tile["bg"] = bg

        self.map_element.update_tiles(tiles)

    @staticmethod
    def _reset_tiles(tile_size):
        width, height = tile_size
        tiles = [[{} for _ in range(0, width)] for _ in range(0, height)]
        return tiles
