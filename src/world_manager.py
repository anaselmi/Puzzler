from esper import World
from src.ecs.processors import *
from src.ecs.components import *


class WorldManager(World):
    def __init__(self, engine, size):
        super().__init__()
        self.engine = engine
        self.width, self.height = size

    def handle(self, action):
        turn_processor = self.get_processor(TurnProcessor)
        active, active_component = turn_processor.get_active()
        action_processor = self.get_processor(ActionProcessor)
        action_processor.handle(active, action)

    def update(self):
        self.process()
