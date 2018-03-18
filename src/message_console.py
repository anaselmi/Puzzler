import tcod
import itertools
from consts import *

# TODO: Create console as an ABC
# TODO: Create ConsoleHandler
# TODO: Create a MapConsole
# TODO: Create a MapConsole


class MessageConsole:
    # TODO: Add logic to MCon that allows it to either calculate its own size or simply use parameters given
    # TODO: MCon takes flags that alter what is printed
    # TODO: Player always printed first
    def __init__(self, SCREEN_X, SCREEN_Y):
        self.x = int(SCREEN_X)
        self.y = int(SCREEN_Y / 4)
        self.console = tcod.console_new(self.x, self.y)
        self.archive = [STARTING_MESSAGE]
        self.new = []
        self.clear_new = True

        tcod.console_set_alignment(self.console, tcod.LEFT)

    def update_archive(self):
        # Gives us the ability to keep records of events that happened earlier since new is always cleared
        self.archive += self.new

        # Deletes older messages if we start archiving too many
        if len(self.archive) > 100:
            new_start = len(self.archive) - 100
            self.archive = self.archive[new_start:100]

    def update_new(self, messages):
        # We bring in the most recent batch of messages, and add them to new so they can be printed
        assert(isinstance(messages, list))
        self.new = list(itertools.chain(self.new, messages))
        self.update_archive()

    def draw(self):
        # Index is to make sure messages don't print on top of each other and don't print out of console
        for i, message in enumerate(self.new):
            if i > 11:
                break
            tcod.console_print(self.console, 0, i, message)

        self.clear_new = True
        if len(self.new) > 12:
            self.clear_new = False
            self.new = self.new[12:]

    def clear(self):
        self.console.clear()

        # Make sure new isn't cleared if we decide to scroll through text
        if self.clear_new:
            self.new = []

    def blit(self, console):
        tcod.console_blit(self.console, 0, 0, 0, 0, console, 0, 0)

    def scroll(self):
        pass











