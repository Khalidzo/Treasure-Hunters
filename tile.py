import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('grey')
        self.rect = self.image.get_rect(center = position)

    def update(self, map_shift):
        self.rect.x += map_shift

