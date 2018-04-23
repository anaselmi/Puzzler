import esper
from itertools import chain
from src.consts import *
from src.ecs.components import *


class RenderProcessor(esper.Processor):

    def __init__(self, window):
        super().__init__()
        self.window = window

    def process(self, context):
        # []
        updated_entities = list(self.world.get_components(Renderable, Positionable, Velocity))
        updated_entities.sort(key=lambda x: x[1][0].priority)
        for ent, (rend, pos, mov) in updated_entities:
            rend.x = pos.x
            rend.y = pos.y
            self.window.draw_char(rend.x, rend.y, rend.char)


class PositionProcessor(esper.Processor):
    def __init__(self, window, game_map):
        super().__init__()
        self.window = window
        self.game_map = game_map

    def process(self, context):
        # Moves all entities with a velocity if the target tile is pathable
        for ent, pos in self.world.get_component(Positionable):
            if self.world.has_component(ent, Velocity):
                pos.moved = True
                vel = self.world.component_for_entity(ent, Velocity)
                loop = vel.loop
                tangible = pos.tangible
                target_x = pos.x + vel.x
                target_y = pos.y + vel.y
                if loop:
                    target_x, target_y = self.loop(target_x, target_y)
                    tile_contents = self.game_map.tile_contents(target_x, target_y)
                if tangible and tile_contents:
                    for entity in tile_contents:
                        if self.check_conflicts(ent, entity):
                            move = False
                            break

                if pos.moved:
                    self.game_map.update_entity(ent, target_x, target_y)
                    pos.x = target_x
                    pos.y = target_y
                vel.x = 0
                vel.y = 0


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

    def add_messages(self, messages):
        self.messages = list(chain(self.messages, messages))

    def send_messages(self):
        messages = self.messages
        self.messages = []
        return messages

