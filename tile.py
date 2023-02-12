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

class AnimatedTile(Tile):
    def __init__(self, position, frames):
        super().__init__(position)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = frames
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.image = self.frames[int(self.frame_index)]
        
    def update(self, x_map_shift, y_map_shift):
        self.animate()
        self.rect.x += x_map_shift
        self.rect.y += y_map_shift
