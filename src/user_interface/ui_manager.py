import tdl
from src.user_interface.message_element import MessageElement
from src.user_interface.map_element import MapElement
from src.ecs.processors import MessageProcessor, RenderProcessor


# TODO: Rename ui windows to elements
class UIManager:
    def __init__(self, engine, size):
        self.engine = engine
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

    def handle(self, action):
        pass

    def render(self):
        self._update_message_element()
        self._update_map_element()
        self._draw_to_console()

    def update(self):
        pass

    def _draw_to_console(self):
        for window in self.windows:
            window.render()

    def clear(self):
        for window in self.windows:
            window.clear()

    def _update_message_element(self):
        message_processor = self.engine.world.get_processor(MessageProcessor)
        messages = message_processor.get_messages()
        self.message_ui.update_messages(messages)

    def _update_map_element(self):
        render_processor = self.engine.world.get_processor(RenderProcessor)
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
