import esper
from itertools import chain
from src.ecs.components import *


class RenderProcessor(esper.Processor):

    def __init__(self, ui_dimensions, level_dimensions):
        super().__init__()
        self.ui_dimensions = ui_dimensions
        self.ui_x, self.ui_y = ui_dimensions
        self.level_dimensions = level_dimensions
        self.level_x, self.level_y = level_dimensions

    def process(self):
        updated_entities = list(self.world.get_components(Renderable, Positionable))
        updated_entities.sort(key=lambda x: x[1][0].priority)
        for ent, (rend, pos, mov) in updated_entities:
            rend.x = pos.x
            rend.y = pos.y


class PositionProcessor(esper.Processor):
    def __init__(self, level_dimensions):
        super().__init__()
        self.level_x, self.level_y = level_dimensions

    def process(self):
        # Moves all entities with a velocity
        for ent, (pos, vel) in self.world.get_components(Positionable, Velocity):
            if vel.dx != 0 or vel.dy != 0:
                continue
            else:
                # Might want to cast these to int's later
                pos.x += vel.dx
                pos.y += vel.dy


class MessageProcessor(esper.Processor):
    def __init__(self, window, messages):
        super().__init__()
        self.window = window
        self.messages = messages

    # Sends out a list of recent messages from all processes that sent them
    def process(self):
        for ent, mes in self.world.get_component(Messaging):
            self.add_messages(mes.messages)
            mes.messages = []

    def add_messages(self, entity, messages):
        self.messages = list(chain(self.messages, messages))

    def send_messages(self):
        messages = self.messages
        self.messages = []
        return messages

