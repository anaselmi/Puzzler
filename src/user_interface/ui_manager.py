from src.user_interface.message_ui import MessageUI
from src.user_interface.level_ui import LevelUI


# Class that handles setting size, receiving data and batched, layered
# drawing for UI elements
class UIManager:
    def __init__(self, console, screen_size):
        self.console = console
        self.screen_width, self.screen_height = screen_size
        message_ui_height = self.screen_height / 5
        self.message_ui = MessageUI(self.console, size=(self.screen_width, message_ui_height), destination=(0, 0))
        self.level_ui = LevelUI(self.console, size=(None, None), destination=(0, message_ui_height))

    def process(self, action):
        self.message_ui.clear()
        self.level_ui.clear()
        self.message_ui.draw()
        self.level_ui.draw()

    def handle_messages(self, messages):
        self.message_ui.handle(messages)

    def handle_tiles(self, tiles):
        self.level_ui.handle(tiles)
