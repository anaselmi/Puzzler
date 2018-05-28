import tdl

from consts import *


class Element:
    """Base class for UI elements.

    Creates and adds framing functionality to a TDL console. Subclasses can modify the console with
    methods that other code interface with in predefined ways they determine from the name of the element.
    For example, an element with the name "inventory" would be expected to have methods like
    "draw_item(name, pos, char, color)" or "draw_item_stats_ratio(stat_name, current, total, pos, char, color)"

    Types:
        Fore/background(f/bg) is a tuple containing three ints where 255>= (f/bg) >= 0.
        Character(char) is a string where len(char) == 1.
        Position(pos) is a tuple containing 2 ints, an x position and a y position.
        Dimensions(size) is a tuple containing 2 ints, a width and a height.

    Notes:
        Because of the way elements are implemented, con_size don't represent
        usable screen dimensions. As such, use size when drawing to the element.

        Because of this, drawing to the console contained by the element should ONLY
        be done through an element and the public methods it exposes.

    Attributes:
        name (string): Used by outside code to determine specialized methods/attributes.
        size: Contains width and height.
        width (int): Width of the element.
        height (int): Height of the element.
        con: A TDL console the element draws onto.
        con_pos: Contains con_x and con_y.
        con_x (int): X position of the console relative to the screen.
        con_y (int): Y position of the console relative to the screen.
        con_size: Contains con_width and con_height.
        con_width (int): Width of the console.
        con_height (int): Height of the console.
        con_fg: Default color of characters drawn inside the element.
        con_bg: Default background color of the element.
        f_size: Contains f_width and f_height.
        f_width (int): Width of the frame.
        f_height (int): Height of the frame.
        f_char (string): Character used to draw the frame.
        f_fg: Default color of the frame character.
        f_bg: Background color of the frame.
    """
    def __init__(self, name, pos, size, screen_size, fg=FG, bg=BG):
        """Initializes element. Creates default value for frame.

        Arguments:
            :param string name: Name of the element.
            :param tuple pos: Position of the console relative to the screen.
            :param tuple size: Dimensions of the console. A value of -1 sets that dimension to it's
            corresponding screen dimension.
            :param tuple screen_size: Dimensions of the screen.
            :param tuple fg: Optional. Default color of characters drawn inside the element. Defaults to consts.FG.
            :param tuple bg: Also optional. Default background color of the element. Defaults to consts.BG.
        """
        super().__init__()
        self.name = name
        self.con_pos = self.con_x, self.con_y = pos
        self._init_console(size, screen_size, fg, bg)
        # Creates a dummy frame with no size that can be overridden later.
        self.init_frame(size=(0, 0), char=None, fg=..., bg=...)

    def init_frame(self, size=FRAME_SIZE, char=FRAME_CHAR, fg=FRAME_FG, bg=FRAME_BG):
        self.con.clear()
        self.f_size = self.f_width, self.f_height = size
        self.f_char = char
        self.f_fg = fg
        self.f_bg = bg
        self._draw_frame(self.f_size, self.f_char, self.f_fg, self.f_bg)
        self.width = self.con_width - (self.f_width * 2)
        self.height = self.con_height - (self.f_height * 2)
        self.size = self.width, self.height

    def clear(self):
        self.con.draw_rect(self.f_width, self.f_height, self.width, self.height, None)

    def _draw_frame(self, size, char, fg, bg):
        width, height = size
        self.con.draw_rect(0, 0,
                           width=width, height=height,
                           string=char, fg=fg, bg=bg)

    def _init_console(self, size, screen_size, fg, bg):
        width, height = size
        screen_width, screen_height = screen_size
        self.con_width = screen_width if width == -1 else width
        self.con_height = screen_height if height == -1 else height
        self.con_size = self.con_width, self.con_height
        self.con = tdl.Console(self.con_width, self.con_height)
        self.con_fg = fg
        self.con_bg = bg
        self.con.set_colors(fg=self.con_fg, bg=self.con_bg)
