import esper
import tdl
import logging
from src.camera import Camera
from tdl import set_font
from tdl import init
from tdl import Console
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

        self.ui_manager = UIManager(self.console, (self.screen_width, self.screen_height))
        priority_stack = [self.ui_manager, self.world]
        self.action_dispatcher = ActionDispatcher(priority_stack)

    def load_world(self, _world, dimensions):
        self.world = _world
        self.world.width, self.world.height = dimensions
        # Adding this just in case it's needed, don't use it as a crutch
        self.world.engine = self

    def loop(self):
        self.action_dispatcher(None)
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


if __name__ == "__main__":
    engine = Engine()
    world = Esper.World()

    player_position = (Positionable(0, 0))
    player_render = Renderable(char="@", fg=WHITE, priority=0)
    player_description = Describable("Player", "You", "A young Inquisitor with a freshly sealed writ.")
    player_playable = Playable()
    player = world.create_entity(player_position, player_render, player_description, player_playable)

    message_processor = MessageProcessor(START_MESSAGE)
    world.add_processor(message_processor)
    render_processor = RenderProcessor()
    world.add_processor(render_processor)
    position_processor = PositionProcessor()
    world.add_processor(position_processor, priority=1)

    engine.load_world(world, dimensions=DIMENSIONS)
    engine.loop()



