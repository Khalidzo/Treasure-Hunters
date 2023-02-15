from os import walk
from csv import reader
from settings import TILE_SIZE
import pygame


def import_images(path):
    image_list = []
    
    for directory, dir_paths, images in walk(path):
        for image in images:
            image_surface = pygame.image.load(path + '\\'  + image).convert_alpha()
            image_list.append(image_surface)   
    
    return image_list

def import_csv(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter= ',')
        for row in level:
            terrain_map.append(list(row))
    
    return terrain_map

def import_sliced_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_width() / TILE_SIZE)
    tile_num_y = int(surface.get_height() / TILE_SIZE)
    sliced_tiles = []

    for row in range(tile_num_y):
        for column in range(tile_num_x):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            sliced_surface = pygame.Surface((TILE_SIZE,TILE_SIZE), flags= pygame.SRCALPHA)
            sliced_surface.blit(surface, (0,0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            sliced_tiles.append(sliced_surface)

    return sliced_tiles
