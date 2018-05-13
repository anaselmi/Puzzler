import tdl

import src.ecs.components as comp
import src.ecs.processors as pro
from src.consts import *
from src.input_handling import InputHandler
from src.state.state_stack import StateStack
from src.state.states.play_state import PlayState
from src.user_interface.play_ui import PlayUI
from src.world_manager import WorldManager


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
        self.create_play_state()

    def create_state_stack(self):
        self.state_stack = StateStack()

    def create_game_ui(self):
        self.game_ui = PlayUI(self, (self.width, self.height))

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

    def create_play_state(self):
        play_state = PlayState(ui=self.game_ui, world=self.world)
        self.state_stack.push(play_state)

    def loop(self):
        running = True
        while running and not tdl.event.is_window_closed():
            # Updating and drawing to screen
            self.state_stack.render(self.console)
            self.root.blit(self.console)
            tdl.flush()
            self.state_stack.clear()

            # Input handling
            # TODO: Make this better
            _inputs = list(tdl.event.get())
            for _input in _inputs:
                action = InputHandler.handle(_input)
                break
            else:
                action = {}

            action = self.state_stack.update(action)

            _exit = action.get("EXIT")
            if _exit:
                running = False


if __name__ == "__main__":
    engine = Engine()
    engine.create_all()
    engine.loop()



