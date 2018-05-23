import itertools

from src.consts import *
from src.user_interface.elements.element_abc import ElementABC


class MessageElement(ElementABC):
    def __init__(self, console, size, destination):
        fg = D_GREY
        bg = BLACK
        super().__init__(console, size, destination, fg, bg)

        self.frame_color = WHITE
        self.frame_char = "."
        self.messages = []

    def render(self):
        self.draw()

    def draw(self):
        self._fill()
        self._draw_frame()
        assert(len(self.messages) < self.height)
        for i, message in enumerate(self.messages):
            text = message.text
            fg = message.color
            # Add 1 to i to make sure we don't render onto the frame
            self.window.draw_str(1, i+1, text, fg)

    def update(self):
        pass

    def update_messages(self, messages):
        self.messages = list(itertools.chain(self.messages, messages))
        self._delete_old_messages()

    def _delete_old_messages(self):
        while len(self.messages) >= self.height - 1:
            del self.messages[0]

    def _draw_frame(self):
        self.window.draw_frame(0, 0, None, None, "?", fg=M_GREY, bg=BLACK)

    def _fill(self):
        self.window.draw_rect(0, 0, width=None, height=None, string=None, bg=self.bg)

    def clear(self):
        self.window.clear(fg=self.fg, bg=self.bg)

    def reset(self):
        self.clear()
        self._fill()
