import pygame
from scraper import import_images

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # basic setup

        # player animation
        self.state = 'idle'
        self.frames = import_images('D:\My Programs\Treasure Hunter\Treasure Hunters\Captain Clown Nose\Sprites\Captain Clown Nose\Captain Clown Nose with Sword\Idle')
        self.frame_index = 0
        self.animate_speed = 0.15
        self.image = self.frames[self.frame_index]

        # player position and movement
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.math.Vector2(0,0)
        self.gravity = 0.8
        self.player_speed = 5

        # player orientation
        self.facing_right = True
        self.on_ground = True

        

    def input(self):
        keys = pygame.key.get_pressed()

        # check keyboard input
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_SPACE]:
            self.jump()
        else:
            self.direction.x = 0
        
    def jump(self):
        if self.on_ground:
            self.direction.y = -15
            self.on_ground = False
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def animate(self):
        self.frame_index += self.animate_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        self.input()