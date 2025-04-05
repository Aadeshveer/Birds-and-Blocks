import pygame
from .utils import load_image

class BlockMap:
    
    def __init__(self, origin, map = None):
        '''
        Origin is a tuuple of ints representing the origin of block printing
        Map is a dictionary of format { (int, int): Block ... }
        '''
        self.origin = origin
        if map is None:
            self.block_map = {}
        else:
            for i in map:
                self.block_map = map
        print(self.origin)

    def render(self, surf):
        for loc in self.block_map:
            img = self.block_map[loc].img
            surf.blit(img, (self.origin[0] + loc[0], self.origin[1] + loc[1] - img.get_height()))
        

class Block:
    
    def __init__(self, type):
        self.type = type
        self.img = load_image('blocks/basic.png')