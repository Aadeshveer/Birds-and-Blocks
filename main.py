import pygame as pygame
import random
import sys

from scripts.modes import Menu, NameInput, GameOver, Tutorial, UtilitiesButtons
from scripts.player import Player
from scripts.cards import Deck
from scripts.utils import load_image, load_images, Animation, load_sound
from scripts.particles import Particles
from scripts.rating import ELO
from scripts.loader import assets_loader

SIZE = (1280,720)
PLAY_MODES = ['card_unpack', 'card_select', 'upgrade_unpack', 'upgrade']

class game():

    def __init__(self):

        pygame.init()

        pygame.font.init()

        pygame.mixer.init()

        pygame.display.set_caption('Birds and Blocks')

        self.SIZE = SIZE

        # window will be the main window to be displayed on screen
        self.window = pygame.display.set_mode(SIZE)

        pygame.mixer.music.load('./assets/audio/game_loop.wav')
        pygame.mixer.music.play(-1)
        self.playing = True

        # loads all the assets at once to prevent lag
        assets_loader(self)

        pygame.display.set_icon(self.assets['UI']['icon'])

        # all the sprites will be blit on display and rescaled to fit window giving a zoom effect
        self.display = pygame.Surface((1280,720))

        # mode dictates what is happening in game
        self.mode = 'menu'

        self.mute = False

        # initializing clock to maintain fps
        self.clock = pygame.time.Clock()

        # manages all the simple particles for effects
        self.particles = Particles(self.window.get_size(),{
            'basic_feather' : self.assets['projectile']['basic']['feather'],
            'wood_feather' : self.assets['projectile']['wood']['feather'],
            'stone_feather' : self.assets['projectile']['stone']['feather'],
            'glass_feather' : self.assets['projectile']['glass']['feather'],
            'basic_feather_flipped' : self.assets['projectile_flipped']['basic']['feather'],
            'wood_feather_flipped' : self.assets['projectile_flipped']['wood']['feather'],
            'stone_feather_flipped' : self.assets['projectile_flipped']['stone']['feather'],
            'glass_feather_flipped' : self.assets['projectile_flipped']['glass']['feather'],
            'shards_glass' : self.assets['shards']['glass'],
            'shards_wood' : self.assets['shards']['wood'],
            'shards_stone' : self.assets['shards']['stone'],
            'dust' : self.assets['effects']['dust'],
            'particle' : self.assets['effects']['particle'],
        })

        self.clouds = Particles(self.window.get_size(),{
            'clouds' : self.assets['clouds']
        })

        # manages the three square buttons in top corners
        self.util_buttons = UtilitiesButtons(
            self,
            self.assets['UI']['util_buttons']
        )

        # resets parts of game required for new game
        self.reset()

    def reset(self):
        '''
        resets the game
        '''

        self.upgrade_cards = Deck(
            self,
            (
                self.display.get_width(),
                self.display.get_height(),
            ),
            ['upgrade_wood', 'upgrade_basic', 'upgrade_stone', 'upgrade_glass'],
            (0,0),
            'dealer',
        )

        self.tutorial = False

        self.leaderboard = False

        self.credits = False

        self.menu = Menu(self, self.assets['UI'])

        self.winner = 'None'
        self.loser = 'None'

        self.rating_handler = ELO(self,'./user_data/players.txt','./user_data/ratings.txt')

        self.name_handler = NameInput(self, self.assets['UI'])

        self.game_over = GameOver(self, self.assets['UI'])

        self.tut = Tutorial(self, self.assets['UI'])

        self.particles.reset()

        self.clouds.reset()

        # scales the display to window for zoom effect
        self.scaling_factor = 1

        # moves the window for scroll effet
        self.off_set = [self.window.get_width() / 4, self.window.get_height() / 4]

        # allow user scrolling
        self.scrolling = True

        # player objects control moves of player
        self.player1 = Player(self, 0, (self.display.get_width() // 32,630))
        self.player2 = Player(self, 1, (self.display.get_width() - 3 * 64 - self.display.get_width() // 32,630))

        # keeps track of which player's turn it is
        self.player_turn = 0

        # maintain a single mpos variable that will be passed to other functions
        self.mpos = (0, 0)

        for _ in range(15):
            self.clouds.add_particles('clouds', (-160 + random.random() * self.window.get_width(), self.window.get_width() * random.random() * 0.6), ['cloud','sequence'],1)

    def run(self):

        while True:

            # filling skyblue in background
            self.display.fill('#87CEEB')

# [Taking input] --------------------------------------------------------------------------------- #

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # window resize can cause errors in scaling
                if event.type == pygame.VIDEORESIZE:
                    raise Exception('Window resize error')

                if self.mode == 'name_input':
                    self.name_handler.take_input(event)

            # maintain one variable to store mpos preventing lag due to multiple calling in other functions
            self.mpos = pygame.mouse.get_pos()
            self.scaled_mpos = (
                (self.mpos[0] - self.off_set[0]) * self.scaling_factor / 2,
                (self.mpos[1] - self.off_set[1]) * self.scaling_factor / 2
            )

            # scrolls the screen
            if self.mode in ['card_unpack', 'card_select', 'menu', 'upgrade_unpack', 'upgrade', 'name_input', 'game_over']:

                # value by which offset will move
                delta = 0

                # go left
                if self.mpos[0] < self.window.get_width()/4:
                    delta = - (self.mpos[0] - self.window.get_width() / 4)/30
                # go right
                if self.mpos[0] > 3*self.window.get_width()/4:
                    delta = - (self.mpos[0] - 3 * self.window.get_width() / 4)/30
                # makes sure x offset does not go out of bounds
                self.off_set[0] = max(
                    min(
                        self.off_set[0] + delta,
                        0
                    ),
                    self.window.get_width() - 2 * self.window.get_width() / self.scaling_factor
                )

                delta = 0
                
                # go up
                if self.mpos[1] < self.window.get_height()/4:
                    delta = - (self.mpos[1] - self.window.get_height() / 4)/30
                # go down
                if self.mpos[1] > 3*self.window.get_height()/4:
                    delta = - (self.mpos[1] - 3 * self.window.get_height() / 4)/30
                # makes sure y offset does not go out of bounds
                self.off_set[1] = max(
                    min(
                        self.off_set[1] + delta,
                        0
                    ),
                    self.window.get_height() - 2 * self.window.get_height() / self.scaling_factor
                )

            if self.mode in PLAY_MODES:
                # a scale of 2 is best to view complete map
                self.change_scaling(2, 14)

# [Updating and rendering the screen] -------------------------------------------------------------------------- #

            # game over condition
            if self.mode != 'game_over':

                if len(self.player1.block_map.block_map) == 0:

                    self.winner = self.name_handler.get_name(1)
                    self.loser = self.name_handler.get_name(0)
                    self.game_over.finish_game()
                    self.mode = 'game_over'

                elif len(self.player2.block_map.block_map) == 0:

                    self.winner = self.name_handler.get_name(0)
                    self.loser = self.name_handler.get_name(1)
                    self.game_over.finish_game()
                    self.mode = 'game_over'
            
            # update and render the clouds
            self.clouds.render(self.display)
            self.clouds.update()

            # blits the background mountains/scene
            self.display.blit(
                self.assets['background'][0],
                (0, 0)
            )

            # display main game mechanics in given conditions only
            if self.mode in PLAY_MODES:

                if self.mode in ['upgrade']:
                    self.upgrade_cards.play_deck()
                if self.mode in ['upgrade_unpack']:
                    if self.upgrade_cards.unpack():
                        self.mode = 'upgrade'

                # blits arm 1 of slingshot 1
                self.display.blit(
                    self.assets['launcher'][0],
                    (
                        self.player1.block_map.tile_size[0] * 3 + self.display.get_width() // 16,
                        648 - self.assets['launcher'][0].get_height()
                    )
                )

                # renders the player 1 associated objects 
                self.player1.render()
                
                # blits arm 2 of slingshot 1
                self.display.blit(
                    self.assets['launcher'][1],
                    (
                        self.player1.block_map.tile_size[1] * 3 + self.display.get_width() // 16,
                        648 - self.assets['launcher'][1].get_height()
                    )
                )



                # blits arm 1 of slingshot 2
                self.display.blit(
                    self.assets['launcher_flipped'][0],
                    (
                        self.display.get_width() - 3 * 64 - 2 * self.display.get_width() // 32 - self.assets['launcher'][0].get_width(),
                        648 - self.assets['launcher_flipped'][0].get_height()
                    )
                )

                # renders the player 2 associated objects
                self.player2.render()
                
                # blits arm 2 of slingshot 2
                self.display.blit(
                    self.assets['launcher_flipped'][1],
                    (
                        self.display.get_width() - 3 * 64 - 2 * self.display.get_width() // 32 - self.assets['launcher'][1].get_width(),
                        648 - self.assets['launcher_flipped'][1].get_height()
                    )
                )

                # taking care of x offset
                self.off_set[0] = max(
                    min(
                        self.off_set[0],
                        0
                    ),
                    self.window.get_width() - 2 * self.window.get_width() / self.scaling_factor
                )
                # taking care of y offset
                self.off_set[1] = max(
                    min(
                        self.off_set[1],
                        0
                    ),
                    self.window.get_height() - 2 * self.window.get_height() / self.scaling_factor
                )
                # taking care of scale value
                self.scaling_factor = min(2, self.scaling_factor)

                # display particles
                self.particles.render(self.display)
                self.particles.update()

            # blits the foreground grass and foundations
            self.display.blit(
                    self.assets['background'][1],
                    (0, 0)
                )


            # blits the scrolled and scaled display on window
            self.window.blit(
                pygame.transform.scale(
                    self.display,
                    (
                        2 * self.window.get_width() / self.scaling_factor,
                        2 * self.window.get_height() / self.scaling_factor,
                    )
                ),
                self.off_set
            )

            # display the upgrade indicators and turn display
            if self.mode in PLAY_MODES:
                self.player1.render_upgrade_indicators(self.window)
                self.player2.render_upgrade_indicators(self.window)
                self.assets['UI']['turn_display'].set_frame(self.player_turn * 10)
                self.window.blit(
                    self.assets['UI']['turn_display'].img(),
                    (0,0),
                )

            # displays the name and rating of each player
            if self.mode in PLAY_MODES + ['name_input']:
                self.name_handler.render(self.window)

            # takes in name for name_input
            if self.mode in ['name_input']:
                self.name_handler.update()

            # displays the menu
            if self.mode in ['menu']:
                self.menu.update()
                self.menu.render(self.window)

            # displays the game over window along the new ratings
            if self.mode in ['game_over']:
                self.game_over.render(self.window)
                self.game_over.update()

            # puts the tutorial slide mask on game
            if self.tutorial:
                self.tut.update()
                self.tut.render(self.window)
            # displays the util buttons on top
            else:
                self.util_buttons.render(self.window)
                self.util_buttons.update()

            # mute main game music
            if self.mute:
                pygame.mixer.music.stop()
            else:
                if not self.playing:
                    pygame.mixer.music.play(-1)
                    self.playing = True

            # updates window
            pygame.display.update()

            # set fps to 60
            self.clock.tick(60)


    def change_scaling(self, expected_scaling, ratio):
        '''
        Used to add a continuous effect in scale change, higher ratio results in a slower but smoother transition
        '''
        self.scaling_factor = (ratio * self.scaling_factor + expected_scaling) / (ratio + 1)

    def get_player_by_id(self, id=None):
        '''
        Returns player by id(return player by default)
        Used by various objects to get present playing player class through game class 
        '''
        if id == None:
            return self.player1 if self.player_turn == 0 else self.player2

        if id == -1:
            return self.player2 if self.player_turn == 0 else self.player1

        return self.player1 if id == 0 else self.player2
    
    def get_font(self, size):
        '''
        Return font object of cutom font with given size
        note that font may break at many values (20, 38 and 60 are safe)
        '''
        return pygame.font.Font('assets/fonts/custom_font.ttf',size=size)

while True:
    try:
        game().run()
    except Exception as e:
        if str(e) == 'Window resize error':
            print("Window was resized! Resetting")
        else:
            raise e
