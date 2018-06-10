class Event:
    def __init__(self, name):
        self.name = name


class MessageEvent(Event):
    def __init__(self, text, color=...):
        name = "log"
        super().__init__(name)
        self.text = text
        self.color = color

