import pygame
from settings import SCREEN_HEIGHT,SCREEN_WIDTH, TILE_SIZE, HORIZONTAL_TILES, VERTICAL_TILES
from tile import Tile, StaticTile, AnimatedTile, Coin, Palm, WaterReflection, Sky, Flag, Crate, fg_palm, Cloud, bg_water
from player import Player
from particles import Particle
from utils import import_csv, import_sliced_graphics, import_images
from random import randint, choice

class Level:
    def __init__(self, screen, level_data):
        # basic setup
        self.screen = screen
        self.current_time = pygame.time.get_ticks()
        self.x_map_shift = 0
        self.y_map_shift = 0

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

        # background balm sprites
        bg_balm_layout = import_csv(level_data['bg_palms'])
        self.bg_balm_sprites = self.create_tile_group(bg_balm_layout, 'bg_balm')

        # background balm sprites
        fg_balm_layout = import_csv(level_data['fg_balms'])
        self.fg_balm_sprites = self.create_tile_group(fg_balm_layout, 'fg_balm')

        # grass sprites
        grass_layout = import_csv(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        
        # background water sprites
        bg_water_layout = import_csv(level_data['bg_water'])
        self.bg_water_sprites = self.create_tile_group(bg_water_layout, 'bg_water')
        
        # water reflection
        water_reflect_layout = import_csv(level_data['water_reflect'])
        self.water_reflect_sprites = self.create_tile_group(water_reflect_layout, 'water_reflect')

        # flag sprite
        flag_layout = import_csv(level_data['flag'])
        self.flag_sprite = self.create_tile_group(flag_layout, 'flag')

        # crate sprites
        crate_layout = import_csv(level_data['crate'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crate')

        # sky
        sky_layout = import_csv(level_data['sky'])
        self.sky_sprites = self.create_tile_group(sky_layout, 'sky')
        
        # clouds
        self.cloud_sprites = pygame.sprite.Group()
        self.cloud_imgs = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\clouds')
        self.spawn_cloud()

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
                            balm_animations = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Back Palm Trees\Back Palm Tree Left')
                            sprite = Palm((x,y), '1', balm_animations)
                        elif column == '2':
                            balm_animations = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Back Palm Trees\Back Palm Tree Right')
                            sprite = Palm((x,y), '2', balm_animations)
                        elif column == '3':
                            balm_animations = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Back Palm Trees\Back Palm Tree Regular')
                            sprite = Palm((x,y), '3', balm_animations)

                        sprite_group.add(sprite)
                    
                    elif type == 'grass':
                        grass_img_list = import_sliced_graphics(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\grass\grass.png')
                        sprite_img = grass_img_list[int(column)]
                        sprite = StaticTile((x,y), sprite_img)
                        sprite_group.add(sprite)
                    
                    elif type == 'bg_water':
                        sprite_img = pygame.image.load('D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Background\Additional Water.v1.png').convert()
                        sprite = bg_water((x,y), sprite_img)
                        sprite_group.add(sprite)
                    
                    elif type == 'water_reflect':
                        water_reflect_animations = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Background\Water reflect')
                        sprite = WaterReflection((x,y), water_reflect_animations)
                        sprite_group.add(sprite)

                    elif type == 'sky':
                        sky_img_list = import_sliced_graphics(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Background\BG Image.v1 (2).png')
                        sprite_img = sky_img_list[int(column)]
                        sprite_img = pygame.transform.scale(sprite_img, (HORIZONTAL_TILES * TILE_SIZE, TILE_SIZE))
                        sprite = Sky((x,y), sprite_img)
                        sprite_group.add(sprite)

                    elif type == 'flag':
                        flag_animations = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Objects\Flag\Flag')
                        sprite = Flag((x,y), flag_animations)
                        sprite_group.add(sprite)
                    
                    elif type == 'crate':
                        crate_img = pygame.image.load(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Objects\crate.png').convert()
                        sprite = Crate((x,y), crate_img)
                        sprite_group.add(sprite)

                    elif type == 'fg_balm':
                        if column == '0':
                            balm_animations = import_images('D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\palm_large')
                            sprite = fg_palm((x,y), balm_animations, '0')
                        elif column == '1':
                            balm_animations = import_images('D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\palm_small')
                            sprite = fg_palm((x,y), balm_animations, '1')
                        sprite_group.add(sprite)

        return sprite_group
    
    def create_jump_particles(self):
        jump_particle_sprite = Particle(self.player.sprite.rect.midbottom, self.player.sprite.dust_animations['jump'], 'jump')
        self.dust_sprites.add(jump_particle_sprite)

    def create_landing_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprites.sprites():
            landing_particle_sprite = Particle(self.player.sprite.rect.midbottom, self.player.sprite.dust_animations['land'], 'land')
            self.dust_sprites.add(landing_particle_sprite)

    def spawn_clouds(self):
        for cloud in range(5):
            img = choice(self.cloud_imgs)
            cloud = Cloud((randint(HORIZONTAL_TILES * TILE_SIZE, 2 * HORIZONTAL_TILES * TILE_SIZE), randint(0, VERTICAL_TILES * TILE_SIZE)), img)
            self.cloud_sprites.add(cloud)

    def spawn_cloud(self):
        img = pygame.image.load('D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\Background\Big Clouds.png').convert_alpha()
        img = pygame.transform.scale2x(img)
        cloud = Cloud((500, (VERTICAL_TILES - 4) * TILE_SIZE), img)
        self.cloud_sprites.add(cloud)

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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x_map_shift = -8
        elif keys[pygame.K_a]:
            self.x_map_shift = 8
        elif keys[pygame.K_s]:
            self.y_map_shift = -4
        elif keys[pygame.K_w]:
            self.y_map_shift = 4
        else:
            self.x_map_shift = 0
            self.y_map_shift = 0

        # render sky
        self.sky_sprites.update(self.y_map_shift)
        self.sky_sprites.draw(self.screen)

        # render clouds
        self.cloud_sprites.update(self.x_map_shift, self.y_map_shift)
        self.cloud_sprites.draw(self.screen)

        # render bg water + horizon
        self.bg_water_sprites.update(self.x_map_shift, self.y_map_shift)
        self.bg_water_sprites.draw(self.screen)

        # render grass
        self.grass_sprites.update(self.x_map_shift, self.y_map_shift)
        self.grass_sprites.draw(self.screen)

        # render flag
        self.flag_sprite.update(self.x_map_shift, self.y_map_shift)
        self.flag_sprite.draw(self.screen)
        
        # render water reflection
        self.water_reflect_sprites.update(self.x_map_shift, self.y_map_shift)
        self.water_reflect_sprites.draw(self.screen)

        # render background balms
        self.bg_balm_sprites.update(self.x_map_shift, self.y_map_shift)
        self.bg_balm_sprites.draw(self.screen)

        # render crates 
        self.crate_sprites.update(self.x_map_shift, self.y_map_shift)
        self.crate_sprites.draw(self.screen)

        # render fg balms
        self.fg_balm_sprites.update(self.x_map_shift, self.y_map_shift)
        self.fg_balm_sprites.draw(self.screen)
        
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