import pygame
import os

BASE_IMG_PATH = './assets/images'

def load_image(path):
    '''
    Loads and returns a pygame image
    '''
    img = pygame.image.load(BASE_IMG_PATH + '/' + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    '''
    Loads and returns an array of pygame images present in that dir
    '''
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + '/' + path)):
        images.append(load_image(path + '/' + img_name))
    return images