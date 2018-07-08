import tdl
import logging

import commands as com
from consts import *
from logging_tools import init_sized_object
from logic.level import Level
from state.state import StateStack
from state.play.state import PlayState

logger = logging.getLogger(__name__)


class Engine:
    def __init__(self, size, font, title, fps):
        # Font must be set before the root console is created.
        tdl.set_font(font.path, greyscale=font.greyscale, altLayout=font.alt_layout)
        logger.debug("Font set to %s" % font.__class__.__name__)
        self.root = tdl.init(*size, title=title, fullscreen=FULLSCREEN)
        init_sized_object("root console", self.root.get_size(), logger)
        tdl.set_fps(fps)
        logger.debug("FPS set to %s" % fps)
        self.stack = StateStack(self.root)
        self.running = False

    def create_play_state(self):
        level = Level(TILE_BASE_SIZE)
        play_state = PlayState(self.stack, level)
        self.stack.push(play_state)

    def loop(self):
        self.running = True
        while self.running and not tdl.event.is_window_closed():
            self.stack.start()

            # Input handling.
            for event in tdl.event.get():
                # Dispatches the command to the active state.
                command = self.stack.dispatch(event=event)
                # Checks to see if an exit command is generated.
                if command.get(com.KEY_EXIT):
                    self.running = False
            # State at the top of the stack updates gamestate.
            self.stack.update()

            # States draw onto internal U.I elements.
            self.stack.draw()
            # Displays changes to the screen.
            self.stack.render()
            tdl.flush()
            self.root.clear()
            # Notifies states that the screen has been cleared and the loop has ended.
            self.stack.reset()
