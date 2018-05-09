import abc


class UI(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        # Flag that gets reset to False every game loop and has to
        # be explicitly switched for UI element to be redrawn
        self.redraw = True

    @abc.abstractmethod
    def handle(self, action, world):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def parse_world(self, world):
        pass

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def clear(self):
        pass
