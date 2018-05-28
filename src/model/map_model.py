from model.model import Model


class MapModel(Model):
    def __init__(self):
        super().__init__()
        self.tiles = []
        self.ents = []
        self.effects = []
