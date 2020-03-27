import random
import pathlib
import pygame


class Background:
    """background class to simulate movement"""

    def __init__(self, screen, screen_width, game_speed):
        """Initialize attributes for the background"""

        # general attributes
        self.screen = screen
        self.screen_width = screen_width

        # layer image stuff
        layer_1_img_path = str(pathlib.Path('images/bg_layer_1.png').resolve())
        layer_2_img_path = str(pathlib.Path('images/bg_layer_2.png').resolve())
        layer_3_img_path = str(pathlib.Path('images/bg_layer_3.png').resolve())
        self.layer_1_img = pygame.image.load(layer_1_img_path)
        self.layer_2_img = pygame.image.load(layer_2_img_path)
        self.layer_3_img = pygame.image.load(layer_3_img_path)

        # layer rect stuff
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

        # layer attributes
        self.layer_2_speed = game_speed // 4
        self.layer_3_speed = game_speed
        self.cloud_speed = game_speed // 2

        # cloud attributes
        self.cloud_amount = 12
        self.clouds = [Cloud(self.screen_width) for _ in range(self.cloud_amount)]

    def update(self, delta_time):
        self.update_layers(delta_time)
        self.update_clouds(delta_time)

    def update_layers(self, delta_time):
        # move layers
        for rect in self.layer_2_rects:
            # tmp = self.layer_2_speed * delta_time * -1
            # print(tmp)
            # rect.left += tmp
            rect.left -= self.layer_2_speed
        for rect in self.layer_3_rects:
            # rect.left += int(self.layer_3_speed * delta_time * -1)
            rect.left -= self.layer_3_speed

        # reposition layer rects that have gone off screen
        if self.layer_2_rect_a.left + self.layer_2_rect_a.width < 0:
            self.layer_2_rect_a.left = self.layer_2_rect_b.left + self.layer_2_rect_b.width
        if self.layer_2_rect_b.left + self.layer_2_rect_b.width < 0:
            self.layer_2_rect_b.left = self.layer_2_rect_a.left + self.layer_2_rect_a.width
        if self.layer_3_rect_a.left + self.layer_3_rect_a.width < 0:
            self.layer_3_rect_a.left = self.layer_3_rect_b.left + self.layer_3_rect_b.width
        if self.layer_3_rect_b.left + self.layer_3_rect_b.width < 0:
            self.layer_3_rect_b.left = self.layer_3_rect_a.left + self.layer_3_rect_a.width

    def update_clouds(self, delta_time):
        # move clouds
        for cloud in self.clouds:
            # cloud.rect.left += int(self.cloud_speed * delta_time * -1)
            cloud.rect.left -= self.cloud_speed

        # reposition clouds that have gone off screen
        for cloud in self.clouds:
            if cloud.rect.left < -cloud.rect.width:
                cloud.rect.left = random.randint(self.screen_width, self.screen_width * 2)
                cloud.image = cloud.cloud_imgs[random.randint(0, 7)]

    def blitme(self):
        """Draw the background onto the screen"""

        # draw all the layers
        self.screen.blit(self.layer_1_img, self.layer_1_rect)
        self.screen.blit(self.layer_2_img, self.layer_2_rect_a)
        self.screen.blit(self.layer_2_img, self.layer_2_rect_b)
        self.screen.blit(self.layer_3_img, self.layer_3_rect_a)
        self.screen.blit(self.layer_3_img, self.layer_3_rect_b)

        # draw all the clouds
        for cloud in self.clouds:
            self.screen.blit(cloud.image, cloud.rect)


class Cloud(pygame.sprite.Sprite):
    """sprite class for clouds, should it be a sprite?"""

    cloud_paths = [str(pathlib.Path(f'images/cloud{i}.png').resolve()) for i in range(1, 9)]
    cloud_imgs = [pygame.image.load(path) for path in cloud_paths]

    def __init__(self, screen_width):
        """constructor"""

        pygame.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        cloud_x = random.randint(self.screen_width, self.screen_width * 2)
        cloud_y = random.randint(20, 160)
        self.image = self.cloud_imgs[random.randint(0, 7)]
        self.rect = self.image.get_rect().move(cloud_x, cloud_y)
