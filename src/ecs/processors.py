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


class VelocityProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        # Moves all entities with a velocity
        for ent, (pos, vel) in self.world.get_components(Positionable, Velocity):
            if vel.dx == 0 and vel.dy == 0:
                continue
            pos.x += vel.dx
            pos.y += vel.dy
            vel.dx = 0
            vel.dy = 0



class ActionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        pass

    def handle(self, entity, action):
        if action is None:
            return
        if action[0:4] == "MOVE":
            if not self.world.has_component(entity, Velocity):
                print(entity)
                return
            vel = self.world.component_for_entity(entity, Velocity)
            if action == "MOVE_NORTH":
                vel.dy -= 1
            elif action == "MOVE_SOUTH":
                vel.dy += 1
            elif action == "MOVE_EAST":
                vel.dx += 1
            elif action == "MOVE_WEST":
                vel.dx -= 1
            elif action == "MOVE_NORTHWEST":
                vel.dy -= 1
                vel.dx -= 1
            elif action == "MOVE_SOUTHWEST":
                vel.dy += 1
                vel.dx -= 1
            elif action == "MOVE_NORTHEAST":
                vel.dy -= 1
                vel.dx += 1
            elif action == "MOVE_SOUTHEAST":
                vel.dy += 1
                vel.dx += 1
            print(vel.dx, vel.dy)


# SPAGHETTI
class TurnProcessor(esper.Processor):
    def __init__(self, ticks_per_turn=100, tick_threshold=0, minimum_ticks=1):
        super().__init__()
        self.ticks_per_turn = ticks_per_turn
        self.tick_threshold = tick_threshold
        self.minimum_ticks = minimum_ticks
        self.ticks = 0
        self.turn = 0

    def process(self):
        active_entity, active_turn_component = self.get_active()

    def get_active(self):
        entities = list(self.world.get_component(TurnTaking))
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

    def set_active(self):
        entities = self.world.get_component(TurnTaking)
        while True:
            entities.sort(key=lambda x: x[1].energy, reverse=True)
            highest_ticks_component = entities[0][1]
            highest_tick_number = highest_ticks_component.ticks
            if highest_tick_number < self.tick_threshold:
                self.tick(self.minimum_ticks)
                continue
            break
        tied_entities = list(filter(lambda ent: ent[1].ticks == highest_tick_number, entities))
        tied_amount = len(tied_entities)
        assert(tied_amount >= 1)
        if tied_amount != 1:
            # If we have more than one possible choice, we choose the one with the highest speed
            tied_entities.sort(key=lambda x: x[1].speed, reverse=True)
        self.reset_active()
        active_entity_component = tied_entities[0][1]
        active_entity_component.active = True

    def reset_active(self):
        for ent, turn_taking in self.world.get_component(TurnTaking):
            turn_taking.active = False

    def tick(self, tick_amount):
        self.ticks += tick_amount
        self.turn = self.ticks / self.ticks_per_turn
        for ent, turn_taking in self.world.get_component(TurnTaking):
            speed = turn_taking.speed
            new_ticks = tick_amount * speed
            turn_taking.ticks += new_ticks
