import tcod
import itertools
from consts import *
from message import Message

# TODO: Create console as an ABC
# TODO: Create ConsoleHandler
# TODO: Create a MapConsole
# TODO: Create a MapConsole


class MessageConsole:
    # TODO: Add logic to MCon that allows it to either calculate its own size or simply use parameters given
    # TODO: MCon takes flags that alter what is printed
    # TODO: Player always printed first
    def __init__(self, SCREEN_X, SCREEN_Y, archive_max=100, current=[]):
        self.x = int(SCREEN_X)
        self.y = int(SCREEN_Y / 4)

        self.console = tcod.console_new(self.x, self.y)
        tcod.console_set_alignment(self.console, tcod.LEFT)

        # Keeps records of messages that happened earlier
        self.archive = []
        self.archive_max = archive_max

        # Messages from the newest turn
        self.current = current

    def update_archive(self, messages=None):
        # Gives us the ability to keep records of events that happened earlier since new is always cleared
        if messages is None:
            self.archive += self.current
        else:
            self.archive += messages

        # Deletes older messages if we start archiving too many
        if len(self.archive) > self.archive_max:
            new_start = len(self.archive) - self.archive_max
            self.archive = self.archive[new_start:]

    def update_current(self, messages):
        # Loop brings in recent messages and sends them to archive
        # Loop should always clear itself at the end of a loop
        self.current = messages
        self.update_archive()

    def draw(self):
        # Draw should be a simple function
        # Index is to make sure messages don't print on top of each other and don't print out of console
        for i, message in enumerate(self.current):
            if i > 11:
                break
            text = message.text
            color = message.color
            tcod.console_print(self.console, 0, i, text)

    def clear(self):
        self.console.clear()

    def blit(self, console):
        tcod.console_blit(self.console, 0, 0, 0, 0, console, 0, 0)

    def scroll(self):
        if self.current >= self.y:
            return False
        self.current = self.current[self.y: -1]
        return True

    def sort(self, messages):
        pass

    # Every console/handler should have an update
    def update(self, messages):

        if self.current:
            self.archive += self.current

        if messages:
            self.current = []
            self.update_current(messages)


