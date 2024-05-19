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
        self.car_y_coordinate = x - random.randrange(110,600)
        self.car_width = 50
        self.rect = self.carImg.get_rect()
        self.rect.x = self.car_x_coordinate


    def show(self, game):
        game.gameDisplay.blit(self.carImg, self.rect)

    def update(self, x):

        self.car_y_coordinate += self.ai_game.settings.car_y_speed * x / 10

        self.rect.y = self.car_y_coordinate



