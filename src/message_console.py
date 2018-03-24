import tdl
import tcod
import itertools
from consts import *
from message import Message

# TODO: Create console as an ABC
# TODO: Create ConsoleHandler
# TODO: Create a MapConsole
# TODO: Create a MapConsole


class MessageConsole:
    # TODO: Add logic to MCon that allows it to either calculate its own size or simply use parameters given
    # TODO: MCon takes flags that alter what is printed
    def __init__(self, SCREEN_X, SCREEN_Y, root, current=[]):
        self.x = int(SCREEN_X)
        self.y = int(SCREEN_Y / 5)

        self.window = tdl.Window(root, 0, 0, None, self.y)
        self.window.set_colors(fg=(0, 0, 0), bg=(200, 200, 200))
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
        # Updates current so that only the most recent messages are printed and we dont print outside of the console
        while len(self.current) > self.y:
            del self.current[0]

    def draw(self):
        # TODO
        # Draw should be a simple function
        # Index is to make sure messages don't print on top of each other and don't print out of console
        assert(len(self.current) <= self.y)
        for i, message in enumerate(self.current):
            text = message.text
            color = message.color
            self.window.draw_str(0, i, text)

    def frame(self):
        self.window

    def clear(self):
        self.window.clear()
