import pygame as pygame
from scripts.blockmap import BlockMap
from scripts.player import Player
from scripts.utils import load_image, load_images, Animation
from scripts.particles import Particles

class game():
    def __init__(self):

        pygame.init()

        pygame.display.set_caption('Birds and Blocks')

        # window will be the main window to be displayed on scree
        self.window = pygame.display.set_mode((1280,720))

        # loading all the assets to prevent lag once game has started
        self.assets = {
            'background' : load_images('background'),
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
                'basic' : load_image('cards/red/red.png'),
                'wood' : load_image('cards/wood/wood.png'),
                'stone' : load_image('cards/stone/stone.png'),
                'glass' : load_image('cards/glass/glass.png'),
            },
            'blocks' : {
                'glass' : Animation(load_images('blocks/glass'), img_dur = 1),
                'wood' : Animation(load_images('blocks/wood'), img_dur = 1),
                'stone' : Animation(load_images('blocks/stone'), img_dur = 1),
                'royal' : Animation(load_images('blocks/royal'), img_dur = 1),
            },
            'effects' : {
                'dust' : Animation(load_images('effects/dust'), img_dur = 1, loop=False),
            },
            'shards' : {
                'glass' : Animation(load_images('effects/shards/glass'), img_dur=10),
                'wood' : Animation(load_images('effects/shards/wood'), img_dur=10),
                'stone' : Animation(load_images('effects/shards/stone'), img_dur=10),
            }
        }

        # all the sprites will be blit on display and rescaled to fit window giving a zoom effect
        self.display = pygame.Surface((1280,720))

        # scales the display to window for zoom effect
        self.scaling_factor = 2

        # moves the window for scroll effet
        self.off_set = [0, 0]

        # mode dictates what is happening in game
        self.mode = 'card_unpack'

        # initializing clock
        self.clock = pygame.time.Clock()

        self.scrolling = True

        self.particles = Particles(self.window.get_size(),{
            'basic_feather' : self.assets['projectile']['basic']['feather'],
            'wood_feather' : self.assets['projectile']['wood']['feather'],
            'stone_feather' : self.assets['projectile']['stone']['feather'],
            'glass_feather' : self.assets['projectile']['glass']['feather'],
            'basic_feather_flipped' : self.assets['projectile_flipped']['basic']['feather'],
            'wood_feather_flipped' : self.assets['projectile_flipped']['wood']['feather'],
            'stone_feather_flipped' : self.assets['projectile_flipped']['stone']['feather'],
            'glass_feather_flipped' : self.assets['projectile_flipped']['glass']['feather'],
            'dust' : self.assets['effects']['dust'],
            'shards_glass' : self.assets['shards']['glass'],
            'shards_wood' : self.assets['shards']['wood'],
            'shards_stone' : self.assets['shards']['stone'],
        })

        self.player1 = Player(self, 0, (self.display.get_width() // 32,630))
        self.player2 = Player(self, 1, (self.display.get_width() - 3 * 64 - self.display.get_width() // 32,630))
        self.player_turn = 0
        # maintain a single mpos variable that will be passed to other functions
        self.mpos = (0, 0)

    def run(self):


        while True:
            # filling skyblue in background
            self.display.fill('#87CEEB')

# [Taking input] --------------------------------------------------------------------------------- #

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if event.type == pygame.VIDEORESIZE:
                    raise Exception('Window resize error')


            self.mpos = pygame.mouse.get_pos()
            self.scaled_mpos = (
                (self.mpos[0] - self.off_set[0]) * self.scaling_factor / 2,
                (self.mpos[1] - self.off_set[1]) * self.scaling_factor / 2
            )
            
            # scrolls the screen
            if self.mode in ['card_unpack', 'card_select']:

                self.change_scaling(2, 14)
                # value by which offset will move
                delta = 0

                if self.mpos[0] < self.window.get_width()/4:
                    delta = - (self.mpos[0] - self.window.get_width() / 4)/30
                if self.mpos[0] > 3*self.window.get_width()/4:
                    delta = - (self.mpos[0] - 3 * self.window.get_width() / 4)/30
                self.off_set[0] = max(
                    min(
                        self.off_set[0] + delta,
                        0
                    ),
                    self.window.get_width() - 2 * self.window.get_width() / self.scaling_factor
                )

                delta = 0
                
                if self.mpos[1] < self.window.get_height()/4:
                    delta = - (self.mpos[1] - self.window.get_height() / 4)/30
                if self.mpos[1] > 3*self.window.get_height()/4:
                    delta = - (self.mpos[1] - 3 * self.window.get_height() / 4)/30
                self.off_set[1] = max(
                    min(
                        self.off_set[1] + delta,
                        0
                    ),
                    self.window.get_height() - 2 * self.window.get_height() / self.scaling_factor
                )

# [Updating the screen] -------------------------------------------------------------------------- #



            # blits the background mountains/scene
            self.display.blit(
                pygame.transform.scale(self.assets['background'][0],
                    (
                        self.display.get_width(),
                        self.display.get_height()
                    )
                ),
                (0, 0)
            )

            # blits arm 1 of slingshot 1
            self.display.blit(
                self.assets['launcher'][0],
                (
                    self.player1.block_map.tile_size[0] * 3 + self.display.get_width() // 16,
                    648 - self.assets['launcher'][0].get_height()
                )
            )

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
                pygame.transform.scale(self.assets['background'][1],
                    (
                        self.display.get_width(),
                        self.display.get_height()
                    )
                ),
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

            # updates window
            pygame.display.update()
            
            # set fps to 60
            self.clock.tick(60)

    def change_scaling(self, expected_scaling, ratio):
        self.scaling_factor = (ratio * self.scaling_factor + expected_scaling) / (ratio + 1)

    def get_player_by_id(self, id):
        return self.player1 if id == 0 else self.player2

while True:            
    try:
        game().run()
    except Exception as e:
        if str(e) == 'Window resize error':
            print("Window was resized! Resetting")
        else:
            raise e