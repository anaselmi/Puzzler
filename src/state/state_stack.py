from commands import update_command


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

    def reset_stack(self):
        old_states = self.states
        self.states = []
        return old_states

    def start(self):
        for state in reversed(self.stack):
            state.start()

    def render(self):
        for state in reversed(self.stack):
            state.render(self.screen)

    # Only the state at the top of the stack can handle input
    def handle(self, command):
        result = self.stack[-1].handle(command)
        command = update_command(command, result)
        return command

    def update(self, dx):
        for state in reversed(self.stack):
            state.update(dx)
