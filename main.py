import pygame as pygame
from scripts.utils import load_image, load_images

class game():
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Birds and Blocks')

        # window will be the main window to be displayed on scree
        self.window = pygame.display.set_mode((1280,720))

        self.assets = {
            'background' : load_images('backgrounds'),
            'projectile/basic' : load_image('projectiles/basic/0.png')
        }
        
        # all the sprites will be blit on display and rescaled to fit window giving a zoom effect
        self.display = pygame.Surface((1280,720))
        
        # scales the display to window for zoom effect
        self.scaling_factor = 1

        # moves the window for scroll effet
        self.off_set = [-160, -90]

        self.clock = pygame.time.Clock()

        self.test_img = pygame.image.load('test.png')

    
    def run(self):
        self.big = True
        while True:
            self.window.fill((0, 0, 0))

            if self.big:
                self.scaling_factor += 0.001
                if self.scaling_factor >= 2:
                    self.big=False
            else:
                self.scaling_factor -= 0.001
                if self.scaling_factor <= 1:
                    self.big=True
            print(self.scaling_factor)
# [Taking input] --------------------------------------------------------------------------------- #

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)


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

            self.display.blit(pygame.transform.scale(self.test_img, self.display.size), (0, 0))
            for background in self.assets['background']:
                self.display.blit(pygame.transform.scale(
                    background,
                    (self.display.get_width(),
                    self.display.get_height())
                ), (0, 0))

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