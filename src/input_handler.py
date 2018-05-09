class InputHandler:
    # Turns user input into strings that different game elements can parse
    # Although these strings are written with player input in mind, they can
    # be parsed by any game element that requires user input
    @staticmethod
    def handle(_input):
        key = _input.keychar
        if key == 'ESCAPE':
            return "QUIT_GAME"
        if key == 'ENTER':
            return "RETURN"
        elif key == "UP" or key == "KP8":
            return "MOVE_NORTH"
        elif key == "DOWN" or key == "KP2":
            return "MOVE_SOUTH"
        elif key == "LEFT" or key == "KP4":
            return "MOVE_WEST"
        elif key == "RIGHT" or key == "KP6":
            return "MOVE_EAST"
        elif key == "KP7":
            return "MOVE_NORTHWEST"
        elif key == "KP1":
            return "MOVE_SOUTHWEST"
        elif key == "KP9":
            return "MOVE_NORTHEAST"
        elif key == "KP3":
            return "MOVE_SOUTHEAST"
        elif key == "l":
            return "LOOK"
        return None

    # Not really possible to use this on the class itself as it tries to
    # instantiate a new object, maybe hijack new if we really need this
    # functionality but for now its better to call process
    def __call__(self, _input):
        return self.handle(_input)

