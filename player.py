import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # basic setup
        self.image = pygame.image.load('D:\\My Programs\\Treasure Hunter\\Treasure Hunters\\Captain Clown Nose\\Sprites\\Captain Clown Nose\\Captain Clown Nose with Sword\\09-Idle Sword\\1.png')
        self.image = pygame.transform.scale(self.image, (132, 80))

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
        self.direction.y = -12
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def animate(self):
        pass

    def update(self):
        self.animate()
        self.input()