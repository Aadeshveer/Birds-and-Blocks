import pygame
import math

class Menu:
    def __init__(self, game, assets):
        self.game = game
        self.assets = {
            'play_button' : assets['play_button'].copy(),
            'tutorial_button' : assets['tutorial_button'].copy(),
            'credits_button' : assets['credits_button'].copy(),
            'title' : assets['title'],
        }

        # play button rect
        self.play_button = pygame.Rect(124*4,134*4,74*4,29*4)
        self.tutorial_button = pygame.Rect(223*4,149*4,76*4,16*4)
        self.credits_button = pygame.Rect(24*4,149*4,76*4,16*4)

        self.play_clicked = False
        self.tutorials_clicked = False
        self.credits_clicked = False

    def update(self):
        # check for button press
        if self.play_button.collidepoint(self.game.mpos[0], self.game.mpos[1]):

            if pygame.mouse.get_pressed()[0]:
                self.assets['play_button'].set_frame(21)
                if not self.play_clicked:
                    self.game.audio['button'].play()
                    self.play_clicked = True

            elif self.assets['play_button'].get_frame() == 21:
                self.game.mode='name_input'

            else:
                self.assets['play_button'].set_frame(11)

        else:
            self.assets['play_button'].set_frame(0)

        if self.tutorial_button.collidepoint(self.game.mpos[0], self.game.mpos[1]):

            if pygame.mouse.get_pressed()[0]:
                self.assets['tutorial_button'].set_frame(21)
                if not self.tutorials_clicked:
                    self.game.audio['button'].play()
                    self.tutorials_clicked = True


            elif self.assets['tutorial_button'].get_frame() == 21:
                self.game.tutorial=True

            else:
                self.assets['tutorial_button'].set_frame(11)

        else:
            self.assets['tutorial_button'].set_frame(0)

        if self.credits_button.collidepoint(self.game.mpos[0], self.game.mpos[1]):

            if pygame.mouse.get_pressed()[0]:
                self.assets['credits_button'].set_frame(21)
                if not self.credits_clicked:
                    self.game.audio['button'].play()
                    self.credits_clicked = True



            elif self.assets['credits_button'].get_frame() == 21:
                self.game.mode = 'game_over'
                self.game.credits = True

            else:
                self.assets['credits_button'].set_frame(11)

        else:
            self.assets['credits_button'].set_frame(0)

    def render(self, surf):
        # blit the title
        surf.blit(
            self.assets['title'],
            (0, 10*math.sin(pygame.time.get_ticks() / 240))
        )

        # blit the play button
        surf.blit(
            self.assets['play_button'].img(),
            (0, 0)
        )

        # blit the tut button
        surf.blit(
            self.assets['tutorial_button'].img(),
            (0, 0)
        )

        # blit the credits button
        surf.blit(
            self.assets['credits_button'].img(),
            (0, 0)
        )




class NameInput:

    def __init__(self, game, assets):
        self.game = game
        self.assets = {
            'player_name' : {
                'left' :  assets['player_name']['left'].copy(),
                'right' :  assets['player_name']['right'].copy(),
            },
        }
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

                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_TAB]:
                    if self.player_turn == 0:
                        self.game.rating_handler.add_playing(self.name1)
                    else:
                        self.game.rating_handler.add_playing(self.name2)
                    self.assets['player_name']['left' if self.player_turn == 0 else 'right'].set_frame(30)
                    self.player_turn += 1
                    self.player_turn %= 2

                    self.read = (event.key == pygame.K_TAB)

                    if self.get_name(self.player_turn) != '':
                        self.game.mode = 'card_unpack'
                        self.read = False
                    
                    if self.read:
                        self.assets['player_name']['left' if self.player_turn == 0 else 'right'].set_frame(20)


                else:
                    if self.player_turn == 0:
                        self.name1 += event.unicode.upper()
                    else:
                        self.name2 += event.unicode.upper()

    def update(self):

        if not self.read:

            if self.assets['player_name']['left'].get_frame() in [20,30]:
                pass

            elif self.name_rect1.collidepoint(self.game.mpos[0], self.game.mpos[1]):

                if pygame.mouse.get_pressed()[0]:
                    self.assets['player_name']['left'].set_frame(20)
                    self.game.audio['button'].play()
                    self.read = True

                else:
                    self.assets['player_name']['left'].set_frame(10)

            else:
                self.assets['player_name']['left'].set_frame(0)

            if self.assets['player_name']['right'].get_frame() in [20,30]:
                pass

            elif self.name_rect2.collidepoint(self.game.mpos[0], self.game.mpos[1]):

                if pygame.mouse.get_pressed()[0]:
                    self.player_turn = 1
                    self.assets['player_name']['right'].set_frame(20)
                    self.game.audio['button'].play()
                    self.read = True

                else:
                    self.assets['player_name']['right'].set_frame(10)

            else:
                self.assets['player_name']['right'].set_frame(0)

    def render(self, surf):


        surf.blit(
            self.assets['player_name']['left'].img(),
            (0, 0)
        )
        surf.blit(
            self.assets['player_name']['right'].img(),
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

        
class GameOver:

    def __init__(self, game, assets):

        self.game = game
        self.assets = {
            'game_over' : assets['game_over'],
            'player_box' : assets['player_box'],
            'menu_button' : assets['menu_button'].copy(),
            'credits' : assets['credits'].copy(),
        }

        # play button rect
        self.menu_button = pygame.Rect(124*4,134*4,74*4,29*4)
        self.winner_name = pygame.Rect(45*4,92*4,150*4,15*4)
        self.loser_name = pygame.Rect(45*4,111*4,150*4,15*4)
        self.winner_rating = pygame.Rect(198*4,92*4,77*4,15*4)
        self.loser_rating = pygame.Rect(198*4,111*4,77*4,15*4)
        
    def finish_game(self):
        self.rating_win, self.rating_lose, self.delta_win, self.delta_lose = self.game.rating_handler.update_rating(self.game.winner,self.game.loser)

    def update(self):
        # check for button press
        if self.menu_button.collidepoint(self.game.mpos[0], self.game.mpos[1]):

            if pygame.mouse.get_pressed()[0]:
                if self.game.credits:
                    self.assets['credits'].set_frame(21)
                else:
                    self.assets['menu_button'].set_frame(21)

            elif self.assets['menu_button'].get_frame() == 21 or self.assets['credits'].get_frame() == 21:
                self.game.audio['button'].play()
                self.game.mode='menu'
                self.game.reset()

            else:
                if self.game.credits:
                    self.assets['credits'].set_frame(11)
                else:
                    self.assets['menu_button'].set_frame(11)

        else:
            if self.game.credits:
                self.assets['credits'].set_frame(0)
            else:
                self.assets['menu_button'].set_frame(0)

    def render(self, surf):
        if self.game.credits:
            surf.blit(
                self.assets['credits'].img(),
                (0,0)
            )
        else:
            # blit game over
            surf.blit(
                self.assets['game_over'],
                (0, 8*math.sin(pygame.time.get_ticks() / 240))
            )

            # blit the winner box
            surf.blit(
                self.assets['player_box'],
                (0, 0)
            )

            # blit the menu button
            surf.blit(
                self.assets['menu_button'].img(),
                (0, 0)
            )
            winner_name_text = pygame.font.Font('assets/fonts/custom_font.ttf',size=60).render(self.game.winner, False, 'black')
            surf.blit(
                winner_name_text,
                (
                    self.winner_name.left + 20 + (self.winner_name.width - winner_name_text.get_width()) / 2,
                    self.winner_name.top + 5,
                )
            )
            loser_name_text = pygame.font.Font('assets/fonts/custom_font.ttf',size=60).render(self.game.loser, False, 'black')
            surf.blit(
                loser_name_text,
                (
                    self.loser_name.left + 20 + (self.loser_name.width - loser_name_text.get_width()) / 2,
                    self.loser_name.top + 5,
                )
            )
            winner_rating_text = pygame.font.Font('assets/fonts/custom_font.ttf',size=20).render(f"{self.rating_win} (+{self.delta_win})", False, 'black')
            surf.blit(
                winner_rating_text,
                (
                    self.winner_rating.left + 10 + (self.winner_rating.width - winner_rating_text.get_width()) / 2,
                    self.winner_rating.top + 20,
                )
            )
            loser_rating_text = pygame.font.Font('assets/fonts/custom_font.ttf',size=20).render(f"{self.rating_lose} ({self.delta_lose})", False, 'black')
            surf.blit(
                loser_rating_text,
                (
                    self.loser_rating.left + 10 + (self.loser_rating.width - loser_rating_text.get_width()) / 2,
                    self.loser_rating.top + 20,
                )
            )

class Tutorial:
    def __init__(self, game, assets):
        self.game = game
        self.anim = assets['tutorial'].copy()
        self.selection = False
        self.upgradation = True
        self.cong_ctr = 0
        self.final_ctr = 0

    def update(self):
        match self.game.mode:
            case 'menu':
                self.frame = 0

            case 'name_input':
                self.frame = 10

            case 'card_unpack':
                self.frame = 50

            case 'card_select':
                deck = self.game.get_player_by_id().deck
                if deck.active != None and not self.selection:
                    match deck.cards[deck.active].projectile.mode:
                        case 'ready':
                            self.frame = 30 if self.upgradation else 80
                        case 'aiming':
                            self.frame = 40 if self.upgradation else 80
                        case 'in_air':
                            self.frame = 50
                            self.selection = True
                elif self.selection:
                    self.cong_ctr += 1
                    self.frame = 50
                else:
                    self.frame = 20

            case 'upgrade_unpack':
                self.frame = 70

            case 'upgrade':
                deck = self.game.get_player_by_id().deck
                if self.upgradation:
                    self.upgradation = False
                    self.selection = False
                    self.frame = 70
                elif self.frame == 70:
                    pass
                else:
                    self.frame = 50

            case 'game_over':
                self.frame = 90

        if 0 < self.cong_ctr < 120:
            self.frame = 60
            self.cong_ctr += 1

        self.anim.set_frame(self.frame)

    def render(self,surf):
        surf.blit(
            self.anim.img(),
            (0, 0),
        )