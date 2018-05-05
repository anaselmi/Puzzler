import tdl
import src.ecs.processors as proc
import src.ecs.components as comp
from src.world_manager import WorldManager
from src.user_interface.ui_manager import UIManager
from src.input_handler import InputHandler
from src.action_dispatcher import ActionDispatcher
from src.consts import *


class Engine:
    def __init__(self, screen_size=SCREEN_SIZE, font=FONT_PATH, title=GAME_TITLE):
        self.screen_width, self.screen_height = screen_size
        self.font = font
        self.title = title
        tdl.set_font(font, greyscale=True, altLayout=True)
        self.root = tdl.init(self.screen_width, self.screen_height, title=self.title, fullscreen=True)
        self.console = tdl.Console(self.screen_width, self.screen_height)

    def create_action_dispatcher(self):
        self.action_dispatcher = ActionDispatcher(self, [])

    def create_ui_manager(self):
        self.ui_manager = UIManager(self, (self.screen_width, self.screen_height))
        self.action_dispatcher.subscribers.append(self.ui_manager)

    def create_world(self, size):
        self.world = WorldManager(engine, size)
        self.action_dispatcher.subscribers.append(self.world)
        self.create_processors()

    def create_processors(self):
        message_processor = proc.MessageProcessor(START_MESSAGE)
        self.world.add_processor(message_processor)
        render_processor = proc.RenderProcessor()
        self.world.add_processor(render_processor)
        position_processor = proc.VelocityProcessor()
        self.world.add_processor(position_processor)

    def create_camera(self):
        world_size = self.world.width, self.world.height
        self.ui_manager.create_camera(world_size)

    @staticmethod
    def create_player():
        player_position = (comp.Positionable(0, 0))
        player_render = comp.Renderable(char="@", fg=WHITE, priority=0)
        player_description = comp.Describable("Player", "You", "A young Inquisitor with a freshly sealed writ.")
        player_playable = comp.Playable()
        engine.world.create_entity(player_position, player_render, player_description, player_playable)

    def loop(self):
        self.action_dispatcher.dispatch(None)
        self.running = True
        while self.running and not tdl.event.is_window_closed():
            self.ui_manager.update()
            self.root.blit(self.console)
            self.ui_manager.clear()
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
    engine.create_action_dispatcher()
    engine.create_ui_manager()
    engine.create_world(SCREEN_SIZE)
    engine.create_processors()
    engine.create_camera()
    engine.create_player()
    engine.loop()



