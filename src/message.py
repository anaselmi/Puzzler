import tdl
import tcod


class Message:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color
        self.subject = []
        self.verb = []
        self.object = []
