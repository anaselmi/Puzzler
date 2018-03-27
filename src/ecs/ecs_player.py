from ecs_meta import Entity
import ecs_components as components
from src.consts import *


class PlayerEntity(Entity):
    def __init__(self, *args):
        super().__init__(self, *args)
        self.id = "EN_Player"
        self.register_components()

PlayerRender = components.RenderComponent(x=0, y=0, char="@", fg=RED, bg=BLACK, active=True)

# TODO: Give the player a move component
Player = PlayerEntity(PlayerRender)

