import pygame
import math
import random
from .birds import Bird

CARD_WIDTH = 64

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
    def __init__(self, game, map_size, origin = (0, 0), cards = None, player='left'):
        self.cards = []
        self.game = game
        self.active = None
        self.origin = origin
        self.map_size = map_size
        self.rect_list = []
        self.pack_ctr = 0
        self.player = player
        if cards is not None:
            for card_type in cards:
                self.cards.append(Card(self.game, card_type, map_size, origin, player))
        for card in self.cards:
            if player=='left':
                self.rect_list.append(card.rect((0,80)))
            else:
                self.rect_list.append(card.rect((self.map_size[0] - CARD_WIDTH,80)))
        self.find_pos()
        self.unpack()

    def render(self, sway = True):
        for i,rect in enumerate(self.rect_list):
            random.seed(i)
            self.game.display.blit(self.cards[i].img, (rect.left, rect.top +((6+3*random.random())*math.sin(pygame.time.get_ticks()/200 + random.random()) if sway else 0)))
            if rect.collidepoint(self.game.scaled_mpos):
                if pygame.mouse.get_pressed()[0]:
                    self.active = i

    def find_pos(self):
        self.pos_list = []
        for i,card in enumerate(self.cards):
            x = self.map_size[0] / (2 * len(self.cards))* i + (self.map_size[0] / (2 * len(self.cards)) - card.img.get_width())
            x = (self.map_size[0]-x if self.player == 'right' else x)
            y = 80
            print((x,y))
            self.pos_list.append((x,y))

    def play_deck(self):
        '''
        Displays the deck and manages the operations of cards
        '''
        if self.active == None:
            self.render()

        else:
            if not self.cards[self.active].bird():
                self.game.mode = 'card_unpack'
                self.cards.pop(self.active)
                self.rect_list.pop(self.active)
                self.active = None
                self.game.player_turn += 1
                self.game.player_turn %= 2
                self.find_pos()

    def unpack(self):
        for i,pos in enumerate(self.pos_list):
            self.rect_list[i].left = (14*self.rect_list[i].left + pos[0]) / 15
            self.rect_list[i].top = (14*self.rect_list[i].top + pos[1]) / 15
            self.pack_ctr += 1
        if self.pack_ctr >= 60:
            self.pack_ctr = 0
            return True
        else:
            return False

        
            

class Card:
    def __init__(self, game, card_type, map_size, origin, player):
        self.type = card_type
        self.player = player
        self.map_size = map_size
        self.origin = origin
        self.game = game
        self.img = self.game.assets['cards'][self.type]
        if self.type in BIRDS:
            self.projectile = Bird(self.game, self.map_size, self.type, self.origin, mode='ready', flip = self.player == 'right')

    def bird(self):
        '''
        Returns if bird is alive
        '''
        if pygame.mouse.get_pressed()[1]:
            self.projectile.mode = 'ready'
        if not self.projectile.update():
            return False
        self.projectile.render()
        return True

    def rect(self, pos):
        return pygame.rect.Rect(pos[0], pos[1], self.img.get_width(), self.img.get_height())

        