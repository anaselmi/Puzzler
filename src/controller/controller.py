import abc


class Controller(abc.ABC):
    def __init__(self, name, element):
        self.name = name
        self.element = element
        self.redraw = True

    @abc.abstractmethod
    def handle(self, data, command=None):
        pass

    @abc.abstractmethod
    def update(self, data, command=None):
        pass

    @abc.abstractmethod
    def draw(self):
        pass
