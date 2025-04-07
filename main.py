import pygame as pygame
from scripts.blockmap import BlockMap
from scripts.player import Player
from scripts.utils import load_image, load_images
from scripts.birds import Bird

class game():
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Birds and Blocks')

        # window will be the main window to be displayed on scree
        self.window = pygame.display.set_mode((1280,720))

        self.assets = {
            'projectile/basic' : load_image('projectiles/basic/0.png'),
            'background' : load_images('background'),
            'launcher' : load_images('projectile_shooter')
        }
        
        # all the sprites will be blit on display and rescaled to fit window giving a zoom effect
        self.display = pygame.Surface((1280,720))

        # scales the display to window for zoom effect
        self.scaling_factor = 1

        # moves the window for scroll effet
        self.off_set = [-160, -90]

        # initializing clock
        self.clock = pygame.time.Clock()

        self.scrolling = True

        self.player1 = Player((self.display.get_width() // 32,630))
        self.player2 = Player((self.display.get_width() - 3 * 64 - self.display.get_width() // 32,630))
    
    def run(self):

        bird = Bird((self.display.get_width(), self.display.get_height()),(290,560), 'idle')

        while True:
            self.display.fill('#87CEEB')

# [Taking input] --------------------------------------------------------------------------------- #

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.scrolling:
                        if pygame.mouse.get_pressed()[2]:
                            self.scaling_factor = 2 if self.scaling_factor==1 else 1

            if pygame.mouse.get_pressed()[1]:
                bird.mode = 'ready'

            mpos = pygame.mouse.get_pos()
            
            if self.scrolling:
                # value by which offset will move
                delta = 0

                if mpos[0] < self.window.get_width()/4:
                    delta = - (mpos[0] - self.window.get_width() / 4)/30
                if mpos[0] > 3*self.window.get_width()/4:
                    delta = - (mpos[0] - 3 * self.window.get_width() / 4)/30
                self.off_set[0] = max(
                    min(
                        self.off_set[0] + delta,
                        0
                    ),
                    self.window.get_width() - 2 * self.window.get_width() / self.scaling_factor
                )

                delta = 0
                
                if mpos[1] < self.window.get_height()/4:
                    delta = - (mpos[1] - self.window.get_height() / 4)/30
                if mpos[1] > 3*self.window.get_height()/4:
                    delta = - (mpos[1] - 3 * self.window.get_height() / 4)/30
                self.off_set[1] = max(
                    min(
                        self.off_set[1] + delta,
                        0
                    ),
                    self.window.get_height() - 2 * self.window.get_height() / self.scaling_factor
                )

            print(self.scaling_factor)
# [Updating the screen] -------------------------------------------------------------------------- #
            mpos = pygame.mouse.get_pos()

            self.scrolling = bird.update([
                (mpos[0] - self.off_set[0]) * self.scaling_factor / 2,
                (mpos[1] - self.off_set[1]) *self.scaling_factor/2
            ])

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

            if self.scrolling:
                _ = bird.render(self.display, self.scaling_factor, self.off_set)
            else:
                self.off_set, self.scaling_factor = bird.render(self.display, self.scaling_factor, self.off_set)
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


            # blits arm 2 of slingshot 1
            self.display.blit(
                self.assets['launcher'][1],
                (
                    self.player1.block_map.tile_size[1] * 3 + self.display.get_width() // 16,
                    648 - self.assets['launcher'][1].get_height()
                )
            )

            # blits the slingshot 2
            self.display.blit(
                pygame.transform.flip(self.assets['launcher'][0], True, False),
                (
                    self.display.get_width() - 3 * 64 - 2 * self.display.get_width() // 32 - self.assets['launcher'][0].get_width(),
                    648 - self.assets['launcher'][0].get_height()
                )
            )
            self.display.blit(
                pygame.transform.flip(self.assets['launcher'][1], True, False),
                (
                    self.display.get_width() - 3 * 64 - 2 * self.display.get_width() // 32 - self.assets['launcher'][1].get_width(),
                    648 - self.assets['launcher'][1].get_height()
                )
            )

            # blits the blocks, birds etc.
            self.player1.render(self.display)
            self.player2.render(self.display)

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

            pygame.display.update()
            
            # set fps to 60
            self.clock.tick(60)
            

game().run()