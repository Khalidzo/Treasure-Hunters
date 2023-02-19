import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from tile import Cloud
from random import randint, choice
from utils import import_images

class Menu:
    def __init__(self, screen):
        # basic setup
        self.screen = screen
        self.play = False

        # background
        self.sky_top = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\sky\sky_top.png').convert()
        self.sky_middle = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\sky\sky_middle.png').convert()
        self.sky_bottom = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\sky\sky_bottom.png').convert()
        self.horizon = 7
        
        # board
        self.board = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Wood and Paper UI\Sprites\Prefabs\3.png').convert_alpha()
        self.board = pygame.transform.scale(self.board, (500,500))

        # icon
        self.icon = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Wood and Paper UI\Sprites\Prefabs\8.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (400,250))

        # button
        self.button = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Wood and Paper UI\Sprites\Green Button\1.png').convert()
        self.button = pygame.transform.scale(self.button, (150,150))
        self.button_rect = pygame.Rect(((SCREEN_HEIGHT - 150)/2 + 250, (SCREEN_HEIGHT - 150)/2 + 100), (150,150))
        self.pressed = False

        # font
        self.font = pygame.font.Font(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Wood and Paper UI\Sprites\ARCADEPI.ttf', 30)
        self.text_1 = self.font.render('main menu', True, 'black')
        self.text_2 = self.font.render('play', True, 'black')

        # clouds
        self.cloud_sprites = pygame.sprite.Group()
        self.cloud_imgs = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\clouds')

    def display_board(self):
        board_x = (SCREEN_WIDTH - 500)/2
        board_y = (SCREEN_HEIGHT - 500)/2

        self.screen.blit(self.board, (board_x, board_y))
        self.screen.blit(self.icon, (board_x + ((500-400)/2), board_y + ((500-400)/2)))

        self.screen.blit(self.text_1, (board_x + ((500-400)/2) + 110, board_y + ((500-400)/2) + 80))
    
    def spawn_cloud(self):
        if len(self.cloud_sprites.sprites()) < 10:
            cloud = Cloud((randint(SCREEN_WIDTH, SCREEN_WIDTH * 2), randint(100, SCREEN_HEIGHT - 200)), choice(self.cloud_imgs))
            self.cloud_sprites.add(cloud)

    def cloud_update(self):
        for cloud in self.cloud_sprites.sprites():
            if cloud.rect.bottomright[0] < 0:
                cloud.kill()

    def display_button(self):
        self.screen.blit(self.button, ((SCREEN_HEIGHT - 150)/2 + 250, (SCREEN_HEIGHT - 150)/2 + 100))
        self.screen.blit(self.text_2, ((SCREEN_HEIGHT - 150)/2 + 290, (SCREEN_HEIGHT - 150)/2 + 150))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.button = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Wood and Paper UI\Sprites\Green Button\1 pressed.png').convert()
                self.button = pygame.transform.scale(self.button, (150,150))
                self.pressed = True
                
            else:
                if self.pressed:
                    self.button = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Wood and Paper UI\Sprites\Green Button\1.png').convert()
                    self.button = pygame.transform.scale(self.button, (150,150))
                    self.play = True
                

    def display_background(self):
        for i in range(0, SCREEN_HEIGHT // TILE_SIZE + 1):
            for j in range(0, SCREEN_WIDTH // TILE_SIZE + 1):
                x = j * TILE_SIZE
                y = i * TILE_SIZE
                if i < self.horizon:
                    self.screen.blit(self.sky_top, (x,y))
                elif i == self.horizon:
                    self.screen.blit(self.sky_middle, (x,y))
                elif i > self.horizon:
                    self.screen.blit(self.sky_bottom, (x,y))
    
    def run(self):
        self.display_background()
        self.cloud_sprites.update()
        self.cloud_sprites.draw(self.screen)
        self.spawn_cloud()
        self.cloud_update()
        self.display_board()
        self.display_button()
        self.check_click()