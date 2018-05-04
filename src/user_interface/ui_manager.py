from src.user_interface.message_ui import MessageUI
from src.user_interface.tile_ui import TileUI
from src.ecs.processors import MessageProcessor, RenderProcessor


# Class that handles setting size, receiving data and batched, layered
# drawing for UI elements
class UIManager:
    def __init__(self, engine, console, screen_size):
        self.engine = engine
        self.console = console
        self.screen_width, self.screen_height = screen_size
        message_ui_height = int(self.screen_height / 5)
        self.message_ui = MessageUI(self, self.console, size=(self.screen_width, message_ui_height), destination=(0, 0))
        self.tile_ui = TileUI(self, self.console, size=(None, None), destination=(0, message_ui_height))

    def process(self, action):
        self.handle_messages()
        self.message_ui.clear()
        self.message_ui.draw()

        self.handle_tiles()
        self.tile_ui.clear()
        self.tile_ui.draw()

    def handle_messages(self):
        message_processor = self.engine.world.get_processor(MessageProcessor)
        messages = message_processor.send_messages()

    def handle_tiles(self):
        render_processor = self.engine.world.get_processor(RenderProcessor)
        tiles = render_processor.send_tiles()
        self.tile_ui.handle(tiles)
