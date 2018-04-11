import tcod
from consts import *


class HandleButton:
    def __init__(self, state=None):
        self.state = state

    def process(self, button):
        key = button.keychar
        if key == 'ESCAPE':
            return "quit_game", True

        if self.state is None:
            if key == "UP":
                return "move", (0, -1)
            elif key == "DOWN":
                return "move", (0, 1)
            elif key == "LEFT":
                return "move", (-1, 0)
            elif key == "RIGHT":
                return "move", (1, 0)
            elif key == "l":
                self.state = "look"
                return "change_state", None

        elif self.state == "look":
            if key == "UP":
                return "move_cursor", (0, -1)
            elif key == "DOWN":
                return "move_cursor", (0, 1)
            elif key == "LEFT":
                return "move_cursor", (-1, 0)
            elif key == "RIGHT":
                return "move_cursor", (1, 0)
            elif key == "ENTER":
                return "look", None
            elif key == "l":
                return "change_back", "look"

        return None, None

