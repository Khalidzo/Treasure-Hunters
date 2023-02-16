import pygame
from settings import TILE_SIZE
from random import randint

class Crabby(pygame.sprite.Sprite):
    def __init__(self, pos, animations):
        super().__init__()
        self.animation_index = 0
        self.animation_speed = 0.15
        self.animations = animations
        self.image = self.animations[self.animation_index]
        self.rect = self.image.get_rect(topleft = (pos[0], pos[1]))
        self.rect.y += TILE_SIZE - self.image.get_height()
        self.speed = randint(2,4)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def reverse_direction(self):
        self.speed *= -1

    def animate(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animations):
            self.animation_index = 0
        else:
            self.image = self.animations[int(self.animation_index)]

        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

    def update(self, x_map_shift, y_map_shift):
        self.animate()
        self.move()
        self.reverse_image()
        self.rect.x += x_map_shift
        self.rect.y += y_map_shift