import esper
from itertools import chain
from src.ecs.components import *


class RenderProcessor(esper.Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        pass

    def get_entities(self):
        entities = list(self.world.get_components(Renderable, Positionable))
        entities.sort(key=lambda entity: entity[1][0].priority, reverse=True)
        return entities

    def get_center(self):
        # List of all entities in the world that can be rendered and are the PC
        players = [x for x in self.world.get_components(Playable, Renderable, Positionable) if x[1][0].is_player]
        if players:
            # Ensures we have one PC, as we always should
            if len(players) != 1:
                print("CANNOT BE CERTAIN THIS IS THE RIGHT CENTER")
            pos = players[0][1][2]
            return pos.x, pos.y
        raise RuntimeError


class VelocityProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

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
    def __init__(self, messages):
        super().__init__()
        self.messages = messages

    # Sends out a list of recent messages from all processes that sent them
    def process(self):
        for ent, mes in self.world.get_component(Messaging):
            self.add_messages(mes.messages)
            mes.messages = []

    def add_messages(self, messages):
        self.messages = list(chain(self.messages, messages))

    def get_messages(self):
        messages = self.messages
        self.messages = []
        return messages

