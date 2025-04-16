import pygame
import math

VMAX = 14

HIT_SHAPE_MAP = {
    'basic' : (22,23,18),
    'wood' : (22,22,21),
    'stone' : (25,30,24),
    'glass' : (16,14,13),
}

DAMAGE_MAP = {
    'basic' : (20,2),
    'wood' : (20,2),
    'stone' : (20,2),
    'glass' : (20,2),
}

class Bird:

    def __init__(self, game, map_size, type, origin = (0, 0), mode = 'idle', flip = False):
        self.game = game
        self.map_size = map_size
        self.type = type
        self.origin = origin
        self.pos = origin # original position is provided origin
        self.mode = mode
        self.flip = flip
        self.stray = False
        self.v = 0 + 0j
        self.hit_shape = HIT_SHAPE_MAP[type] # Helps in forming a rectangle which if hits will cause damage to blocks
        self.anim_id = 'projectile_flipped' if flip else 'projectile' 
        self.animation = self.game.assets[self.anim_id][self.type]['idle'].copy()
        self.width = self.animation.img().get_width()
        self.height = self.animation.img().get_height()
        self.stray_projectiles = []
        self.damage_factor = 1

    def calculate_next_pos(self):
        '''
        Calculates and moves bird to next position
        Returns true if bird is in screen False if offscreen
        '''
        pos = list(self.pos)
        upgrade_index = self.game.get_player_by_id().upgrades[self.type]
        if pygame.mouse.get_pressed()[0] and upgrade_index > 1:
            if self.power:
                match self.type:
                    
                    case 'wood':
                        self.v += 4 * (-1 if self.flip else 1) * upgrade_index
                        self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=5)

                    case 'stone':
                        rel_loc = (
                            (self.pos[0] - self.game.get_player_by_id(-1).origin[0] - self.hit_shape[0] / 2) / self.game.get_player_by_id(-1).block_map.tile_size[0],
                            (- self.pos[1] + self.game.get_player_by_id(-1).origin[1] - self.hit_shape[1] / 2) / self.game.get_player_by_id(-1).block_map.tile_size[1],
                        )
                        for block_loc in self.game.get_player_by_id(-1).block_map.block_map.copy():
                            block = self.game.get_player_by_id(-1).block_map.block_map[block_loc]
                            loc = (
                                block_loc[0] + 0.5,
                                block_loc[1] + 0.5,
                            )
                            dist = math.dist(rel_loc, loc)

                            self.game.particles.add_particles('particle', self.pos, effects = ['radial','random','fast'], num=30 + 10*upgrade_index)
                            if dist < 3:
                                if (self.game.get_player_by_id(-1).block_map.block_map[block_loc].damage((10 + 30 * (1 - dist/3)) * upgrade_index)):
                                    # runs if block is destroyed
                                    self.game.get_player_by_id(-1).block_map.block_map.pop(block_loc)
                                    # run broken bird shard animation
                                    self.game.particles.add_particles('shards_' + block.type, self.game.get_player_by_id(-1).block_map.loc_to_pos(block_loc), effects=['gravity', 'sequence', 'radial'])
                        
                        pos[0] += self.map_size[0]

                    case 'glass':
                        self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=10)
                        self.stray_projectiles.append(self.make_stray_projectile(2j))
                        self.stray_projectiles.append(self.make_stray_projectile(-2j))
                        self.damage_factor /= 2

                    case 'basic':
                        self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=10)
                        self.damage_factor *= 3

                self.power = False
        if not self.power:
            match self.type:
                case 'wood':
                    self.game.particles.add_particles('particle', self.pos, effects = ['radial','random','truncated'], num=1)
                case 'basic':
                    self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=1)

        pos[0] += self.v.real
        pos[1] += self.v.imag
        
        self.v = self.v.real + 1j * min(self.v.imag + 1/6, 10)
        
        self.pos = tuple(pos)
        
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

        stray_operating = False
        for strays in self.stray_projectiles:
            if strays.update():
                stray_operating = True

        self.animation.update()

        if self.mode == 'in_air':
            return self.calculate_next_pos() or stray_operating

        if self.mode == 'ready':
            if (
                pygame.mouse.get_pressed()[0]
                and
                math.dist((self.origin[0] + 16, self.origin[1] + 16), self.game.scaled_mpos) < 30 # we can click in 30 pixel radius of center of sprite
            ):
                self.mode = 'aiming'

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
                
                self.mode = 'in_air'
                self.animation = self.game.assets[self.anim_id][self.type]['in_air'].copy()

                # set velocity proportional to displacement
                self.v = (self.origin[0] - self.game.scaled_mpos[0])/5 + 1j * (self.origin[1] - self.game.scaled_mpos[1])/5
                modulus = abs(self.v)
                # reset velocity modulus to asymptotically reach a maximum
                self.v /= abs(self.v)
                self.v *= VMAX * (1-math.exp(-modulus))

        return True


    def render(self):
        '''
        Renders bird on surf and returns a scaling factor for better effect
        '''
        for stray in self.stray_projectiles:
            stray.render()

        surf = self.game.display
        present_offset = self.game.off_set

        surf.blit(self.animation.img(), self.pos)
        
        if self.mode == 'ready' or self.mode == 'aiming':
            expected_scaling = 2
        
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

        for i in range(2):

            for j in range(2):
            
                rel_loc.append(
                    (
                        (self.pos[0] - origin[0] - self.hit_shape[0] + i * self.hit_shape[2]) // self.game.get_player_by_id(-1).block_map.tile_size[0],
                        (- self.pos[1] + origin[1] - self.hit_shape[1] + j * self.hit_shape[2]) // self.game.get_player_by_id(-1).block_map.tile_size[1],
                    )
                )
        
        for loc in rel_loc:

            if loc in self.game.get_player_by_id(-1).block_map.block_map: # there is a block placed at given location
            
                block = self.game.get_player_by_id(-1).block_map.block_map[loc]

                # add bird feathers effect
                self.game.particles.add_particles(self.type + '_feather', self.pos, effects = ['float','gravity','random'], num=5)
                # adds magic dust effect
                self.game.particles.add_particles('dust', self.pos, effects = ['radial','random'], num=5)

                if block.damage(self.damage()):
                    # runs if block is destroyed
                    self.game.get_player_by_id(-1).block_map.block_map.pop(loc)
                    # run broken bird shard animation
                    self.game.particles.add_particles('shards_' + block.type, self.game.get_player_by_id(-1).block_map.loc_to_pos(loc), effects=['gravity', 'sequence', 'radial'])
                
                self.pos = (0,self.map_size[1]) if self.flip else self.map_size

                return True
        
        return False
    
    def damage(self):
        '''
        Returns damage of bird
        '''
        return (DAMAGE_MAP[self.type][0] + DAMAGE_MAP[self.type][1] * abs(self.v)) * self.damage_factor
    
    def make_stray_projectile(self, vel_offset):
        projectile = Bird(self.game, self.map_size, self.type, self.origin, self.mode, self.flip)
        projectile.pos = self.pos
        projectile.stray = True
        projectile.v = self.v + vel_offset
        projectile.power = False
        return projectile