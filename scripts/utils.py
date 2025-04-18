import pygame
import os

BASE_IMG_PATH = './assets/images'

def load_image(path, scaling = None, alpha = False):
    '''
    Loads and returns a pygame image
    '''
    if alpha:
        img = pygame.image.load(BASE_IMG_PATH + '/' + path).convert_alpha()
    else:
        img = pygame.image.load(BASE_IMG_PATH + '/' + path).convert()
    if scaling != None:
        img = pygame.transform.scale(img, scaling)
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path, flip = False, scaling = None, alpha = False):
    '''
    Loads and returns an array of pygame images present in that dir
    I flip is true mirrors the image
    '''
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + '/' + path)):
        images.append(pygame.transform.flip(load_image(path + '/' + img_name, scaling, alpha), flip, False))
    return images

class Animation:
    '''
    Helps in managing multi image animations
    '''
    def __init__(self, images, img_dur = 5, loop = True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.frame = 0
        self.done = False
        self.length = len(self.images)

    def copy(self):
        '''
        Returns a deepcopy of animation
        '''
        return Animation(self.images, self.img_dur, self.loop)

    def update(self):
        '''
        Updates the frame and image of sprite
        Returns if the animation is complete
        '''

        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.img_dur)
        
        else:
            self.frame += 1
            if self.frame >= len(self.images) * self.img_dur:
                self.done = True

        return self.done

    def set_frame(self, frame):
        '''
        Allows manual setting of frame
        '''
        if self.frame >= len(self.images) * self.img_dur:
            raise Exception('Entered frame is out of range')
        self.frame = frame

    def get_frame(self):
        '''
        Returns present frame of animation
        '''
        return self.frame

    def img(self):
        '''
        Returns the present frame image for rendering
        '''
        return self.images[int(self.frame / self.img_dur)]
