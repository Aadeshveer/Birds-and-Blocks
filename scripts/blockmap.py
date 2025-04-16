import pygame

HEALTH_MAP = {
    'glass' : 5,
    'wood' : 75,
    'stone' : 95,
}

class BlockMap:
    
    def __init__(self, game, origin, map = None):
        '''
        Origin is a tuple of ints representing the origin of block printing
        Map is a dictionary of format { (int, int): type ... }
        '''
        self.tile_size = (64, 64)
        self.game = game
        self.origin = origin
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
            surf.blit(
                img,
                (
                    self.origin[0] + loc[0]*self.tile_size[0],
                    self.origin[1] - loc[1]*self.tile_size[1] - img.get_height(),
                ),
            )
        
    def loc_to_pos(self, loc):
        '''
        Takes in a relative loc and returns pos according to its origin
        '''
        return (
            self.origin[0] + loc[0] * self.tile_size[0],
            self.origin[1] - (loc[1] + 1) * self.tile_size[1],
        )

    def add_block(self, loc, type):
        '''
        Adds a block at relative location loc
        '''
        self.block_map[loc] = Block(self.game, type)

class Block:
    
    def __init__(self, game, type):
        '''
        Just a class to store small some data for blocks
        '''
        self.game = game
        self.type = type
        
        self.anim = self.game.assets['blocks'][type].copy()
        
        self.HP = HEALTH_MAP[type]
        
        self.tile_size = self.anim.img().get_size()

    def damage(self, n):
        '''
        Reduces the health of block
        Returns if the block is destroyed
        '''
        self.HP -= n
        if self.HP <= 0:
            return True
        self.anim.set_frame(5 * (HEALTH_MAP[self.type] - self.HP)//HEALTH_MAP[self.type])
