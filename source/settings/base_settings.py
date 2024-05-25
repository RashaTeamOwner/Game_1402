

class Settings:
    white_color = (255, 255, 255)
    red_color = (255, 0, 0)
    black_color = (0, 0, 0)
    green_color = (0, 255, 0)
    blue_color = (0, 0, 255)

    def __init__(self, display_width: int = 900, display_height: int = 600, color: tuple = white_color):
        self.display_width = display_width
        self.display_height = display_height
        self.car_x_speed = 2.0
        self.car_y_speed = 2.0

        self.max_num_cars = 4

        self.increase = 0.0


