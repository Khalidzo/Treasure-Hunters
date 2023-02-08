import pygame

class Particle(pygame.sprite.Sprite):
    def __init__(self, position, frames, state):
        super().__init__()

        # animation
        self.frame_index = 0
        self.animate_speed = 0.5

        # image and shape
        self.frames = frames
        self.state = state
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = (position[0], position[1] - 5))
    
    def animate(self):
        self.frame_index += self.animate_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, map_shift):
        self.animate()
        self.rect.x += map_shift
