import pygame
from pygame.sprite import Sprite


class Car(Sprite):
    def __init__(self, game):
        self.settings = game.settings
        self.game = game
        self.carImg = pygame.image.load('..\\images\\car1.png')
        self.car_x_coordinate = (game.settings.display_width / 2) - 25
        self.car_y_coordinate = (game.settings.display_height * 0.82)
        self.car_width = 50
        self.moving_right = False
        self.moving_left = False
        self.rect = self.carImg.get_rect()
        # BackgroundS

    def show(self, game):
        game.gameDisplay.blit(self.carImg, (self.car_x_coordinate, self.car_y_coordinate))

    def update(self):
        if self.moving_right:
            self.car_x_coordinate += self.settings.car_x_speed
            if self.car_x_coordinate >= 510:
                self.moving_right = False
                self.car_x_coordinate = 495

                if self.settings.car_y_speed > 1:
                    self.settings.increase /= 3
                    self.settings.car_y_speed /= 2
                    if self.settings.car_x_speed > 2:
                        self.settings.car_x_speed /= 2

                if self.game.points > 50:
                    self.game.points -= 50
                else:
                    self.game.points = 0
            # print("CAR X COORDINATES: %s" % self.car_x_coordinate)
        if self.moving_left:
            self.car_x_coordinate -= self.settings.car_x_speed
            if self.car_x_coordinate <= 340:
                self.moving_left = False
                self.car_x_coordinate = 355

                if self.settings.car_y_speed > 1:
                    self.settings.increase /= 3
                    self.settings.car_y_speed /= 2
                    if self.settings.car_x_speed > 2:
                        self.settings.car_x_speed /= 2

                if self.game.points > 50:
                    self.game.points -= 50
                else:
                    self.game.points = 0
            # print("CAR X COORDINATES: %s" % self.car_x_coordinate)

        self.rect.x = self.car_x_coordinate
        self.rect.y = self.car_y_coordinate

        if pygame.sprite.spritecollideany(self.game.car, self.game.enemy_cars):
            self.game.game_over = True
            print("CRASHED")

