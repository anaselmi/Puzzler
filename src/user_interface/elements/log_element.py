from src.consts import *
from src.user_interface.elements.element import Element


class MessageElement(Element):
    name = "log"
    con_fg = D_GREY

    def __init__(self, con, size, pos):
        name = MessageElement.name
        fg = MessageElement.fg
        super().__init__(name, con, pos, size, fg=fg)
        super().create_frame(fg=fg)

    def draw_logs(self, logs):
        x = 0
        self.clear_contents()
        assert(len(logs) < self.height)
        for y, log in enumerate(logs):
            self.draw_log(log, x, y)

    def draw_log(self, log, x, y):
        pass

    def _draw_log(self, x, y, text, color):
        self.window.draw_str(x + self.frame_width, y + self.frame_height, text, color)

    def draw_frame(self):
        self.window.draw_frame(0, 0,
                               width=self.frame_width, height=self.frame_height,
                               string=self.frame_char, fg=self.frame_fg, bg=self.frame_bg)

    def clear_log(self, x, y=0):
        self.window.draw_rect(x + self.frame_char, y + self.frame_height,
                              width=self.frame_width, height=self.frame_height,
                              string=self.frame_char, bg=self.frame_bg)

    def clear_contents(self):
        self.window.draw_rect(0, 0, width=None, height=None, string=None, bg=self.con_bg)
