import pathlib
import pygame


class Bird(pygame.sprite.Sprite):
    """player character bird class"""

    def __init__(self, screen):
        """constructor"""

        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

        # Get background image and rect of screen and image
        floppy_img_path = str(pathlib.Path('images/floppy.png').expanduser().resolve())
        self.image = pygame.image.load(floppy_img_path)
        self.rect = self.image.get_rect().move(100, 100)
        self.screen_rect = self.screen.get_rect()

    def blitme(self):
        """Draw the background onto the screen"""

        self.screen.blit(self.image, self.rect)