import random
import math

class Particles:
    '''
    Allows us to mange bunch of non interactive particles for special effects
    '''
    def __init__(self, window_size, assets):
        
        self.assets = assets
        self.window_size = window_size
        self.particles = []

    def add_particles(self, type, pos, effects, num = None):
        '''
        Adds a particle to particle manager
        Possible effects:
            random: spawns particles at random positions close to given
            sequence: if animation has a specific sequence of unique particles and none is to be updated
            radial: gives a random initial radial velocity
            float: gives the particle random up push to cause variable velocity along y axis
            gravity: adds gravity to motion of particle
            truncated: removes few inital frames
            fast: launches the particle at high speed
            cloud: drifts the particle right slowly
        '''
        
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
        '''
        Updates all particles and removes some if their animation is finished
        '''
        for particle in self.particles:
            if particle.update():
                self.particles.remove(particle)

    def render(self, surf):
        '''
        Renders all the particles on given surface
        '''
        for particle in self.particles:
            particle.render(surf)

    def reset(self):
        self.particles = []

class Particle:
    '''
    Handles non interactve special effects
    '''
    def __init__(self, animation, window_size, type, pos, vx, vy = 1, effects = None, idx = None):

        if effects == None:
            self.effects = []
        
        else:
            self.effects = effects
        
        self.window_size = window_size
        
        # animation setting
        self.anim = animation
        
        if idx != None:
            self.anim.set_frame(10*idx)

        elif 'truncated' in self.effects:
            self.anim.set_frame(8)
        else:
            self.anim.set_frame(30*int(random.random()))
        
        if 'cloud' in self.effects:
            self.anim.set_frame(10 * math.floor(self.anim.length * random.random() - 0.001))

        self.type = type

        self.pos = list(pos)
        
        self.vx = (- 0.2 - random.random() / 5) if 'cloud' in self.effects else vx * (10 if 'fast' in self.effects else 1)
        self.vy = 0 if 'cloud' in self.effects else vy * (10 if 'fast' in self.effects else 1)
        
        if 'radial' in self.effects:
            # gives speed itself in radial case
            angle = 2 * math.pi * random.random()
            speed = (1+0.5 * random.random()) * (5 if 'fast' in self.effects else 1)
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)

    def update(self):
        '''
        Updates the animation
        Return True if animation has ended
        '''

        self.pos[0] += self.vx
        self.pos[1] += self.vy * (1 + (math.sin(2 * math.pi * random.random()) if 'float' in self.effects else 0))

        if 'gravity' in self.effects:

            if 'float' in self.effects:
                self.vy += 0.02 

            else:
                self.vy += 0.2 

        if 'sequence' in self.effects:
            if (-self.anim.img().get_width() < self.pos[0]):
                return False
            else:
                if 'cloud' in self.effects:
                    self.pos[0] = self.window_size[0]
                    self.pos[1] = self.window_size[1] * random.random() * 0.6
                    return False
                return True
        
        else:
            return self.anim.update()

    def render(self, surf):
        '''
        Renders the animation to given surface
        '''
        surf.blit(self.anim.img(), self.pos)
