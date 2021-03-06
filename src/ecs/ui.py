import abc
import tdl


class UI(abc.ABC):
    def __init__(self, console, size, destination, fg, bg):
        self.console = console
        width, height = size
        self.x, self.y = destination
        self.window = tdl.Window(self.console, self.x, self.y, width, height)
        self.width, self.height = self.window.get_size()
        self.fg, self.bg = fg, bg
        self.window.set_colors(fg=self.fg, bg=self.bg)