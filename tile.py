import pygame
from random import randint, choice
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = position)

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
        
    def update(self):
        self.animate()

class Coin(AnimatedTile):
    def __init__(self, position, frames, value):
        super().__init__(position, frames)
        self.value = value
        self.rect = self.image.get_rect(center = (position[0] + TILE_SIZE/2, position[1] + TILE_SIZE/2))

class Palm(AnimatedTile):
    def __init__(self, position, type, frames):
        super().__init__(position, frames)
        if type == '3':
            self.rect = self.image.get_rect(center = (position[0] + 20, position[1] + randint(0,50)))
        elif type == '2':
            self.rect = self.image.get_rect(center = (position[0] + 30, position[1] - 15))
        elif type == '1':
            self.rect = self.image.get_rect(center = (position[0] + 20, position[1] - 10))

class WaterReflection(AnimatedTile):
    def __init__(self, position, frames):
        super().__init__(position, frames)
        self.rect = self.image.get_rect(center = (position[0], position[1] + 32))

class Sky(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
    
    """ def update(self, y_map_shift):
        self.rect.y += y_map_shift """

class Flag(AnimatedTile):
    def __init__(self, position, frames):
        super().__init__(position, frames)
        self.rect = self.image.get_rect(center = (position[0] + TILE_SIZE/2, position[1] - 28))

class Crate(StaticTile):
    def __init__(self, position, surface):
        super().__init__(position, surface)
        self.rect = self.image.get_rect(bottomleft = (position[0], position[1] + TILE_SIZE))

class fg_palm(AnimatedTile):
    def __init__(self, position, frames, type):
        super().__init__(position, frames)
        if type == '0':
            self.rect = self.image.get_rect(center = (position[0] + 20, position[1]))
        elif type == '1':
            self.rect = self.image.get_rect(center = (position[0] + 10, position[1] + 14))

class Cloud(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(bottomleft = position)
        self.speed_index = 0
        self.speed = choice([0.5, 1])

    def update(self):
        self.speed_index += self.speed
        if self.speed_index > 1:
            self.speed_index = 0
        self.rect.x -= int(self.speed_index)
        if self.rect.x < -HORIZONTAL_TILES * TILE_SIZE:
            self.kill()

class bg_water(StaticTile):
    def __init__(self, position, surface):
        super().__init__(position, surface)
        self.rect = self.image.get_rect(topleft = (position[0], position[1] + 20))
        