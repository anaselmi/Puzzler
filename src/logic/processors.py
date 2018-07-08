from esper import Processor
import src.commands as com
from src.logic.components import *


class RenderProcessor(Processor):
    def process(self, command):
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


class LoggingProcessor(Processor):
    def process(self, command):
        pass

    def receive(self, message):
        name = message.name
        if name == "moved":
            ent = message.subject
            if self.world.has_component(ent, Controllable):
                cont = self.world.component_for_entity(Controllable)
                if cont.player:
                    pass


# This processor is only responsible for updating position based on velocity, not for checking validity
class VelocityProcessor(Processor):
    def process(self, command):
        # Moves all entities with a velocity
        for ent, (pos, vel) in self.world.get_components(Positionable, Velocity):
            if vel.dx == 0 and vel.dy == 0:
                continue
            pos_old = pos.x, pos.y
            pos.x += vel.dx
            pos.y += vel.dy
            pos_new = pos.x, pos.y
            vel.dx = 0
            vel.dy = 0
            if pos_old != pos_new:
                # pass
                print(f"Controllable entity moved from {pos_old} to {pos_new}.")


class CommandProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.is_player_turn = False

    # TODO: Process should take who's turn it is into account.
    def process(self, command):
        self.is_player_turn = False
        for entity, controllable in self.world.get_component(Controllable):
            data = entity, command
            if self._move(*data):
                break
        # Code takes this branch if we don't break from the loop, meaning no action has been taken.
        else:
            return
        self.is_player_turn = True

    def _move(self, entity, command):
        move = command.get(com.KEY_MOVE)
        if move is None:
            return False
        vel = self.world.component_for_entity(entity, Velocity)
        vel.dx += move[0]
        vel.dy += move[1]
        return True


class TurnProcessor(Processor):
    def __init__(self, ticks_per_turn=100, tick_threshold=0, minimum_ticks=1):
        super().__init__()
        self.ticks_per_turn = ticks_per_turn
        self.tick_threshold = tick_threshold
        self.minimum_ticks = minimum_ticks
        self.ticks = 0
        self.turn = 0

    def process(self, event):
        pass

    def get_active(self):
        pass
