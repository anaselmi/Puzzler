import tdl

from game.processors.processors import RenderProcessor
from ui.elements.map_element import MapElement
from ui.elements.log_element import MessageElement


# TODO: Rename ui windows to elements
class PlayUI:
    def __init__(self, size):
        self.width, self.height = size
        self.console = tdl.Console(self.width, self.height)
        self.elements = []
        log_element_height = int(self.height / 5)
        map_element_height = self.height - log_element_height
        self._create_map_element(size=(None, map_element_height), destination=(0, 0))
        self._create_log_element(size=(None, None), destination=(0, map_element_height))

    def _create_log_element(self, size, destination):
        self.log_element = MessageElement(self.console, size=size, pos=destination)
        self.elements.append(self.log_element)

    def _create_map_element(self, size, destination):
        self.map_element = MapElement(self.console, size=size, pos=destination)
        self.elements.append(self.map_element)

    def render(self, console):
        console.blit(self.console)

    def handle(self, command, level):
        self._update_map_element(level)

    def update(self):
        pass
