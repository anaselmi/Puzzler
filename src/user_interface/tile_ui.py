import tdl
from src.user_interface.ui import UI
from src.camera import Camera
from src.consts import *


class TileUI(UI):
    def __init__(self, manager, size, destination=(0, 0)):
        super().__init__()
        self.fg = P_L_GREEN
        self.bg = BLACK
        self.default_char = "."
        self.tiles = None

        self.manager = manager
        self.width, self.height = self.size = size
        self.x, self.y = self.destination = destination

        self.console = tdl.Console(self.width, self.height)
        self.console.set_colors(fg=self.fg, bg=self.bg)

    def handle(self, action, world):
        pass

    def parse_world(self, world):
        center = world.send_center
        self.camera.adjust(center)

        tiles = self._reset_tiles()
        entities = world.send_renderable_entities()
        self.add_entities(tiles, entities)

        if tiles != self.tiles:
            self.redraw = True
            self.tiles = tiles

    def update(self):
        pass

    def draw(self):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                valid = tile.get("valid")
                if not valid:
                    continue
                fg = tile.get("fg", self.fg)
                bg = tile.get("bg", self.bg)
                char = tile.get("char")
                if char is None:
                    raise RuntimeError
                self.console.draw_char(x, y, char=char, fg=fg, bg=bg)

    def _fill(self):
        self.console.draw_rect(0, 0, None, None, string=None, fg=self.fg, bg=self.bg)

    def clear(self):
        self.console.clear(fg=self.fg, bg=self.bg)

    def add_entities(self, tiles, entities):
        for ent, (rend, pos) in entities:
            world_x, world_y = world_pos = pos.x, pos.y
            screen_x, screen_y = screen_pos = self.camera.translate(world_pos, source="world")
            if screen_x is None or screen_y is None:
                continue
            x = screen_x
            y = screen_y
            tile = tiles[y][x]
            char = rend.char
            tile["char"] = char
            fg = rend.fg if rend.fg is not None else ...
            tile["fg"] = fg
            bg = rend.bg if rend.bg is not None else ...
            tile["bg"] = bg

    def create_camera(self, world_size):
        self.camera = Camera(screen_size=self.size, world_size=world_size)

    def _reset_tiles(self):
        width, height = self.size
        tiles = [[{} for _ in range(0, width)] for _ in range(0, height)]
        return tiles
