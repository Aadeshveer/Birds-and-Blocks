import pygame
import math

class Menu:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets
        
        # play button rect
        self.play_button = pygame.Rect(124*4,134*4,74*4,29*4)

    def update(self):
        # check for button press
        if self.play_button.collidepoint(self.game.mpos[0], self.game.mpos[1]):

            if pygame.mouse.get_pressed(num_buttons=5)[0]:
                self.assets['play_button'].set_frame(21)

            elif self.assets['play_button'].get_frame() == 21:
                self.game.mode='name_input'
        
            else:
                self.assets['play_button'].set_frame(11)
        else:
            self.assets['play_button'].set_frame(0)

    def render(self, surf):
        # blit the title
        surf.blit(
            pygame.transform.scale(
                self.assets['title'],
                (
                    surf.get_width(),
                    surf.get_height(),
                )
            ),
            (0, 10*math.sin(pygame.time.get_ticks() / 240))
        )

        # blit the play button
        surf.blit(
            pygame.transform.scale(
                self.assets['play_button'].img(),
                (
                    surf.get_width(),
                    surf.get_height(),
                )
            ),
            (0, 0)
        )




class NameInput:
    
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets
        self.name_rect1 = pygame.rect.Rect(10, self.game.window.get_height() - 56, 224, 42)
        self.name_rect2 = pygame.rect.Rect(self.game.window.get_width() - 234 , self.game.window.get_height() - 56, 224, 42)
        self.name1 = ''
        self.name2 = ''
        self.fonts = self.game.fonts
        self.player_turn = 0
        self.read = False


    def take_input(self, event):

        if self.read:
        
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    if self.player_turn == 0:
                        self.name1 = self.name1[:-1]
                    else:
                        self.name2 = self.name2[:-1]
            
                elif event.key == pygame.K_RETURN:

                    self.player_turn += 1
                    self.player_turn %= 2
                    
                    self.read = False

                    if self.get_name(self.player_turn) != '':
                        self.game.mode = 'card_unpack'
                
                else:
                    if self.player_turn == 0:
                        self.name1 += event.unicode.upper()
                    else:
                        self.name2 += event.unicode.upper()

    def update(self):

        if self.assets['player_name']['left'].get_frame() == 21:
            pass

        elif self.name_rect1.collidepoint(self.game.mpos[0], self.game.mpos[1]):

            if pygame.mouse.get_pressed()[0]:
                self.assets['player_name']['left'].set_frame(21)
                self.read = True

            else:
                self.assets['player_name']['left'].set_frame(11)

        else:
            self.assets['player_name']['left'].set_frame(0)

        if self.assets['player_name']['right'].get_frame() == 21:
            pass

        elif self.name_rect2.collidepoint(self.game.mpos[0], self.game.mpos[1]):

            if pygame.mouse.get_pressed()[0]:
                self.player_turn = 1
                self.assets['player_name']['right'].set_frame(21)
                self.read = True

            else:
                self.assets['player_name']['right'].set_frame(11)

        else:
            self.assets['player_name']['right'].set_frame(0)

    def render(self, surf):


        surf.blit(
            pygame.transform.scale(
                self.assets['player_name']['left'].img(),
                (
                    surf.get_width(),
                    surf.get_height(),
                )
            ),
            (0, 0)
        )
        surf.blit(
            pygame.transform.scale(
                self.assets['player_name']['right'].img(),
                (
                    surf.get_width(),
                    surf.get_height(),
                )
            ),
            (0, 0)
        )

        text1 = self.fonts['monospace'].render(self.name1[:17], False, 'black')
        surf.blit(
            text1,
            (
                self.name_rect1.left + 10,
                self.name_rect1.top + 10,
            )
        )
        text2 = self.fonts['monospace'].render(self.name2[:17], False, 'black')
        surf.blit(
            text2,
            (
                self.name_rect2.left + 10,
                self.name_rect2.top + 10,
            )
        )

    def get_name(self,id):
        if id == 0:
            return self.name1
        else:
            return self.name2