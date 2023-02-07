import pygame
from scraper import import_images

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # basic setup

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
        self.player_speed = 5

        # player orientation
        self.facing_right = True
        self.on_ground = True      

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
        elif keys[pygame.K_SPACE]:
            self.jump()
        else:
            self.direction.x = 0
        
    def jump(self):
        if self.on_ground:
            self.direction.y = -15
            #self.state = 'jump'
            self.on_ground = False
        
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

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
        else:
            self.image = self.image
        
        # check movement
        if self.direction.x != 0:
            print(self.direction.x)
            self.state = 'run'
        elif self.direction.x == 0 and self.on_ground:
            self.state = 'idle'
            
    def update(self):
        self.animate()
        self.input()