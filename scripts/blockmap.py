import pygame

HEALTH_MAP = {
    'glass' : 100,
    'wood' : 200,
    'stone' : 300,
    'royal' : 1000,
}

class BlockMap:
    
    def __init__(self, game, origin, map = None):
        '''
        Origin is a tuple of ints representing the origin of block printing
        Map is a dictionary of format { (int, int): type ... }
        '''
        self.origin = origin
        self.game = game
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
            img = self.block_map[loc].anim.img()
            surf.blit(img, (self.origin[0] + loc[0]*self.tile_size[0], self.origin[1] - loc[1]*self.tile_size[1] - img.get_height()))
        
    def add_block(self, loc, type):
        '''
        Adds a block at relative location loc
        '''
        self.block_map[loc] = Block(self.game, type)

class Block:
    
    def __init__(self, game, type):
        self.type = type
        self.game = game
        self.anim = self.game.assets['blocks'][type].copy()
        self.HP = HEALTH_MAP[type]
        self.tile_size = self.anim.img().get_size()
