import pygame, sys, random, math
from pygame.locals import *


WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
FPS = 60
SIZE = 4.5 # Kích thước viên đạn nổ ra
SPEED_CHANGE_SIZE = 0.05 # Tốc độ nhỏ lại của viên đạn khi nổ ra
CHANGE_SPEED = 0.07 # Tốc độ chậm lại của viên đạn
RAD = math.pi/180 # Đỏi từ radian sang độ
A_FALL = 1.2 # Gia tốc rơi tự do
NUM_BULLET = 50 # Số đạn nổ ra trong 1 quả pháo
SPEED_MIN = 2 # Tốc độ nhỏ nhất của 1 viên đạn
SPEED_MAX = 4 # Tốc độ lớn nhất của một viên đạn
TIME_CREAT_FW = 40 # Khoảng thời gian liên tiếp giữa 2 lần bắn
NUM_FIREWORKS_MAX = 5 # Số lượng pháo lớn nhất bắn lên
NUM_FIREWORKS_MIN = 1 # Số lượng pháo nhỏ nhất bắn lên
SPEED_FLY_UP_MAX = 12 # Tốc độ lớn nhất của viên đạn bay lên (trước khi nổ)
SPEED_FLY_UP_MIN = 8 # Tốc độ nhỏ nhất của viên đạn bay lên (trước khi nổ)
TRANSPARENT_COLOR = (0, 0, 0, 0)  # Màu trong suốt RGBA

class Dot(): # Những chấm theo sau của mỗi viên đạn
    def __init__(self, x, y, size, color, window):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.window = window
    def update(self):
        # Giảm kích thước chấm
        if self.size > 0:
            self.size -= SPEED_CHANGE_SIZE*5
        else:
            self.size = 0
    def draw(self): # Vẽ một chấm
        if self.size > 0:
            pygame.draw.circle(self.window, self.color, (int(self.x), int(self.y)), int(self.size))


class BulletFlyUp(): # Viên đạn bay lên trước khi nổ
    def __init__(self, speed, x, window):
        self.speed = speed
        self.x = x
        self.y = WINDOWHEIGHT
        self.dots = [] # Một list các chấm theo sau
        self.size = SIZE/2
        self.color = (255, 255, 100)
        self.window = window

    def update(self):
        self.dots.append(Dot(self.x, self.y, self.size, self.color, self.window)) # Mỗi lần đạn đi qua sẽ có một chấm thêm vào
        # Xác định lại vị trí viên đạn
        self.y -= self.speed
        self.speed -= A_FALL*0.1
        # update từng chấm
        for dot in self.dots:
            dot.update()
        # Xoá những chấm có kích thước <= 0
        for dot in self.dots:
            if dot.size <= 0:
                self.dots.pop(self.dots.index(dot))

    def draw(self):
        pygame.draw.circle(self.window, self.color, (int(self.x), int(self.y)), int(self.size)) # Vẽ viên đạn
        # Vẽ từng chấm
        for dot in self.dots:
            dot.draw()



class Bullet(): # Viên đạn sau khi nổ
    def __init__(self, x, y, speed, angle, color, window):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle # Góc hợp bởi viên đạn và phương ngang
        self.size = SIZE
        self.color = color
        self.window = window

    def update(self):
        # Xác định tốc độ theo 2 phương
        speedX = self.speed * math.cos(self.angle*RAD)
        speedY = self.speed * -math.sin(self.angle*RAD)
        # Xác định lại vị trí viên đạn
        self.x += speedX
        self.y += speedY
        self.y += A_FALL
        # Giảm tốc độ đạn
        if self.size > 0:
            self.size -= SPEED_CHANGE_SIZE
        else:
            self.size = 0
        # Giảm kích thước đạn
        if self.speed > 0:
            self.speed -= CHANGE_SPEED
        else:
            self.speed = 0

    def draw(self): # Vẽ 1 viên đạn
        if self.size > 0:
            pygame.draw.circle(self.window, self.color, (int(self.x), int(self.y)), int(self.size))


class FireWork(): # Quả pháo hoa
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.dots = [] # List các chấm theo sau mỗi viên đạn
        self.window = window

        def creatBullets(): # Tạo list các viên đạn
            bullets = []
            color = Random.color()
            for i in range(NUM_BULLET):
                angle =  (360/NUM_BULLET)*i
                speed = random.uniform(SPEED_MIN, SPEED_MAX)
                bullets.append(Bullet(self.x, self.y, speed, angle, color, self.window))
            return bullets
        self.bullets = creatBullets();

    def update(self):
        for bullet in self.bullets: # update từng viên đạn
            bullet.update()
            self.dots.append(Dot(bullet.x, bullet.y, bullet.size, bullet.color, self.window))
        for dot in self.dots: # update từng chấm
            dot.update()
        # Xoá những chấm có kích thước <= 0
        for dot in self.dots:
            if dot.size <= 0:
                self.dots.pop(self.dots.index(dot))

    def draw(self):
        for bullet in self.bullets: # Vẽ từng viên đạn
            bullet.draw()
        for dot in self.dots: # Vẽ từng chấm
            dot.draw()

class Random():
    def __init__(self):
        pass

    def color(): # Tạo màu ngẫu nhiên (màu sáng)

        color1 = random.randint(0, 255)
        color2 = random.randint(0, 255)
        if color1 + color2 >= 255:
            color3 = random.randint(0, 255)
        else:
            color3 = random.randint(255 - color1 - color2, 255)
        colorList = [color1, color2, color3]
        random.shuffle(colorList)
        return colorList
    def num_fireworks(): # Số pháo mỗi lần bắn
        return random.randint(NUM_FIREWORKS_MIN, NUM_FIREWORKS_MAX)
    def randomBulletFlyUp_speed(): # Tốc độ viên đạn bay lên
        speed = random.uniform(SPEED_FLY_UP_MIN, SPEED_FLY_UP_MAX)
        return speed
    def randomBulletFlyUp_x(): # Vị trí viên đạn bay lên
        x = random.randint(int(WINDOWWIDTH*0.2), int(WINDOWWIDTH*0.8))
        return x
