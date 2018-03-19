from consts import *
from message import Message
import tcod


class Unit:
    # The class from which all game objects inherit from, might just end up being for the PC only
    # TODO: Turn into an ABC
    # TODO: Start adding a lot more stats, only after creating design docs
    def __init__(self, x=0, y=0, char=1, color=tcod.white, texts=[], text_color=tcod.white, text_priority=2):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.texts = texts
        self.text_color = text_color
        self.text_priority = text_priority
        self.messages = []

    def loop(self):
        # Method that will probably be deprecated fairly soon

        # Moving left
        if self.x < 0:
            self.x = SCREEN_X - 1
            self.texts.append("You looped")
        # Moving right
        if self.x > SCREEN_X - 1:
            self.x = 0
            self.texts.append("You looped")
        # Moving up
        if self.y < 0:
            self.y = SCREEN_Y - 1
            self.texts.append("You looped")
        # Moving down
        if self.y > SCREEN_Y - 1:
            self.y = 0
            self.texts.append("You looped")

    def move(self, update):
        dx = update[0]
        dy = update[1]
        if dx != 0:
            self.x += dx

            if dx >= 1:
                direction = "right"
            elif dx <= -1:
                direction = "left"

        elif dy != 0:
            self.y += dy

            if dy >= 1:
                direction = "down"
            elif dy <= -1:
                direction = "up"

        self.texts.append("You moved " + direction)

        self.loop()

    def draw(self, console):
        # Call before blitting and flushing con
        tcod.console_put_char(console, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, console):
        # Call after blitting and flushing con
        tcod.console_put_char(console, self.x, self.y, T_SPACE, tcod.BKGND_NONE)

    def output_messages(self):
        out_messages = []
        for text in self.texts:

            out_messages.append(Message(text, self.color))

        self.texts = []


        return out_messages



