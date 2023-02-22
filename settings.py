import os
dir_name = os.path.dirname(__file__)

level_0 = {
    'terrain': dir_name + r'\Code\Level\0\terrain_terrain.csv',
    'bg_palms': dir_name + r'\Code\Level\0\terrain_bg_balms.csv',
    'fg_balms': dir_name + r'\Code\Level\0\terrain_fg balms.csv',
    'coins': dir_name + r'\Code\Level\0\terrain_coins.csv',
    'grass': dir_name + r'\Code\Level\0\terrain_grass.csv',
    'bg_water': dir_name + r'\Code\Level\0\terrain_horizon.csv',
    'water_reflect': dir_name + r'\Code\Level\0\terrain_water_reflect.csv',
    'sky': dir_name + r'\Code\Level\0\terrain_sky.csv',
    'flag': dir_name + r'\Code\Level\0\terrain_flag.csv',
    'crate': dir_name + r'\Code\Level\0\terrain_crates.csv',
    'enemies': dir_name + r'\Code\Level\0\terrain_enemies.csv',
    'borders': dir_name+ r'\Code\Level\0\terrain_borders.csv',
    'player': dir_name + r'\Code\Level\0\terrain_player.csv'
}

HORIZONTAL_TILES = 90
VERTICAL_TILES = 30
TILE_SIZE = 64
SCREEN_WIDTH = 1200 
SCREEN_HEIGHT = 720

CAMERA_BORDERS = {
    'left': 300,
    'right': 300,
    'top': 200,
    'bottom': 250
}