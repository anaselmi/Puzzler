import tdl

from src.consts import *
from src.commands import parse_input
from src.logic.level import Level
from src.state.state import StateStack
from state.play_state import PlayState


class Engine:
    def __init__(self, size=SIZE):
        self.width, self.height = self.size = size
        self.font = FONT_PATH
        self.title = TITLE
        tdl.set_font(self.font, greyscale=GREYSCALE, altLayout=ALT_LAYOUT)
        self.root = tdl.init(self.width, self.height, title=self.title, fullscreen=FULLSCREEN)
        tdl.set_fps(FPS)
        self.screen = tdl.Console(self.width, self.height)
        self.state_stack = StateStack(self.screen)

    def create_play_state(self):
        level_size = TILE_BASE_SIZE
        level = Level(level_size)
        play_state = PlayState(self.state_stack, level)
        self.state_stack.push(play_state)

    def loop(self):
        running = True
        while running and not tdl.event.is_window_closed():
            self.state_stack.start()

            # Input handling.
            for _input in tdl.event.get():
                command = parse_input(_input)
                # Dispatches the command to the stack and checks to see if an exit command is generated.
                if self.state_stack.dispatch(command=command).get(C_K_EXIT):
                    running = False

            # Updating consoles/windows.
            self.state_stack.update()

            # Drawing to screen and flushing to root.
            self.state_stack.render()
            self.root.blit(self.screen)
            tdl.flush()
            # Clearing root/screen and notifying states that the screen has just been cleared.
            self.root.clear()
            self.screen.clear()
            self.state_stack.reset()


if __name__ == "__main__":
    engine = Engine()
    engine.create_play_state()
    engine.loop()



