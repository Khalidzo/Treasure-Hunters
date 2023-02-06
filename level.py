import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self, screen, level_map):
        self.screen = screen
        self.level_map = level_map
        self.map_shift = 0
        self.render_level()
    
    def render_level(self):
        self.tile_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(self.level_map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    tile = Tile((x,y))
                    self.tile_sprites.add(tile)

                elif col == 'P':
                    player = Player((x,y))
                    self.player.add(player)
                    

    def run(self):
        # render tiles
        self.tile_sprites.update(self.map_shift)
        self.tile_sprites.draw(self.screen)

        # render player
        self.player.update()
        self.player.draw(self.screen)
                
