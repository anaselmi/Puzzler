import tdl
import tcod
from consts import *
from message import Message
import tcod


class Unit:
    # The class from which all game objects inherit from, might just end up being for the PC only
    # TODO: Turn into an ABC
    # TODO: Start adding a lot more stats, only after creating design docs
    def __init__(self, fg, bg, window, x=0, y=0, char=1, texts=[], text_color=tcod.white):
        self.x = x
        self.y = y
        self.char = char
        self.fg = fg
        self.bg = bg
        self.texts = texts
        self.text_color = text_color
        self.window = window
        self.messages = []

    def loop(self):
        # Method that will probably be deprecated fairly soon

        # Moving left
        if self.x < 0:
            self.x = self.window.width - 1
            self.texts.append("You looped to the right.")
        # Moving right
        if self.x > self.window.width - 1:
            self.x = 0
            self.texts.append("You looped to the left.")
        # Moving up
        if self.y < 0:
            self.y = self.window.height - 1
            self.texts.append("You looped to the bottom.")
        # Moving down
        if self.y > self.window.height - 1:
            self.y = 0
            self.texts.append("You looped to the top.")

    def move(self, update):
        dx = update[0]
        dy = update[1]
        if dx != 0:
            self.x += dx

            if dx >= 1:
                direction = "right."
            elif dx <= -1:
                direction = "left."

        elif dy != 0:
            self.y += dy

            if dy >= 1:
                direction = "down."
            elif dy <= -1:
                direction = "up."

        self.texts.append("You moved " + direction)

        self.loop()

    def draw(self, window=None):
        window = self.window_missing(window)
        window.draw_char(self.x, self.y, self.char, bg=(0, 0, 0), fg=(255, 255, 255))

    def clear(self, window=None):
        window = self.window_missing(window)
        window.draw_char(self.x, self.y, char=" ")

    def window_missing(self, window):
        if window is None:
            return self.window
        return window

    def output_messages(self):
        out_messages = []
        for text in self.texts:

            out_messages.append(Message(text, self.fg))

        self.texts = []
        return out_messages



