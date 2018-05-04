import esper
import tdl
import logging
from tdl import set_font
from tdl import init
from tdl import Console
from src.camera import Camera
from src.user_interface.ui_manager import UIManager
from src.input_handler import InputHandler
from src.action_dispatcher import ActionDispatcher
from src.ecs.processors import *
from src.ecs.components import *
from src.consts import *


class Engine:
    def __init__(self, dimensions=DIMENSIONS, font=FONT_PATH, title=GAME_TITLE):
        self.screen_width, self.screen_height = dimensions
        self.font = font
        self.title = title
        set_font(font, greyscale=True, altLayout=True)
        self.root = init(self.screen_width, self.screen_height, title=self.title, fullscreen=True)
        self.console = Console(self.screen_width, self.screen_height)

        self.ui_manager = UIManager(self, self.console, (self.screen_width, self.screen_height))
        self.action_dispatcher = ActionDispatcher(self, [self.ui_manager])

    def create_world(self, dimensions):
        self.world = esper.World()
        self.world.engine = self
        self.world.width, self.world.height = dimensions
        # Deletes the old world from the list, if we have one
        if isinstance(self.action_dispatcher.subscribers[-1], esper.World):
            del self.action_dispatcher.subscribers[-1]
        self.action_dispatcher.subscribers.append(self.world)
        self.add_processors()
        self.create_camera()

    def loop(self):
        self.action_dispatcher.dispatch(None)
        self.running = True
        while self.running and not tdl.event.is_window_closed():
            self.root.blit(self.console)
            tdl.flush()
            # Event handling/logic
            _input = tdl.event.key_wait()
            action = InputHandler.process(_input)
            if action == "QUIT_GAME":
                self.running = False
            else:
                self.action_dispatcher(action)

    def add_processors(self):
        message_processor = MessageProcessor(START_MESSAGE)
        self.world.add_processor(message_processor)
        render_processor = RenderProcessor()
        self.world.add_processor(render_processor)
        position_processor = VelocityProcessor()
        self.world.add_processor(position_processor)

    def create_camera(self):
        level_width = self.world.width
        level_height = self.world.height
        level_dimensions = level_width, level_height

        tile_ui_width = self.ui_manager.tile_ui.window.width
        tile_ui_height = self.ui_manager.tile_ui.window.height
        tile_ui_dimensions = tile_ui_width, tile_ui_height

        self.camera = Camera(level_dimensions, tile_ui_dimensions)


if __name__ == "__main__":
    engine = Engine()
    engine.create_world(dimensions=DIMENSIONS)

    player_position = (Positionable(0, 0))
    player_render = Renderable(char="@", fg=WHITE, priority=0)
    player_description = Describable("Player", "You", "A young Inquisitor with a freshly sealed writ.")
    player_playable = Playable()
    player = engine.world.create_entity(player_position, player_render, player_description, player_playable)

    engine.loop()



