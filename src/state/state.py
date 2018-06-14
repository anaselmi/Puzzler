import abc


class StateStack:
    def __init__(self, screen):
        self.screen = screen
        self.stack = []

    def push(self, state):
        self.stack.append(state)
        state.enter(self.screen)
        return state

    def pop(self):
        state = self.stack.pop()
        state.exit()
        return state

    # Called at the beginning of each loop.
    def start(self):
        for state in reversed(self.stack):
            state.start()

    # Called once per command. May be called multiple times per loop.
    # Only the state at the top of the stack can dispatch commands.
    def dispatch(self, command):
        return self.stack[-1].dispatch(command)

    # Called right before rendering.
    def update(self):
        for state in reversed(self.stack):
            state.update()

    # Called right before flushing to root.
    def render(self):
        for state in reversed(self.stack):
            state.render(self.screen)

    # Called right after flushing to root.
    def reset(self):
        for state in reversed(self.stack):
            state.reset()

    def reset_stack(self):
        states = self.states
        self.states = []
        return states


class State(abc.ABC):
    def __init__(self, stack):
        self.stack = stack

    # @abc.abstractmethod
    # Called when state is pushed onto the stack.
    def enter(self, screen):
        pass

    # @abc.abstractmethod
    # Called when state is popped from the stack.
    def exit(self):
        pass

    # @abc.abstractmethod
    # Used by models to store data before it is updated to allow for complex animations.
    def start(self):
        pass

    # @abc.abstractmethod
    # Allows state to update gamestate based on the command. Only called if state is at the top of the stack.
    def dispatch(self, command):
        pass

    # @abc.abstractmethod
    # Updates elements based on gamestate and animation context.
    def update(self):
        pass

    # @abc.abstractmethod
    #  Blits elements onto the screen. Should not be used to update elements.
    def render(self, screen):
        pass

    # @abc.abstractmethod
    # Ensures elements are only rendered once. Not all elements are actually cleared.
    def reset(self):
        pass
