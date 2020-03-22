import pygame


class Pipes(pygame.sprite.Sprite):
    
    def __init__(self, screen, rect, color):
        """Initialize attributes of the pipes"""

        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.rect = rect
        self.color = color

    def draw(self):
        """Draw pipe"""

        pygame.draw.rect(self.screen, self.color, self.rect)
