import random
import pygame
from pygame.sprite import Sprite


class EnemyCar(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.carImg = random.choice(
            [pygame.image.load('..\\images\\car1.png'), pygame.image.load('..\\images\\car.png'),
             pygame.image.load('..\\images\\car2.png')])

        self.car_x_coordinate = random.choice([355, 425, 495])  # قرار گیری در یکی از سه لاین جاده

        # --------------------- محاسبات برای جلوگیری از قرار گرفتن خودروها روی یکدیگر----------
        try:
            last_y = self.ai_game.enemy_cars.sprites()[-1].car_y_coordinate
            last_x = self.ai_game.enemy_cars.sprites()[-1].car_x_coordinate
        except:
            last_y = 0
            last_x = 0

        temp = random.randrange(0, 600) * -1
        if last_y - 100 < temp and last_x == self.car_x_coordinate:  #  دو ماشین روی یکدیگر قرار نمیگیرند
            temp = last_y - 150

        self.car_y_coordinate = temp
        self.car_width = 50
        self.rect = pygame.Rect(self.car_x_coordinate - 1, self.car_y_coordinate, 48, 100)  # ایجاد یک مستطیل برای مکانیزم تصادف
        self.rect.x = self.car_x_coordinate
        self.rect.y = self.car_y_coordinate
        self.speed = random.randrange(40, 60)

    def show(self, game):
        game.gameDisplay.blit(self.carImg, self.rect)

    def update(self):

        self.car_y_coordinate += self.ai_game.settings.car_y_speed * self.speed / 100

        self.rect.y = self.car_y_coordinate
        self.rect.x = self.car_x_coordinate

        other_cars = pygame.sprite.Group(self.ai_game.enemy_cars)
        other_cars.remove(self)

        if pygame.sprite.spritecollideany(self, other_cars):
            self.speed = random.randrange(65, 85)
