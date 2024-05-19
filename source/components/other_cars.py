import random
import pygame
from pygame.sprite import Sprite



class EnemyCar(Sprite):
    def __init__(self, ai_game, x):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.carImg = random.choice([pygame.image.load('..\\images\\car1.png'), pygame.image.load('..\\images\\car.png'), pygame.image.load('..\\images\\car2.png')])
        self.car_x_coordinate = random.choice([355,425,495])

        try:
            last_y = self.ai_game.enemy_cars.sprites()[-1].car_y_coordinate
        except:
            last_y = 0

        temp = random.randrange(0,600) * -1
        if last_y - 100 < temp:
            temp = last_y - 150



        self.car_y_coordinate = temp
        self.car_width = 50
        self.rect = pygame.Rect(self.car_x_coordinate - 1, self.car_y_coordinate, 48, 100)
        self.rect.x = self.car_x_coordinate
        self.rect.y = self.car_y_coordinate



    def show(self, game):
        game.gameDisplay.blit(self.carImg, self.rect)

    def update(self, x):

        self.car_y_coordinate += self.ai_game.settings.car_y_speed * x / 10

        self.rect.y = self.car_y_coordinate


