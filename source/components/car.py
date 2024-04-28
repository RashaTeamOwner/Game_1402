class Car:
    def __init__(self, game, pygame):
        self.carImg = pygame.image.load('..\\images\\car.png')
        self.car_x_coordinate = (game.settings.display_width / 2) - 25
        self.car_y_coordinate = (game.settings.display_height * 0.82)
        self.car_width = 50
        # Background


    def show(self, game):
        game.gameDisplay.blit(self.carImg, (self.car_x_coordinate, self.car_y_coordinate))
