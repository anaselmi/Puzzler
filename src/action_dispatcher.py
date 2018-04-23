

# Responsible for taking an action and chain feeding it to different functions/methods
# until it returns None, which means it is currently at the top of the stack
class ActionDispatcher:
    def __init__(self, subscribers):
        self.subscribers = subscribers
        self.current_priority = None

    # Everything subscriber of the stack must have a function called handle,
    # which either returns None, signifying that it has been parsed and handled
    # the same action, signifying that it has not been parsed, or ellipses, signifying
    # that is has been parsed and the subscriber requires further input
    def dispatch(self, action):
        if self.current_priority is None:
            for subscriber in self.subscribers:
                action = subscriber.process(action)
                if action is ...:
                    self.current_priority = subscriber
                    break
        else:
            current_priority = self.current_priority
            action = self.current_priority.process(action)
            if action is not ...:
                self.current_priority = None
                if action is not None:
                    action = self._dispatch_from(action, current_priority)
        return action

    # This code simply sends an action to the list starting from a current subscriber, useful for resolving
    # edge cases after resolving a priority subscriber
    def _dispatch_from(self, action, subscriber):
        subscriber_index = self.subscribers.index(subscriber)
        for subscriber in self.subscribers[subscriber_index:]:
            action = subscriber.process(action)
            if action is ...:
                self.current_priority = subscriber
                break
        return action

    def __call__(self, action):
        return self.dispatch(action)



