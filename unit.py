from consts import *
import tcod


class Unit:
    # Potentially the class from which all game objects inherit from, might just end up being for the PC only
    # TODO: Add an interface for certain methods
    # TODO: Start adding a lot more stats
    def __init__(self, x=0, y=0, char=1, color=tcod.white, messages=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        if messages:
            self.messages = messages
        else:
            self.messages = []

    def loop(self):
        # Method that will probably be deprecated fairly soon

        # Moving left
        if self.x < 0:
            self.x = SCREEN_X - 1
            self.messages.append("You looped")
        # Moving right
        if self.x > SCREEN_X - 1:
            self.x = 0
            self.messages.append("You looped")
        # Moving up
        if self.y < 0:
            self.y = SCREEN_Y - 1
            self.messages.append("You looped")
        # Moving down
        if self.y > SCREEN_Y - 1:
            self.y = 0
            self.messages.append("You looped")

    def move(self, update):
        dx = update[0]
        dy = update[1]
        if dx != 0:
            self.x += dx

        if dy != 0:
            self.y += dy

        self.loop()

    def draw(self, console):
        # Call before blitting and flushing con
        tcod.console_put_char(console, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, console):
        # Call after blitting and flushing con
        tcod.console_put_char(console, self.x, self.y, T_SPACE, tcod.BKGND_NONE)


