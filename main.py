import pygame, sys, os
from settings import *
from level import Level
from ui import Menu

pygame.init()
class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.level = Level(self.screen, level_0)
        self.menu = Menu(self.screen, self.level.play_music)
    
    def run(self):
        if not self.menu.play:
            self.menu.run()
        else:   
            self.level.playing = True
            self.level.run()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
cloud_spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(cloud_spawn_event, 3000)
game = Game()

if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == cloud_spawn_event:
                    game.level.spawn_clouds()
                
        screen.fill('black')
        game.run()
        pygame.display.update()
        clock.tick(60)  

