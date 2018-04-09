from src.consts import *
from itertools import chain
import esper


class RenderProcessor(esper.Processor):

    def __init__(self, window):
        super().__init__()
        self.window = window

    def process(self):
        self.window.clear()

        # This allows the game to always draw the player on top of everything else
        playable = []
        for ent, rend in self.world.get_component(Renderable):
            if not rend.active:
                continue
            if self.world.has_component(ent, Playable):
                playable.append(rend)
                continue

            self.window.draw_char(rend.x, rend.y, rend.char, fg=rend.fg)

        for rend in playable:
            self.window.draw_char(rend.x, rend.y, rend.char, fg=rend.fg)


class Renderable:
    def __init__(self, x, y, char, fg=WHITE, active=True):
        self.x = x
        self.y = y
        self.char = char
        self.fg = fg
        self.active = active


class MovementProcessor(esper.Processor):
    def __init__(self, window_x, window_y):
        super().__init__()
        self.window_x = window_x
        self.window_y = window_y

    def process(self):
        for ent, (vel, rend) in self.world.get_components(Velocity, Renderable):
            rend.x += vel.x * vel.speed
            rend.y += vel.y * vel.speed
            vel.x = 0
            vel.y = 0


class Velocity:
    def __init__(self, x=0, y=0, speed=1):
        self.x = x
        self.y = y
        self.speed = speed


class LoopingProcessor(esper.Processor):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.min_x = 0
        self.max_x = self.window.width
        self.min_y = 0
        self.max_y = self.window.height

    def process(self):
        for ent, (vel, rend) in self.world.get_components(Velocity, Renderable):
            message = ""
            # Moving left
            if rend.x < self.min_x:
                rend.x = self.max_x - 1
                message = " looped to the right!"
            # Moving right
            elif rend.x > self.max_x - 1:
                rend.x = self.min_x
                message = " looped to the left!"
            # Moving up
            elif rend.y < self.min_y:
                rend.y = self.max_y - 1
                message = " looped to the bottom!"
            # Moving down
            elif rend.y > self.max_y - 1:
                rend.y = self.min_y
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
    def process(self):
        self.window.process(self.messages)
        self.messages = []

    def add_messages(self, messages):
        self.messages = list(chain(self.messages, messages))


class Describable:
    def __init__(self, name, reference, description):
        self.name = name
        self.reference = reference
        self.description = description


class Playable:
    def __init__(self):
        pass
