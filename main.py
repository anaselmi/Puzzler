import tdl
import src.ecs.processors as pro
import src.ecs.components as comp
from src.world_manager import WorldManager
from src.user_interface.ui_manager import UIManager
from src.state.state_stack import StateStack
from src.input_handling import InputHandler
from src.consts import *


class Engine:
    def __init__(self, size=SCREEN_SIZE, font=FONT_PATH, title=GAME_TITLE):
        self.width, self.height = size
        self.font = font
        self.title = title
        tdl.set_font(font, greyscale=True, altLayout=True)
        self.root = tdl.init(self.width, self.height, title=self.title, fullscreen=True)
        self.console = tdl.Console(self.width, self.height)

    def create_all(self):
        self.create_state_stack()
        self.create_game_ui()
        self.create_world(SCREEN_SIZE)
        self.create_processors()
        self.create_player()

    def create_state_stack(self):
        self.state_stack = StateStack()

    def create_game_ui(self):
        self.game_ui = UIManager(self, (self.width, self.height))
        self.state_stack.stack.append(self.game_ui)

    def create_world(self, size):
        self.world = WorldManager(engine, size)

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
        running = True
        while running and not tdl.event.is_window_closed():
            # Updating and drawing to screen
            self.state_stack.render(self.console)
            self.root.blit(self.console)
            tdl.flush()
            self.game_ui.clear()

            # Input handling
            _inputs = list(tdl.event.get())
            for _input in _inputs:
                action = InputHandler.handle(_input)
                break
            else:
                action = {}

            _exit = action.get("EXIT")
            if _exit:
                running = False

            # Action handling
            action = self.state_stack.handle(action)
            self.world.update(action)

if __name__ == "__main__":
    engine = Engine()
    engine.create_all()
    engine.loop()



