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

def load_images(path, flip = False):
    '''
    Loads and returns an array of pygame images present in that dir
    I flip is true mirrors the image
    '''
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + '/' + path)):
        images.append(pygame.transform.flip(load_image(path + '/' + img_name), flip, False))
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
        return self.done

    def set_frame(self, frame):
        if self.frame >= len(self.images) * self.img_dur:
            raise Exception('Entered frame is out of range')
        self.frame = frame

    def img(self):
        return self.images[int(self.frame / self.img_dur)]