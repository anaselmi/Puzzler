

class Camera:
    def __init__(self, screen_size, world_size):
        self.screen_size = screen_size
        self.screen_width, self.screen_height = self.screen_size
        self.world_size = world_size
        self.world_width, self.world_height = self.world_size

    def set_top_left_from_center(self, center):
        center_x, center_y = center

        screen_min_x = int(center_x - self.screen_width / 2)
        screen_max_x = int(center_x + self.screen_width / 2)
        screen_center_x = int(self.screen_width / 2)
        world_center_x = int(self.world_width / 2)
        if screen_min_x < 0 and screen_max_x > self.world_width:
            # Go to center of screen and half a world back
            center_x = screen_center_x - world_center_x
        elif screen_min_x < 0:
            center_x = screen_center_x
        elif screen_max_x > self.world_width:
            center_x = self.world_width - screen_center_x
        else:
            center_x = center_x

        self.left = center_x - screen_center_x

        screen_min_y = int(center_y - self.screen_height / 2)
        screen_max_y = int(center_y + self.screen_height / 2)
        screen_center_y = int(self.screen_height / 2)
        world_center_y = int(self.world_height / 2)
        if screen_min_y < 0 and screen_max_y > self.world_height:
            # Go to center of screen and half a world back
            center_y = screen_center_y - world_center_y
        elif screen_min_y < 0:
            center_y = screen_center_y
        elif screen_max_y > self.world_height:
            center_y = self.world_height - screen_center_y
        else:
            center_y = center_y

        self.top = center_y - screen_center_y

        self.top_left = (self.left, self.top)

    def adjust_to_screen(self, pos):
        pos_x, pos_y = pos
        translated_x = pos_x - self.left
        translated_y = pos_y - self.top

        if self.screen_width >= translated_x >= 0:
            pass
        else:
            return None

        if self.screen_height >= translated_y >= 0:
            pass
        else:
            return None

        return translated_x, translated_y


