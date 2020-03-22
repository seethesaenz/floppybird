import pathlib
import random
from random import randint
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group


class FloppyBird:
    """main game class"""

    def __init__(self):
        """constructor"""

        self.screen_width = 800
        self.screen_height = 600
        pygame.init()
        pygame.display.set_caption('FloppyBird')
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.run = True
        self.jump = False
        self.space_down = False

        self.background = Background(self.screen)
        self.clock = pygame.time.Clock()

        self.pipegroup = Group()
        self.bird = Bird(self.screen)
        self.bird_min_grav = 4
        self.bird_max_grav = 8
        self.bird_jump_height = 15
        
        # pygame.display.set_icon(pygame.image.load())
        self.flopdabird()



    def flopdabird(self):
        """Function which is responsible for running the game"""
        while self.run:
            # add function for rotating bird up if grav > 0 and down if grav < 0
            self.draw()
            self.pipe_controls()
            self.eventmanager()
            self.movement()
            self.collision()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def collision(self):
        if pygame.sprite.spritecollide(self.bird, self.pipegroup, 0):
            self.run = False
            

    def movement(self):
        """movement logic"""
        if self.bird_min_grav < self.bird_max_grav:
           self.bird_min_grav += 1
        elif self.bird_min_grav > self.bird_max_grav:
            self.bird_min_grav = self.bird_max_grav

        self.bird.rect.bottom += self.bird_min_grav

        if self.bird.rect.bottom >= self.screen_height:
            self.bird.rect.bottom = self.screen_height
            self.run = False
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

        space_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if not self.space_down:
                        space_clicked = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.space_down = False
        if space_clicked:
            self.bird_min_grav = -self.bird_jump_height

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
        color = colors[randint(0, len(colors) - 1)]
        return color

    def pipe_controls(self):
        """create, remove, and move the pipes"""
        
        for pipe in self.pipegroup.sprites():
            pipe.rect.left -= 8
        for pipe in self.pipegroup.sprites():
            if pipe.rect.left <= -80:
                self.pipegroup.remove(pipe)
                # make two sets of pipe on screen 
                # make points display and addition when pipes are removed
                #
        if not self.pipegroup:
            space = randint(200, 300)
            color = self.getrandomcolor()
            x = 800
            width = 85
            top_y = 0
            top_height = randint(50, 350)
            bottom_y = top_height + space
            bottom_height = self.screen_height - top_height - space
            top_rect = pygame.Rect(x, top_y, width, top_height)
            bottom_rect = pygame.Rect(x, bottom_y, width, bottom_height)
            self.pipegroup.add(Pipesclass(self.screen, top_rect, color))
            self.pipegroup.add(Pipesclass(self.screen, bottom_rect, color))


class Pipesclass(Sprite):

    def __init__(self, screen, rect, color):
        """Initialize attributes of the pipes"""
        
        Sprite.__init__(self)
        self.screen = screen
        self.rect = rect
        self.color = color

    def draw(self):
        """Draw pipes"""
        
        pygame.draw.rect(
            self.screen,
            self.color,
            self.rect,
        )


class Bird(Sprite):
    """player character bird class"""

    def __init__(self, screen):
        """constructor"""

        Sprite.__init__(self)
        self.screen = screen

        # Get background image and rect of screen and image
        floppy_img_path = str(pathlib.Path('images/floppy.png').expanduser().resolve())
        self.image = pygame.image.load(floppy_img_path)
        self.rect = self.image.get_rect().move(100, 100)
        self.screen_rect = self.screen.get_rect()

    def blitme(self):
        """Draw the background onto the screen"""

        self.screen.blit(self.image, self.rect)


class Background:
    """background class to simulate movement"""

    def __init__(self, screen):
        """Initialize attributes for the background"""

        self.screen = screen

        # Get background image and rect of screen and image
        background_img_path = str(pathlib.Path('images/bg1.png').expanduser().resolve())
        self.image = pygame.image.load(background_img_path)
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Set rects together
        self.rect = self.screen_rect
        self.clouds = []
        self.cloud_amount = 6

    def update(self):
        if len(self.clouds) < self.cloud_amount:
            self.clouds.append(Cloud())
        for cloud in self.clouds:
            if cloud.rect.left < -cloud.rect.width:
                cloud.rect.left = random.randint(800, 1800)
        for cloud in self.clouds:
            cloud.rect.left -= cloud.movement_speed


    def blitme(self):
        """Draw the background onto the screen"""

        self.update()
        self.screen.blit(self.image, self.rect)
        for cloud in self.clouds:
            self.screen.blit(cloud.image, cloud.rect)


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movement_speed = 4
        cloud_type = str(random.randint(1, 8))
        cloud_x = random.randint(800, 1800)
        cloud_y = random.randint(20, 160)
        floppy_img_path = str(pathlib.Path('images/cloud' + cloud_type + '.png').expanduser().resolve())
        self.image = pygame.image.load(floppy_img_path)
        self.rect = self.image.get_rect().move(cloud_x, cloud_y)


if __name__ == "__main__":
    FloppyBird()
