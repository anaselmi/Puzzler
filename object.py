import tcod
from consts import *


class Object:
    # Potentially the class from which all game objects inherit from, might just end up being for the PC only
    def __init__(self, X=0, Y=0, char="@", color=tcod.white):
        self.X = X
        self.Y = Y
        self.char = char
        self.color = color

    def act(self, action):
        if action == "MOVE UP":
            self.Y -= 1
        if action == "MOVE DOWN":
            self.Y += 1
        if action == "MOVE LEFT":
            self.X -= 1
        if action == "MOVE RIGHT":
            self.X += 1
