import pygame, sys
from settings import *
from level import Level
from ui import Menu

pygame.init()
class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.level = Level(self.screen, level_0)
        self.menu = Menu(self.screen, self.level.play_music)
        self.cloud_spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.cloud_spawn_event, 3000)
    
    def run(self):
        if not self.menu.play:
            self.menu.run()
        else:
            for event in pygame.event.get():
                if event.type == self.cloud_spawn_event:
                    self.level.spawn_clouds()
            self.level.playing = True
            self.level.run()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

game = Game()

if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill('black')
        game.run()
        pygame.display.update()
        clock.tick(60)  

