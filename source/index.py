from time import sleep
import sys
import pygame

from source.components.car import Car
from source.settings.base_settings import Settings


class CarRacing:
    def __init__(self):

        pygame.init()
        self.settings = Settings(color=(230, 230, 230))
        self.screen = pygame.display.set_mode((self.settings.display_width, self.settings.display_height))
        pygame.display.set_caption("Car racing")
        self.clock = pygame.time.Clock()
        self.gameDisplay = None

        self.bgImg = pygame.image.load("..\\images\\background.jpg")
        self.bg_x = (self.settings.display_width / 2) - (360 / 2)
        self.bg_y = 0

        self.car = Car(self, pygame)
        # self.initialize()

    def initialize(self):

        self.carImg = pygame.image.load('..\\images\\car.png')
        self.car_x_coordinate = (self.settings.display_width / 2) - 25
        self.car_y_coordinate = (self.settings.display_height * 0.82)
        self.car_width = 50
        # Background
        self.bgImg = pygame.image.load("..\\images\\background.jpg")
        self.bg_x = (self.settings.display_width / 2) - (360 / 2)
        self.bg_y = 0

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.settings.display_width, self.settings.display_height))

        self.run_car()

    def run_car(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # print(event)

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT):
                        self.car.car_x_coordinate -= 75
                        print("CAR X COORDINATES: %s" % self.car.car_x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.car.car_x_coordinate += 75
                        print("CAR X COORDINATES: %s" % self.car.car_x_coordinate)
                    print("x: {x}, y: {y}".format(x=self.car.car_x_coordinate, y=self.car.car_y_coordinate))

            self.set_background()

            self.car.show(self)

            pygame.display.update()
            self.clock.tick(60)

    def set_background(self):
        self.gameDisplay.fill(self.settings.black_color)
        self.gameDisplay.blit(self.bgImg, (self.bg_x, self.bg_y))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
