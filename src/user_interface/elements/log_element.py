import itertools

from src.consts import *
from src.user_interface.elements.element_abc import ElementABC


class MessageElement(ElementABC):
    def __init__(self, console, size, destination):
        name = "log"
        fg = D_GREY
        bg = BLACK
        super().__init__(name, console, size, destination, fg, bg)

        self.frame_color = WHITE
        self.frame_char = "."

    def draw_log(self, log):
        self._fill()
        self._draw_frame()
        assert(len(log) < self.height)
        for i, message in enumerate(log):
            text = message.text
            fg = message.color
            # Add 1 to i to make sure we don't render onto the frame
            self.window.draw_str(1, i+1, text, fg)

    def update(self):
        pass

    def _draw_frame(self):
        self.window.draw_frame(0, 0, None, None, "?", fg=M_GREY, bg=BLACK)

    def _fill(self):
        self.window.draw_rect(0, 0, width=None, height=None, string=None, bg=self.bg)

    def clear(self):
        self.window.clear(fg=self.fg, bg=self.bg)

    def reset(self):
        self.clear()
        self._fill()