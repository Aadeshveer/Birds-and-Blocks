import pygame
from .utils import load_image

class BlockMap:
    
    def __init__(self, origin, map = None):
        '''
        Origin is a tuple of ints representing the origin of block printing
        Map is a dictionary of format { (int, int): type ... }
        '''
        self.origin = origin
        self.tile_size = (64, 64)
        self.block_map = {}
        if map is not None:
            for i in map:
                self.add_block(i, map[i])

    def render(self, surf):
        '''
        Renders each block in block map
        '''
        for loc in self.block_map:
            img = self.block_map[loc].img
            surf.blit(img, (self.origin[0] + loc[0]*self.tile_size[0], self.origin[1] - loc[1]*self.tile_size[1] - img.get_height()))
        
    def add_block(self, loc, type):
        '''
        Adds a block at relative location loc
        '''
        self.block_map[loc] = Block(type, self.tile_size)

class Block:
    
    def __init__(self, type = None, tile_size = None):
        if type is None:
            self.type = 'test'
        self.type = type
        self.img = load_image('blocks/' + self.type + '.png')
        if tile_size == None:
            self.tile_size = self.img.get_size()
        else:
            self.tile_size = tile_size
            self.img = pygame.transform.scale(self.img, (tile_size))
            