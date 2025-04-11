import pygame
import math

class Bird:

    def __init__(self, game, map_size, origin = (0, 0), mode = 'idle', flip = False):
        self.origin = origin
        self.pos = origin
        self.mode = mode
        self.game = game
        self.v = 0 + 0j
        self.animation = self.game.assets['projectile']['basic']['idle'].copy()
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
        return (0 < self.pos[0] < self.map_size[0] - self.width and 0 < self.pos[1] < self.map_size[1])

    def update(self):
        '''
        Manges the bird movement
        Return True if bird operates
        '''
        self.animation.update()
        if self.mode == 'in_air':
            return self.calculate_next_pos()

        if self.mode == 'ready':
            if pygame.mouse.get_pressed()[0] and math.dist((self.origin[0] + 16, self.origin[1] + 16), self.game.scaled_mpos) < 20:
                self.mode = 'aiming'

        if self.mode == 'aiming':
            if not pygame.mouse.get_pressed()[0]:
                self.mode = 'in_air'
                self.animation = self.game.assets['projectile']['basic']['in_air'].copy()
                self.v = (self.origin[0] - self.game.scaled_mpos[0])/5 * (-1 if self.flip else 1) + 1j * (self.origin[1] - self.game.scaled_mpos[1])/5
                modulus = abs(self.v)
                self.v /= abs(self.v)
                self.v *= 14 * (1-math.exp(-modulus))
            dist = math.dist(self.game.scaled_mpos, self.origin)
            if dist < 50:
                self.pos = self.game.scaled_mpos
            else:
                self.pos = (
                    self.origin[0] + (self.game.scaled_mpos[0]-self.origin[0])/dist*50,
                    self.origin[1] + (self.game.scaled_mpos[1]-self.origin[1])/dist*50
                )
        return True


    def render(self):
        '''
        Renders bird on surf and returns a scaling factor for better effect
        '''
        surf = self.game.display
        present_offset = self.game.off_set
        present_scaling = self.game.scaling_factor
        surf.blit(self.animation.img(), self.pos)
        if self.mode == 'ready' or self.mode == 'aiming':
            expected_scaling = 2
        else:
            expected_scaling = 1 + abs(self.pos[0]) / surf.get_width()
        expected_scaling = (14 * present_scaling + expected_scaling) / 15
        expected_offset = [- self.pos[0] + surf.get_width() * expected_scaling / 4, - self.pos[1] - surf.get_height() * expected_scaling / 4]
        expected_offset[0] = (expected_offset[0] + 14 * present_offset[0]) / 15
        expected_offset[1] = (expected_offset[1] + 14 * present_offset[1]) / 15
        self.game.off_set = expected_offset
        self.game.scaling_factor = expected_scaling
