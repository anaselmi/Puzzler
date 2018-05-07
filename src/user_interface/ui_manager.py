from src.camera import Camera
from src.user_interface.message_ui import MessageUI
from src.user_interface.tile_ui import TileUI
from src.ecs.processors import MessageProcessor, RenderProcessor
from src.consts import *


class UIManager:
    def __init__(self, engine, screen_size):
        self.engine = engine
        self.console = self.engine.console
        self.screen_width, self.screen_height = screen_size
        assert(isinstance(self.screen_width, int))
        assert (isinstance(self.screen_height, int))
        self.windows = []
        message_ui_height = int(self.screen_height / 5)
        tile_ui_height = int(self.screen_height - message_ui_height)
        self._create_tile_ui(size=(None, tile_ui_height), destination=(0, 0))
        self._create_message_ui(size=(None, None), destination=(0, tile_ui_height))

    def _create_message_ui(self, size, destination):
        self.message_ui = MessageUI(self, self.console, size=size, destination=destination)
        self.windows.append(self.message_ui)

    def _create_tile_ui(self, size, destination):
        self.tile_ui = TileUI(self, self.console, size=size, destination=destination)
        self.windows.append(self.tile_ui)

    def create_camera(self, world_size):
        self.tile_ui.create_camera(world_size=world_size)

    def handle(self, action):
        pass

    def update(self):
        for window in self.windows:
            window.update()

    def draw(self):
        for window in self.windows:
            window.draw()

    def clear(self):
        for window in self.windows:
            window.clear()
