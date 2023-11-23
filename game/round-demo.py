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

# Set up players
player_size = 50
num_players = 6

# Adjust starting positions and y-coordinates
players = [{"x": 0, "y": 110 +85*i,
            "speed": random.uniform(2, 5), "speed_multiplier": 1.0, "power_up_timer": 0, "power_up": None, "image": image,
            "normal_image": pygame.transform.scale(pygame.image.load(os.path.join("assets/sets/Set 3", f"player{i+1}.png")), (player_size, player_size)),
            "turnaround_image": pygame.transform.scale(pygame.image.load(os.path.join("assets/sets/Set 3", f"rplayer{i+1}.png")), (player_size, player_size)),
            "current_image": pygame.transform.scale(pygame.image.load(os.path.join("assets/sets/Set 3", f"player{i+1}.png")), (player_size, player_size)),  # Dùng để lưu ảnh hiện tại của người chơi
            "order": 0, "finished": False}
           for i in range(num_players)]

# Set up power-ups
power_ups = ["SpeedUp", "SlowDown", "TurnAround", "GoBack", "StraightToFinish", "MoveToPosition"]
power_up_probabilities = [0.05, 0.05, 0.05, 0.01, 0.01, 0.03]

# Apply power-up effects
def apply_power_up(player):
    global players
    if player["power_up"] == "SpeedUp":
        player["speed_multiplier"] = 3.0  # Hệ số tăng tốc là 3
    elif player["power_up"] == "SlowDown":
        player["speed_multiplier"] = 0.5
    elif player["power_up"] == "TurnAround":
        player["speed_multiplier"] *= -1.0  # Đảo chiều tốc độ
        player["current_image"] = player["turnaround_image"]
    elif player["power_up"] == "GoBack":
        player["x"] -= width - player_size
    elif player["power_up"] == "StraightToFinish":
        player["x"] = width - player_size
    elif player["power_up"] == "MoveToPosition":
        player["x"] = random.randint(0, width // 2 - player_size)
        player["power_up"] = None  # Kết thúc hiệu ứng bùa

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move players
    for player in players:
        if not player["finished"]:
            if player["power_up_timer"] > 0:
                player["power_up_timer"] -= 1
                apply_power_up(player)
                player["x"] += player["speed"] * player["speed_multiplier"]
            else:
                player["current_image"] = player["normal_image"]
                player["x"] += random.uniform(2, 5)  # Tốc độ ngẫu nhiên       

            # Check for boundaries
            if player["x"] < 0:
                player["x"] = 0
            elif player["x"] > width - player_size:
                player["x"] = width - player_size

    # Generate power-ups
    for player in players:
        if not player["finished"] and random.random() < 0.01 and player["power_up"] is None:
            power_up_type = random.choices(power_ups, weights=power_up_probabilities)[0]
            print(f"Player {players.index(player) + 1} got a power-up: {power_up_type}")
            player["power_up"] = power_up_type
            player["power_up_timer"] = random.randint(10, 20)  # Thời gian dính bùa

    # Draw the tiled image horizontally
    window.blit(background,(0,0))
    for i in range(num_repetitions):
        window.blit(image, (i * image_width, 100))  # Render the image at each multiple of image width
    window.blit(race_start, (0, 100))
    window.blit(race_end, (width - end_width, 100))
    pygame.display.flip()  # Update the display

    # Draw players
    for player in players:
        window.blit(player["current_image"], (player["x"], player["y"]))

    # Check for winners
    finished_players = [player for player in players if player["finished"]]
    if len(finished_players) == num_players:
        print("All players reached the finish line!")
        running = False

    # Check for players reaching the finish line
    for player in players:
        if not player["finished"] and player["x"] >= width - player_size:
            player["current_image"] = player["normal_image"]
            player["finished"] = True
            player["order"] = sum(p["finished"] for p in players)  # Thứ tự kết thúc
            print(f"Player {players.index(player) + 1} finished in {player['order']}th place!")
            player["y"] = player["y"]  # Giữ nguyên hàng ngang cuối cùng mà họ đạt được

    # Update display
    pygame.display.flip()

    # Set frames per second
    clock.tick(30)  # 30 fps

# Quit Pygame
pygame.quit()
sys.exit()