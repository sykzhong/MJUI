import pygame
import random
import os

black = (0, 0, 0)
white = (255, 255, 255)

DISPLAY_WIDTH  = 1024
DISPLAY_HEIGHT = 1024
TILE_WIDTH     = -1     #dynamic
TILE_HEIGHT    = -1     #dynamic

class graphic_system(object):
    def __init__(self):
        global DISPLAY_WIDTH, DISPLAY_HEIGHT
        pygame.init()
        self.screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])
        self.all_sprites = pygame.sprite.OrderedUpdates()       #update by addition sequence
        self.all_text = []

    def clear_all_sprites(self):
        self.all_sprites.empty()

    def add_sprite(self, sprite):
        self.all_sprites.add(sprite)