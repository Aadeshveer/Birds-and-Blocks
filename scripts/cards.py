import pygame
import math
import random
from .birds import Bird

CARD_WIDTH = 64
CARD_UPPER_BUFFER = 80

BIRDS = (
    'basic',
    'glass',
    'wood',
    'stone',
)

class Deck:
    '''
    Stores the cards and renders them
    '''
    def __init__(self, game, map_size, cards, origin = (0, 0), player='left'):
        self.game = game
        self.map_size = map_size
        self.origin = origin
        self.player = player
        self.active = None # index of card being run
        self.pack_ctr = 0 # Helps in smoother transaction for unpacking
        self.rect_list = [] # stores rects for all cards
        self.cards = [] # stores all the card objects
        
        for card_type in cards:
    
            self.cards.append(Card(self.game, card_type, map_size, origin, player))
        
        for card in self.cards:
        
            if player=='left':
                self.rect_list.append(card.rect((0,CARD_UPPER_BUFFER)))

            else:
                self.rect_list.append(card.rect((self.map_size[0] - CARD_WIDTH, CARD_UPPER_BUFFER)))

        # create a list of positions for cards
        self.find_pos()

        # by default smoothly transition cards from default to expected position
        self.unpack()

    def render(self, sway = True):
        '''
        Renders the cards and takes care of card selection
        '''
        for i,rect in enumerate(self.rect_list):
            random.seed(i)
            self.game.display.blit(self.cards[i].img, (rect.left, rect.top +((3+6*random.random())*math.sin(pygame.time.get_ticks()/200 + random.random()) if sway else 0)))
            if rect.collidepoint(self.game.scaled_mpos):
                if pygame.mouse.get_pressed()[0]:
                    self.active = i

    def find_pos(self):
        '''
        Based on number of Cards updates self.pos_list with desired positions of card sprites
        '''
        self.pos_list = []

        variation = (self.map_size[0] / 2 - CARD_WIDTH) // len(self.cards)
        
        for i in range(len(self.cards)):
        
            x = variation * i + 80
            x = (self.map_size[0] - x - CARD_WIDTH if self.player == 'right' else x)
        
            y = 80
        
            self.pos_list.append((x,y))

    def play_deck(self):
        '''
        Displays the deck and manages the operations of cards
        '''
        if self.active == None:
            self.render()

        else:

            if not self.cards[self.active].bird():
                # runs when a cards action finishes and resets everything for next player
                self.cards.pop(self.active)
                self.rect_list.pop(self.active)
                self.game.mode = 'card_unpack'
                self.active = None
                self.game.player_turn += 1
                self.game.player_turn %= 2
                self.find_pos()

    def unpack(self):
        '''
        Updates the position of cards for smooth unpacking
        '''
        for i,pos in enumerate(self.pos_list):

            self.rect_list[i].left = (14*self.rect_list[i].left + pos[0]) / 15
            self.rect_list[i].top = (14*self.rect_list[i].top + pos[1]) / 15
            self.pack_ctr += 1
        
        if self.pack_ctr >= 60:
            # reset pack_ctr
            self.pack_ctr = 0
            return True
        
        else:
            return False

        
            

class Card:
    def __init__(self, game, card_type, map_size, origin, player):
        '''
        Handles the various actions possible
        '''
        self.game = game
        self.type = card_type
        self.map_size = map_size
        self.origin = origin
        self.player = player
        self.img = self.game.assets['cards'][self.type]
        # if a bird calling card declares a bird projectile
        if self.type in BIRDS:
            self.projectile = Bird(self.game, self.map_size, self.type, self.origin, mode='ready', flip = self.player == 'right')

    def bird(self):
        '''
        Updates the bird
        Returns if bird is alive
        '''
        if pygame.mouse.get_pressed()[1]:
            self.projectile.mode = 'ready'
        
        if not self.projectile.update():
            return False
        
        self.projectile.render()

        return True

    def rect(self, pos):
        '''
        Returns a rect in which the card lies
        '''
        return pygame.rect.Rect(pos[0], pos[1], self.img.get_width(), self.img.get_height())

        