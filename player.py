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
        self.gravity = 20
        self.player_speed = 5

        # player orientation
        self.facing_right = True


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        

    def animate(self):
        pass

    def update(self):
        self.rect.x += self.direction.x * self.player_speed
        self.animate()
        self.input()