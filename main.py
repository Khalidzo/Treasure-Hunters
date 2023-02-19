import pygame, sys
from settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
level = Level(screen, level_0)
cloud_spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(cloud_spawn_event, 3000)

if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == cloud_spawn_event:
                level.spawn_clouds()

        screen.fill('black')
        level.run()
        pygame.display.update()
        clock.tick(60)