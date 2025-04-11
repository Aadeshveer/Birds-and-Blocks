import pygame
import math
import random
from .birds import Bird

BIRDS = (
    'red',
    'blue',
    'chuck',
    'bomb',
)

class Deck:
    '''
    Stores the cards and renders them
    '''
    def __init__(self, game, map_size, origin = (0, 0), cards = None, player='left'):
        self.cards = []
        self.game = game
        self.rect_list = []
        self.active = None
        self.origin = origin
        self.map_size = map_size
        if cards is not None:
            for card_type in cards:
                self.cards.append(Card(self.game, card_type, map_size, origin, player))
        for i,card in enumerate(self.cards):
            x = map_size[0] // len(self.cards) * i + (map_size[1] // len(self.cards) - card.img.get_width())
            y = 80
            self.rect_list.append(card.rect((x,y)))

    def play_deck(self):
        '''
        Displays the deck and manages the operations of cards
        '''
        if self.active == None:
            for i,rect in enumerate(self.rect_list):
                random.seed(i)
                self.game.display.blit(self.cards[i].img, (rect.left, rect.top + + (6+3*random.random())*math.sin(pygame.time.get_ticks()/200 + random.random())))
                if rect.collidepoint(self.game.scaled_mpos):
                    if pygame.mouse.get_pressed()[0]:
                        self.active = i

        else:
            if not self.cards[self.active].bird():
                self.cards.pop(self.active)
                self.rect_list = []
                self.active = None
                self.game.player_turn += 1
                self.game.player_turn %= 2
                for i,card in enumerate(self.cards):
                    x = self.map_size[0] // len(self.cards) * i + (self.map_size[1] // len(self.cards) - card.img.get_width())
                    y = 80
                    self.rect_list.append(card.rect((x,y)))
            

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

        