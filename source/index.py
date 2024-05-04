from time import sleep
import sys
import pygame

from components.car import Car
from settings import Settings
from components import Car


def gradientRect(window, left_colour, right_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour, (0, 0), (1, 0))  # left colour line
    pygame.draw.line(colour_rect, right_colour, (0, 1), (1, 1))  # right colour line
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)


class CarRacing:
    def __init__(self):

        pygame.init()
        self.settings = Settings(color=(230, 230, 230))
        self.screen = pygame.display.set_mode((self.settings.display_width, self.settings.display_height))
        pygame.display.set_caption("Car racing")
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        self.clock = pygame.time.Clock()
        self.gameDisplay = None

        self.bgImg1 = pygame.image.load("..\\images\\background.jpg")
        self.bgImg2 = pygame.image.load("..\\images\\background.jpg")
        self.bg_x1 = (self.settings.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.settings.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600

        self.points = 1
        self.counter = 1

        self.car = Car(self, pygame)
        pygame.display.set_icon(self.car.carImg)

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.settings.display_width, self.settings.display_height))

        self.run_car()

    def run_car(self):

        while True:
            self._check_events()

            self.set_background()
            self.car.update()
            self.car.show(self)
            self.road()
            self.show_text()
            pygame.display.update()
            self.clock.tick(300)

    def set_background(self):
        self.gameDisplay.fill(self.settings.black_color)
        self.gameDisplay.blit(self.bgImg1, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg2, (self.bg_x2, self.bg_y2))

    def road(self):
        self.bg_y1 += self.settings.car_y_speed
        self.bg_y2 += self.settings.car_y_speed
        if self.bg_y1 >= 600:
            self.bg_y1 -= 1200
        if self.bg_y2 >= 600:
            self.bg_y2 -= 1200

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.car.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.car.moving_left = False

        # print("x: {x}, y: {y}".format(x=self.car.car_x_coordinate, y=self.car.car_y_coordinate))

    def _check_keydown_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.car.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.car.moving_left = True

    def show_text(self):
        self.counter += 1
        if self.counter % 10 == 0:
            self.points += 1 * self.settings.increase

        if self.counter % 10 == 0:
            if self.settings.increase < 0.8:
                self.settings.increase += 0.001
                if self.counter % 1000 == 0:
                    self.settings.car_y_speed += self.settings.increase
                    if self.settings.car_y_speed > 5:
                        self.settings.car_y_speed = 5
                    self.settings.car_x_speed += self.settings.increase / 3
            print(f'increase is: {self.settings.increase}')
            # print(f'y speed is: {self.settings.car_y_speed}')
            # print(f'x speed is: {self.settings.car_x_speed}')
            print('-' * 30)

        text = self.font.render(f'Points : {int(self.points)}', True, self.settings.green_color)
        text2 = self.font.render(f'<-- {int(self.settings.increase * 200)}', True,
                                 (self.settings.car_y_speed * 48, 255 - self.settings.car_y_speed * 48, 0))
        text3 = self.font.render(f'Speed', True, self.settings.white_color)
        text_rect = text.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text2.get_rect()
        text_rect.center = (150, 580)
        text_rect2.center = (722, 520 - self.settings.increase * 400)
        text_rect3.center = (700, 520)
        self.gameDisplay.blit(text, text_rect)
        self.gameDisplay.blit(text2, text_rect2)
        self.gameDisplay.blit(text3, text_rect3)
        # pygame.draw.rect(self.gameDisplay, self.settings.blue_color, (670, 300, 10, 200))
        gradientRect(self.gameDisplay, (255, 0, 0), (255, 255, 0), pygame.Rect(670, 200, 10, 300))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
