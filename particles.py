import pygame
from scraper import import_images
class Particle(pygame.sprite.Sprite):
    def __init__(self, player_state):
        super().__init__()
        self.import_animations()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = self.animations[player_state]
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frame_index):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def import_dust_animations(self):
        self.dust_animations = {'jump':[], 'land':[], 'run':[]}
        for animation in self.animations.keys():
            full_path = 'D:\\My Programs\\Treasure Hunter\\Treasure Hunters\\Captain Clown Nose\\Sprites\\Captain Clown Nose\\Captain Clown Nose with Sword\\dust_particles' + '\\' + animation
            self.animations[animation] = import_images(full_path)

    def update(self):
        self.animate()  
