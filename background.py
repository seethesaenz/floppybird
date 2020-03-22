import random
import pathlib
import pygame


class Background:
    """background class to simulate movement"""

    def __init__(self, screen, screen_width):
        """Initialize attributes for the background"""

        self.screen = screen
        self.screen_width = screen_width
        layer_1_img_path = str(pathlib.Path('images/bg_layer_1.png').resolve())
        layer_2_img_path = str(pathlib.Path('images/bg_layer_2.png').resolve())
        layer_3_img_path = str(pathlib.Path('images/bg_layer_3.png').resolve())
        self.layer_1_img = pygame.image.load(layer_1_img_path)
        self.layer_2_img = pygame.image.load(layer_2_img_path)
        self.layer_3_img = pygame.image.load(layer_3_img_path)

        self.layer_1_rect = self.layer_1_img.get_rect()

        self.layer_2_rect_a = self.layer_2_img.get_rect()
        self.layer_2_rect_b = self.layer_2_rect_a.copy()
        self.layer_2_rect_b.left += self.layer_2_rect_b.width

        self.layer_3_rect_a = self.layer_3_img.get_rect()
        self.layer_3_rect_b = self.layer_3_rect_a.copy()
        self.layer_3_rect_b.left += self.layer_3_rect_b.width

        self.layer_2_rects = [
            self.layer_2_rect_a,
            self.layer_2_rect_b,
        ]
        self.layer_3_rects = [
            self.layer_3_rect_a,
            self.layer_3_rect_b,
        ]
        self.clouds = []
        self.cloud_amount = 12

        self.layer_2_speed = 2
        self.layer_3_speed = 8
        self.cloud_speed = 4

    def update(self):
        self.update_layers()
        self.update_clouds()

    def update_layers(self):
        for rect in self.layer_2_rects:
            rect.left -= self.layer_2_speed
        for rect in self.layer_3_rects:
            rect.left -= self.layer_3_speed
        if self.layer_2_rect_a.left + self.layer_2_rect_a.width < 0:
            self.layer_2_rect_a.left = self.layer_2_rect_b.left + self.layer_2_rect_b.width
        if self.layer_2_rect_b.left + self.layer_2_rect_b.width < 0:
            self.layer_2_rect_b.left = self.layer_2_rect_a.left + self.layer_2_rect_a.width
        if self.layer_3_rect_a.left + self.layer_3_rect_a.width < 0:
            self.layer_3_rect_a.left = self.layer_3_rect_b.left + self.layer_3_rect_b.width
        if self.layer_3_rect_b.left + self.layer_3_rect_b.width < 0:
            self.layer_3_rect_b.left = self.layer_3_rect_a.left + self.layer_3_rect_a.width

    def update_clouds(self):
        if len(self.clouds) < self.cloud_amount:
            self.clouds.append(Cloud(self.screen_width))
        for cloud in self.clouds:
            if cloud.rect.left < -cloud.rect.width:
                cloud.rect.left = random.randint(self.screen_width, self.screen_width * 2)
                cloud.image = cloud.get_image()
        for cloud in self.clouds:
            cloud.rect.left -= self.cloud_speed

    def blitme(self):
        """Draw the background onto the screen"""

        self.update()
        self.screen.blit(self.layer_1_img, self.layer_1_rect)
        self.screen.blit(self.layer_2_img, self.layer_2_rect_a)
        self.screen.blit(self.layer_2_img, self.layer_2_rect_b)
        self.screen.blit(self.layer_3_img, self.layer_3_rect_a)
        self.screen.blit(self.layer_3_img, self.layer_3_rect_b)

        for cloud in self.clouds:
            self.screen.blit(cloud.image, cloud.rect)


class Cloud(pygame.sprite.Sprite):
    """sprite class for clouds, should it be a sprite?"""

    cloud_paths = [str(pathlib.Path(f'images/cloud{i}.png').resolve()) for i in range(1, 9)]

    def __init__(self, screen_width):
        """constructor"""

        pygame.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        cloud_x = random.randint(self.screen_width, self.screen_width * 2)
        cloud_y = random.randint(20, 160)
        self.image = self.get_image()
        self.rect = self.image.get_rect().move(cloud_x, cloud_y)

    # make cache a class var
    def get_image(self, cache={}):
        """method for getting random cloud image"""

        cloud_type = random.randint(0, 7)
        cloud_path = self.cloud_paths[cloud_type]
        if cloud_path in cache:
            return cache[cloud_path]
        image = pygame.image.load(cloud_path)
        cache.update({cloud_path: image})
        return image