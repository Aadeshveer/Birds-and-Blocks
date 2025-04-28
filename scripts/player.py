from .blockmap import BlockMap
from .cards import Deck
import pygame

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
            'wood' : 1,
            'stone' : 1,
        }
        self.origin = origin # origin is the lowerleft most of tower
        # initializing tower
        if block_map is not None:
            self.block_map = BlockMap(self.game, origin, block_map)
        else:
            self.block_map = BlockMap(
                self.game,
                origin,
                # {
                #     (0,0) : 'stone',
                #     (2,0) : 'stone',
                #     (1,0) : 'stone',
                #     (0,1) : 'wood',
                #     (1,1) : 'wood',
                #     (2,1) : 'wood',
                #     (0,2) : 'glass',
                #     (1,2) : 'glass',
                #     (2,2) : 'glass',
                #     # (0,3) : 'stone',
                #     # (2,3) : 'stone',
                #     # (1,3) : 'stone',
                #     # (0,4) : 'wood',
                #     # (1,4) : 'wood',
                #     # (2,4) : 'wood',
                #     # (0,5) : 'glass',
                #     # (1,5) : 'glass',
                #     # (2,5) : 'glass',
                # }
            )
        # initailize the player deck of cards
        self.deck = Deck(
            self.game,
            (
                self.game.display.get_width(),
                self.game.display.get_height()
            ),
            ['glass', 'basic', 'stone', 'wood',],
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

            if self.game.mode in ['card_select']:

                if self.deck.active == None:
                    self.game.scrolling = True

                else:
                    self.game.scrolling = False

                self.deck.play_deck()

    def render_upgrade_indicators(self, surf):
        '''
        Manges the rendering of bottom upgrade level indicators
        '''
        origin1 = (125*2, 333*2)
        origin2 = (490*2, 333*2)
        for i,type in enumerate(['basic','glass', 'wood', 'stone']):
            surf.blit(
                self.game.assets['projectile' + ('_flipped' if self.identity==1 else '')][type]['upgrade'],
                (origin1[0] + i * (48 + 20), origin1[1]) if self.identity == 0 else (origin2[0] - i * (48 + 20), origin2[1])
            )
            text = pygame.font.Font('assets/fonts/custom_font.ttf',size=20).render(str(self.upgrades[type]), False, "#00ff00")
            surf.blit(
                text,
                (origin1[0] + i * (48 + 20) + 15, origin1[1] + 24) if self.identity == 0 else (origin2[0] - i * (48 + 20) + 25, origin2[1] + 24)
            )