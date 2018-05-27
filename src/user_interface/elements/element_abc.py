import abc
import tdl


class ElementABC(abc.ABC):
    def __init__(self, name, console, size, destination, fg, bg):
        self.name = name
        self.console = console
        width, height = size
        self.x, self.y = destination
        self.window = tdl.Window(self.console, self.x, self.y, width, height)
        self.width, self.height = self.window.get_size()
        self.fg, self.bg = fg, bg
        self.window.set_colors(fg=self.fg, bg=self.bg)

    @abc.abstractmethod
    def update(self):
        pass
