import pygame
from .blockmap import BlockMap
from .cards import Deck

class Player:
    '''
    Player class manages the blockmap, cards, birds etc.
    '''
    def __init__(self, game, identity, origin, block_map = None):
        self.game = game
        self.identity = identity
        self.upgrades = {
            'basic' : 1,
            'glass' : 1,
            'wood' : 2,
            'stone' : 2,
        }
        self.origin = origin # origin is the lowerleft most of tower
        # initializing tower
        if block_map is not None:
            self.block_map = BlockMap(self.game, origin, block_map)
        else:
            self.block_map = BlockMap(
                self.game,
                origin,
                {
                    (0,0) : 'stone',
                    (2,0) : 'stone',
                    (1,0) : 'stone',
                    (0,1) : 'wood',
                    (1,1) : 'wood',
                    (2,1) : 'wood',
                    (0,2) : 'glass',
                    (1,2) : 'glass',
                    (2,2) : 'glass',
                }
            )
        # initailize the player deck of cards
        self.deck = Deck(
            self.game,
            (
                self.game.display.get_width(),
                self.game.display.get_height()
            ),
            ['stone'],#, 'basic', 'stone', 'glass',],
            (
                origin[0] + ((self.block_map.tile_size[0] * 3 + 60) if self.identity == 0 else -92),
                origin[1] - 60
            ),
            'left' if self.identity==0 else 'right'
        )
            

    def render(self):
        '''
        Renders all the blocks, projectiles, cards ... 
        '''
        # always render block tower
        self.block_map.render(self.game.display)
        
        if self.game.player_turn == self.identity:

            if self.game.mode in ['card_unpack']:
                
                if self.deck.unpack():
                    self.game.mode = 'card_select'
                
                else:
                    self.deck.render(sway=False)
            
            if self.game.mode in ['card_select', 'play', 'in_air']:
                
                if self.deck.active == None:
                    self.game.scrolling = True
                
                else:
                    self.game.scrolling = False
                
                self.deck.play_deck()
