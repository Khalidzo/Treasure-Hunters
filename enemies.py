import pygame
from settings import TILE_SIZE
from random import randint

class Crabby(pygame.sprite.Sprite):
    def __init__(self, pos, animations, death_animations):
        super().__init__()
        self.animation_index = 0
        self.death_animation_index = 0
        self.animation_speed = 0.15
        self.death_animations = death_animations
        self.animations = animations
        self.image = self.animations[self.animation_index]
        self.rect = self.image.get_rect(topleft = (pos[0], pos[1]))
        self.rect.y += TILE_SIZE - self.image.get_height()
        self.speed = randint(2,4)
        self.dead = False

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
    
    def death(self):
        self.speed = 0
        if self.death_animation_index > len(self.death_animations):
            self.kill()
        else:
            self.image = self.death_animations[int(self.death_animation_index)]
            self.death_animation_index += self.animation_speed

    def update(self):
        self.animate()
        self.move()
        self.reverse_image()
        if self.dead == True:
            self.death()
