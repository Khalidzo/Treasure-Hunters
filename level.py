import pygame
from settings import SCREEN_HEIGHT,SCREEN_WIDTH, TILE_SIZE
from tile import Tile, StaticTile, AnimatedTile, Coin, Palm
from player import Player
from particles import Particle
from utils import import_csv, import_sliced_graphics, import_images

class Level:
    def __init__(self, screen, level_data):
        # basic setup
        self.screen = screen
        self.x_map_shift = -2
        self.y_map_shift = -2

        # camera setup
        self.camera_top = 1/5 * SCREEN_HEIGHT
        self.camera_bottom = 2/3 * SCREEN_HEIGHT
        self.camera_right = 2/3 * SCREEN_WIDTH
        self.camera_left = 1/3 * SCREEN_WIDTH

        # dust particles
        self.dust_sprites = pygame.sprite.Group()
        self.player_on_ground = False
        
        # terrain sprites
        terrain_layout = import_csv(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # coin sprites
        coin_layout = import_csv(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coin')

        # background balms sprites
        bg_balm_layout = import_csv(level_data['bg_palms'])
        self.bg_balm_sprites = self.create_tile_group(bg_balm_layout, 'bg_balm')

        # grass sprites
        grass_layout = import_csv(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        
        # horizon sprites
        horizon_layout = import_csv(level_data['horizon'])
        self.horizon_sprites = self.create_tile_group(horizon_layout, 'horizon')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                if column != '-1':
                    x = column_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'terrain':
                        terrain_img_list = import_sliced_graphics(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Terrain\Terrain (64x64).png')
                        sprite_img = terrain_img_list[int(column)]
                        sprite = StaticTile((x,y), sprite_img)
                        sprite_group.add(sprite)
                    
                    elif type == 'coin':
                        if column == '0':
                            coin_animations = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Pirate Treasure\Sprites\coins\gold')
                        else:
                            coin_animations = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Pirate Treasure\Sprites\coins\silver')

                        sprite = Coin((x,y), coin_animations)
                        sprite_group.add(sprite)
                    
                    elif type == 'bg_balm':
                        if column == '1':
                            sprite_img = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Back Palm Trees\Back Palm Tree Left 01.v1.png').convert_alpha()
                            sprite = Palm((x,y), sprite_img, '1')
                        elif column == '2':
                            sprite_img = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Back Palm Trees\Back Palm Tree Right 03.v1 (1).png').convert_alpha()
                            sprite = Palm((x,y), sprite_img, '2')
                        elif column == '3':
                            sprite_img = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Back Palm Trees\Back Palm Tree Regular 01.v1.png').convert_alpha()
                            sprite = Palm((x,y), sprite_img, '3')

                        sprite_group.add(sprite)
                    
                    elif type == 'grass':
                        grass_img_list = import_sliced_graphics(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\grass\grass.png')
                        sprite_img = grass_img_list[int(column)]
                        sprite = StaticTile((x,y), sprite_img)
                        sprite_group.add(sprite)
                    
                    elif type == 'horizon':
                        horizon_img_list = import_sliced_graphics(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Background\BG Image.png')
                        sprite_img = horizon_img_list[int(column)]
                        sprite = StaticTile((x,y), sprite_img)
                        sprite_group.add(sprite)
                        print(column)

        return sprite_group
    
    def create_jump_particles(self):
        jump_particle_sprite = Particle(self.player.sprite.rect.midbottom, self.player.sprite.dust_animations['jump'], 'jump')
        self.dust_sprites.add(jump_particle_sprite)

    def create_landing_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprites.sprites():
            landing_particle_sprite = Particle(self.player.sprite.rect.midbottom, self.player.sprite.dust_animations['land'], 'land')
            self.dust_sprites.add(landing_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
                    
    def scroll_map_x(self):
        # player moving to the right of the map
        if self.player.sprite.rect.centerx >= self.camera_right and self.player.sprite.direction.x > 0:
            self.x_map_shift = -self.player.sprite.player_speed
            self.player.sprite.direction.x = 0
        # player moving to the left of the map
        elif self.player.sprite.rect.centerx <= self.camera_left and self.player.sprite.direction.x < 0:
            self.x_map_shift = self.player.sprite.player_speed
            self.player.sprite.direction.x = 0
        else:
            self.x_map_shift = 0
    
    def scroll_map_y(self):
        # player moving upwards
        if self.player.sprite.rect.centery <= self.camera_top and self.player.sprite.direction.y < 0:
            self.y_map_shift = self.player.sprite.player_speed
            self.camera_top -= self.player.sprite.player_speed
            self.camera_bottom -= self.player.sprite.player_speed
            
        # player moving downwards
        elif self.player.sprite.rect.centery >= self.camera_bottom and self.player.sprite.direction.y > 0.8 and self.player.sprite.state == 'fall':
            self.y_map_shift = -self.player.sprite.player_speed
            self.camera_top += self.player.sprite.player_speed
            self.camera_bottom += self.player.sprite.player_speed
        else:
            self.y_map_shift = 0

    def vertical_collisions(self):
        self.player.sprite.apply_gravity()

         # check collision
        for sprite in self.tile_sprites.sprites():
            if sprite.rect.colliderect(self.player.sprite.collision_rect):
                if self.player.sprite.direction.y > 0:
                    # player is on ground/falling
                    self.player.sprite.collision_rect.bottom = sprite.rect.top
                    self.player.sprite.direction.y = 0
                    self.player.sprite.on_ground = True
                    self.y_current_standing_level = sprite.rect.top
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
        #self.scroll_map_x()
        #self.scroll_map_y()
        # dust particles
        #self.dust_sprites.update(self.x_map_shift, self.y_map_shift)
        #self.dust_sprites.draw(self.screen)

        # render horizon
        self.horizon_sprites.update(self.x_map_shift, self.y_map_shift)
        self.horizon_sprites.draw(self.screen)

        # render grass

        self.grass_sprites.update(self.x_map_shift, self.y_map_shift)
        self.grass_sprites.draw(self.screen)

        # render background balms
        self.bg_balm_sprites.update(self.x_map_shift, self.y_map_shift)
        self.bg_balm_sprites.draw(self.screen)

         # render horizon
        self.horizon_sprites.draw(self.screen)

        # render terrain
        self.terrain_sprites.update(self.x_map_shift, self.y_map_shift)
        self.terrain_sprites.draw(self.screen)

       

        # render coins
        self.coin_sprites.update(self.x_map_shift, self.y_map_shift)
        self.coin_sprites.draw(self.screen)

        # collision detection
        #self.horizontal_collisions()
        #self.get_player_on_ground()
        #self.vertical_collisions()
        #self.create_landing_particles()

        # render player
        #self.player.update()
        #self.player.draw(self.screen)