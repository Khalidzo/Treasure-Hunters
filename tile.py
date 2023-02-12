import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = position)

    def update(self, x_map_shift, y_map_shift):
        self.rect.x += x_map_shift
        self.rect.y += y_map_shift

class StaticTile(Tile):
    def __init__(self, position, surface):
        super().__init__(position)
        self.image = surface
