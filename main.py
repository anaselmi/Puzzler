import tdl

import src.ecs.components as comp
import src.ecs.processors as pro
from src.consts import *
from src.input_handling import InputHandler
from src.state.state_stack import StateStack
from src.state.states.play_state import PlayState
from src.user_interface.play_ui import PlayUI
from src.level import Level


class Engine:
    def __init__(self, size=SCREEN_SIZE, font=FONT_PATH, title=GAME_TITLE):
        self.width, self.height = self.size = size
        self.font = font
        self.title = title
        tdl.set_font(font, greyscale=True, altLayout=True)
        self.root = tdl.init(self.width, self.height, title=self.title, fullscreen=True)
        self.console = tdl.Console(self.width, self.height)
        self.state_stack = StateStack()

    def create_all(self):
        self.create_play_state(self.size)

    def create_play_state(self, ui_size=None, level_size=None):
        ui_size = self.size if ui_size is None else ui_size
        level_size = self.size if level_size is None else level_size

        play_ui = PlayUI(ui_size)
        level = Level(level_size)
        level.create_processors()
        level.create_player()

        play_state = PlayState(ui=play_ui, level=level)
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
                command = InputHandler.handle(_input)
                break
            else:
                command = {}
            command = self.state_stack.handle(command)
            _exit = command.get("EXIT")
            if _exit:
                running = False

            self.state_stack.update()


if __name__ == "__main__":
    engine = Engine()
    engine.create_play_state()
    engine.loop()



