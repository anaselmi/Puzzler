class EventManager:
    def __init__(self, world):
        self.world = world
        self.listeners = {}
        self.messages = []

    def add_listener(self, listener, event_name):
        if self.listeners.get(event_name) is None:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def remove_listener(self, listener, event_name):
        if self.listeners.get(event_name) is None:
            return
        if listener not in self.listeners[event_name]:
            return
        self.listeners[event_name].remove(listener)

    def notify(self, message):
        self.messages.append(message)
        message_name = message.name
        for listener in self.listeners.get(message_name, []):
            listener.receive(message)