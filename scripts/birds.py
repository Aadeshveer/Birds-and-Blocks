import pygame
import math

VMAX = 14
GRAVITY = 1/6 # equivalant to 10 per sec

# the visual hit shape of bird first two numbers give its top left corner and third is size of square
HIT_SHAPE_MAP = {
    'basic' : (22,23,18),
    'wood' : (22,22,21),
    'stone' : (25,30,24),
    'glass' : (16,14,13),
}

# damage = constant[0] + constant[1] * speed
DAMAGE_MAP = {
    'basic' : (35,2),
    'wood' : (20,2),
    'stone' : (20,2),
    'glass' : (20,2),
}

# maps the sprite location for strap
LAUNCHER_STRAP_MAP = {
    'basic' : (14,22),
    'glass' : (8,16),
    'wood' : (14,22),
    'stone' : (20,28),
}

# returns the visual center of bird
BIRD_CENTER = {
    'basic' : (12,12),
    'glass' : (10,10),
    'wood' : (12,12),
    'stone' : (14,20),
}

class Bird:

    def __init__(self, game, map_size, type, origin = (0, 0), mode = 'idle', flip = False, stray = False):
        '''
        Initializes the projectile bird object
        '''
        self.game = game
        self.map_size = map_size
        self.origin = origin
        
        self.pos = origin # original position is provided origin
        self.type = type
        self.mode = mode
        self.stray = stray # stray projectiles have a very limited functionality and are associated with some real projectile
        self.v = 0 + 0j
        self.damage_factor = 1
        self.stray_projectiles = []

        self.flip = flip
        self.hit_shape = HIT_SHAPE_MAP[type] # Helps in forming a rectangle which if hits will cause damage to blocks
        self.anim_id = 'projectile_flipped' if flip else 'projectile' 
        self.animation = self.game.assets[self.anim_id][self.type]['in_air' if self.stray else 'idle'].copy()
        self.width = self.animation.img().get_width()
        self.height = self.animation.img().get_height()

    def calculate_next_pos(self):
        '''
        Calculates and moves bird to next position
        Returns true if bird is in screen False if offscreen
        '''
        pos = list(self.pos)

        # used to identify if the bird has been upgraded
        upgrade_index = self.game.get_player_by_id().upgrades[self.type]
        
        # if upgrade_index > 1 => bird is upgraded and has some special power activated on click
        if pygame.mouse.get_pressed()[0] and upgrade_index > 1:

            # to prevent use of power more than once in a flight
            if self.power:

                match self.type:
                    
                    case 'wood':
                        # increase the speed of bird thus increasing damage
                        self.v += 4 * (-1 if self.flip else 1) * upgrade_index
                        # trail of star particles
                        self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=5)

                    case 'stone':

                        # blast sound
                        if not self.game.mute:
                            self.game.audio['bomb'].play()

                        # location of center of blast relative to grid
                        rel_loc = (
                            (self.pos[0] - self.game.get_player_by_id(-1).origin[0] - self.hit_shape[0] / 2) / self.game.get_player_by_id(-1).block_map.tile_size[0],
                            (- self.pos[1] + self.game.get_player_by_id(-1).origin[1] - self.hit_shape[1] / 2) / self.game.get_player_by_id(-1).block_map.tile_size[1],
                        )

                        # for blocks in enemy fortress damage it as per (10 + 30 * (1 - dist/3)) * upgrade_index) if it is less than 3 relative units away
                        for block_loc in self.game.get_player_by_id(-1).block_map.block_map.copy():
                            
                            block = self.game.get_player_by_id(-1).block_map.block_map[block_loc]
                            # relative center of block
                            loc = (
                                block_loc[0] + 0.5,
                                block_loc[1] + 0.5,
                            )
                            dist = math.dist(rel_loc, loc)
                            
                            # adds blast particles capped at 90 to prevent lag at higher levels
                            self.game.particles.add_particles('particle', self.pos, effects = ['radial','random','fast'], num = max(90,30 + 10*upgrade_index))
                            
                            if dist < 3:

                                # runs if block breaks
                                if (self.game.get_player_by_id(-1).block_map.block_map[block_loc].damage((10 + 30 * (1 - dist/3)) * upgrade_index)):
                                    
                                    if not self.game.mute:
                                        self.game.audio[block.type + '_break'].play()

                                    # runs if block is destroyed
                                    self.game.get_player_by_id(-1).block_map.block_map.pop(block_loc)
                                    
                                    # run broken block shard animation
                                    self.game.particles.add_particles('shards_' + block.type, self.game.get_player_by_id(-1).block_map.loc_to_pos(block_loc), effects=['gravity', 'sequence', 'radial'])
                        
                        # takes the bird out of screen killing it
                        pos[0] += self.map_size[0]

                    case 'glass':
                        # halves the damage but triples the number by adding stray projectiles

                        self.stray_projectiles.append(self.make_stray_projectile(2j))
                        self.stray_projectiles.append(self.make_stray_projectile(-2j))
                        self.damage_factor /= 4 * upgrade_index
                        
                        # adds special effect to the division
                        self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=10)

                    case 'basic':
                        # just triple the damage every index
                        self.damage_factor *= 3 * upgrade_index / 2
                        self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=10)

                # power cannot be reactivated
                self.power = False

        # power has been used
        if not self.power:

            match self.type:
                
                case 'wood':
                    # keep adding a trail of particles
                    self.game.particles.add_particles('particle', self.pos, effects = ['radial','random','truncated'], num=1)
                
                case 'basic':
                    # keep adding a trail of particles
                    self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=1)

        # move to next pos
        pos[0] += self.v.real
        pos[1] += self.v.imag
        
        # update the velocity
        self.v = self.v.real + 1j * min(self.v.imag + GRAVITY, 10)
        
        self.pos = tuple(pos)
        
        # return true if bird is alive
        return (
            0 < self.pos[0] < self.map_size[0] - self.width
            and
            0 < self.pos[1] < self.map_size[1]
            and
            not self.collision_check()
        )

    def update(self):
        '''
        Manges the bird movement
        Return True if bird is operating
        '''
        # keeps bird alive until its strays are alive
        stray_operating = False
        for strays in self.stray_projectiles:
            if strays.update():
                stray_operating = True

        self.animation.update()

        if self.mode == 'in_air':
            return self.calculate_next_pos() or stray_operating

        # animate bird sitting on slingshot
        if self.mode == 'ready':
            # for tutorial purpose
            if self.game.tutorial:
                pygame.draw.circle(self.game.display, 'red', (self.origin[0] + 16, self.origin[1] + 16), 30)
            
            if (
                pygame.mouse.get_pressed()[0]
                and
                math.dist((self.origin[0] + 16, self.origin[1] + 16), self.game.scaled_mpos) < 30 # we can click in 30 pixel radius of center of sprite
            ):
                self.mode = 'aiming'

        # animate bird in hand of player
        if self.mode == 'aiming':

            if pygame.mouse.get_pressed()[0]: # if mouse button is kept pressed
            
                dist = math.dist(self.game.scaled_mpos, self.origin)

                if dist < 50:
                    self.pos = self.game.scaled_mpos

                else:
                    self.pos = (
                        self.origin[0] + (self.game.scaled_mpos[0]-self.origin[0])/dist*50,
                        self.origin[1] + (self.game.scaled_mpos[1]-self.origin[1])/dist*50
                    )

            else:
                
                self.power = True
                
                if not self.game.mute:
                    self.game.audio[self.type+'_yell'].play()

                self.mode = 'in_air'
                self.animation = self.game.assets[self.anim_id][self.type]['in_air'].copy()

                # set velocity proportional to displacement
                self.v = (self.origin[0] - self.game.scaled_mpos[0] + BIRD_CENTER[self.type][0])/5 + 1j * (self.origin[1] - self.game.scaled_mpos[1] + BIRD_CENTER[self.type][1])/5
                modulus = abs(self.v)
                # reset velocity modulus to asymptotically reach a maximum
                self.v /= abs(self.v)
                self.v *= VMAX * (1-math.exp(-modulus))

        return True


    def render(self):
        '''
        Renders bird on surf and returns a scaling factor for better effect
        '''
        # first render the strays
        for stray in self.stray_projectiles:
            stray.render()

        # render itself and update the game offset and scaling for better zoom effect
        surf = self.game.display
        present_offset = self.game.off_set

        if self.mode == 'ready' or self.mode == 'aiming':
            self.strap_back(surf)

        surf.blit(self.animation.img(), self.pos)
        
        if self.mode in ['aiming']:
            v = (self.origin[0] - self.game.scaled_mpos[0] + BIRD_CENTER[self.type][0])/5 + 1j * (self.origin[1] - self.game.scaled_mpos[1] + BIRD_CENTER[self.type][1])/5
            modulus = abs(v)
            v /= modulus
            v *= VMAX * (1-math.exp(-modulus))
            for i in range(1, 30, 4):
                pygame.draw.circle(surf, 'white', (self.origin[0] + v.real*i,self.origin[1] + v.imag*i + GRAVITY/2 * i**2), 2 + ( 30 - i ) / 4)


        if self.mode == 'ready' or self.mode == 'aiming':
            expected_scaling = 2
            self.strap_front(surf)

        
        elif not self.stray:
        
            if self.flip:
                expected_scaling = 1 + abs(surf.get_width() - self.pos[0]) / surf.get_width()
        
            else:
                expected_scaling = 1 + abs(self.pos[0]) / surf.get_width()

            expected_offset = [
                - self.pos[0] + surf.get_width() * expected_scaling / 4,
                - self.pos[1] - surf.get_height() * expected_scaling / 4
            ]

            # smoothen the camera scroll
            expected_offset[0] = (expected_offset[0] + 14 * present_offset[0]) / 15
            expected_offset[1] = (expected_offset[1] + 14 * present_offset[1]) / 15
            
            self.game.off_set = expected_offset

            self.game.change_scaling(expected_scaling, 14)


    def collision_check(self):
        '''
        Manages bird in air environment
        Returns if bird has collided
        '''

        # origin of to hit player
        origin = self.game.get_player_by_id(-1).origin
        
        rel_loc = [] # location of bird vertices of hit box of bird relative to origin

        # define relative locations of edges of bird
        for i in range(2):

            for j in range(2):
            
                rel_loc.append(
                    (
                        (self.pos[0] - origin[0] - self.hit_shape[0] + i * self.hit_shape[2]) // self.game.get_player_by_id(-1).block_map.tile_size[0],
                        (- self.pos[1] + origin[1] - self.hit_shape[1] + j * self.hit_shape[2]) // self.game.get_player_by_id(-1).block_map.tile_size[1],
                    )
                )

        # reset the relative location order for different sidewise priority
        if self.game.get_player_by_id().identity == 1:
            rel_loc = [
                rel_loc[1],
                rel_loc[2],
                rel_loc[0],
                rel_loc[3],
            ]
        else:
            rel_loc = [
                rel_loc[0],
                rel_loc[2],
                rel_loc[1],
                rel_loc[3],
            ]

        # if rel loc of any bird edge is in a block collision occurs
        for loc in rel_loc:

            if loc in self.game.get_player_by_id(-1).block_map.block_map: # there is a block placed at given location
            
                block = self.game.get_player_by_id(-1).block_map.block_map[loc]

                # add bird feathers effect
                self.game.particles.add_particles(self.type + '_feather', self.pos, effects = ['float','gravity','random'], num=5)
                # adds magic dust effect
                self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=5)

                if not self.game.mute:
                    self.game.audio['hit'].play()

                if block.damage(self.damage(block.type)):
                    if not self.game.mute:
                        self.game.audio[block.type + '_break'].play()
                    # runs if block is destroyed
                    self.game.get_player_by_id(-1).block_map.block_map.pop(loc)
                    # run broken block shard animation
                    self.game.particles.add_particles('shards_' + block.type, self.game.get_player_by_id(-1).block_map.loc_to_pos(loc), effects=['gravity', 'sequence', 'radial'])
                
                self.pos = (0,self.map_size[1]) if self.flip else self.map_size

                return True
        
        return False
    
    def damage(self, block_type):
        '''
        Returns damage of bird
        '''
        return (DAMAGE_MAP[self.type][0] + DAMAGE_MAP[self.type][1] * abs(self.v)) * self.damage_factor * (1.5 if block_type==self.type else 0.7)
    
    def make_stray_projectile(self, vel_offset):
        '''
        Generates a stray projectile with limited functionality
        '''
        projectile = Bird(self.game, self.map_size, self.type, self.origin, self.mode, self.flip, True)
        projectile.pos = self.pos
        projectile.v = self.v + vel_offset
        projectile.power = False
        return projectile
    
    def strap_back(self, surf):
        '''
        Draws the back of strap of slingshot
        '''
        pygame.draw.polygon(surf, 'brown', [
            (self.pos[0] + (3 if self.type not in ['stone'] else 0) * (-1 if self.flip else 1) + (32 if self.flip else 0), self.pos[1] + LAUNCHER_STRAP_MAP[self.type][0]),
            (self.pos[0] + (3 if self.type not in ['stone'] else 0) * (-1 if self.flip else 1) + (32 if self.flip else 0), self.pos[1] + LAUNCHER_STRAP_MAP[self.type][1]),
            (self.map_size[0]-308 if self.flip else 308, 572),
            (self.map_size[0]-308 if self.flip else 308, 568),
        ])

    def strap_front(self, surf):
        '''
        Draws the front of strap of slingshot
        '''
        pygame.draw.polygon(surf, 'brown', [
            (self.pos[0] + (3 if self.type not in ['stone'] else 0) * (-1 if self.flip else 1) + (32 if self.flip else 0), self.pos[1] + LAUNCHER_STRAP_MAP[self.type][0]),
            (self.pos[0] + (3 if self.type not in ['stone'] else 0) * (-1 if self.flip else 1) + (32 if self.flip else 0), self.pos[1] + LAUNCHER_STRAP_MAP[self.type][1]),
            (self.map_size[0]-284 if self.flip else 284, 572),
            (self.map_size[0]-284 if self.flip else 284, 568),
        ])