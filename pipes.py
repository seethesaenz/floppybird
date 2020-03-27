import pygame
import pathlib

class Pipes(pygame.sprite.Sprite):
    
    def __init__(self, screen, rect, color):
        """Initialize attributes of the pipes"""

        pygame.sprite.Sprite.__init__(self)
        # floppy1_img_path = str(pathlib.Path('images/pipe.png').expanduser().resolve())
        # self.image = pygame.image.load()
        self.screen = screen
        self.rect = rect
        self.color = color

    def draw(self):
        """Draw pipe"""

        pygame.draw.rect(self.screen, self.color, self.rect)
