import tdl
import src.ecs.processors as pro
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

    def create_game_ui(self):
        self.game_ui = UIManager(self, (self.screen_width, self.screen_height))
        self.action_dispatcher.subscribers.append(self.game_ui)

    def create_world(self, size):
        self.world = WorldManager(engine, size)
        self.action_dispatcher.subscribers.append(self.world)
        self.create_processors()

    def create_processors(self):
        processors = []

        message_processor = pro.MessageProcessor(START_MESSAGE)
        processors.append(message_processor)
        render_processor = pro.RenderProcessor()
        processors.append(render_processor)
        position_processor = pro.VelocityProcessor()
        processors.append(position_processor)
        action_processor = pro.ActionProcessor()
        processors.append(action_processor)
        tick_processor = pro.TickProcessor()
        processors.append(tick_processor)

        for i, processor in enumerate(processors):
            self.world.add_processor(processor, priority=i)

    def create_player(self):
        components = []

        player_position = (comp.Positionable(0, 0))
        components.append(player_position)
        player_render = comp.Renderable(char="@", fg=WHITE, priority=0)
        components.append(player_render)
        player_description = comp.Describable("Player", "You", "A young Inquisitor with a freshly sealed writ.")
        components.append(player_description)
        player_playable = comp.Playable()
        components.append(player_playable)
        player_tick = comp.Ticking()
        components.append(player_tick)
        player_vel = comp.Velocity()
        components.append(player_vel)

        player = self.world.create_entity()
        for component in components:
            self.world.add_component(player, component)

    def loop(self):
        self.action_dispatcher(None)
        self.running = True
        while self.running and not tdl.event.is_window_closed():
            # Updating and drawing to screen
            self.game_ui.draw()
            self.root.blit(self.console)
            self.game_ui.clear()
            tdl.flush()
            # Input handling
            _inputs = list(tdl.event.get())
            for _input in _inputs:
                action = InputHandler.handle(_input)
                break
            else:
                action = {}

            if action.get("EXIT"):
                self.running = False
            # Action handling
            self.action_dispatcher(action)
            # Runs the world until game reaches a point where input is required
            self.world.update()

if __name__ == "__main__":
    engine = Engine()
    # Run these methods in this order or things will crash
    engine.create_action_dispatcher()
    engine.create_game_ui()
    engine.create_world(SCREEN_SIZE)
    engine.create_processors()
    engine.create_player()
    engine.loop()



