import pygame
import sys
from consts import *
from pygame.locals import *


def exit_game():
    pygame.quit()
    sys.exit()


class EventHandler:
    def __init__(self, button_map=BUTTON_MAP):
        self.button_map = button_map
        print(self.button_map)

    def parse_event(self, event):
        if event.type == KEYDOWN and event.type in self.button_map:
            if self.button_map[event.type] == "QUIT":
                exit_game()

        if event.type == pygame.QUIT:
            exit_game()