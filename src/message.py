import tcod


class Message:
    def __init__(self, text, color=tcod.white, priority=2):
        self.text = text
        self.color = color
        # The lower the priority the better, only the PC can be 0
        self.priority = priority


