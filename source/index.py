from time import sleep
import sys
import pygame

from components.car import Car
from settings import Settings
from components import Car


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
        pygame.display.set_icon(self.car.carImg)

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.settings.display_width, self.settings.display_height))

        self.run_car()

    def run_car(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

            self.set_background()

            self.car.show(self)

            pygame.display.update()
            self.clock.tick(60)

    def set_background(self):
        self.gameDisplay.fill(self.settings.black_color)
        self.gameDisplay.blit(self.bgImg, (self.bg_x, self.bg_y))

    def _check_keydown_events(self, event):
        match event.key:
            case pygame.K_LEFT:
                self.car.car_x_coordinate -= 75
                print("CAR X COORDINATES: %s" % self.car.car_x_coordinate)
            case pygame.K_RIGHT:
                self.car.car_x_coordinate += 75
                print("CAR X COORDINATES: %s" % self.car.car_x_coordinate)

        print("x: {x}, y: {y}".format(x=self.car.car_x_coordinate, y=self.car.car_y_coordinate))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
