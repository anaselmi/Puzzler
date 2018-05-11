class StateStack:

    # Should we treat the world as a special case?
    def __init__(self):
        self.stack = []

    def push(self, state):
        self.stack.append(state)

    def pop(self):
        popped = self.stack.pop()
        return popped

    def render(self):
        for state in reversed(self.stack):
            state.render()

    def clear(self):
        old_states = self.states
        self.states = []
        return old_states

    # Only the state at the top of the stack can receive input
    def handle(self, action, **kwargs):
        result = self.stack[-1].handle(action, **kwargs)
        action = self._update_action(action, result)
        return action

    @staticmethod
    def _update_action(action, result):
        print(result)
        # State did not consume action
        if result == {} or result is None:
            return action
        # State consumed action
        if result == action:
            return None
        # State generated new action
        else:
            return result
