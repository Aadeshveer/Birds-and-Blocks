import pygame
import random
import math

class Particles:
    def __init__(self, window_size, assets):
        self.assets = assets
        self.window_size = window_size
        self.particles = []

    def add_particles(self, type, pos, effects, num = None):
        if num == None:
            num = self.assets[type].length
        for i in range(num):
            self.particles.append(
                Particle(
                    self.assets[type + ('_flipped' if (random.random() > 0.5 and type+'_flipped' in self.assets) else '')].copy(),
                    self.window_size,
                    type,
                    (
                        pos[0] + (16 * random.random() if 'random' in effects else 0),
                        pos[1] + (16 * random.random() if 'random' in effects else 0),
                    ),
                    vx = 2*random.random()-1,
                    vy = 1,
                    effects=effects,
                    idx = i if 'sequence' in effects else None
                )
            )

    def update(self):
        for particle in self.particles:
            if particle.update():
                self.particles.remove(particle)

    def render(self, surf):
        for particle in self.particles:
            particle.render(surf)

class Particle:
    def __init__(self, animation, window_size, type, pos, vx, vy = 1, effects = None, idx = None):
        if effects == None:
            self.effects = []
        else:
            self.effects = effects
        self.window_size = window_size
        self.anim = animation
        if idx != None:
            self.anim.set_frame(10*idx)
        else:
            self.anim.set_frame(30*int(random.random()))
        self.type = type
        self.vx = vx
        self.vy = vy
        self.pos = list(pos)
        if 'radial' in self.effects:
            angle = 2 * math.pi * random.random()
            speed = 1+0.5 * random.random()
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)

    def update(self):
        self.pos[0] += self.vx
        self.pos[1] += self.vy * (1 + (math.sin(2 * math.pi * random.random()) if 'float' in self.effects else 0))
        if 'gravity' in self.effects:
            if 'float' in self.effects:
                self.vy += 0.02 
            else:
                self.vy += 0.2 
        if 'sequence' in self.effects:
            return not ((0 < self.pos[0] < self.window_size[0]) and (0 < self.pos[1] < self.window_size[1]))
        else:
            return self.anim.update()

    def render(self, surf):
        surf.blit(self.anim.img(), self.pos)