from src.consts import *
from itertools import chain
import esper


class RenderProcessor(esper.Processor):

    def __init__(self, window, clear_color=WHITE):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        self.window.clear()
        for ent, rend in self.world.get_component(Renderable):
            self.window.draw_char(rend.x, rend.y, rend.char)



class Renderable:
    def __init__(self, x, y, char, color=WHITE):
        self.x = x
        self.y = y
        self.char = char
        self.color = color


class MovementProcessor(esper.Processor):
    def __init__(self, window_x, window_y):
        super().__init__()
        self.window_x = window_x
        self.window_y = window_y

    def process(self):
        for ent, (mov, rend) in self.world.get_components(Moving, Renderable):
            rend.x += mov.x
            rend.y += mov.y
            mov.x = 0
            mov.y = 0


class Moving:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class LoopingProcessor(esper.Processor):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.min_x = 0
        self.max_x = self.window.width
        self.min_y = 0
        self.max_y = self.window.height

    def process(self):
        for ent, rend in self.world.get_component(Renderable):
            # Moving left
            if rend.x < self.min_x:
                rend.x = self.max_x - 1
                message = "You looped left!"
            # Moving right
            if rend.x > self.max_x - 1:
                rend.x = self.min_x
            message = "You looped right!"
            # Moving up
            if rend.y < self.min_y:
                rend.y = self.max_y - 1
            message = "You looped up!"
            # Moving down
            if rend.y > self.max_y - 1:
                rend.y = self.min_y
                message = "You looped down!"

            if self.world.has_component(ent, Logging):
                log = self.world.component_for_entity(ent, Logging)
                log.messages += message


class LoggingProcessor(esper.Processor):
    def __init__(self, window, outgoing=[]):
        super().__init__()
        self.window = window
        self.outgoing = outgoing

    # Sends out a list of recent messages from all entities, and resets their lists
    def process(self):
        for ent, log in self.world.get_component(Logging):
            if not log.messages:
                pass
            self.outgoing = list(chain(self.outgoing, log.messages))
            log.messages = []
        self.window.process(self.outgoing)
        self.outgoing = []


class Logging:
    def __init__(self, messages=[]):
        self.messages = messages
