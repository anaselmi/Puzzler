from itertools import chain

import esper

from src.logic.components import *


class RenderProcessor(esper.Processor):

    def __init__(self):
        super().__init__()

    def process(self, event, context):
        pass

    def get_entities(self):
        entities = list(self.world.get_components(Renderable, Positionable))
        entities.sort(key=lambda entity: entity[1][0].priority, reverse=True)
        return entities

    def get_center(self):
        # List of all entities in the world that can be rendered and are the PC
        players = [x for x in self.world.get_components(Controllable, Renderable, Positionable) if x[1][0].is_player]
        if players:
            # Ensures we have one PC, as we always should
            if len(players) != 1:
                print("CANNOT BE CERTAIN THIS IS THE RIGHT CENTER")
            pos = players[0][1][2]
            return pos.x, pos.y
        raise RuntimeError


class MessageProcessor(esper.Processor):
    def __init__(self, messages):
        super().__init__()
        self.messages = messages

    # Sends out a list of recent messages from all processes that sent them
    def process(self, event, context):
        for ent, mes in self.world.get_component(Messaging):
            self.add_messages(mes.messages)
            mes.messages = []

    def add_messages(self, messages):
        self.messages = list(chain(self.messages, messages))

    def get_messages(self):
        messages = self.messages
        self.messages = []
        return messages


# This processor is only responsible for updating position based on velocity, not for checking validity
class VelocityProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, event, context):
        # Moves all entities with a velocity
        for ent, (pos, vel) in self.world.get_components(Positionable, Velocity):
            if vel.dx == 0 and vel.dy == 0:
                continue
            pos.x += vel.dx
            pos.y += vel.dy
            vel.dx = 0
            vel.dy = 0


# For now this processor essentially parses actions and modifies components
# but it should eventually create the most logical event based on the command and gamestate
class CommandProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, event, context):
        command = kwargs.get("command", {})
        for entity, (_, controllable) in self.world.get_components(Active, Controllable):
            move = command.get("move")
            if move and self.world.has_component(entity, Velocity):
                vel = self.world.component_for_entity(entity, Velocity)
                if move.startswith("north"):
                    vel.dy -= 1
                elif move.startswith("south"):
                    vel.dy += 1

                if move.endswith("east"):
                    vel.dx += 1
                elif move.endswith("west"):
                    vel.dx -= 1

    def _move(self, entity, direction):
        pass


class TurnProcessor(esper.Processor):
    def __init__(self, ticks_per_turn=100, tick_threshold=0, minimum_ticks=1):
        super().__init__()
        self.ticks_per_turn = ticks_per_turn
        self.tick_threshold = tick_threshold
        self.minimum_ticks = minimum_ticks
        self.ticks = 0
        self.turn = 0

    def process(self, kwargs):
        active_entities = list(self.world.get_component(Active))
        assert(len(active_entities) == 1)

        active_component = active_entities[0][1]
        time_passed = active_component.ticks
        assert(isinstance(time_passed, int))
        active_component.ticks = 0

    def get_active(self):
        entities = list(self.world.get_component(Ticking))
        while True:
            entities.sort(key=lambda x: x[1].energy, reverse=True)
            highest_tick_component = entities[0][1]
            highest_tick_number = highest_tick_component.energy
            if highest_tick_number < self.tick_threshold:
                self.tick(self.minimum_ticks)
                continue
            break
        tied_entities = list(filter(lambda ent: ent[1].energy == highest_tick_number, entities))
        tied_amount = len(tied_entities)
        assert (tied_amount >= 1)
        if tied_amount != 1:
            # If we have more than one possible choice, we choose the one with the highest speed
            tied_entities.sort(key=lambda x: x[1].speed, reverse=True)
        self.reset_active()
        active = tied_entities[0]
        active_entity = active[0]
        active_entity_component = active[1]
        active_entity_component.active = True
        return active_entity, active_entity_component

    def reset_active(self):
        for ent, active in self.world.get_component(Active):
            self.world.remove_component(ent, active)

    def tick(self, time_passed):
        self.ticks += time_passed
        self.turn = self.ticks / self.ticks_per_turn
        for ent, tick in self.world.get_component(Ticking):
            speed = tick.speed
            new_ticks = time_passed * speed
            tick.ticks += new_ticks
