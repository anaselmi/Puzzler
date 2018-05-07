from esper import World
from src.ecs.processors import *
from src.ecs.components import *


class WorldManager(World):
    def __init__(self, engine, size):
        super().__init__()
        self.engine = engine
        self.width, self.height = size

    # Turns actions (parsed player inputs) into an event
    def handle(self, action):
        tick_processor = self.get_processor(TickProcessor)
        entity, tick = tick_processor.get_active()
        if not self.has_component(entity, Playable):
            return
        action_processor = self.get_processor(ActionProcessor)
        action_processor.handle(entity, action)

    # Feeds an event into
    def update(self):
        self.process()

    def add_message(self, entity, message):
        if not self.has_component(entity, Messaging):
            mes = Messaging()
            self.add_component(entity, mes)
        else:
            mes = self.component_for_entity(entity, Messaging)
        mes.messages.append(message)
