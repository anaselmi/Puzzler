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
    def clear(self):
        pass

    @abc.abstractmethod
    def update(self, action):
        pass
