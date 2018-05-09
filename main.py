import tdl

import src.ecs.components as comp
import src.ecs.processors as pro
from src.action_dispatcher import ActionDispatcher
from src.consts import *
from src.ecs.world_manager import WorldManager
from src.input_handler import InputHandler
from src.user_interface.ui_manager import UIManager


class Engine:
    def __init__(self, screen_size=SCREEN_SIZE, font=FONT_PATH, title=GAME_TITLE):
        self.screen_width, self.screen_height = self.screen_size = screen_size
        assert (isinstance(self.screen_width, int))
        assert (isinstance(self.screen_height, int))
        self.font = font
        self.title = title
        tdl.set_font(font, greyscale=True, altLayout=True)
        self.root = tdl.init(self.screen_width, self.screen_height, title=self.title, fullscreen=True)

    def create_game(self):
        self.create_ui()
        self.create_game_ui()
        self.create_world(SCREEN_SIZE)
        self.create_processors()
        self.create_player()
        self.create_camera()

    def create_action_dispatcher(self):
        self.action_dispatcher = ActionDispatcher(self, [])

    def create_ui(self):
        self.ui = UIManager(self, (self.screen_width, self.screen_height))
        self.action_dispatcher.subscribers.append(self.ui)

    def create_game_ui(self):
        self.ui.create_game_ui()

    def create_world(self, size):
        assert (isinstance(size[0], int))
        assert (isinstance(size[1], int))
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

    def create_camera(self):
        world_size = self.world.width, self.world.height
        self.ui.create_camera(world_size)

    def loop(self):
        updated = self.world.update()
        self.ui.update(updated)
        running = True

        while running and not tdl.event.is_window_closed():
            # Updating and drawing to screen:
            # Redraws ui elements that have updated
            # Blits all ui elements to the ui
            self.ui.draw()
            self.ui.blit(self.root)
            tdl.flush()
            # Sets all ui elements redraw flag to False
            self.ui.clear()

            # Input handling:
            inputs = list(tdl.event.get())
            # Reversed to allow newer inputs to have priority
            inputs.reverse()
            for _input in inputs:
                player_input = InputHandler.handle(_input)
                if player_input is not None:
                    break
            else:
                player_input = None

            if player_input == "QUIT_GAME":
                running = False
            # Action handling:
            player_input = self.ui.handle(player_input, self.world)
            updated = self.world.update(player_input)
            self.ui.update(updated)

if __name__ == "__main__":
    engine = Engine()
    engine.create_game()
    engine.loop()



