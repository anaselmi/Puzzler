import tcod
import itertools


class MessageConsole:
    def __init__(self, screen_x, screen_y):
        self.x = int(screen_x / 6)
        self.y = int(screen_y / 3)
        self.console = tcod.console_new(self.x, self.y)
        self.message_archive = []

        tcod.console_set_alignment(self.console, tcod.LEFT)

    def update_archive(self, messages):
        if isinstance(messages, str):
            self.message_archive.append(messages)

        elif isinstance(messages, list):
            self.message_archive = itertools.chain(self.message_archive, messages)

        if len(self.message_archive) >= 100:
            pass

    def draw(self, text):
        tcod.console_print(self.console, 0, 0, text)

    def clear(self):
        self.console.clear()

    def blit(self, console):
        tcod.console_blit(self.console, 0, 0, 0, 0, console, 0, 0)











