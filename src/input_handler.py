class InputHandler:
    # Turns user input into strings that different game elements can parse
    # Although these strings are written with player input in mind, they can
    # be parsed by any game element that requires user input
    @staticmethod
    def handle(_input):
        _type = _input.type
        if _type == "KEYDOWN":
            key = _input.keychar
            if key == 'ESCAPE':
                return {"EXIT": True}
            if key == 'ENTER':
                return {"RETURN": True}
            elif key == "UP" or key == "KP8":
                return {"MOVE": "NORTH"}
            elif key == "DOWN" or key == "KP2":
                return {"MOVE": "SOUTH"}
            elif key == "LEFT" or key == "KP4":
                return {"MOVE": "WEST"}
            elif key == "RIGHT" or key == "KP6":
                return {"MOVE": "EAST"}
            elif key == "KP7":
                return {"MOVE": "NORTHWEST"}
            elif key == "KP1":
                return {"MOVE": "SOUTHWEST"}
            elif key == "KP9":
                return {"MOVE": "NORTHEAST"}
            elif key == "KP3":
                return {"MOVE": "SOUTHEAST"}

            elif key == "l":
                return {"LOOK": True}
        return {}

    # Not really possible to use this on the class itself as it tries to
    # instantiate a new object, maybe hijack new if we really need this
    # functionality but for now its better to call process
    def __call__(self, _input):
        return self.handle(_input)

