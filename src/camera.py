

class Camera:
    def __init__(self, level_dimensions, ui_dimensions):
        self.level_width, self.level_height = level_dimensions
        self.ui_width, self.ui_height = ui_dimensions

    # Adjusts top left coordinates based on center pos
    def set_top_left(self, center_pos):
        center_x, center_y = center_pos

        ui_min_x = int(center_x - self.ui_width / 2)
        ui_max_x = int(center_x + self.ui_width / 2)
        ui_center_x = int(self.ui_width / 2)
        level_center_x = int(self.level_width / 2)
        if ui_min_x < 0 and ui_max_x > self.level_width:
            # Go to center of UI and half a level back
            center_x = ui_center_x - level_center_x
        elif ui_min_x < 0:
            center_x = ui_center_x
        elif ui_max_x > self.level_width:
            center_x = self.level_width - ui_center_x
        else:
            center_x = center_x

        self.left = center_x - ui_center_x

        ui_min_y = int(center_y - self.ui_height / 2)
        ui_max_y = int(center_y + self.ui_height / 2)
        ui_center_y = int(self.ui_height / 2)
        level_center_y = int(self.level_height / 2)
        if ui_min_y < 0 and ui_max_y > self.level_height:
            # Go to center of UI and half a level back
            center_y = ui_center_y - level_center_y
        elif ui_min_y < 0:
            center_y = ui_center_y
        elif ui_max_y > self.level_height:
            center_y = self.level_height - ui_center_y
        else:
            center_y = center_y

        self.top = center_y - ui_center_y

        self.top_left = (self.left, self.top)

    def to_ui(self, pos):
        pos_x, pos_y = pos
        offset_x = pos_x - self.left
        offset_y = pos_y - self.top

        if self.ui_width >= offset_x >= 0:
            pass
        else:
            return None

        if self.ui_height >= offset_y >= 0:
            pass
        else:
            return None

        return offset_x, offset_y


