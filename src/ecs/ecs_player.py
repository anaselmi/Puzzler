from ecs_classes import Entity
import components


class PlayerEntity(Entity):
    def __init__(self, *args):
        super().__init__(self, *args)
        self.id = "EN_Player"

# TODO: Give the player a move component
Player = PlayerEntity(components.PlayerRender)

