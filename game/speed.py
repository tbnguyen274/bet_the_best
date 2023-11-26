import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racing Game")

Length = 2
race_scale = 1
if Length == 1:
    race_scale = 1
elif Length == 2:
    race_scale = 0.7
else:
    race_scale = 0.5

# Load the image to be looped
background = pygame.image.load('./assets/BG-pic/galaxy.jpg')
image = pygame.image.load('./assets/race/race-mid.png')
image.set_alpha(120)
image_width = image.get_width()
image_height = image.get_height()
pygame.transform.scale(image,(int(race_scale*image_width),int(race_scale*image_height)))
race_start = pygame.image.load('./assets/race/race-start.png')
race_start.set_alpha(120)
race_s_w = race_start.get_width()
race_s_h = race_start.get_height()
pygame.transform.scale(race_start,(int(race_scale*race_s_w),int(race_scale*race_s_h)))
race_end = pygame.image.load('./assets/race/race-end.png')
race_end.set_alpha(120)
race_e_w = race_end.get_width()
race_e_h = race_end.get_height()
pygame.transform.scale(race_end,(int(race_scale*race_e_w),int(race_scale*race_e_h)))
end_width = race_end.get_width()

# Calculate the number of repetitions needed to fill the window horizontally
num_repetitions = width // image_width + 1  # Add 1 to ensure the whole window is filled

# class RacingBackground:
#     def __init__(self, width, height, length):
#         self.width, self.height = width, height
#         self.window = pygame.display.set_mode((width, height))

#         self.race_scale = self.calculate_race_scale(length)

#         # Load images
#         self.background = self.load_scaled_image('./assets/BG-pic/galaxy.jpg')
#         self.image = self.load_scaled_image('./assets/race/race-mid.png')
#         self.race_start = self.load_scaled_image('./assets/race/race-start.png')
#         self.race_end = self.load_scaled_image('./assets/race/race-end.png')
#         self.end_width = self.race_end.get_width()

#         self.num_repetitions = width // self.image.get_width() + 1

#     def calculate_race_scale(self, length):
#         if length == 1:
#             return 1
#         elif length == 2:
#             return 0.7
#         else:
#             return 0.5

#     def load_scaled_image(self, path):
#         image = pygame.image.load(path)
#         image.set_alpha(120)
#         scaled_width = int(self.race_scale * image.get_width())
#         scaled_height = int(self.race_scale * image.get_height())
#         return pygame.transform.scale(image, (scaled_width, scaled_height))

#     def draw_background(self):
#         total_width = self.num_repetitions * self.image.get_width()
#         for x in range(0, total_width, self.image.get_width()):
#             self.window.blit(self.image, (x, 0))

#         # Draw the start and end signs
#         self.window.blit(self.race_start, (0, 0))
#         self.window.blit(self.race_end, (self.width - self.end_width, 0))


# # Tạo đối tượng RacingBackground
# race_background = RacingBackground(width, height, 2)

# Người chơi
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image_original = pygame.transform.scale(pygame.image.load(image_path), (50, 50))
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = random.randint(1, 2)  # Tốc độ ban đầu ngẫu nhiên
        self.effect = None
        self.start_delay = 180  # Đếm ngược trước khi bắt đầu chạy
        self.is_running = False

    def update(self):
        # Đếm ngược trước khi bắt đầu chạy
        if self.start_delay > 0:
            self.start_delay -= 1
        else:
            self.is_running = True

        # Di chuyển người chơi khi đã bắt đầu chạy
        if self.is_running:
            self.rect.x += self.speed

            # Giữ người chơi trong khung cửa sổ
            if self.rect.left < 0:
                self.rect.left = 0
                self.speed = 0  # Dừng khi đến biên trái
            elif self.rect.right > width:
                self.rect.right = width
                self.speed = 0  # Dừng khi đến biên phải
                
        # Lật ngược hình ảnh khi tốc độ là âm
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image_original, True, False)
        else:
            self.image = self.image_original

# Chướng ngại vật
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image_path = image_path  # Thêm thuộc tính image_path để lưu đường dẫn của hình ảnh
        self.image = pygame.transform.scale(pygame.image.load(image_path), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.visible = False  # Khởi tạo chướng ngại vật ẩn đi
        self.effect_duration = 0  # Thêm thuộc tính để lưu thời gian của hiệu ứng

    def update(self):
        if self.effect_duration > 0:
            self.effect_duration -= 1
        else:
            self.visible = False
            self.kill()

# Hiệu ứng khi đụng chướng ngại vật
class Effect:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = pygame.time.get_ticks()  # Thời điểm bắt đầu hiệu ứng
        
    def speedup(self, player):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time < self.duration * 1000:  # Kiểm tra xem hiệu ứng đã kết thúc chưa
            player.speed *= 1.25

    def slow(self, player):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time < self.duration * 1000:  # Kiểm tra xem hiệu ứng đã kết thúc chưa
            player.speed *= 0.99
    
    def stun(self, player):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time < self.duration * 1000:  # Kiểm tra xem hiệu ứng đã kết thúc chưa
            player.speed = 0.8

    def rotate(self, player):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time < self.duration * 1000:  # Kiểm tra xem hiệu ứng đã kết thúc chưa
            player.speed *= -1
    
    def teleport(self, player):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time < self.duration * 1000:  # Kiểm tra xem hiệu ứng đã kết thúc chưa
            player.speed *= 1.5
    
    def restart(self, player):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time < self.duration * 1000:  # Kiểm tra xem hiệu ứng đã kết thúc chưa
            player.speed *= 1.5

    def goal(self, player):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time < self.duration * 1000:  # Kiểm tra xem hiệu ứng đã kết thúc chưa
            player.speed *= 1.5

# Tạo người chơi
players = [
    Player(0, 110, "assets/sets/Set 3/player1.png"),
    Player(0, 200, "assets/sets/Set 3/player2.png"),
    Player(0, 280, "assets/sets/Set 3/player3.png"),
    Player(0, 370, "assets/sets/Set 3/player4.png"),
    Player(0, 450, "assets/sets/Set 3/player5.png"),
    Player(0, 530, "assets/sets/Set 3/player6.png")
]

# Tạo chướng ngại vật
obstacle_types = [
    "assets/icons/buff/speedup.png",
    "assets/icons/buff/slow.png",
    "assets/icons/buff/stun.png",
    "assets/icons/buff/rotate.png",
    "assets/icons/buff/teleport.png",
    "assets/icons/buff/restart.png",
    "assets/icons/buff/goal.png"
]

# Xác suất xuất hiện cnv
power_up_probabilities = [0.05, 0.05, 0.05, 0.03, 0.02, 0.01, 0.01]

obstacles = []

# Thời điểm xuất hiện chướng ngại vật cuối cùng
time_since_last_obstacle = 0

# Khoảng thời gian giữa các chướng ngại vật (tính bằng frame)
time_to_next_obstacle = random.randint(30, 60)

# Vị trí hàng ngang của chướng ngại vật
obstacle_rows = [110, 200, 280, 370, 450, 530]

clock = pygame.time.Clock()

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Kiểm tra va chạm với chướng ngại vật
    for player in players:
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                obstacle.visible = True  # Hiển thị chướng ngại vật khi va chạm
                if obstacle.image_path == "assets/icons/buff/speedup.png":
                # Áp dụng hiệu ứng tăng tốc nếu là chướng ngại vật tăng tốc
                    player.effect = Effect(30)  # Hiệu ứng tăng tốc trong 3 giây
                    player.effect.speedup(player)
                    obstacle.effect_duration = 120  # Đặt thời gian hiệu ứng (3 giây * 60 frame/giây)
                    obstacle.visible = True

                elif obstacle.image_path == "assets/icons/buff/slow.png":
                    player.effect = Effect(120)
                    player.effect.slow(player)
                    obstacle.effect_duration = 120  # Đặt thời gian hiệu ứng (3 giây * 60 frame/giây)
                    obstacle.visible = True

                elif obstacle.image_path == "assets/icons/buff/stun.png":
                    player.effect = Effect(120)
                    player.effect.stun(player)
                    obstacle.effect_duration = 120  # Đặt thời gian hiệu ứng (3 giây * 60 frame/giây)
                    obstacle.visible = True

                elif obstacle.image_path == "assets/icons/buff/rotate.png":
                    player.effect = Effect(120)
                    player.effect.rotate(player)
                    obstacle.effect_duration = 120  # Đặt thời gian hiệu ứng (3 giây * 60 frame/giây)
                    obstacle.visible = True

                elif obstacle.image_path == "assets/icons/buff/teleport.png":
                    pass
                elif obstacle.image_path == "assets/icons/buff/restart.png":
                    pass
                elif obstacle.image_path == "assets/icons/buff/goal.png":
                    pass
                

        # Áp dụng hiệu ứng nếu có
        if player.effect:
            player.effect.duration -= 1
            if player.effect.duration == 0:
                player.effect = None
                player.speed = random.randint(1, 2)  # Khôi phục tốc độ ban đầu
                
            

        # Cập nhật người chơi
        player.update()

    

    # Tăng thời gian từ lần xuất hiện chướng ngại vật cuối cùng
    time_since_last_obstacle += 1

    # Kiểm tra nếu đã đến thời điểm xuất hiện chướng ngại vật mới
    if time_since_last_obstacle >= time_to_next_obstacle:
        # Chọn ngẫu nhiên một loại chướng ngại vật
        random_obstacle_type = random.choices(obstacle_types, weights = power_up_probabilities)[0]

        # Chọn ngẫu nhiên một hàng ngang để xuất hiện chướng ngại vật
        random_obstacle_row = random.choice(obstacle_rows)

        # Tạo chướng ngại vật
        obstacles.append(Obstacle(random.randint(200, width - 100), random_obstacle_row, random_obstacle_type))

        # Đặt lại thời điểm và khoảng thời gian cho lần xuất hiện chướng ngại vật tiếp theo
        time_since_last_obstacle = 0
        time_to_next_obstacle = random.randint(30, 60)  # Khoảng thời gian giữa các chướng ngại vật (tính bằng frame)

    # Vẽ màn hình
    screen.blit(background, (0, 0))
    for i in range(num_repetitions):
        screen.blit(image, (i * image_width, 100))  # Render the image at each multiple of image width
    screen.blit(race_start, (0, 100))
    screen.blit(race_end, (width - end_width, 100))

    # Vẽ người chơi và chướng ngại vật
    for player in players:
        screen.blit(player.image, player.rect)

    # Trong vòng lặp chính
    for obstacle in obstacles:
        if obstacle.visible:
            screen.blit(obstacle.image, obstacle.rect)
            obstacle.update()  # Cập nhật thời gian hiệu ứng


    pygame.display.flip()

    clock.tick(60)
