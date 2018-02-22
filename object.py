import tcod
from consts import *


class Object:
    # Potentially the class from which all game objects inherit from, might just end up being for the PC only
    # TODO: Start adding a lot more stats
    def __init__(self, x=0, y=0, char=1, color=tcod.white):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def loop(self):
        # Method that will probably be deprecated fairly soon

        # Moving left
        if self.x < 0:
            self.x = SCREEN_X - 1
        # Moving right
        if self.x > SCREEN_X - 1:
            self.x = 0
        # Moving up
        if self.y < 0:
            self.y = SCREEN_Y - 1
        # Moving down
        if self.y > SCREEN_Y - 1:
            self.y = 0

    def move(self, update):
        dx = update[0]
        dy = update[1]
        if dx != 0:
            self.x += dx

        if dy != 0:
            self.y += dy

        self.loop()

    def draw(self, console):
        # Call before blitting and flushing 0
        tcod.console_put_char(console, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, console):
        # Call after blitting and flushing 0
        tcod.console_put_char(console, self.x, self.y, T_SPACE, tcod.BKGND_NONE)


