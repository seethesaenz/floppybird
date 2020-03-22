import random
import pygame
from bird import Bird
from pipes import Pipes
from background import Background, Cloud


class FloppyBird:
    """main game class"""

    def __init__(self):
        """constructor"""
        pygame.init()

        self.screen_width = 1300
        self.screen_height = 700
        pygame.display.set_caption('FloppyBird')
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.run = True
        self.jump = False

        self.pipegroup = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.bird = Bird(self.screen)
        self.background = Background(self.screen)

        self.bird_grav = 4
        self.bird_max_grav = 8
        self.bird_jump_height = 15

        self.debug = True

        # pygame.display.set_icon(pygame.image.load())
        self.flopdabird()

    def flopdabird(self):
        """Function which is responsible for running the game"""
        while self.run:
            self.draw()
            self.pipe_controls()
            self.eventmanager()
            self.movement()
            if not self.debug:
                self.collision()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def collision(self):
        if pygame.sprite.spritecollide(self.bird, self.pipegroup, 0):
            self.run = False

    def movement(self):
        """movement logic"""
        if self.bird_grav < self.bird_max_grav:
           self.bird_grav += 1
        elif self.bird_grav > self.bird_max_grav:
            self.bird_grav = self.bird_max_grav

        self.bird.rect.bottom += self.bird_grav

        # end game if bird hits ground
        if self.bird.rect.bottom >= self.screen_height:
            self.bird.rect.bottom = self.screen_height
            self.run = False

        # don't allow bird to go past top of screen
        if self.bird.rect.top <= 0:
            self.bird.rect.top = 0

    def draw(self):
        """handles drawing"""

        self.background.blitme()
        self.bird.blitme()
        for pipe in self.pipegroup.sprites():
            pipe.draw()


    def eventmanager(self):
        """handles events"""

        space_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True

        if space_pressed:
            self.bird_grav = -self.bird_jump_height

    def getrandomcolor(self):
        """pick a color at random from the colors list"""

        colors = [
            (255, 0, 0),
            (255, 128, 0),
            (255, 255, 0),
            (128, 255, 0),
            (0, 255, 0),
            (0, 255, 128),
            (0, 255, 255),
            (0, 128, 255),
            (0, 0, 255),
            (128, 0, 255),
            (255, 0, 255),
            (255, 0, 128)
        ]
        return colors[random.randint(0, len(colors) - 1)]

    def pipe_controls(self):
        """create, remove, and move the pipes"""

        pipe_width = 85
        pipe_speed = 8  # bird speed basically

        for pipe in self.pipegroup.sprites():
            pipe.rect.left -= pipe_speed

        for pipe in self.pipegroup.sprites():
            if pipe.rect.left <= -pipe_width:
                self.pipegroup.remove(pipe)

        if not self.pipegroup:
            # for adjusting pipes
            space = random.randint(200, 300)
            top_height = random.randint(50, self.screen_height - space)

            # no need to modify below
            color = self.getrandomcolor()
            x = self.screen_width
            bottom_y = top_height + space
            bottom_height = self.screen_height - top_height - space
            top_rect = pygame.Rect(x, 0, pipe_width, top_height)
            bottom_rect = pygame.Rect(x, bottom_y, pipe_width, bottom_height)
            self.pipegroup.add(Pipes(self.screen, top_rect, color))
            self.pipegroup.add(Pipes(self.screen, bottom_rect, color))


if __name__ == "__main__":
    FloppyBird()





