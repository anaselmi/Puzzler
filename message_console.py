import tcod
import itertools

class MessageConsole:
    def __init__(self, screen_x, screen_y):
        self.x = screen_x / 6
        self.y = screen_y / 3
        self.console = tcod.console_new(self.x, self.y)
        self.message_archive = []

    def update_archive(self, messages):
        if isinstance(messages, str):
            self.message_archive.append(messages)

        elif isinstance(messages, list):
            self.message_archive = itertools.chain(self.message_archive, messages)








