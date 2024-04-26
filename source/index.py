from time import sleep
import sys
import pygame

class CarRacing:
    def __init__(self):
        
        pygame.init()
        self.display_width = 900
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        
        self.initialize()

    def initialize(self):

        self.carImg = pygame.image.load('..\\images\\car.png')
        self.car_x_coordinate = (self.display_width / 2) - 25
        self.car_y_coordinate = (self.display_height*0.82)
        self.car_width = 50
        # Background
        self.bgImg = pygame.image.load("..\\images\\background.jpg")
        self.bg_x = (self.display_width / 2) - (360 / 2)
        self.bg_y = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        
        self.run_car()

    def run_car(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # print(event)

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT):
                        self.car_x_coordinate -= 75
                        print ("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.car_x_coordinate += 75
                        print ("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    print ("x: {x}, y: {y}".format(x=self.car_x_coordinate, y=self.car_y_coordinate))

            self.gameDisplay.fill(self.black)
            self.gameDisplay.blit(self.bgImg, (self.bg_x, self.bg_y))

            self.car(self.car_x_coordinate, self.car_y_coordinate)
           
            pygame.display.update()
            self.clock.tick(60)

        


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
