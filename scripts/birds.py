import pygame
from .utils import load_images,Animation
import math

class Bird:

    def __init__(self, map_size, origin = (0, 0), mode = 'idle', flip = False):
        self.origin = origin
        self.pos = origin
        self.mode = mode
        self.v = 0 + 0j
        self.animations ={
            'idle' : Animation(load_images('projectiles/basic/idle')),
            'in_air' : Animation(load_images('projectiles/basic/in_air'))
        }
        self.animation = self.animations['idle'].copy()
        self.width = self.animation.img().get_width()
        self.height = self.animation.img().get_height()
        self.flip = flip
        self.map_size = map_size
        if self.flip:
            self.img = pygame.transform.flip(self.img, True, False)

    def calculate_next_pos(self):
        '''
        Returns true if bird is in screen False if offscreen
        '''
        pos = list(self.pos)
        pos[0] += self.v.real
        pos[1] += self.v.imag
        self.v = self.v.real + 1j * min(self.v.imag + 1/6, 5)
        self.pos = tuple(pos)
        if not (0 < self.pos[0] < self.map_size[0] - self.width and 0 < self.pos[1] < self.map_size[1]):
            raise Exception('Bird out of bounds')

    def update(self, mpos):
        '''
        Manges the bird movement
        Returns True if scrolling is allowed else False
        '''
        self.animation.update()
        if self.mode == 'in_air':
            self.calculate_next_pos()
            self.animation = self.animations['in_air'].copy()

        if self.mode == 'ready':
            if pygame.mouse.get_pressed()[0] and math.dist((self.origin[0] + 16, self.origin[1] + 16), mpos) < 20:
                self.mode = 'aiming'

        if self.mode == 'aiming':
            if not pygame.mouse.get_pressed()[0]:
                self.mode = 'in_air'
                self.v = (self.origin[0] - mpos[0])/5 * (-1 if self.flip else 1) + 1j * (self.origin[1] - mpos[1])/5
                modulus = abs(self.v)
                self.v /= abs(self.v)
                self.v *= 14 * (1-math.exp(-modulus))
            dist = math.dist(mpos, self.origin)
            if dist < 50:
                self.pos = mpos
            else:
                self.pos = (
                    self.origin[0] + (mpos[0]-self.origin[0])/dist*50,
                    self.origin[1] + (mpos[1]-self.origin[1])/dist*50
                )


    def render(self, surf, present_scaling, present_offset):
        '''
        Renders bird on surf and returns a scaling factor for better effect
        '''
        surf.blit(self.animation.img(), self.pos)
        if self.mode == 'ready' or self.mode == 'aiming':
            expected_scaling = 2
        else:
            expected_scaling = 1 + abs(self.pos[0]) / surf.get_width()
        expected_scaling = (14 * present_scaling + expected_scaling) / 15
        expected_offset = [- self.pos[0] + surf.get_width() * expected_scaling / 4, - self.pos[1] - surf.get_height() * expected_scaling / 4]
        expected_offset[0] = (expected_offset[0] + 14 * present_offset[0]) / 15
        expected_offset[1] = (expected_offset[1] + 14 * present_offset[1]) / 15
        return (expected_offset, expected_scaling)
