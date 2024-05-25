import random
from time import sleep
import sys
import pygame

from components.car import Car
from settings import Settings
from components import Car, EnemyCar

pygame.mixer.init()
brake_sound = pygame.mixer.Sound("..\\sounds\\brake-6315.mp3")
crashed_sound = pygame.mixer.Sound("..\\sounds\\crash-7075.mp3")
horn_sound = pygame.mixer.Sound("..\\sounds\\automobile-horn.mp3")

with open('file.txt', 'r+') as f:
    try:
        MAX_SCORE = int(f.readline().strip())
    except ValueError:
        # If the file is empty or doesn't contain a valid number, set the current number to 0
        MAX_SCORE = 0


def gradientRect(window, left_colour, right_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour, (0, 0), (1, 0))  # left colour line
    pygame.draw.line(colour_rect, right_colour, (0, 1), (1, 1))  # right colour line
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)


def save_point(points):
    """
    تابعی برای ذخیره امتیاز بالاتر در فایل
    :param points:
    :return:
    """
    with open('file.txt', 'r+') as f:
        try:
            current_number = int(f.readline().strip())
        except ValueError:
            # If the file is empty or doesn't contain a valid number, set the current number to 0
            current_number = 0

        if int(points) > current_number:
            # Truncate the file to remove the existing content
            f.truncate(0)
            # Move the file pointer to the beginning of the file
            f.seek(0)
            # Write the new number to the file
            f.write(str(int(points)))


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

        self.state = 's'  # or 'p'  | Setting mode or Playing mode

        self.game_over = False
        self.chances = 3  # chances is 3  for fill hearts

        self.heart_outline = pygame.image.load("..\\images\\heart_outline.png")
        self.heart_fill = pygame.image.load("..\\images\\heart_fill.png")

        self.car = Car(self)
        self.enemy_cars = pygame.sprite.Group()

        pygame.display.set_icon(self.car.carImg)

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.settings.display_width, self.settings.display_height))

        self.run_car()

    def run_car(self):
        if self.state == 's':  # playing music in menu for first time
            pygame.mixer.music.load('..\\sounds\\Michael_Hunter_Grand_Theft_Auto_San_Andreas_Official_Theme_S.mp3')
            pygame.mixer.music.play(-1)

        while True:

            self._check_events()  # مدیریت کلیک ها

            if not self.game_over:  # چک کردن حالت گیم اور

                if self.state == 's':  # چک کردن حالت تنظیمات Setting
                    self.set_setting_background()  # فراخوانی تابع برای صفحه تنظیمات

                if self.state == 'p':  # شروع حالت بازی کردن
                    self.set_background()
                    self.car.update()
                    self.car.show(self)

                    self.road()
                    self.speed_change()
                    self.show_text()

                    if self.brake:
                        pygame.mixer.Sound.play(brake_sound)  # صدای بوق

            pygame.display.update()
            self.clock.tick(120)

            if self.game_over:
                # ---- نمایش متن گیم اور -------
                text = pygame.font.Font('freesansbold.ttf', 100).render(f'GAME OVER', True, self.settings.green_color,
                                                                        self.settings.red_color)
                text_rect = text.get_rect()
                text_rect.center = (450, 300)
                self.gameDisplay.blit(text, text_rect)

                # ----- نمایش متن امتیازات -----
                text = pygame.font.Font('freesansbold.ttf', 50).render(f'Points : {int(self.points)}', True,
                                                                       self.settings.green_color,
                                                                       self.settings.black_color)
                text_rect = text.get_rect()
                text_rect.center = (450, 375)
                self.gameDisplay.blit(text, text_rect)

                # ---- نمایش متن اینتر بزنین -----
                text = pygame.font.Font("freesansbold.ttf", 50).render(f'Press Enter To Play', True,
                                                                       self.settings.white_color,
                                                                       self.settings.black_color)
                text_rect = text.get_rect()
                text_rect.center = (450, 420)
                self.gameDisplay.blit(text, text_rect)

                # صدا زدن تابع ذخیره امتیازات
                save_point(self.points)

    def set_background(self):
        self.gameDisplay.fill(self.settings.black_color)
        self.gameDisplay.blit(self.bgImg1, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg2, (self.bg_x2, self.bg_y2))

    def road(self):

        for enemy_car in self.enemy_cars.copy():
            #  اگر ماشینی از پایین صفحه خارج شد حذف شود
            if enemy_car.car_y_coordinate > 700:
                self.enemy_cars.remove(enemy_car)

        if len(self.enemy_cars) < self.settings.max_num_cars:  #  تعداد ماشین های روی صفحه باید برابر با این مقدار باشند
            new_enemy = EnemyCar(self)
            self.enemy_cars.add(new_enemy)

        for enemy_car in self.enemy_cars.sprites():
            # تغییر جایگاه ماشین ها
            enemy_car.update()

        for enemy_car in self.enemy_cars.sprites():
            # نمایش ماشین ها
            enemy_car.show(self)

        # مکانیزم تکرار پس زمینه و شناور شدن جاده
        self.bg_y1 += self.settings.car_y_speed
        self.bg_y2 += self.settings.car_y_speed
        if self.bg_y1 >= 600:
            self.bg_y1 -= 1200
        if self.bg_y2 >= 600:
            self.bg_y2 -= 1200

    def _check_events(self):
        """
        چک کردن فشرده شدن کلید ها
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # اگه ضربدر زده شد امتیاز را سیو کن و پنجره را ببند
                save_point(self.points)
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                # چک کردن فشرده شدن موس
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])  # گرفتن مکان موس
                button = pygame.Rect(340, 190, 244, 60)  # مختصات دکمه شروع
                if button.collidepoint(mouse_pos) and self.state == 's':
                    # جک کردن اینکه آیا کلیک روی دکمه بوده یا خیر
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.state = 'p'
                    self.chances = 3
                    # آماده سازی برای شروع و پخش صدای استارت
                    car_start_sound = pygame.mixer.Sound("..\\sounds\\carengine-5998.mp3")
                    pygame.mixer.Sound.play(car_start_sound)
                    pygame.mixer.music.stop()  # ایست صدای منو
                    pygame.mixer.music.load("..\\sounds\\lamborghini-urus-racing-sound-effect-163336 (mp3cut.net).mp3")
                    # پخش صدای ماشین
                    pygame.mixer.music.play(-1)

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


    def _check_keydown_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.car.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.car.moving_left = True

        elif event.key == pygame.K_SPACE:
            self.brake = True


        elif event.key == pygame.K_RETURN and self.game_over:
            # فشردن دکمه اینتر در حالت گیم اور
            for enemy_car in self.enemy_cars.sprites():
                # پاک کردن ماشینهای دشمن
                self.enemy_cars.remove(enemy_car)

            # قرار دادن بازی در حالت تنظیمات و پخش آهنگ منو (S)
            self.state = 's'
            pygame.mixer.music.load('..\\sounds\\Michael_Hunter_Grand_Theft_Auto_San_Andreas_Official_Theme_S.mp3')
            pygame.mixer.music.play(-1)

            # ----------  ریستارت کردن بازی و متغیر های اولیه ------------------
            self.points = 1
            self.counter = 1
            self.settings = Settings(color=(230, 230, 230))

            # نمایش بیشترین امتیاز در روی صفحه
            global MAX_SCORE
            with open('file.txt', 'r+') as f:
                try:
                    MAX_SCORE = int(f.readline().strip())
                except ValueError:
                    MAX_SCORE = 0
            self.game_over = False

        elif event.key == pygame.K_h:
            # کلید بوق
            pygame.mixer.Sound.play(horn_sound)

    def show_text(self):

        text = self.font.render(f'Points : {int(self.points)}', True, self.settings.green_color)
        text2 = self.font.render(f'<-- {int(self.settings.car_y_speed * 32)}', True,
                                 (self.settings.car_y_speed * 42.5, 255 - self.settings.car_y_speed * 42.5, 0))
        text3 = self.font.render(f'Speed', True, self.settings.white_color)
        text4 = self.font.render(f'MAX_SCORE : {MAX_SCORE}', True, self.settings.white_color)

        text_rect = text.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()
        text_rect4 = text4.get_rect()
        text_rect.center = (150, 580)
        text_rect2.center = (722, 520 - self.settings.car_y_speed * 60)
        text_rect3.center = (700, 540)
        text_rect4.center = (100, 200)
        self.gameDisplay.blit(text, text_rect)
        self.gameDisplay.blit(text2, text_rect2)
        self.gameDisplay.blit(text3, text_rect3)
        self.gameDisplay.blit(text4, text_rect4)
        # pygame.draw.rect(self.gameDisplay, self.settings.blue_color, (670, 300, 10, 200))
        gradientRect(self.gameDisplay, (255, 0, 0), (0, 255, 0), pygame.Rect(670, 120, 10, 400))


        #  -------  نمایش قلب ها ------------
        for i in range(3):
            # سه عدد قلب خالی
            self.gameDisplay.blit(self.heart_outline, (650 + (i * 60), 30))

        for i in range(self.chances):
            # قلب پر به تعداد شانس ها
            self.gameDisplay.blit(self.heart_fill, (650 + (i * 60), 30))

    def speed_change(self):
        """
        متغیر کانتر فقط شمارنده است تا با توجه به آن بتوان بقیه مقادیر را مدیریت کرد
        :return:
        """
        self.counter += 1

        if self.brake:
            # حالت ترمز و کاهش سرعت
            if self.counter % 10 == 0:
                if self.settings.increase > 0.01:
                    self.settings.increase -= 0.0001 # ضرایبی که با آزمون و خطا به دست آمده
                if self.settings.car_y_speed > 1:
                    self.settings.car_y_speed -= max(0.01875, self.settings.increase * 10)
                    # این ضرایب با آزمون و خطا به دست آمده است

                if not self.settings.car_x_speed < 2:
                    self.settings.car_x_speed -= 0.006

        else:
            # حالت افزایش سرعت
            if self.counter % 10 == 0:
                self.points += 0.1 + self.settings.increase * 10
                self.settings.increase += 0.0001

            if self.counter % 10 == 0:
                if not self.settings.car_y_speed > 6:
                    self.settings.car_y_speed += max(0.01875, self.settings.increase)
                    if self.settings.car_y_speed > 6:
                        # مدیریت کردن اینکه سرعت از 6 بیشتر نشود
                        self.settings.car_y_speed = 6

                if not self.settings.car_x_speed > 3:
                    self.settings.car_x_speed += 0.006

    def set_setting_background(self):
        # صفحه منو یا تنظیمات
        self.gameDisplay.fill(self.settings.black_color)
        self.gameDisplay.blit(pygame.image.load("..\\images\\bgmain.png"), (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        if 584 > mouse_pos[0] > 340 and 250 > mouse_pos[1] > 190:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
