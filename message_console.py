import tcod
import itertools


class MessageConsole:
    def __init__(self, SCREEN_X, SCREEN_Y):
        self.x = int(SCREEN_X)
        self.y = int(SCREEN_Y / 3)
        self.console = tcod.console_new(self.x, self.y)
        self.message_archive = ["Welcome to Puzzler"]

        tcod.console_set_alignment(self.console, tcod.LEFT)

    def update_archive(self, messages):
        if isinstance(messages, str):
            self.message_archive.append(messages)

        elif isinstance(messages, list):
            self.message_archive = list(itertools.chain(self.message_archive, messages))

        if len(self.message_archive) >= 100:
            pass

    def draw(self):
        tcod.console_print(self.console, 0, 0, self.message_archive[-1])
        print(self.message_archive[-1])

    def clear(self):
        self.console.clear()

    def blit(self, console):
        tcod.console_blit(self.console, 0, 0, 0, 0, console, 0, 0)











