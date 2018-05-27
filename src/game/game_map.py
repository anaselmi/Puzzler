import tdl


class GameMap(tdl.map.Map):
    def __init__(self, size):
        width, height = self.size = size
        super().__init__(width, height)