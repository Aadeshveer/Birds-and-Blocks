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

class Animation:
    def __init__(self, images, img_dur = 5, loop = True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.frame = 0
        self.done = False

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.img_dur)
        else:
            self.frame += 1
            if self.frame >= len(self.images) * self.img_dur:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_dur)]