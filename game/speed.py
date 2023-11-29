import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
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

class Player:
    def __init__(self, x, y, speed, image, normal_image, turnaround_image, current_image, order, finished):
        self.x = x
        self.y = y
        self.speed = speed
        self.speed_multiplier = 1.0
        self.power_up_timer = 0
        self.power_up = None
        self.image = image
        self.normal_image = normal_image
        self.turnaround_image = turnaround_image
        self.current_image = current_image
        self.order = order
        self.finished = finished

class PowerUpIcon:
    def __init__(self, x, y, type, image):
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.type = type
        self.image = image
        self.active = True  # Thêm thuộc tính active để kiểm tra xem biểu tượng có còn hoạt động không

class Game:
    def __init__(self, width, height, player_size, num_players, num_power_up_icons):
        self.width = width
        self.height = height
        self.player_size = player_size
        self.num_players = num_players
        self.num_power_up_icons = num_power_up_icons
        self.players = []
        self.power_up_icons = []
        self.power_ups = ["SpeedUp", "SlowDown", "TurnAround", "GoBack", "StraightToFinish", "MoveToPosition"]
        self.power_up_probabilities = [0.05, 0.05, 0.03, 0.01, 0.01, 0.03]
        self.power_up_images = {power_up: pygame.transform.scale(pygame.image.load(os.path.join("assets/icons/buff", f"powerup{i+1}.png")), (player_size, player_size)) for i, power_up in enumerate(self.power_ups)}
        self.mystery_icon = pygame.transform.scale(pygame.image.load(os.path.join("assets/icons/buff", f"unknown.png")), (self.player_size, self.player_size))
        # self.running = True

    def draw_background(self):
        window.blit(background, (0, 0))
        for i in range(num_repetitions):
            window.blit(image, (i * image_width, 100))  # Render the image at each multiple of image width
        window.blit(race_start, (0, 100))
        window.blit(race_end, (self.width - end_width, 100))

    def draw_powerup_icons(self):
        for power_up_icon in self.power_up_icons:
            if power_up_icon.active:
                window.blit(power_up_icon.image, power_up_icon.rect.topleft)

    def draw_players(self):
        for player in self.players:
            window.blit(player.current_image, (player.x, player.y))

    def create_players(self):
        self.players = [Player(0, 110 +85*i, random.uniform(1, 3), image,
                               pygame.transform.scale(pygame.image.load(os.path.join("assets/sets/Set 3", f"player{i+1}.png")), (self.player_size, self.player_size)),
                               pygame.transform.scale(pygame.image.load(os.path.join("assets/sets/Set 3", f"rplayer{i+1}.png")), (self.player_size, self.player_size)),
                               pygame.transform.scale(pygame.image.load(os.path.join("assets/sets/Set 3", f"player{i+1}.png")), (self.player_size, self.player_size)),
                               0, False)
                          for i in range(self.num_players)]

    def create_power_up_icons(self):
        self.power_up_icons = []

    def add_random_power_up_icon(self):
        if len(self.power_up_icons) >= self.num_power_up_icons:
            return

        player = random.choice(self.players)
        x = random.randint(200, self.width - 100)
        y = player.y

        # Bua chi xuat hien tren doan duong phia truoc nguoi choi
        if x > player.x:
            icon = PowerUpIcon(x, y, None, self.mystery_icon)
            self.power_up_icons.append(icon)
        

    def apply_power_up(self, player):
        player_rect = pygame.Rect(player.x, player.y, self.player_size, self.player_size)  # Định nghĩa player_rect ở đây
        if player.power_up == "SpeedUp":
            player.speed_multiplier = 1.5
        elif player.power_up == "SlowDown":
            player.speed_multiplier = 0.5
        elif player.power_up == "TurnAround":
            player.speed_multiplier *= -1.0
            player.current_image = player.turnaround_image
        elif player.power_up == "GoBack":
            player.x -= self.width - self.player_size
        elif player.power_up == "StraightToFinish":
            player.x = self.width - self.player_size
        elif player.power_up == "MoveToPosition":
            player.x = random.randint(player.y, self.width // 2 - self.player_size)

        # Tìm biểu tượng bùa liên quan và đặt active về False khi hiệu ứng kết thúc
        for power_up_icon in self.power_up_icons:
            if power_up_icon.rect.colliderect(player_rect) and power_up_icon.type == player.power_up and power_up_icon.active:
                power_up_icon.active = False
                break
        player.power_up = None

    def move_players(self):
        for player in self.players:
            if not player.finished:
                if player.power_up_timer > 0:
                    player.power_up_timer -= 1
                    self.apply_power_up(player)
                    player.x += player.speed * player.speed_multiplier
                else:
                    player.current_image = player.normal_image
                    player.x += random.uniform(1, 3)  # Tốc độ ngẫu nhiên

    def check_boundaries(self):
        for player in self.players:
            if player.x < 0:
                player.x = 0
            elif player.x > self.width - self.player_size:
                player.x = self.width - self.player_size

    def check_power_up_collided(self):
        for player in self.players:
            player_rect = pygame.Rect(player.x, player.y, self.player_size, self.player_size)
            for power_up_icon in self.power_up_icons:
                if player_rect.colliderect(power_up_icon.rect):
                    if power_up_icon.type is None:
                        power_up_type = random.choices(self.power_ups, weights=self.power_up_probabilities)[0]
                        power_up_icon.type = power_up_type
                        print(f"Player {self.players.index(player) + 1} got a power-up: {power_up_type}")
                        player.power_up = power_up_type
                        player.power_up_timer = random.randint(60, 80)  # Power-up duration
                        power_up_icon.image = self.power_up_images[power_up_type]  # Change the icon to the actual power-up icon
                        #break  # Exit the loop as the player can only pick up one power-up at a time

    # def check_winners(self):
    #     finished_players = [player for player in self.players if player.finished]
    #     if len(finished_players) == self.num_players:
    #         print("All players reached the finish line!")
    #         self.running = False

    def check_finish(self):
        for player in self.players:
            if not player.finished and player.x >= self.width - self.player_size:
                player.current_image = player.normal_image
                player.finished = True
                player.order = sum(p.finished for p in self.players)  # Thứ tự kết thúc
                print(f"Player {self.players.index(player) + 1} finished in {player.order}th place!")
                player.y = player.y  # Giữ nguyên hàng ngang cuối cùng mà họ đạt được

    def run(self):
        
        # Main game loop
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Move players
            self.move_players()

            # Check for boundaries
            self.check_boundaries()

            # Check if it's time to add a random power-up icon
            if random.random() < 0.02:  # Thay đổi giá trị này để điều chỉnh tần suất xuất hiện
                self.add_random_power_up_icon()

            # Check if any player has collided with a power-up icon
            self.check_power_up_collided()

            # Check for winners
            finished_players = [player for player in self.players if player.finished]
            if len(finished_players) == self.num_players:
                print("All players reached the finish line!")
                running = False

            # Check for players reaching the finish line
            self.check_finish()

            # Draw the tiled image horizontally
            self.draw_background()

            # Draw power-up icons
            self.draw_powerup_icons()
            # Draw players
            self.draw_players()

            # Update display
            pygame.display.flip()

            # Set frames per second
            clock.tick(60)  # 60 fps

        # Quit Pygame
        pygame.quit()
        sys.exit()

# Initialize the game
game = Game(1280, 720, 50, 6, 10)

# Create players and power-up icons
game.create_players()
game.create_power_up_icons()

# Run the game
game.run()
