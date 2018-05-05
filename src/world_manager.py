import esper


class WorldManager(esper.World):
    def __init__(self, engine, size):
        super().__init__()
        self.engine = engine
        self.width, self.height = size

    def handle(self, action):
        pass
