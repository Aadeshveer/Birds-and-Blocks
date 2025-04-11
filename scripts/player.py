from .blockmap import BlockMap
from .cards import Deck

class Player:
    def __init__(self, game, origin, block_map = None):
        self.origin = origin
        self.game = game
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
        self.deck = Deck(
            (
                self.game.display.get_width(),
                self.game.display.get_height()
            ),
            (
                origin[0] + self.block_map.tile_size[0] * 3 + 60,
                origin[1] - 60
            ),
            ['red', 'red', 'red', 'red', 'red', 'red', 'red'],
            'left'
        )
            

    def render(self):
        self.block_map.render(self.game.display)
        if self.deck.active == None:
            self.game.scrolling = True
            self.deck.play_deck(self.game.display, self.game.scaled_mpos, self.game.off_set, self.game.scaling_factor)
        else:
            self.game.scrolling = False
            self.game.off_set, self.game.scaling_factor = self.deck.play_deck(self.game.display, self.game.scaled_mpos, self.game.off_set, self.game.scaling_factor)
