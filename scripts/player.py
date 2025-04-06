from .blockmap import BlockMap

class Player:
    def __init__(self, origin, block_map = None):
        self.origin = origin
        if block_map is not None:
            self.block_map = BlockMap(origin,block_map)
        else:
            self.block_map = BlockMap(
                origin,
                {
                    (0,0) : 'stone',
                    (2,0) : 'stone',
                    (1,0) : 'royal',
                    (1,1) : 'stone',
                    (0,1) : 'wood',
                    (2,1) : 'wood',
                    (1,2) : 'wood',
                    (0,2) : 'glass',
                    (2,2) : 'glass',
                    (1,3) : 'glass',
                }
            )
            

    def render(self, surf):
        self.block_map.render(surf)
