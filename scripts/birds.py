import pygame
from .utils import load_image
import math

class Bird:

    def __init__(self, origin = (0, 0), mode = 'idle'):
        self.origin = origin
        self.pos = origin
        self.mode = mode
        self.velx = 0
        self.vely = 0
        self.img = load_image('projectiles/basic/0.png')

    def calculate_next_pos(self):
        print(self.velx, self.vely)
        pos = list(self.pos)
        pos[0] += self.velx
        pos[1] += self.vely
        self.vely = min(self.vely + 1/60, 3)
        self.pos = tuple(pos)

    def update(self, mpos):
        
        if self.mode == 'in_air':
            self.calculate_next_pos()
            return False

        if self.mode == 'ready':
            if pygame.mouse.get_pressed()[0]:
                self.mode = 'aiming'
            return False

        if self.mode == 'aiming':
            if not pygame.mouse.get_pressed()[0]:
                self.mode = 'in_air'
                self.velx = (self.origin[0] - mpos[0])/10
                self.vely = (self.origin[1] - mpos[1])/10
            if math.dist(mpos, self.pos) < 50:
                self.pos = mpos
            return False
        return True

    def render(self, surf):
        surf.blit(self.img, self.pos)
