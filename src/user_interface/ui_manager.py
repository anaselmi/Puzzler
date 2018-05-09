import tdl
from src.action_dispatcher import ActionDispatcher
from src.user_interface.message_ui import MessageUI
from src.user_interface.tile_ui import TileUI


class UIManager:
    def __init__(self, engine, size):
        self.action_dispatcher = ActionDispatcher([])
        self.uis = []

        self.engine = engine
        self.width, self.height = self.size = size

        self.console = tdl.Console(self.width, self.height)

    def handle(self, action, world):
        # TODO Add an action dispatcher
        for ui in self.uis:
            ui.handle(action, world)

    def update(self, world_updated):
        for ui in self.uis:
            if world_updated:
                ui.parse_world()
            ui.update()

    def draw(self):
        for ui in self.uis:
            if ui.redraw:
                ui.clear()
                ui.draw()
            ui_con = ui.console
            x, y = ui.destination
            width, height = ui.size
            self.console.blit(source=ui_con, x=x, y=y, width=width, height=height)

    def clear(self):
        self.console.clear()
        for ui in self.uis:
            ui.redraw = False

    def blit(self, console):
        console.blit(self.console)

    # Will be deleted soon, along with all references to names of UIs and the camera
    def create_game_ui(self):
        message_ui_height = int(self.height / 5)
        tile_ui_height = int(self.height - message_ui_height)
        self._create_tile_ui(size=(self.width, tile_ui_height), destination=(0, 0))
        self._create_message_ui(size=self.size, destination=(0, tile_ui_height))
        self.action_dispatcher.subscribers = self.uis

    def create_camera(self, world_size):
        self.tile_ui.create_camera(world_size=world_size)

    def _create_message_ui(self, size, destination):
        self.message_ui = MessageUI(self, size=size, destination=destination)
        self.uis.append(self.message_ui)

    def _create_tile_ui(self, size, destination):
        self.tile_ui = TileUI(self, size=size, destination=destination)
        self.uis.append(self.tile_ui)
