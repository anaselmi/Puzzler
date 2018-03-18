from consts import *
import tcod


class Unit:
    # The class from which all game objects inherit from, might just end up being for the PC only
    # TODO: Turn into an ABC
    # TODO: Start adding a lot more stats, only after creating design docs
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

            if dx > 1:
                self.messages.append("You moved right")
            else:
                self.messages.append("You moved left")

        if dy != 0:
            self.y += dy
            for sd in range(0, 25):
                self.messages.append(str(sd))

            if dy > 1:
                self.messages.append("You moved down")
            else:
                self.messages.append("You moved up")

        self.loop()

    def draw(self, console):
        # Call before blitting and flushing con
        tcod.console_put_char(console, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, console):
        # Call after blitting and flushing con
        tcod.console_put_char(console, self.x, self.y, T_SPACE, tcod.BKGND_NONE)

    def get_messages(self):
        new_messages = self.messages
        self.messages = []
        return new_messages


