import pygame
import math

HIT_SHAPE_MAP = {
    'basic' : (22,23,18),
    'wood' : (22,22,21),
    'stone' : (25,30,24),
    'glass' : (16,14,13),
}

DAMAGE_MAP = {
    'basic' : (20,0),
    'wood' : (20,0),
    'stone' : (20,0),
    'glass' : (20,0),
}

class Bird:

    def __init__(self, game, map_size, type, origin = (0, 0), mode = 'idle', flip = False):
        self.origin = origin
        self.pos = origin
        self.mode = mode
        self.game = game
        self.type = type
        self.hit_shape = HIT_SHAPE_MAP[type]
        self.v = 0 + 0j
        self.anim_id = 'projectile_flipped' if flip else 'projectile'
        self.animation = self.game.assets[self.anim_id][self.type]['idle'].copy()
        self.width = self.animation.img().get_width()
        self.height = self.animation.img().get_height()
        self.flip = flip
        self.map_size = map_size

    def calculate_next_pos(self):
        '''
        Returns true if bird is in screen False if offscreen
        '''
        pos = list(self.pos)
        pos[0] += self.v.real
        pos[1] += self.v.imag
        self.v = self.v.real + 1j * min(self.v.imag + 1/6, 10)
        self.pos = tuple(pos)
        return (0 < self.pos[0] < self.map_size[0] - self.width and 0 < self.pos[1] < self.map_size[1]) and not self.collision_check()

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
                self.animation = self.game.assets[self.anim_id][self.type]['in_air'].copy()
                self.v = (self.origin[0] - self.game.scaled_mpos[0])/5 + 1j * (self.origin[1] - self.game.scaled_mpos[1])/5
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
        surf.blit(self.animation.img(), self.pos)
        if self.mode == 'ready' or self.mode == 'aiming':
            expected_scaling = 2
        else:
            if self.flip:
                expected_scaling = 1 + abs(surf.get_width() - self.pos[0]) / surf.get_width()
            else:
                expected_scaling = 1 + abs(self.pos[0]) / surf.get_width()
        expected_offset = [- self.pos[0] + surf.get_width() * expected_scaling / 4, - self.pos[1] - surf.get_height() * expected_scaling / 4]
        expected_offset[0] = (expected_offset[0] + 14 * present_offset[0]) / 15
        expected_offset[1] = (expected_offset[1] + 14 * present_offset[1]) / 15
        self.game.off_set = expected_offset
        self.game.change_scaling(expected_scaling, 14)

    def collision_check(self):
        playing = self.game.player_turn
        to_hit = (playing + 1) % 2
        rel_loc = []
        for i in range(2):
            for j in range(2):
                rel_loc.append(
                    (
                        (self.pos[0] - self.game.get_player_by_id(to_hit).origin[0] - self.hit_shape[0] + i * self.hit_shape[2]) // self.game.get_player_by_id(to_hit).block_map.tile_size[0],
                        (- self.pos[1] + self.game.get_player_by_id(to_hit).origin[1] - self.hit_shape[1] + j * self.hit_shape[2]) // self.game.get_player_by_id(to_hit).block_map.tile_size[1],
                    )
                )
        for loc in rel_loc:
            if loc in self.game.get_player_by_id(to_hit).block_map.block_map:
                self.game.particles.add_particles(self.type + '_feather', self.pos, 5)
                if self.game.get_player_by_id(to_hit).block_map.block_map[loc].damage(self.damage()):
                    self.game.get_player_by_id(to_hit).block_map.block_map.pop(loc)
                return True
        return False
    
    def damage(self):
        return DAMAGE_MAP[self.type][0] + DAMAGE_MAP[self.type][1] * abs(self.v)
        