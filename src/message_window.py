import tdl
import tcod
import itertools
from consts import *
from message import Message

# TODO: Create console as an ABC
# TODO: Create ConsoleHandler
# TODO: Create a MapConsole
# TODO: Create a MapConsole


class MessageWindow:
    # TODO: Add logic to MCon that allows it to either calculate its own size or simply use parameters given
    # TODO: MCon takes flags that alter what is printed
    def __init__(self, SCREEN_X, SCREEN_Y, root, current=[]):
        self.x = int(SCREEN_X)
        self.y = int(SCREEN_Y / 5)

        self.window = tdl.Window(root, 0, 0, None, self.y)
        self.window.set_colors(fg=BLACK, bg=BEIGE)
        self.root = root
        # Messages currently being displayed
        self.current = current

    def update(self, messages):
        # Loop brings in recent messages
        # Loop should always clear itself at the end of a loop
        assert(isinstance(messages, list))
        self.current = list(itertools.chain(self.current, messages))
        self.purge_current()

    def purge_current(self):
        # We subtract 1 from y to make sure we don't draw text onto the frame
        while len(self.current) >= self.y - 1:
            del self.current[0]

    def draw(self):
        self.fill()
        self.frame()
        assert(len(self.current) < self.y)
        for i, message in enumerate(self.current):
            text = message.text
            color = message.color
            # We add 1 to i to make sure we don't draw onto the frame
            self.window.draw_str(1, i+1, text)

    def frame(self):
        self.window.draw_frame(0, 0, None, None, ".", WHITE, BLACK)

    def fill(self):
        self.window.draw_rect(0, 0, None, None, None)

    def clear(self):
        self.window.clear()
