import abc


class ModelABC(abc.ABC):
    def __init__(self):
        self.rerender = True

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def handle(self, command, level):
        pass

    @abc.abstractmethod
    def update(self, level):
        pass
