from src.consts import *
from src.ui.elements.element import Element


class MessageElement(Element):
    name = "log"
    plt = (D_GREY, BLACK)

    def __init__(self, con, size, pos):
        name = MessageElement.name
        plt = MessageElement.plt
        super().__init__(name, con, pos, size, plt=plt)

    def draw_logs(self, logs):
        x = 0
        self.clear()
        assert(len(logs) < self.h)
        for y, log in enumerate(logs):
            self.draw_log(log, x, y)

    def draw_log(self, log, x, y):
        pass

    def _draw_log(self, x, y, text, color):
        self.c.draw_str(x + self.f_w, y + self.f_h, text, color)
