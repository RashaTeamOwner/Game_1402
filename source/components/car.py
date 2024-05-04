class Car:
    def __init__(self, game, pygame):
        self.settings = game.settings
        self.game = game
        self.carImg = pygame.image.load('..\\images\\car.png')
        self.car_x_coordinate = (game.settings.display_width / 2) - 25
        self.car_y_coordinate = (game.settings.display_height * 0.82)
        self.car_width = 50
        self.moving_right = False
        self.moving_left = False
        # Background

    def show(self, game):
        game.gameDisplay.blit(self.carImg, (self.car_x_coordinate, self.car_y_coordinate))

    def update(self):
        if self.moving_right:
            self.car_x_coordinate += self.settings.car_x_speed
            if self.car_x_coordinate >= 510:
                self.moving_right = False
                self.car_x_coordinate = 495

                if self.settings.car_y_speed > 1:
                    self.settings.increase /= 2
                    self.settings.car_y_speed /= 2
                    self.settings.car_x_speed /= 2

                if self.game.points > 100:
                    self.game.points -= 100
                else:
                    self.game.points = 0
            # print("CAR X COORDINATES: %s" % self.car_x_coordinate)
        if self.moving_left:
            self.car_x_coordinate -= self.settings.car_x_speed
            if self.car_x_coordinate <= 340:
                self.moving_left = False
                self.car_x_coordinate = 355

                if self.settings.car_y_speed > 1:
                    self.settings.increase /= 2
                    self.settings.car_y_speed /= 2
                    self.settings.car_x_speed /= 2

                if self.game.points > 100:
                    self.game.points -= 100
                else:
                    self.game.points = 0
            # print("CAR X COORDINATES: %s" % self.car_x_coordinate)

        # Update rect object from self.x.
