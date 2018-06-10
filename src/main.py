import time

import tdl

from src.consts import *
from src.commands import handle
from src.logic.level import Level
from src.state.state_stack import StateStack
from src.state.states.play_state import PlayState


class Engine:
    def __init__(self, size=SIZE):
        self.width, self.height = self.size = size
        self.font = FONT_PATH
        self.title = TITLE
        tdl.set_font(self.font, greyscale=GREYSCALE, altLayout=ALT_LAYOUT)
        self.root = tdl.init(self.width, self.height, title=self.title, fullscreen=FULLSCREEN)
        self.screen = tdl.Console(self.width, self.height)
        self.state_stack = StateStack(self.screen)

    def create_play_state(self, level_size=None):
        level_size = self.size if level_size is None else level_size
        level = Level(level_size)
        level.create_processors()
        level.create_player()
        play_state = PlayState(self.state_stack, level)
        self.state_stack.push(play_state)

    def loop(self):
        time_previous = time.time()
        running = True
        while running and not tdl.event.is_window_closed():
            time_current = time.time()
            time_elapsed = time_current - time_previous

            # Input handling
            for _input in tdl.event.get():
                command = handle(_input)
                # Feeds command to state stack and checks to see if game should be exited
                if self.state_stack.handle(command).get(C_K_EXIT):
                    running = False

            # Updating the screen
            self.state_stack.update(time_elapsed)

            # Drawing to screen
            self.state_stack.render()
            self.root.blit(self.screen)
            tdl.flush()
            self.root.clear()
            self.screen.clear()


if __name__ == "__main__":
    engine = Engine()
    engine.create_play_state()
    engine.loop()



