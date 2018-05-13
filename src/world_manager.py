from esper import World
from src.ecs.processors import *
from src.ecs.components import *


class WorldManager(World):
    def __init__(self, engine, size):
        super().__init__()
        self.engine = engine
        self.width, self.height = size

    def handle(self, action):
        tick_processor = self.get_processor(TickProcessor)
        active, active_component = tick_processor.get_active()
        action_processor = self.get_processor(ActionProcessor)
        action_processor.handle(active, action)
        self.process()

    def update(self, action):
        tick_processor = self.get_processor(TickProcessor)
        active, active_component = tick_processor.get_active()
        action_processor = self.get_processor(ActionProcessor)
        action_processor.handle(active, action)
        self.process()
