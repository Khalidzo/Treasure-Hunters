from os import walk
import pygame

def import_images(path):
    image_list = []
    
    for directory, dir_paths, images in walk(path):
        for image in images:
            image_surface = pygame.image.load(path + '\\'  + image).convert_alpha()
            image_list.append(image_surface)
    
    return image_list