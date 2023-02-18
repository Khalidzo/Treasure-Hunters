import pygame
from settings import SCREEN_HEIGHT,SCREEN_WIDTH, TILE_SIZE, HORIZONTAL_TILES, VERTICAL_TILES, CAMERA_BORDERS
from tile import Tile, StaticTile, AnimatedTile, Coin, Palm, WaterReflection, Sky, Flag, Crate, fg_palm, Cloud, bg_water
from player import Player
from enemies import Crabby
from particles import Particle
from utils import import_csv, import_sliced_graphics, import_images
from random import randint, choice

class Level:
    def __init__(self, screen, level_data):
        # basic setup
        self.screen = screen
        self.current_time = pygame.time.get_ticks()

        # dust particles
        self.dust_sprites = CameraGroup()
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

        # fg balm sprites
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
        self.cloud_sprites = CameraGroup()
        self.cloud_imgs = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\Palm Tree Island\Sprites\clouds')

        # enemies
        self.crabby_animations = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\The Crusty Crew\Sprites\Crabby\Run (scaled)')
        self.crabby_death_animations = import_images(r'D:\My Programs\Treasure Hunter\Treasure Hunters\The Crusty Crew\Sprites\Crabby\09-Dead Hit\Dead Scaled')
        self.enemy_layout = import_csv(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(self.enemy_layout, 'enemy')

        # borders
        self.border_layout = import_csv(level_data['borders'])
        self.border_sprites = self.create_tile_group(self.border_layout, 'border')

        # player
        player_layout = import_csv(level_data['player'])
        self.player_sprite = CameraGroup()
        self.spawn_player(player_layout)

    def create_tile_group(self, layout, type):
        sprite_group = CameraGroup()

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
                    
                    elif type == 'enemy':
                        sprite = Crabby((x,y), self.crabby_animations, self.crabby_death_animations)
                        sprite_group.add(sprite)

                    elif type == 'border':
                        sprite = Tile((x,y))
                        sprite_group.add(sprite)

        return sprite_group
    
    def create_jump_particles(self):
        jump_particle_sprite = Particle(self.player.rect.midbottom, self.player.dust_animations['jump'], 'jump')
        self.dust_sprites.add(jump_particle_sprite)

    def create_landing_particles(self):
        if not self.player_on_ground and self.player.on_ground and not self.dust_sprites.sprites():
            landing_particle_sprite = Particle(self.player.rect.midbottom, self.player.dust_animations['land'], 'land')
            self.dust_sprites.add(landing_particle_sprite)

    def spawn_player(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                if column != '-1':
                    x = column_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    self.player = Player((x,y), self.screen, self.create_jump_particles)
                    self.player_sprite.add(self.player)

    def enemy_border_collision(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.border_sprites, False):
                enemy.reverse_direction()

    def enemy_player_collision(self):
        for enemy in self.enemy_sprites.sprites():
            if enemy.rect.colliderect(self.player.collision_rect) and self.player.direction.y > self.player.gravity:
                self.player.direction.y = self.player.jump_power
                enemy.dead = True

    def spawn_clouds(self):
        img = choice(self.cloud_imgs)
        cloud = Cloud((randint(HORIZONTAL_TILES * TILE_SIZE, 2 * HORIZONTAL_TILES * TILE_SIZE), randint(0, (VERTICAL_TILES - 8) * TILE_SIZE)), img)
        self.cloud_sprites.add(cloud)

    def get_player_on_ground(self):
        if self.player.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
        
    def vertical_collisions(self):
        self.player.apply_gravity()

         # check collision
        for sprite in self.terrain_sprites.sprites() + self.crate_sprites.sprites():
            if sprite.rect.colliderect(self.player.collision_rect):
                if self.player.direction.y > 0:
                    # player is on ground
                    self.player.collision_rect.bottom = sprite.rect.top
                    self.player.direction.y = 0
                    self.player.on_ground = True
                elif self.player.direction.y < 0:
                    # player is hitting object while jumping
                    self.player.collision_rect.top = sprite.rect.bottom
                    self.player.direction.y = 0


        if self.player.on_ground and self.player.direction.y < 0 or self.player.direction.y > 1:
            self.player.on_ground = False
                   
    def horizontal_collisions(self):
        self.player.collision_rect.x += self.player.direction.x * self.player.player_speed

        # check collision
        for sprite in self.terrain_sprites.sprites() + self.crate_sprites.sprites():
            if sprite.rect.colliderect(self.player.collision_rect):
                if self.player.direction.x < 0:
                    # player moving to the right
                    self.player.collision_rect.left = sprite.rect.right 
                     
                elif self.player.direction.x > 0:
                    # player moving to the left
                    self.player.collision_rect.right = sprite.rect.left
                                                      
    def run(self):

        # render sky
        self.sky_sprites.update()
        self.sky_sprites.custom_draw(self.player)

        # render clouds
        self.cloud_sprites.update()
        self.cloud_sprites.custom_draw(self.player)

        # render bg water
        self.bg_water_sprites.update()
        self.bg_water_sprites.custom_draw(self.player)
        
        # render grass
        self.grass_sprites.update()
        self.grass_sprites.custom_draw(self.player)

        # render flag
        self.flag_sprite.update()
        self.flag_sprite.custom_draw(self.player)
        
        # render water reflection
        self.water_reflect_sprites.update()
        self.water_reflect_sprites.custom_draw(self.player)

        # render background balms
        self.bg_balm_sprites.update()
        self.bg_balm_sprites.custom_draw(self.player)

        # render crates 
        self.crate_sprites.update()
        self.crate_sprites.custom_draw(self.player)
        
        # render coins
        self.coin_sprites.update()
        self.coin_sprites.custom_draw(self.player)

        # render enemies
        self.enemy_sprites.update()
        self.enemy_sprites.custom_draw(self.player)

        # render fg balms
        self.fg_balm_sprites.update()
        self.fg_balm_sprites.custom_draw(self.player)
        
        # render terrain
        self.terrain_sprites.update()
        self.terrain_sprites.custom_draw(self.player)

        # collision detection
        self.horizontal_collisions()
        self.get_player_on_ground()
        self.vertical_collisions()
        self.create_landing_particles()

        # dust particles
        self.dust_sprites.update()
        self.dust_sprites.custom_draw(self.player)
 
        # render player and his particles
        self.player_sprite.update()
        self.player_sprite.custom_draw(self.player)
        self.player.dust_particles_animate(self.player_sprite.offset)
        # update borders
        self.border_sprites.update(self.player)
        
        # enemy collisions
        self.enemy_border_collision()
        self.enemy_player_collision()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera box
        camera_left = CAMERA_BORDERS['left']
        camera_top = CAMERA_BORDERS['top']
        camera_width = SCREEN_WIDTH - (CAMERA_BORDERS['left'] + CAMERA_BORDERS['right'])
        camera_height = SCREEN_HEIGHT - (CAMERA_BORDERS['top'] + CAMERA_BORDERS['bottom'])
        self.camera_rect = pygame.Rect(camera_left, camera_top, camera_width, camera_height)

    def custom_draw(self, player):
        # update camera position
        if player.collision_rect.left < self.camera_rect.left:
            self.camera_rect.left = player.collision_rect.left
        elif player.collision_rect.right > self.camera_rect.right:
            self.camera_rect.right = player.collision_rect.right
        elif player.collision_rect.top < self.camera_rect.top:
            self.camera_rect.top = player.collision_rect.top
        elif player.collision_rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.collision_rect.bottom
        
        # camera offset
        self.offset = pygame.math.Vector2(self.camera_rect.left - CAMERA_BORDERS['left'], 
                                          self.camera_rect.top - CAMERA_BORDERS['top'])
        
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)