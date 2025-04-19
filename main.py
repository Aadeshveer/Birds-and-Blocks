import pygame as pygame
import random

from scripts.modes import Menu, NameInput, GameOver, Tutorial
from scripts.player import Player
from scripts.cards import Deck
from scripts.utils import load_image, load_images, Animation, load_sound
from scripts.particles import Particles


SIZE = (1280,720)
PLAY_MODES = ['card_unpack', 'card_select', 'upgrade_unpack', 'upgrade']

class game():
    def __init__(self):

        pygame.init()

        pygame.font.init()

        pygame.mixer.init()

        pygame.display.set_caption('Birds and Blocks')

        # window will be the main window to be displayed on scree
        self.window = pygame.display.set_mode(SIZE)

        pygame.mixer.music.load('./assets/audio/game_loop.wav')
        pygame.mixer.music.play(-1)

        # loading all the assets to prevent lag once game has started
        self.assets = {
            'background' : load_images('background',scaling=SIZE),
            'launcher' : load_images('projectile_shooter'),
            'launcher_flipped' : load_images('projectile_shooter', flip = True),
            'projectile' : {
                'basic' : {
                    'idle' : Animation(load_images('projectiles/basic/idle')),
                    'in_air' : Animation(load_images('projectiles/basic/in_air')),
                    'feather' : Animation(load_images('projectiles/basic/feather'), img_dur=10, loop=False),
                },
                'wood' : {
                    'idle' : Animation(load_images('projectiles/wood/idle')),
                    'in_air' : Animation(load_images('projectiles/wood/in_air')),
                    'feather' : Animation(load_images('projectiles/wood/feather'), img_dur=10, loop=False),
                },
                'stone' : {
                    'idle' : Animation(load_images('projectiles/stone/idle')),
                    'in_air' : Animation(load_images('projectiles/stone/in_air')),
                    'feather' : Animation(load_images('projectiles/stone/feather'), img_dur=10, loop=False),
                },
                'glass' : {
                    'idle' : Animation(load_images('projectiles/glass/idle')),
                    'in_air' : Animation(load_images('projectiles/glass/in_air')),
                    'feather' : Animation(load_images('projectiles/glass/feather'), img_dur=10, loop=False),
                },
            },
            'projectile_flipped' : {
                'basic' : {
                    'idle' : Animation(load_images('projectiles/basic/idle', flip = True)),
                    'in_air' : Animation(load_images('projectiles/basic/in_air', flip = True)),
                    'feather' : Animation(load_images('projectiles/basic/feather', flip = True), img_dur=10, loop=False),
                },
                'wood' : {
                    'idle' : Animation(load_images('projectiles/wood/idle', flip = True)),
                    'in_air' : Animation(load_images('projectiles/wood/in_air', flip = True)),
                    'feather' : Animation(load_images('projectiles/wood/feather', flip = True), img_dur=10, loop=False),
                },
                'stone' : {
                    'idle' : Animation(load_images('projectiles/stone/idle', flip = True)),
                    'in_air' : Animation(load_images('projectiles/stone/in_air', flip = True)),
                    'feather' : Animation(load_images('projectiles/stone/feather', flip = True), img_dur=10, loop=False),
                },
                'glass' : {
                    'idle' : Animation(load_images('projectiles/glass/idle', flip = True)),
                    'in_air' : Animation(load_images('projectiles/glass/in_air', flip = True)),
                    'feather' : Animation(load_images('projectiles/glass/feather', flip = True), img_dur=10, loop=False),
                },
            },
            'cards' : {
                'basic' : load_image('cards/bird/red/red.png'),
                'wood' : load_image('cards/bird/wood/wood.png'),
                'stone' : load_image('cards/bird/stone/stone.png'),
                'glass' : load_image('cards/bird/glass/glass.png'),
                'upgrade_basic' : load_image('cards/upgrade/red/red.png'),
                'upgrade_wood' : load_image('cards/upgrade/wood/wood.png'),
                'upgrade_stone' : load_image('cards/upgrade/stone/stone.png'),
                'upgrade_glass' : load_image('cards/upgrade/glass/glass.png'),
            },
            'blocks' : {
                'glass' : Animation(load_images('blocks/glass'), img_dur = 1),
                'wood' : Animation(load_images('blocks/wood'), img_dur = 1),
                'stone' : Animation(load_images('blocks/stone'), img_dur = 1),
                'royal' : Animation(load_images('blocks/royal'), img_dur = 1),
            },
            'effects' : {
                'dust' : Animation(load_images('effects/dust'), img_dur = 1, loop=False),
                'particle' : Animation(load_images('effects/particles'), img_dur=3, loop=False)
            },
            'shards' : {
                'glass' : Animation(load_images('effects/shards/glass'), img_dur=10),
                'wood' : Animation(load_images('effects/shards/wood'), img_dur=10),
                'stone' : Animation(load_images('effects/shards/stone'), img_dur=10),
            },
            'clouds' : Animation(load_images('clouds', scaling=(160,64)), img_dur=10),
            'UI' : {
                'title' : load_image('UI/menu/title.png', scaling=SIZE),
                'play_button' : Animation(load_images('UI/menu/play_button', scaling=SIZE), img_dur=10),
                'tutorial_button' : Animation(load_images('UI/menu/tutorial_button', scaling=SIZE), img_dur=10),
                'credits_button' : Animation(load_images('UI/menu/credits_button', scaling=SIZE), img_dur=10),
                'game_over' : load_image('UI/game_over/game_over.png', scaling=SIZE),
                'winner' : load_image('UI/game_over/winner_box.png', scaling=SIZE),
                'menu_button' : Animation(load_images('UI/game_over/menu_button', scaling=SIZE), img_dur=10),
                'player_name' : {
                    'left' : Animation(load_images('UI/player_name/1', scaling=SIZE), img_dur=10),
                    'right' : Animation(load_images('UI/player_name/2', scaling=SIZE), img_dur=10),
                },
                'tutorial' : Animation(load_images('UI/tutorial', scaling=SIZE, alpha=True), img_dur=10),
                'credits' : Animation(load_images('UI/credits', scaling=SIZE, alpha=True), img_dur=10)
            },
        }

        self.audio = {
            'glass_break' : load_sound('glass_break'),
            'stone_break' : load_sound('stone_break'),
            'wood_break' : load_sound('wood_break'),
            'glass_yell' : load_sound('glass_yell'),
            'basic_yell' : load_sound('basic_yell'),
            'wood_yell' : load_sound('wood_yell'),
            'stone_yell' : load_sound('stone_yell'),
            'button' : load_sound('button'),
            'upgrade' : load_sound('upgrade'),
            'bomb' : load_sound('bomb'),
        }

        self.fonts = {
            'monospace' : pygame.font.Font('assets/fonts/custom_font.ttf'),
        }


        # all the sprites will be blit on display and rescaled to fit window giving a zoom effect
        self.display = pygame.Surface((1280,720))

        # mode dictates what is happening in game
        self.mode = 'menu'

        # initializing clock
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

        # resets parts of game required for new game
        self.reset()

    def reset(self):

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

        self.credits = False

        self.menu = Menu(self, self.assets['UI'])

        self.game_over = GameOver(self, self.assets['UI'])

        self.winner = 'None'

        self.name_handler = NameInput(self, self.assets['UI'])

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
                    exit(0)

                # window resize can cause errors in scaling
                if event.type == pygame.VIDEORESIZE:
                    raise Exception('Window resize error')

                if self.mode == 'name_input':

                    self.name_handler.take_input(event)


            self.mpos = pygame.mouse.get_pos()
            self.scaled_mpos = (
                (self.mpos[0] - self.off_set[0]) * self.scaling_factor / 2,
                (self.mpos[1] - self.off_set[1]) * self.scaling_factor / 2
            )

            # scrolls the screen
            if self.mode in ['card_unpack', 'card_select', 'menu', 'upgrade_unpack', 'upgrade', 'name_input','game_over']:

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

            if len(self.player1.block_map.block_map) == 0:
                self.winner = self.name_handler.get_name(1)
                self.mode = 'game_over'
            elif len(self.player2.block_map.block_map) == 0:
                self.winner = self.name_handler.get_name(0)
                self.mode = 'game_over'
            
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

            if self.mode in PLAY_MODES + ['name_input']:
                self.name_handler.render(self.window)

            if self.mode in ['name_input']:
                self.name_handler.update()

            if self.mode in ['menu']:
                self.menu.update()
                self.menu.render(self.window)

            if self.mode in ['game_over']:
                self.game_over.update()
                self.game_over.render(self.window)

            if self.tutorial:
                self.tut.update()
                self.tut.render(self.window)

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

while True:
    try:
        game().run()
    except Exception as e:
        if str(e) == 'Window resize error':
            print("Window was resized! Resetting")
        else:
            raise e
