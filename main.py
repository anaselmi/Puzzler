import sys
import pygame
from pygame.locals import *
from consts import *
from event_handler import *
# Initializing everything
pygame.init()
pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Puzzler: The Puzzle")
FINALSURFACE = pygame.Surface((0,0))
EventHandler = EventHandler()

# Main game loop
while True:

    for event in pygame.event.get():
        EventHandler.parse_event(event)

    pygame.display.update()
