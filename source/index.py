import random
from time import sleep
import sys
import pygame

from components.car import Car
from settings import Settings
from components import Car, EnemyCar


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

        self.brake = False

        self.game_over = False

        self.car = Car(self)
        self.enemy_cars = pygame.sprite.Group()

        pygame.display.set_icon(self.car.carImg)

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.settings.display_width, self.settings.display_height))

        self.run_car()

    def run_car(self):

        while True:
            self._check_events()

            if not self.game_over:
                self.set_background()
                self.car.update()
                self.car.show(self)

                self.road()
                self.speed_change()
                self.show_text()
            pygame.display.update()
            self.clock.tick(120)

            if self.game_over:
                text = pygame.font.Font('freesansbold.ttf', 100).render(f'GAME OVER', True, self.settings.green_color,
                                                                        self.settings.red_color)
                text_rect = text.get_rect()
                text_rect.center = (450, 300)
                self.gameDisplay.blit(text, text_rect)
                text = pygame.font.Font('freesansbold.ttf', 50).render(f'Points : {int(self.points)}', True,
                                                                       self.settings.green_color,
                                                                       self.settings.black_color)
                text_rect = text.get_rect()
                text_rect.center = (450, 375)
                self.gameDisplay.blit(text, text_rect)

                with open('file.txt', 'r+') as f:
                    try:
                        current_number = int(f.readline().strip())
                    except ValueError:
                        # If the file is empty or doesn't contain a valid number, set the current number to 0
                        current_number = 0

                    if int(self.points) > current_number:
                        # Truncate the file to remove the existing content
                        f.truncate(0)
                        # Move the file pointer to the beginning of the file
                        f.seek(0)
                        # Write the new number to the file
                        f.write(str(int(self.points)))



    def set_background(self):
        self.gameDisplay.fill(self.settings.black_color)
        self.gameDisplay.blit(self.bgImg1, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg2, (self.bg_x2, self.bg_y2))


    def road(self):

        for enemy_car in self.enemy_cars.copy():
            if enemy_car.car_y_coordinate > 700:
                print('removed')
                self.enemy_cars.remove(enemy_car)

        if len(self.enemy_cars) < 3:
            try:
                x = self.enemy_cars.sprites()[-1].rect.bottom
                if x > 100:
                    x = 0
            except:
                x = 0
            new_enemy = EnemyCar(self, x)
            self.enemy_cars.add(new_enemy)

        for enemy_car in self.enemy_cars.sprites():
            x = random.randrange(1, 5)
            enemy_car.update(x)

        for enemy_car in self.enemy_cars.sprites():
            enemy_car.show(self)

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

        elif event.key == pygame.K_SPACE:
            self.brake = False

        # print("x: {x}, y: {y}".format(x=self.car.car_x_coordinate, y=self.car.car_y_coordinate))

    def _check_keydown_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.car.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.car.moving_left = True

        elif event.key == pygame.K_SPACE:
            self.brake = True

    def show_text(self):

        text = self.font.render(f'Points : {int(self.points)}', True, self.settings.green_color)
        text2 = self.font.render(f'<-- {int(self.settings.car_y_speed * 32)}', True,
                                 (self.settings.car_y_speed * 42.5, 255 - self.settings.car_y_speed * 42.5, 0))
        text3 = self.font.render(f'Speed', True, self.settings.white_color)
        text_rect = text.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text2.get_rect()
        text_rect.center = (150, 580)
        text_rect2.center = (722, 520 - self.settings.car_y_speed * 60)
        text_rect3.center = (700, 540)
        self.gameDisplay.blit(text, text_rect)
        self.gameDisplay.blit(text2, text_rect2)
        self.gameDisplay.blit(text3, text_rect3)
        # pygame.draw.rect(self.gameDisplay, self.settings.blue_color, (670, 300, 10, 200))
        gradientRect(self.gameDisplay, (255, 0, 0), (0, 255, 0), pygame.Rect(670, 120, 10, 400))

    def speed_change(self):
        self.counter += 1
        if self.brake:
            if self.counter % 10 == 0:
                if self.settings.increase > 0.01:
                    self.settings.increase -= 0.0001
                if self.settings.car_y_speed > 1:
                    self.settings.car_y_speed -= max(0.01875, self.settings.increase * 10)

                if not self.settings.car_x_speed < 2:
                    self.settings.car_x_speed -= 0.006

        else:
            if self.counter % 10 == 0:
                self.points += 0.1 + self.settings.increase * 10
                self.settings.increase += 0.0001

            if self.counter % 10 == 0:
                if not self.settings.car_y_speed > 6:
                    self.settings.car_y_speed += max(0.01875, self.settings.increase)

                if not self.settings.car_x_speed > 3:
                    self.settings.car_x_speed += 0.006


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
