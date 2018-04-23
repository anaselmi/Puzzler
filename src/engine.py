import esper
import tdl
import logging
from src.helper_functions import silent_console
from src.user_interface.ui_manager import UIManager
from src.input_handler import InputHandler
from src.action_dispatcher import ActionDispatcher
from src.ecs.processors import *
from src.ecs.components import *
from src.ecs.processor_manager import ProcessorManager
from src.consts import *


class Engine:
    def __init__(self, size=(SCREEN_WIDTH, SCREEN_HEIGHT), font=FONT_PATH, log=False):
        self.log = log
        self.screen_width, self.screen_height = size
        self.font = font
        tdl.set_font(font, greyscale=True, altLayout=True)
        self.root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=GAME_TITLE, fullscreen=True)
        if not self.log:
            # Useful for silencing the amount of printing this function does
            self.console = silent_console(self.screen_width, self.screen_height)
        else:
            self.console = tdl.Console(self.screen_width, self.screen_height)

        self.ui_manager = UIManager(self.console, (self.screen_width, self.screen_height))
        priority_stack = [self.ui_manager, self.world]
        self.action_dispatcher = ActionDispatcher(priority_stack)

    def load_level(self, world, level_size):
        self.world = world
        self.level_x, self.level_y = level_size
        self.level = [[] for _ in self.level_x for _ in self.level_y]
        self.ui_manager.handle_level(self.level)

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

    World = ProcessorManager()
    Player = World.create_entity()
    World.add_component(Player, Renderable(char="@", fg=White, priority=2))
    World.add_component(Player, Positionable(CENTER_X, CENTER_Y))
    World.add_component(Player, Velocity())
    World.add_component(Player, Describable("Player", "You", "lost Assembler with a freshly minted Royal Seal."))
    World.add_component(Player, Playable())
    PlayerVelocityComp = World.component_for_entity(Player, Velocity)
    PlayerRenderableComp = World.component_for_entity(Player, Renderable)

    Gleamer = World.create_entity()
    World.add_component(Gleamer, Renderable("g", fg=RED))
    World.add_component(Gleamer, Positionable(30, 30, pathable=False))
    World.add_component(Gleamer, Velocity())
    World.add_component(Gleamer, Describable("Kazaram", "The Gleamer", "hunchbacked monstrosity with piercing eyes."))

    Cursor = World.create_entity()
    World.add_component(Cursor, Renderable(".", fg=GREEN, active=False, priority=3))
    World.add_component(Cursor, Positionable(0, 0, tangible=False))
    World.add_component(Cursor, Velocity())
    CursorVelocityComp = World.component_for_entity(Cursor, Velocity)
    CursorRenderableComp = World.component_for_entity(Cursor, Renderable)

    render_processor = RenderProcessor(GWin)
    World.add_processor(render_processor)

    position_processor = PositionProcessor(GWin, GMap)
    World.add_processor(position_processor, priority=1)

    logging_processor = LoggingProcessor(MesWin)
    World.add_processor(logging_processor)
    logging_processor.add_messages(START_MESSAGE)