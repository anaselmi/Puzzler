from src.user_interface.message_ui import MessageUI
from src.user_interface.tile_ui import TileUI
from src.ecs.processors import MessageProcessor, RenderProcessor


class UIManager:
    def __init__(self, engine, screen_size):
        self.engine = engine
        self.console = self.engine.console
        self.screen_width, self.screen_height = screen_size
        self.windows = []
        message_ui_height = int(self.screen_height / 5)
        tile_ui_height = self.screen_height - message_ui_height
        self._create_tile_ui(size=(None, tile_ui_height), destination=(0, 0))
        self._create_message_ui(size=(None, None), destination=(0, tile_ui_height))

    def _create_message_ui(self, size, destination):
        self.message_ui = MessageUI(self.console, size=size, destination=destination)
        self.windows.append(self.message_ui)

    def _create_tile_ui(self, size, destination):
        self.tile_ui = TileUI(self.console, size=size, destination=destination)
        self.windows.append(self.tile_ui)

    def handle(self, action):
        pass

    def draw(self):
        self._update_message_ui()
        self._update_tile_ui()
        self._draw_to_console()

    def _draw_to_console(self):
        for window in self.windows:
            window.draw()

    def clear(self):
        for window in self.windows:
            window.clear()

    def _update_message_ui(self):
        message_processor = self.engine.world.get_processor(MessageProcessor)
        messages = message_processor.get_messages()
        self.message_ui.update(messages)

    def _update_tile_ui(self):
        render_processor = self.engine.world.get_processor(RenderProcessor)
        tile_ui_size = self.tile_ui.window.get_size()
        tiles = self._reset_tiles(tile_ui_size)
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

        self.tile_ui.update(tiles)

    @staticmethod
    def _reset_tiles(tile_size):
        width, height = tile_size
        tiles = [[{} for _ in range(0, width)] for _ in range(0, height)]
        return tiles
