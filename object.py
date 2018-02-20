import tcod
from consts import *

class Object:
    def __init__(self, X=0, Y=0, char="@", color=tcod.white):
        self.X = X
        self.Y = Y
        self.char = char
        self.color = color

    def act(self, action):
        if action == "MOVE UP":
            print("UP")
            self.Y -= 1
        if action == "MOVE DOWN":
            print("DOWN")
            self.Y += 1
        if action == "MOVE LEFT":
            print("LEFT")
            self.X -= 1
        if action == "MOVE RIGHT":
            print("RIGHT")
            self.X += 1
