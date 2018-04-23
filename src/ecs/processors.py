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

    def valid_tile(self, ent, target_x, target_y):
        tile_contents = self.game_map.tile_contents
        if not tile_contents:
            return target_x, target_y
        for entity in tile_contents:
            pass

    def loop(self, target_x, target_y):

        # Moving left
        if target_x < self.window.x:
            print("{} is greater than {}".format(target_x, self.window.x))
            print("LEFT")
            offset = abs(self.window.x - target_x - 1)
            target_x = self.window.width - offset

        # Moving right
        elif target_x > self.window.width - 1:
            print("{} is greater than {}".format(target_x, self.window.width))
            print("RIGHT")
            offset = self.target_x - self.window.width - 1
            target_x = self.window.x + offset

        # Moving up
        if target_y < self.window.y:
            print("{} is greater than {}".format(target_y, self.window.y))
            print("UP")
            offset = abs(self.window.x - target_x - 1)
            target_y = self.window.height - offset

        # Moving down
        elif target_y > self.window.height - 1:
            "{} is greater than {}".format(target_y, self.window.height)
            print("DOWN")
            offset = self.target_y - self.window.y - 1
            target_y = self.window.y + offset

        return target_x, target_y

    def check_conflicts(self, ent, other_ent):
        ent_pos = self.world.component_for_entity(ent, Positionable)
        other_ent_pos = self.world.component_for_entity(other_ent, Positionable)
        if not other_ent_pos.pathable:
            return False
        return True


class GameMap:
    def __init__(self, width, height, world):
        self.width = width
        self.height = height
        self.world = world
        self.tiles = [[[] for x in range(0, self.width)] for y in range(0, self.height)]
        print(self.tiles)

    def update_tile(self, ent, x, y):
        pass

    def tile_contents(self, x, y):
        print(x, y, "GM TARGETS")
        print(self.width, self.height, "MAP SIZE")
        print(len(self.tiles[21]), "TILE LEN")
        contents = self.tiles[y][x]
        if contents:
            return contents
        return None

    def empty_tile(self, x, y):
        pass

    def update_entity(self, ent, x, y):
        ent_pos = self.world.component_for_entity(ent, Positionable)
        current_x = ent_pos.x
        current_y = ent_pos.y
        if ent in self.tiles[current_y][current_x]:
            self.tiles[current_y][current_x].remove(ent)
        self.tiles[y][x].append(ent)

    def populate_tiles(self):
        for ent, pos in self.world.get_component(Positionable):
            x = pos.x
            y = pos.y
            self.tiles[y][x] += ent


class LoopingProcessor(esper.Processor):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.min_x = 0
        self.max_x = self.window.width
        self.min_y = 0
        self.max_y = self.window.height

    def process(self, context):
        print("LOOPING")
        for ent, (vel, pos) in self.world.get_components(Velocity, Positionable):
            message = ""
            # Moving left
            if pos.x < self.min_x:
                pos.x = self.max_x - 1
                message = " looped to the right!"
            # Moving right
            elif pos.x > self.max_x - 1:
                pos.x = self.min_x
                message = " looped to the left!"
            # Moving up
            elif pos.y < self.min_y:
                pos.y = self.max_y - 1
                message = " looped to the bottom!"
            # Moving down
            elif pos.y > self.max_y - 1:
                pos.y = self.min_y
                message = " looped to the top!"
            else:
                continue
            if not self.world.has_component(ent, Describable):
                continue

            desc = self.world.component_for_entity(ent, Describable)
            logging_processor = self.world.get_processor(LoggingProcessor)
            message = [desc.reference + message]
            logging_processor.add_messages(message)


class LoggingProcessor(esper.Processor):
    def __init__(self, window, messages=[]):
        super().__init__()
        self.window = window
        self.messages = messages

    # Sends out a list of recent messages from all processes that sent them
    def process(self, context):
        print("LOGGING")
        self.window.process(self.messages)
        self.messages = []

    def add_messages(self, messages):
        self.messages = list(chain(self.messages, messages))

