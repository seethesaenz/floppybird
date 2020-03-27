import pathlib
import pygame


class Bird(pygame.sprite.Sprite):
    """player character bird class"""

    def __init__(self, screen):
        """constructor"""

        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

        # Get background image and rect of screen and image
        floppy1_img_path = str(pathlib.Path('images/floppy.png').expanduser().resolve())
        self.image = pygame.image.load(floppy1_img_path)
        floppy2_img_path = str(pathlib.Path('images/floppyup.png').expanduser().resolve())
        self.imageup = pygame.image.load(floppy2_img_path)
        floppy3_img_path = str(pathlib.Path('images/floppydown.png').expanduser().resolve())
        self.imagedown = pygame.image.load(floppy3_img_path)
        self.rect = self.image.get_rect().move(100, 100)
        self.screen_rect = self.screen.get_rect()

        