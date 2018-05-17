from src.input_handling import update_command


class StateStack:

    # Should we treat the world as a special case?
    def __init__(self):
        self.stack = []

    def push(self, state):
        self.stack.append(state)
        state.enter()
        return state

    def pop(self):
        state = self.stack.pop()
        state.exit()
        return state

    def reset_stack(self):
        old_states = self.states
        self.states = []
        return old_states

    def render(self, console):
        for state in reversed(self.stack):
            state.render(console)

    def clear(self):
        for state in reversed(self.stack):
            state.clear()

    # Only the state at the top of the stack can receive input
    def handle(self, command):
        result = self.stack[-1].handle(command)
        command = update_command(command, result)
        return command

    def update(self):
        for state in reversed(self.stack):
            state.update()

