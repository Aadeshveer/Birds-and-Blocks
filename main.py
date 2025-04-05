import pygame as pygame
from scripts.blockmap import Block, BlockMap
from scripts.utils import load_image, load_images

class game():
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Birds and Blocks')

        # window will be the main window to be displayed on scree
        self.window = pygame.display.set_mode((1280,720))

        self.assets = {
            'projectile/basic' : load_image('projectiles/basic/0.png'),
            'background' : load_images('background'),
        }
        
        # all the sprites will be blit on display and rescaled to fit window giving a zoom effect
        self.display = pygame.Surface((1280,720))

        # scales the display to window for zoom effect
        self.scaling_factor = 1

        # moves the window for scroll effet
        self.off_set = [-160, -90]

        # initializing clock
        self.clock = pygame.time.Clock()
    
    def run(self):
        self.block_map = BlockMap((40,640),{(0,0):Block('wood'),(0,-64):Block('wood'),(64,0):Block('wood')})

        while True:
            self.display.fill('#87CEEB')

# [Taking input] --------------------------------------------------------------------------------- #

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.scaling_factor = 2


            mpos = pygame.mouse.get_pos()
            
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

# [Updating the screen] -------------------------------------------------------------------------- #

            for img in self.assets['background']:
                self.display.blit(
                    pygame.transform.scale(img,
                        (
                            self.display.get_width(),
                            self.display.get_height()
                        )
                    ),
                    (0, 0)
                )

            self.block_map.render(self.display)

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