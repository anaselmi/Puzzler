import tdl
import itertools
from src.user_interface.ui import UI
from src.consts import *


class MessageUI(UI):
    def __init__(self, manager, size, destination=(0, 0)):
        super().__init__()
        self.fg = D_GREY
        self.bg = BLACK
        self.frame_color = WHITE
        self.frame_char = "."
        self.messages = []

        self.manager = manager
        self.width, self.height = self.size = size
        self.x, self.y = self.destination = destination

        self.console = tdl.Console(self.width, self.height)
        self.console.set_colors(fg=self.fg, bg=self.bg)

    def handle(self, action, world):
        pass

    def parse_world(self, world):
        messages = world.send_messages()
        if messages:
            self.add_messages(messages)
            self.redraw = True

    def draw(self):
        self._fill()
        self._draw_frame()
        assert(len(self.messages) < self.height)
        for i, message in enumerate(self.messages):
            if isinstance(message, str):
                text = message
                color = self.fg
            else:
                assert(isinstance(message, tuple))
                assert(len(message) == 2)
                text = message[0]
                color = message[1]
            # Add 1 to i to make sure we don't draw onto the frame
            self.console.draw_str(1, i + 1, text, fg=color)

    def process(self, action):
        pass

    def update(self):
        if self.redraw:
            pass

    def add_messages(self, messages):
        self.messages = list(itertools.chain(self.messages, messages))
        self._delete_old_messages()

    def _delete_old_messages(self):
        while len(self.messages) >= self.height - 1:
            del self.messages[0]

    def _draw_frame(self):
        self.console.draw_frame(0, 0, None, None, "?", fg=M_GREY, bg=BLACK)

    def _fill(self):
        self.console.draw_rect(0, 0, width=None, height=None, string=None, bg=self.bg)

    def clear(self):
        self.console.clear(fg=self.fg, bg=self.bg)

    def reset(self):
        self.clear()
        self._fill()
