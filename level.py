import pygame
from settings import *
from tile import Tile

class Level:
    def __init__(self, screen, level_map):
        self.screen = screen
        self.level_map = level_map
        self.map_shift = -1
        self.render_level()
    
    def render_level(self):
        self.tile_sprites = pygame.sprite.Group()

        for row_index, row in enumerate(self.level_map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    tile = Tile((x,y))
                    self.tile_sprites.add(tile)
                    

    def run(self):
        self.tile_sprites.update(self.map_shift)
        self.tile_sprites.draw(self.screen)
                
