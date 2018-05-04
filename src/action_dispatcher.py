from src.input_handler import InputHandler


class ActionDispatcher:
    def __init__(self, engine, subscribers):
        self.engine = engine
        self.subscribers = subscribers
        self.current_priority = None

    # Every subscriber to the dispatcher must have a function called process.
    # Process either returns None (signifying that it ran without the action),
    # the same action (signifying that it has been consumed),
    # a different action (signifying that it has been consumed and replaced),
    # or ellipses (signifying that is has been consumed and the subscriber requests more actions).
    def dispatch(self, action):
        if self.current_priority is not None:
            self._priority_dispatch(action)
            return
        for subscriber in self.subscribers:
            result = subscriber.process(action)
            if result is ...:
                self.current_priority = subscriber
            action = self._update_action(action, result)

    # If a subscriber requests more actions, then they get priority over all other processors
    # until they signify that they no longer want priority by returning None
    def _priority_dispatch(self, action):
        result = self.current_priority.process(action)
        if result is None:
            self.current_priority = None
        action = self._update_action(action, result)

        for subscriber in self.subscribers:
            # Currently not allowing priority to change while we have a current priority
            # this may change when we actually try it out in practice
            result = subscriber.process(action)
            action = self._update_action(action, result)

    @staticmethod
    def _update_action(action, result):
        if result is None:
            return action
        if result is ... or result == action:
            return None
        else:
            return result

    def __call__(self, action):
        return self.dispatch(action)



