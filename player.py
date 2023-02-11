import pygame
from utils import import_images
from particles import Particle

class Player(pygame.sprite.Sprite):
    def __init__(self, position, screen, create_jump_particles):
        super().__init__()
        # basic setup
        self.screen = screen

        # player animation
        self.import_animations()
        self.frame_index = 0
        self.animate_speed = 0.2
        self.image = self.animations['idle'][self.frame_index]
        self.state = 'idle'

        # player position and movement
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.math.Vector2(0,0)
        self.gravity = 0.8
        self.player_speed = 6
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height))

        # player orientation
        self.facing_right = True
        self.on_ground = True      

        # dust particles
        self.create_jump_particles = create_jump_particles
        self.import_dust_animations()
        self.dust_frame_index = 0
        self.dust_animate_speed = self.animate_speed

    def import_dust_animations(self):
        self.dust_animations = {'jump':[], 'land':[], 'run':[]}
        for animation in self.dust_animations.keys():
            print('hi' + animation)
            full_path = 'D:\\My Programs\\Treasure Hunter\\Treasure Hunters\\Captain Clown Nose\\Sprites\\Captain Clown Nose\\Captain Clown Nose with Sword\\dust_particles' + '\\' + animation
            self.dust_animations[animation] = import_images(full_path)
            

    def import_animations(self):
        self.animations = {'idle':[], 'jump':[], 'run':[], 'fall':[]}
        img_path = 'D:\My Programs\Treasure Hunter\Treasure Hunters\Captain Clown Nose\Sprites\Captain Clown Nose\Captain Clown Nose with Sword'

        for animation in self.animations.keys():
            full_path = img_path + '\\' + animation
            self.animations[animation] = import_images(full_path)
    
    def input(self):
        keys = pygame.key.get_pressed()

        # check keyboard input
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles()
        else:
            self.direction.x = 0
        
    def jump(self):
        self.direction.y = -15
        self.on_ground = False 

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def animate(self):
        animation = self.animations[self.state]

        # animate frames
        self.frame_index += self.animate_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

        # fix orientation
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.bottomright = self.collision_rect.bottomright
        else:
            self.image = self.image
            self.rect.bottomleft = self.collision_rect.bottomleft
        
        # set bottom of the rect with the bottom of img
        if self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

    def dust_particles_animate(self):
        if self.state == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animate_speed
            if self.dust_frame_index >= len(self.dust_animations):
                self.dust_frame_index = 0
            dust_particle = self.dust_animations['run'][int(self.dust_frame_index)]

            if self.facing_right:
                self.screen.blit(dust_particle, (self.rect.bottomleft[0] - 15, self.rect.bottomleft[1] - 10))
            else:
                dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.screen.blit(dust_particle, (self.rect.bottomright[0] + 5, self.rect.bottomright[1] - 10))

    def update_status(self):
        if self.direction.y < 0:
            self.state = 'jump'
        elif self.direction.y > self.gravity:
            self.state = 'fall'
        elif self.direction.x != 0 and self.on_ground:
            self.state = 'run'
        else:
            self.state = 'idle'

    def update(self):
        self.dust_particles_animate()
        self.update_status()
        self.animate()
        self.input()
