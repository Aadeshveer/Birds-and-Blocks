import pygame
import random
import math

class Particles:
    def __init__(self, assets):
        self.assets = assets
        self.particles = []

    def add_particles(self, type, pos, num = 1):
        for _ in range(num):
            self.particles.append(
                Particle(
                    self.assets[type + ('_flipped' if random.random() > 0.5 else '')].copy(),
                    (
                        pos[0] + 16 * random.random(),
                        pos[1] + 16 * random.random(),
                    ),
                    vx = 2*random.random(),
                    vy = 1,
                    effect='float',
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
    def __init__(self, animation, pos, vx, vy = 1, effect = 'none'):
        self.anim = animation
        self.anim.set_frame(30*int(random.random()))
        self.vx = vx
        self.vy = vy
        self.effect = effect
        self.pos = list(pos)

    def update(self):
        self.pos[0] += self.vx
        self.pos[1] += self.vy * (1 + (math.sin(2 * math.pi * random.random()) if self.effect == 'float' else 0))
        self.vy += 0.02
        return self.anim.update()

    def render(self, surf):
        surf.blit(self.anim.img(), self.pos)