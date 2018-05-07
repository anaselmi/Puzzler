import tdl
import random
from src.ecs.processors import RenderProcessor
from src.camera import Camera
from src.consts import *


class TileUI:
    def __init__(self, manager, console, size, destination=(0, 0)):
        fg = P_L_GREEN
        bg = BLACK
        default_chars = [".", ";", ":"]
        self.fg = fg
        self.bg = bg
        self.default_chars = default_chars
        self.manager = manager
        self.console = console
        width, height = size
        self.x, self.y = destination

        self.window = tdl.Window(self.console, self.x, self.y, width, height)
        # Width and height aren't assigned to the object to account for initializing window with None
        self.width, self.height = self.window.get_size()
        self.window.set_colors(fg=self.fg, bg=self.bg)
        self.tiles = None

    def create_camera(self, world_size):
        screen_size = self.get_screen_size()
        self.camera = Camera(screen_size=screen_size, world_size=world_size)

    def draw(self):
        self._fill()
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
                self.window.draw_char(x, y, char=char, fg=fg, bg=bg)

    def _fill(self):
        self.window.draw_rect(0, 0, None, None, string=None, fg=self.fg, bg=self.bg)

    def clear(self):
        self.window.clear(fg=self.fg, bg=self.bg)

    def get_screen_size(self):
        return self.window.get_size()

    def random_default(self):
        return random.choice(self.default_chars)

    def process(self, action):
        pass

    def update(self):
        old_top, old_left = self.camera.top, self.camera.left
        self.adjust_camera()
        if self.camera.top != old_top or self.camera.left != old_left:
            self.reset_valid_tiles()
        self._reset_tiles()
        self.update_valid_tiles()
        self.update_entities()

    def reset_valid_tiles(self):
        screen_width, screen_height = self.get_screen_size()
        rows = list(range(0, screen_width))
        valid_rows = []
        for row in rows:
            pos = row, 0
            translated_row = self.camera.translate(pos, source="screen")[0]
            valid_row = isinstance(translated_row, int)
            if valid_row:
                valid_rows.append(row)
            else:
                assert(translated_row is None)

        cols = list(range(0, screen_height))
        valid_cols = []
        for col in cols:
            pos = 0, col
            translated_col = self.camera.translate(pos, source="screen")[1]
            valid_col = isinstance(translated_col, int)
            if valid_col:
                valid_cols.append(col)
            else:
                assert(translated_col is None)

        self.valid_tiles = valid_rows, valid_cols

    def update_tiles(self):
        self._reset_tiles()
        self.update_valid_tiles()
        self.update_entities()

    def update_valid_tiles(self):
        rows, cols = self.valid_tiles
        for y in cols:
            for x in rows:
                tile = self.tiles[y][x]
                tile["valid"] = True
                tile["char"] = self.random_default()

    def update_entities(self):
        entities = self.get_renderable_entities()
        for ent, (rend, pos) in entities:
            world_x, world_y = world_pos = pos.x, pos.y
            screen_x, screen_y = screen_pos = self.camera.translate(world_pos, source="world")
            if screen_x is None or screen_y is None:
                continue
            x = screen_x
            assert (x in self.valid_tiles[0])
            y = screen_y
            assert(y in self.valid_tiles[1])
            tile = self.tiles[y][x]
            char = rend.char
            tile["char"] = char
            fg = rend.fg if rend.fg is not None else ...
            tile["fg"] = fg
            bg = rend.bg if rend.bg is not None else ...
            tile["bg"] = bg

    def adjust_camera(self):
        render_processor = self.get_render_processor()
        center = render_processor.get_center()
        adjusted = self.camera.adjust(center=center)
        return adjusted

    def get_renderable_entities(self):
        render_processor = self.get_render_processor()
        entities = render_processor.get_entities()
        return entities

    def get_render_processor(self):
        return self.manager.engine.world.get_processor(RenderProcessor)

    def _reset_tiles(self):
        width, height = self.get_screen_size()
        tiles = [[{} for _ in range(0, width)] for _ in range(0, height)]
        self.tiles = tiles
