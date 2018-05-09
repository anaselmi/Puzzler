import esper
from itertools import chain
from src.consts import *
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


# This processor should only be responsible for updating
# position based on velocity, it shouldn't have to care about whether the move is even possible
class VelocityProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        # Moves all entities with a velocity
        for ent, (pos, vel) in self.world.get_components(Positionable, Velocity):
            if vel.dx == 0 and vel.dy == 0:
                continue
            print(pos.x, pos.y, "BEFORE")
            pos.x = int(pos.x + vel.dx)
            pos.y = int(pos.y + vel.dy)
            print(pos.x, pos.y, "AFTER")
            vel.dx = 0
            vel.dy = 0


# For now this processor essentially parses actions and modifies components
# but it should eventually create the most logical event based on the action and gamestate
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
                direction = "north."
                color = WHITE
            elif action == "MOVE_SOUTH":
                vel.dy += 1
                direction = "south."
                color = WHITE
            elif action == "MOVE_EAST":
                vel.dx += 1
                direction = "east."
                color = WHITE
            elif action == "MOVE_WEST":
                vel.dx -= 1
                direction = "west."
                color = WHITE
            elif action == "MOVE_NORTHWEST":
                vel.dy -= 1
                vel.dx -= 1
                direction = "northwest."
                color = GREEN
            elif action == "MOVE_SOUTHWEST":
                vel.dy += 1
                vel.dx -= 1
                direction = "southwest."
                color = GREEN
            elif action == "MOVE_NORTHEAST":
                vel.dy -= 1
                vel.dx += 1
                direction = "northeast."
                color = GREEN
            elif action == "MOVE_SOUTHEAST":
                vel.dy += 1
                vel.dx += 1
                direction = "southeast."
                color = GREEN
            else:
                raise RuntimeError
            text = "You moved " + direction
            message = (text, color)
            self.world.add_message(entity, message)


# Vocabulary:
# Tick: The smallest possible unit of time, every event takes a certain amount of ticks to happen.
# Every tick, entities
# Turn: 100 ticks. Repeating events are often measured in turns instead of ticks, and every turn,
# some of these events might fire.
# Energy: An int representing how many ticks an entity has collected, has a cap unique to that entity.
# Speed: A number that represents how much energy an entity gains each tick.
class TickProcessor(esper.Processor):
    def __init__(self, ticks_per_turn=100, tick_threshold=0, minimum_ticks=1):
        super().__init__()
        self.ticks_per_turn = ticks_per_turn
        self.tick_threshold = tick_threshold
        self.minimum_ticks = minimum_ticks
        self.ticks = 0
        self.turn = 0

    def process(self):
        pass

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
        for ent, tick in self.world.get_component(Ticking):
            tick.active = False

    def tick(self, tick_amount):
        self.ticks += tick_amount
        self.turn = self.ticks / self.ticks_per_turn
        for ent, tick in self.world.get_component(Ticking):
            speed = tick.speed
            new_ticks = tick_amount * speed
            tick.ticks += new_ticks
