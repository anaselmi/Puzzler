import abc
import logging
from commands import get_command, KEY_CONSUMED

logger = logging.getLogger(__name__)


class StateStack:
    def __init__(self, screen):
        self.screen = screen
        self.stack = []
        logger.debug("State stack created.")

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

    # Called once per event. May be called multiple times per loop.
    # Only the state at the top of the stack can dispatch commands.
    def dispatch(self, event):
        return self.stack[-1].dispatch(event)

    def update(self):
        self.stack[-1].update()

    # Called right before rendering. States draw onto internet elements.
    def draw(self):
        for state in self.stack:
            state.draw()

    # Called right before flushing to root.
    def render(self):
        for state in self.stack:
            state.render(self.screen)

    # Called right after flushing to root.
    def reset(self):
        for state in self.stack:
            state.reset()

    def reset_stack(self):
        states = self.states
        self.states = []
        return states


class State(abc.ABC):
    def __init__(self, stack, event_map):
        self.stack = stack
        self.event_map = event_map
        self.handlers = []
        self.coms = []
        self.elems = []
        self.ctrls = []

    # @abc.abstractmethod
    # Called when state is pushed onto the stack.
    def enter(self, screen):
        pass

    # @abc.abstractmethod
    # Called when state is popped from the stack.
    def exit(self):
        pass

    # @abc.abstractmethod
    # Called at the start of a new loop.
    def start(self):
        pass

    # @abc.abstractmethod
    # Parse and modify commands. Only called if state is at the top of the stack.
    def dispatch(self, event):
        command = get_command(event, self.event_map)
        for handler, args, kwargs in self.handlers:
            result = self._dispatch(handler, command, *args, **kwargs)
            # Command consumed by handler and has been appended to self.coms.
            if result is None:
                return command
            command = result
        return command

    # @abc.abstractmethod
    # Modify gamestate based on commands and rules determined by state
    def update(self):
        pass

    # Updates elements based on gamestate and animation state.
    def draw(self):
        pass

    # @abc.abstractmethod
    #  Blits elements onto the screen. Should not be used to update elements.
    def render(self, screen):
        pass

    # @abc.abstractmethod
    # Resets states for the next loop.
    def reset(self):
        self.coms = []
        [elem.reset() for elem in self.elems]

    def add_handler(self, handler, *args, **kwargs):
        handler_data = (handler, args, kwargs)
        self.handlers.append(handler_data)

    def get_command(self, event):
        return get_command(event, self.event_map)

    def _dispatch(self, handler, command, *args, **kwargs):
        result = handler.handle(command=command, *args, **kwargs)
        consumed = result.get(KEY_CONSUMED)
        if consumed:
            command_data = [handler, command]
            self.coms.append(command_data)
            return None
        return result

