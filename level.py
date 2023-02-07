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
                    player = Player((x,y), self.screen)
                    self.player.add(player)
                    
    def scroll_map(self):
        # player moving to the right of the map
        if self.player.sprite.rect.centerx >= (2/3 * SCREEN_WIDTH) and self.player.sprite.direction.x > 0:
            self.map_shift = -self.player.sprite.player_speed
            self.player.sprite.direction.x = 0
        # player moving to the left of the map
        elif self.player.sprite.rect.centerx <= (1/3 * SCREEN_WIDTH) and self.player.sprite.direction.x < 0:
            self.map_shift = self.player.sprite.player_speed
            self.player.sprite.direction.x = 0
        else:
            self.map_shift = 0
    
    def vertical_collisions(self):
        self.player.sprite.apply_gravity()

         # check collision
        for sprite in self.tile_sprites.sprites():
            if sprite.rect.colliderect(self.player.sprite.collision_rect):
                if self.player.sprite.direction.y > 0:
                    # player is falling
                    self.player.sprite.collision_rect.bottom = sprite.rect.top
                    self.player.sprite.direction.y = 0
                    self.player.sprite.on_ground = True
                elif self.player.sprite.direction.y < 0:
                    # player is hitting object while jumping
                    self.player.sprite.collision_rect.top = sprite.rect.bottom
                    self.player.sprite.direction.y = 0

        if self.player.sprite.on_ground and self.player.sprite.direction.y < 0 or self.player.sprite.direction.y > 1:
            self.player.sprite.on_ground = False
                    
    
    def horizontal_collisions(self):
        self.player.sprite.collision_rect.x += self.player.sprite.direction.x * self.player.sprite.player_speed

        # check collision
        for sprite in self.tile_sprites.sprites():
            if sprite.rect.colliderect(self.player.sprite.collision_rect):
                if self.player.sprite.direction.x < 0:
                    # player moving to the right
                    self.player.sprite.collision_rect.left = sprite.rect.right
                    
                elif self.player.sprite.direction.x > 0:
                    # player moving to the left
                    self.player.sprite.collision_rect.right = sprite.rect.left                                      
    
    def run(self):
        # map
        self.scroll_map()

        # render tiles
        self.tile_sprites.update(self.map_shift)
        self.tile_sprites.draw(self.screen)

        # collision detection
        self.vertical_collisions()
        self.horizontal_collisions()

        # render player
        self.player.update()
        self.player.draw(self.screen)

