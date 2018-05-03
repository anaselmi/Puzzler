import esper
from itertools import chain
from src.ecs.components import *


class RenderProcessor(esper.Processor):

    def __init__(self):
        super().__init__()
        self.tiles = self._reset_tiles()

    def process(self):
        entities = list(self.world.get_components(Renderable, Positionable))
        # Overwrites tile with entities of higher priorities so that they are drawn on the very top
        entities.sort(key=lambda entity: entity[1][0].priority, reverse=True)
        for ent, (rend, pos) in entities:
            x, y = pos.x, pos.y
            tile = self.tiles[y][x]
            tile["fg"] = rend.fg
            tile["bg"] = rend.bg
            tile["char"] = rend.char

    def send_tiles(self):
        tiles = self.tiles
        self.tiles = self._reset_tiles()
        return tiles

    def _reset_tiles(self):
        # tiles is a nested dictionary of tiles contents nested in a list of lists
        # corresponding to [y][x] dimensions
        width = self.world.width
        height = self.world.height
        return [[{} for _ in range(0, height + 1)] for _ in range(0, width + 1)]


class PositionProcessor(esper.Processor):
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

    def send_messages(self):
        messages = self.messages
        self.messages = []
        return messages

