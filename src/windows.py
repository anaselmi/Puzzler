import tdl
import tcod
import itertools
from consts import *


class MessageWindow:
    def __init__(self, screen_x, screen_y, con):
        self.x = int(screen_x)
        self.y = int(screen_y / 5)

        self.window = tdl.Window(con, 0, 0, None, self.y)
        self.window.set_colors(fg=BLUE, bg=BLACK)
        self.root = con
        self.recent_messages = []

    def draw(self):
        self.fill()
        self.frame()
        assert(len(self.recent_messages) < self.y)
        for i, text in enumerate(self.recent_messages):
            # We add 1 to i to make sure we don't draw onto the frame
            self.window.draw_str(1, i+1, text)

    def process(self, messages):
        self.clear()
        self.recent_messages = list(itertools.chain(self.recent_messages, messages))
        self.purge_recent()
        self.draw()

    def purge_recent(self):
        # We subtract 1 from y to make sure we don't draw text onto the frame
        while len(self.recent_messages) >= self.y - 1:
            del self.recent_messages[0]

    def frame(self):
        self.window.draw_frame(0, 0, None, None, ".", WHITE, BLACK)

    def fill(self):
        self.window.draw_rect(0, 0, None, None, None)

    def clear(self):
        self.window.clear()
