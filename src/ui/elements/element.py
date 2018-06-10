import tdl

from consts import *


class Element:
    """Base class for UI elements.

    Creates and adds framing functionality to a TDL console. Exposes methods that users can
    use in predefined ways they determine from the name of the element."

    Notes:
        Do not draw onto the console outside of methods provided by class and subclasses.

    Attributes:
        name (string): Used by outside code to determine specialized methods/attributes.
        size: Contains width and height of the element.
        c: The TDL console the element draws onto.
        c_pos: Contains c_x and c_y. Position relative to the screen.
        c_size: Contains c_width and c_height.
        c_width (int): Width of the console.
        c_height (int): Height of the console.
        plt: Foreground/Background colors of the element.
        f_size: Contains f_w and f_h. Width and height of the frame
        f_char (string): Character used to draw the frame.
        f_plt: Fore/Background of the frame.
    """
    def __init__(self, name, pos, size, sc_size, plt=PLT_WB, f_size=FRAME_SIZE, f_char=FRAME_CHAR, f_plt=(..., ...)):
        """Initializes element and optional frame.

        :param string name: Sets name for element.
        :param tuple pos: Sets default blit coordinates for console (takes frame into account).
        :param tuple size: Size of the base console. A value of -1 causes that dimension to fill the screen.
        :param tuple sc_size: Size of the screen.
        :param tuple plt: Palette used by element.
        :param tuple f_size: Size of the frame.
        :param tuple f_char: Character used to frame element.
        :param tuple f_plt: Palette used by frame.
        """
        super().__init__()
        self.name = name
        self.c_pos = self.c_x, self.c_y = pos
        self._init_console(size, sc_size, plt)
        self._init_frame(f_size, f_char, f_plt)

    def _init_console(self, size, screen_size, plt):
        width, height = size
        screen_width, screen_height = screen_size
        self.c_width = screen_width if width == -1 else width
        self.c_height = screen_height if height == -1 else height
        self.c_size = self.c_width, self.c_height
        self.c = tdl.Console(self.c_width, self.c_height)
        self.plt = self.fg, self.bg = plt
        self.c.set_colors(fg=self.fg, bg=self.bg)

    def _init_frame(self, size, char, plt):
        self.f_size = self.f_width, self.f_height = size
        self.f_char = char
        self.f_plt = self.f_fg, self.f_bg = plt
        if self.f_width == 0 or self.f_height == 0:
            self._draw_frame((0, 0), "", (..., ...))
        else:
            self._draw_frame(self.f_size, self.f_char, self.f_plt)
        self.width = self.c_width - (self.f_width * 2)
        self.height = self.c_height - (self.f_height * 2)
        self.size = self.width, self.height

    def clear(self):
        """Clears the element. Does not clear the frame.

        :return: None
        """
        self.c.draw_rect(self.f_width, self.f_height, self.width, self.height, None)

    def _draw_frame(self, size, char, plt):
        width, height = size
        fg, bg = plt
        self.c.draw_rect(0, 0,
                         width=width, height=height,
                         string=char, fg=fg, bg=bg)

    def _adjust(self, pos):
        x, y = pos
        adjusted = x + self.f_width, y + self.f_height
        return adjusted

    def in_elem(self, pos):
        """ Checks if a position is within the drawable portion of the screen.

        :param tuple pos: The position in question. (x, y).
        :return bool: Whether the position is in the usable part of the element or not.
        """
        x, y = pos
        if not (x >= 0 + self.f_width) or not (x < self.width - self.f_width):
            return False
        if not (y >= 0 + self.f_height) or not (y < self.height - self.f_height):
            return False
        return True
