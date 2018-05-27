import abc


class StateABC(abc.ABC):
    @abc.abstractmethod
    def enter(self):
        pass

    @abc.abstractmethod
    def exit(self):
        pass

    @abc.abstractmethod
    def render(self, console):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def handle(self, command):
        pass
