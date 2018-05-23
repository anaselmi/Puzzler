import tdl

from src.logic.processors.processors import LoggingProcessor, RenderProcessor
from src.user_interface.elements.map_element import MapElement
from src.user_interface.elements.message_element import MessageElement


# TODO: Rename ui windows to elements
class PlayUI:
    def __init__(self, size):
        self.width, self.height = size
        self.console = tdl.Console(self.width, self.height)
        self.windows = []
        message_ui_height = int(self.height / 5)
        map_ui_height = self.height - message_ui_height
        self._create_map_element(size=(None, map_ui_height), destination=(0, 0))
        self._create_message_element(size=(None, None), destination=(0, map_ui_height))

    def _create_message_element(self, size, destination):
        self.message_ui = MessageElement(self.console, size=size, destination=destination)
        self.windows.append(self.message_ui)

    def _create_map_element(self, size, destination):
        self.map_ui = MapElement(self.console, size=size, destination=destination)
        self.windows.append(self.map_ui)

    def render(self, console):
        self.draw()
        console.blit(self.console)

    def handle(self, command, level):
        self._update_message_element(level)
        self._update_map_element(level)

    def update(self):
        pass

    def draw(self):
        for window in self.windows:
            window.render()

    def clear(self):
        for window in self.windows:
            window.clear()

    def _update_message_element(self, level):
        messages = level.send_logs()
        self.message_ui.update_messages(messages)

    def _update_map_element(self, level):
        render_processor = level.get_processor(RenderProcessor)
        map_ui_size = self.map_ui.window.get_size()
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

        self.map_ui.update_tiles(tiles)

    @staticmethod
    def _reset_tiles(tile_size):
        width, height = tile_size
        tiles = [[{} for _ in range(0, width)] for _ in range(0, height)]
        return tiles
