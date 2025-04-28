import pygame
import math

class Button:
    '''
    Maintains button operations
    '''
    def __init__(self, game, asset, pos, size, function, frame_offset = 0):
        self.game = game
        self.asset = asset
        self.function = function
        self.frame_offset = frame_offset
        self.rect = pygame.Rect(*pos, *size)
        self.clicked = False


    def update(self):
        '''
        Updates the frame animation of button
        '''
        if self.rect.collidepoint(self.game.mpos[0], self.game.mpos[1]):

            if pygame.mouse.get_pressed()[0]:
                # button is pressed down
                self.asset.set_frame(self.frame_offset + 21)
                if not self.clicked:
                    if not self.game.mute:
                        self.game.audio['button'].play()
                        self.clicked = True

            elif self.asset.get_frame() == self.frame_offset + 21:
                # button is released calling its function
                self.asset.set_frame(self.frame_offset + 11)
                self.clicked = False
                self.function()

            else:
                # button is highlighted
                self.asset.set_frame(self.frame_offset + 11)

        else:
            # button in default state
            self.asset.set_frame(self.frame_offset)

    def render(self, surf):
        '''
        Renders the button on screen
        '''
        surf.blit(
            self.asset.img(),
            (0, 0)
        )
    
    def change_offset(self, offset):
        '''
        Change the button animation offset specifically for more than 3 frame button animations
        '''
        self.frame_offset = offset

class UtilitiesButtons:
    '''
    Handles the three top row buttons
    '''
    def __init__(self, game, assets):
        self.game = game
        self.mute = Button(self.game, assets['mute_button'].copy(), (35*4, 13*4), (16*4,16*4), self.switch_audio, 0)
        self.back = Button(self.game, assets['back_button'].copy(), (13*4, 13*4), (16*4,16*4), self.restart)
        self.leaderboard = Button(self.game, assets['leaderboard'].copy(), (self.game.SIZE[0]-13*4 - 16*4, 13*4), (16*4,16*4), self.leader_board)

    def switch_audio(self):
        '''
        Function called by mute button
        '''
        self.game.mute = not self.game.mute
        self.game.playing = False
        self.mute.change_offset(30 if self.game.mute else 0)
    def restart(self):
        '''
        Function called by back to menu button
        '''
        self.game.mode='menu'
        self.game.reset()
    def leader_board(self):
        '''
        Function called by leaderboard button
        '''
        self.game.leaderboard = True
        self.game.mode='game_over'

    def update(self):
        '''
        Updates the buttons
        '''
        self.mute.update()
        self.back.update()
        if self.game.mode in ['menu']:
            self.leaderboard.update()

    def render(self, surf):
        '''
        Renders the button animation
        '''
        self.mute.render(surf)
        self.back.render(surf)
        if self.game.mode in ['menu']:
            self.leaderboard.render(surf)

class Menu:
    '''
    Class to maintain the main game menu
    '''
    def __init__(self, game, assets):
        self.game = game
        self.assets = {
            'play_button' : assets['play_button'].copy(),
            'tutorial_button' : assets['tutorial_button'].copy(),
            'credits_button' : assets['credits_button'].copy(),
            'title' : assets['title'],
        }

        self.play_button = Button(self.game, self.assets['play_button'], (124*4, 134*4), (74*4, 29*4), self.change_mode_to_input)
        self.tutorial_button = Button(self.game, self.assets['tutorial_button'], (223*4,149*4), (76*4,16*4), self.activate_tutorial)
        self.credits_button = Button(self.game, self.assets['credits_button'], (24*4, 149*4), (76*4, 16*4), self.activate_credits)

    def change_mode_to_input(self):
        '''
        Function called by play button
        '''
        self.game.mode='name_input'
    def activate_tutorial(self):
        '''
        Function called by tutorial button
        '''
        self.game.tutorial=True
    def activate_credits(self):
        '''
        Function called by creditss button
        '''
        self.game.mode = 'game_over'
        self.game.credits = True

    def update(self):
        '''
        Updates the menu buttons
        '''
        # check for button press
        self.play_button.update()

        self.tutorial_button.update()

        self.credits_button.update()

    def render(self, surf):
        '''
        Renders the menu buttons
        '''
        # blit the title
        surf.blit(
            self.assets['title'],
            (0, 10*math.sin(pygame.time.get_ticks() / 240))
        )

        # blit the play button
        self.play_button.render(surf)

        # blit the tut button
        self.tutorial_button.render(surf)

        # blit the credits button
        self.credits_button.render(surf)




class NameInput:
    '''
    Class that handles player name input
    '''
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
        '''
        Takes name input from key down event
        '''
        if self.read:

            if event.type == pygame.KEYDOWN:

                # truncate name
                if event.key == pygame.K_BACKSPACE:
                    if self.player_turn == 0:
                        self.name1 = self.name1[:-1]
                    else:
                        self.name2 = self.name2[:-1]

                # freeze the name
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_TAB]:
                    if self.get_name(self.player_turn) != '':
                        # add rating if not already exists
                        if self.player_turn == 0:
                            self.game.rating_handler.add_playing(self.name1)
                        else:
                            self.game.rating_handler.add_playing(self.name2)
                        
                        self.assets['player_name']['left' if self.player_turn == 0 else 'right'].set_frame(30)
                        
                        self.player_turn += 1
                        self.player_turn %= 2

                        # continue reading in case of tab
                        self.read = (event.key == pygame.K_TAB)

                        # if name is other player name is not an empty string go to card unpacking
                        if self.get_name(self.player_turn) != '':
                            self.game.mode = 'card_unpack'
                            self.read = False
                        
                        if self.read:
                            self.assets['player_name']['left' if self.player_turn == 0 else 'right'].set_frame(20)


                # update name
                else:
                    if self.player_turn == 0:
                        self.name1 += event.unicode.upper()
                    else:
                        self.name2 += event.unicode.upper()

    def update(self):
        '''
        Update the name button animation
        '''
        if not self.read:

            if self.assets['player_name']['left'].get_frame() in [20,30]:
                pass

            elif self.name_rect1.collidepoint(self.game.mpos[0], self.game.mpos[1]):

                if pygame.mouse.get_pressed()[0]:
                    self.assets['player_name']['left'].set_frame(20)
                    if not self.game.mute:
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
                    if not self.game.mute:
                        self.game.audio['button'].play()
                    self.read = True

                else:
                    self.assets['player_name']['right'].set_frame(10)

            else:
                self.assets['player_name']['right'].set_frame(0)

    def render(self, surf):
        '''
        Renders the update button
        '''
        surf.blit(
            self.assets['player_name']['left'].img(),
            (0, 0)
        )
        surf.blit(
            self.assets['player_name']['right'].img(),
            (0, 0)
        )

        # renders the player name and rating
        text1 = self.fonts['monospace'].render(self.name1[:12]+self.game.rating_handler.get_rating_str(self.name1), False, 'black')
        surf.blit(
            text1,
            (
                self.name_rect1.left + 10,
                self.name_rect1.top + 10,
            )
        )
        text2 = self.fonts['monospace'].render(self.name2[:12]+self.game.rating_handler.get_rating_str(self.name2), False, 'black')
        surf.blit(
            text2,
            (
                self.name_rect2.left + 10,
                self.name_rect2.top + 10,
            )
        )

    def get_name(self,id):
        '''
        Returns the name of player from id
        '''
        if id == 0:
            return self.name1
        else:
            return self.name2

        
class GameOver:
    '''
    Handles the game over animation, also used in credits and leaderboard as menu button only class
    '''
    def __init__(self, game, assets):

        self.game = game
        self.assets = {
            'game_over' : assets['game_over'],
            'player_box' : assets['player_box'],
            'menu_button' : assets['menu_button'].copy(),
            'credits' : assets['credits'].copy(),
            'leaderboard' : assets['leaderboard'].copy(),
            'pygame' : assets['pygame'],
        }

        # play button rect
        self.menu_button = pygame.Rect(124*4,134*4,74*4,29*4)
        self.winner_name = pygame.Rect(45*4,92*4,150*4,15*4)
        self.loser_name = pygame.Rect(45*4,111*4,150*4,15*4)
        self.winner_rating = pygame.Rect(198*4,92*4,77*4,15*4)
        self.loser_rating = pygame.Rect(198*4,111*4,77*4,15*4)
        
    def finish_game(self):
        '''
        Updates ratings  when game is finished
        '''
        self.rating_win, self.rating_lose, self.delta_win, self.delta_lose = self.game.rating_handler.update_rating(self.game.winner,self.game.loser)

    def update(self):
        '''
        Update the game over window
        '''
        # check for button press
        if self.menu_button.collidepoint(self.game.mpos[0], self.game.mpos[1]):

            if pygame.mouse.get_pressed()[0]:
                if self.game.credits:
                    self.assets['credits'].set_frame(21)
                elif self.game.leaderboard:
                    self.assets['leaderboard'].set_frame(21)
                else:
                    self.assets['menu_button'].set_frame(21)

            elif self.assets['menu_button'].get_frame() == 21 or self.assets['credits'].get_frame() == 21 or self.assets['leaderboard'].get_frame() == 21:
                if not self.game.mute:
                    self.game.audio['button'].play()
                self.game.mode='menu'
                self.game.reset()

            else:
                if self.game.credits:
                    self.assets['credits'].set_frame(11)
                elif self.game.leaderboard:
                    self.assets['leaderboard'].set_frame(11)
                else:
                    self.assets['menu_button'].set_frame(11)

        else:
            if self.game.credits:
                self.assets['credits'].set_frame(0)
            elif self.game.leaderboard:
                self.assets['leaderboard'].set_frame(0)
            else:
                self.assets['menu_button'].set_frame(0)

    def render(self, surf):
        '''
        Renders the game over window
        '''
        if self.game.credits:
            surf.blit(
                self.assets['credits'].img(),
                (0,0)
            )

            surf.blit(
                self.assets['pygame'],
                (40,500)
            )

        elif self.game.leaderboard:
            surf.blit(
                self.assets['leaderboard'].img(),
                (0,0)
            )
            ratings = self.game.rating_handler.get_leaderboard(9,40)
            surf.blit(
                ratings,
                ((surf.width-ratings.width)/2,(surf.height-ratings.height)/2 - 40)
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
            winner_name_text = self.game.get_font(60).render(self.game.winner, False, 'black')
            surf.blit(
                winner_name_text,
                (
                    self.winner_name.left + 20 + (self.winner_name.width - winner_name_text.get_width()) / 2,
                    self.winner_name.top + 5,
                )
            )
            loser_name_text = self.game.get_font(60).render(self.game.loser, False, 'black')
            surf.blit(
                loser_name_text,
                (
                    self.loser_name.left + 20 + (self.loser_name.width - loser_name_text.get_width()) / 2,
                    self.loser_name.top + 5,
                )
            )
            winner_rating_text = self.game.get_font(38).render(f"{self.rating_win} (+{self.delta_win})", False, 'black')
            surf.blit(
                winner_rating_text,
                (
                    self.winner_rating.left + 10 + (self.winner_rating.width - winner_rating_text.get_width()) / 2,
                    self.winner_rating.top + 20,
                )
            )
            loser_rating_text = self.game.get_font(38).render(f"{self.rating_lose} ({self.delta_lose})", False, 'black')
            surf.blit(
                loser_rating_text,
                (
                    self.loser_rating.left + 10 + (self.loser_rating.width - loser_rating_text.get_width()) / 2,
                    self.loser_rating.top + 20,
                )
            )

class Tutorial:
    '''
    Hadles the tutorial help in game
    '''
    def __init__(self, game, assets):
        self.game = game
        self.anim = assets['tutorial'].copy()
        self.selection = False
        self.upgradation = True
        self.start_ctr = 0
        self.cong_ctr = 0
        self.final_ctr = 0
        self.frame = 0
        self.new = True

    def update(self):
        '''
        Updates the tutorial mask frame
        '''
        if self.frame == 100:
            if pygame.mouse.get_pressed()[0] and self.start_ctr < 1000:
                self.new = False
            if self.start_ctr < 60:
                self.start_ctr += 1

        match self.game.mode:
            case 'menu':
                self.frame = 0

            case 'name_input':
                if self.new:
                    self.frame=100
                else:
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
                    self.frame = 20 if self.game.player_turn == 0 else 110

            case 'upgrade_unpack':
                self.frame = 70

            case 'upgrade':
                # reactivates selection for mask no 8 to be viewed next time
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
        '''
        Renders the mask on surface
        '''
        surf.blit(
            self.anim.img(),
            (0, 0),
        )