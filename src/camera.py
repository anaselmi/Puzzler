

class Camera:
    def __init__(self, screen_size, world_size):
        self.screen_size = screen_size
        self.screen_width, self.screen_height = self.screen_size
        # The width/height of the screen/ you are drawing to must be odd.
        # This is to avoid having no/two centers for an even dimension.
        assert(self.screen_width % 2 and self.screen_height % 2)
        self.world_size = world_size
        self.world_width, self.world_height = self.world_size

    def adjust(self, center):
        try:
            old_top = self.top
            old_left = self.left
        except AttributeError:
            old_top = None
            old_left = None
        center_x, center_y = center
        adjusted_x = self._adjust(center=center_x, screen=self.screen_width, world=self.world_width)
        self.left = adjusted_x
        adjusted_y = self._adjust(center=center_y, screen=self.screen_height, world=self.world_height)
        self.top = adjusted_y
        if self.top == old_top and self.left == old_left:
            return False
        return True

    def _adjust(self, center, screen, world):
        if screen == world:
            return 0
        if screen > world:
            # Don't think this is something to worry about as of right now
            raise NotImplementedError
        # Index of position at center of screen/max
        # distance away from center still on screen
        screen_center = int((screen - 1) / 2)
        assert screen_center == (screen - 1)
        # Camera has the same size as screen, but
        # has positions relative to the world
        camera_min = center - screen_center
        camera_max = center + screen_center
        # Account for camera scrolling outside of world boundaries
        if camera_min < 0:
            adjusted = 0
        elif camera_max > world:
            adjusted = world - screen_center
        else:
            adjusted = camera_min
        return adjusted

    def translate(self, pos, source="world"):
        if source == "world":
            return self._to_screen(pos)
        if source == "screen":
            return self._to_world(pos)
        raise ValueError

    def _to_screen(self, pos):
        pos_x, pos_y = pos
        # assert(isinstance(pos_x, int))
        # assert (isinstance(pos_y, int))
        translated_x = self._translate_position(pos=pos_x, offset=-self.left, _min=0, _max=self.screen_width)
        translated_y = self._translate_position(pos=pos_y, offset=-self.top, _min=0, _max=self.screen_height)
        assert (isinstance(translated_x, int))
        if not isinstance(translated_y, int):
            print(self.top)
            print(pos_y)
            print(translated_y)
            raise RuntimeError
        translated = translated_x, translated_y
        return translated

    def _to_world(self, pos):
        pos_x, pos_y = pos
        assert (isinstance(pos_x, int))
        assert (isinstance(pos_y, int))
        translated_x = self._translate_position(pos=pos_x, offset=self.left, _min=0, _max=self.world_width)
        translated_y = self._translate_position(pos=pos_y, offset=self.top, _min=0, _max=self.world_height)
        assert (isinstance(translated_x, int))
        if not isinstance(translated_y, int):
            print(self.top, "OFFSET")
            print(pos_y)
            print(translated_y)
            raise RuntimeError
        translated = translated_x, translated_y
        return translated

    @staticmethod
    def _translate_position(pos, offset, _min=None, _max=None):
        translated_pos = pos + offset
        if _min is not None:
            if translated_pos < _min:
                return
        if _max is not None:
            if translated_pos > _max:
                return
        return translated_pos



