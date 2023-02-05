import pygame
from settings import *

class Level:
    def __init__(self, screen, level_map):
        self.screen = screen
        self.level_map = level_map
        self.tile_sprites = pygame.sprite.Group()
    
    def render_level(self):
        for row_index, row in enumerate(self.level_map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    tile.fill('grey')
                    tile_rect = tile.get_rect(topleft = (x,y))
                    self.screen.blit(tile, tile_rect)

    def run(self):
        self.render_level()
                
