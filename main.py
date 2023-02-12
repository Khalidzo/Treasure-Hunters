import pygame, sys
from settings import *
from level import Level
from utils import import_csv

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
level = Level(screen, level_0)


if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')
        level.run()
        pygame.display.update()
        clock.tick(60)