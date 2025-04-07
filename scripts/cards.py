import pygame
import math
import random
from .birds import Bird
from .utils import load_image,load_images

class Deck:
    def __init__(self, map_size, origin = (0, 0), cards = None, player='left'):
        self.cards = []
        self.rect_list = []
        self.ctr = 0
        self.active = None
        self.origin = origin
        self.map_size = map_size
        if cards is not None:
            for card_type in cards:
                self.cards.append(Card(card_type, map_size, origin, player))
        for i,card in enumerate(self.cards):
            x = map_size[0] // len(self.cards) * i + (map_size[1] // len(self.cards) - card.img.get_width())
            y = 40
            self.rect_list.append(card.rect((x,y)))

    def play_deck(self, surf, mpos, offset, scaling_factor):
        self.ctr+=1
        if self.active == None:
            for i,rect in enumerate(self.rect_list):
                random.seed(i)
                surf.blit(self.cards[i].img, rect.topleft)
                if rect.collidepoint(mpos):
                    if pygame.mouse.get_pressed()[0]:
                        self.active = i
                else:
                    rect.top += 2*math.sin(self.ctr/10 + random.random())
        else:
            try:
                return self.cards[self.active].bird(surf, mpos, offset, scaling_factor)
            except Exception as e:
                self.cards.pop(self.active)
                self.rect_list = []
                self.active = None
                for i,card in enumerate(self.cards):
                    x = self.map_size[0] // len(self.cards) * i + (self.map_size[1] // len(self.cards) - card.img.get_width())
                    y = 40
                    self.rect_list.append(card.rect((x,y)))
                return  (offset, scaling_factor)
            

class Card:
    def __init__(self, card_type, map_size, origin, player):
        self.type = card_type
        self.player = player
        self.map_size = map_size
        self.origin = origin
        self.img = load_image('cards/' + self.type + '/' + self.type + '.png')
        self.projectile = Bird(self.map_size, self.origin, mode='ready', flip=True if self.player == 'right' else False)

    def bird(self, surf, mpos, offset, scaling_factor):
        print(self.projectile.origin)
        if pygame.mouse.get_pressed()[1]:
            self.projectile.mode = 'ready'
        self.projectile.update(mpos)
        return self.projectile.render(surf, scaling_factor, offset)

    def rect(self, pos):
        return pygame.rect.Rect(pos[0], pos[1], self.img.get_width(), self.img.get_height())

        