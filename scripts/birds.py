import pygame
from .utils import load_image
import math

class Bird:

    def __init__(self, map_size, origin = (0, 0), mode = 'idle', flip = False):
        self.origin = origin
        self.pos = origin
        self.mode = mode
        self.v = 0 + 0j
        self.img = load_image('projectiles/basic/0.png')
        self.width = self.img.get_width()
        self.height = self.img.get_height()
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
        if 0 < self.pos[0] < self.map_size[0] - self.width and 0 < self.pos[1] < self.map_size[1]:
            return True
        self.mode = 'idle'
        self.pos = self.origin
        return False


    def update(self, mpos):
        '''
        Manges the bird movement
        Returns True if scrolling is allowed else False
        '''
        if self.mode == 'in_air':
            if self.calculate_next_pos():
                return False
            else:
                return True

        if self.mode == 'ready':
            if pygame.mouse.get_pressed()[0]:
                self.mode = 'aiming'
            return False

        if self.mode == 'aiming':
            if not pygame.mouse.get_pressed()[0]:
                self.mode = 'in_air'
                self.v = abs(self.origin[0] - mpos[0])/5 * (-1 if self.flip else 1) - 1j * abs(self.origin[1] - mpos[1])/5
                self.v *= 1.2
                if abs(self.v) >= 16:
                    self.v /= abs(self.v)
                    self.v *= 16
            if math.dist(mpos, self.pos) < 50:
                self.pos = mpos
            return False
        return True

    def render(self, surf, present_scaling, present_offset):
        '''
        Renders bird on surf and returns a scaling factor for better effect
        '''
        surf.blit(self.img, self.pos)
        if self.mode == 'aiming':
            expected_scaling = 2
            expected_scaling = (present_scaling + expected_scaling) / 2
        else:
            expected_scaling = 1 + abs(self.pos[0]) / surf.get_width()
            expected_scaling = (9 * present_scaling + expected_scaling) / 10
        expected_offset = [- self.pos[0] + surf.get_width() * expected_scaling / 4, - self.pos[1] - surf.get_height() * expected_scaling / 4]
        expected_offset[0] = (expected_offset[0] + 14 * present_offset[0]) / 15
        expected_offset[1] = (expected_offset[1] + 14 * present_offset[1]) / 15
        return (expected_offset, expected_scaling)
