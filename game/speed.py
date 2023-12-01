import pygame
import random
import sys
import os
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racing Game")

class Background:
    def __init__(self, length, width, height, bg_type):
        self.length = length
        self.width = width
        self.height = height
        self.race_scale = 0.8 if length > 2 else 1 if length == 2 else 1.2
        self.bg_type = bg_type
        self.load_images()
        
    def load_images(self):
        self.background = pygame.image.load('./assets/BG-pic/galaxy.jpg' if self.bg_type == 3 else
                                            './assets/BG-pic/jungle.jpg' if self.bg_type == 2 else
                                            './assets/BG-pic/underwater.jpg')
                
        self.image = self.load_and_scale_image('./assets/race/race-mid.png')
        self.race_start = self.load_and_scale_image('./assets/race/race-start.png')
        self.race_end = self.load_and_scale_image('./assets/race/race-end.png')
        self.end_width = self.race_end.get_width()

    def load_and_scale_image(self, path):
        image = pygame.image.load(path)
        image.set_alpha(120)
        image_width = image.get_width()
        image_height = image.get_height()
        image = pygame.transform.scale(image,(int(self.race_scale*image_width),int(self.race_scale*image_height)))
        return image

    def draw_background(self, window):
        window.blit(self.background, (0, 0))
        num_repetitions = self.width // self.image.get_width() + 1
        for i in range(num_repetitions):
            window.blit(self.image, (i * self.image.get_width(), self.height - self.image.get_height() - 10))  # Render the image at each multiple of image width
            window.blit(self.race_start, (0, self.height - self.image.get_height() - 10))
            window.blit(self.race_end, (self.width - self.end_width, self.height - self.image.get_height() - 10))


class Player:
    def __init__(self, x, y, normal_image, turnaround_image):
        self.x = x  # player's x-coordinate
        self.y = y  # player's y-coordinate
        self.speed = random.uniform(1, 3)  
        self.speed_multiplier = 1.0 # Use to change player's speed when experiencing powerup's effect
        self.power_up_timer = 0 # time that powerup takes effect
        self.power_up = None
        self.normal_image = normal_image
        self.turnaround_image = turnaround_image
        self.current_image = normal_image
        self.order = 0
        self.finished = False

class PowerUpIcon:
    def __init__(self, x, y, type, image):
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.type = type
        self.image = image
        self.timer = 0
        self.active = True  # active attribute checks if a power-up is still active
        self.collided = False
        
class Announcement:
    def __init__(self):
        self.announce_font = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.announce_render = None
        self.announce_position = None
        
    def update_power_up(self, text):
        
        self.announce_render = self.announce_font.render(text, True, (22, 27, 33), (248,248,255))
        self.announce_position = (bg.width // 2 - self.announce_render.get_width() // 2, 10 + self.announce_render.get_height() // 2)
        
    def update_finish(self, text):
        self.announce_render = self.announce_font.render(text, True, (244, 169, 80), (22, 27, 33))
        self.announce_position = (bg.width // 2 - self.announce_render.get_width() // 2, 60 + self.announce_render.get_height() // 2)
    
    def draw_power_up(self):
        border_rect_1 = pygame.Rect(310, 15, 660, 50)     
        pygame.Surface.fill(window, (248,248,255), border_rect_1)
        pygame.draw.rect(window, (255,0,0),border_rect_1 , 3)

        if self.announce_render is not None and self.announce_position is not None:
            window.blit(self.announce_render, self.announce_position)
            
    def draw_finish(self):
        border_rect_2 = pygame.Rect(310, 65, 660, 50)
        pygame.Surface.fill(window, (22, 27, 33), border_rect_2)
        pygame.draw.rect(window, (255,0,0),border_rect_2 , 3)
        if self.announce_render is not None and self.announce_position is not None:
            window.blit(self.announce_render, self.announce_position)

class Game:
    def __init__(self, num_player_set, num_power_up_icons):
        self.width = 1280
        self.height = 720
        self.player_size = 40 if bg.length > 2 else 50 if bg.length == 2 else 60
        self.num_players = 6
        self.num_player_set = num_player_set
        self.num_power_up_icons = num_power_up_icons
        self.players = []
        self.power_up_icons = []
        self.power_ups = ["SpeedUp", "SlowDown", "TurnAround", "Restart", "StraightToFinish", "Teleport"]
        self.power_up_probabilities = [0.02, 0.04, 0.03, 0.03, 0.005, 0.03]
        self.power_up_images = {power_up: pygame.transform.scale(pygame.image.load(os.path.join("assets/icons/buff", f"powerup{i+1}.png")), (self.player_size, self.player_size))
                               for i, power_up in enumerate(self.power_ups)}
        self.mystery_icon = pygame.transform.scale(pygame.image.load(os.path.join("assets/icons/buff", f"unknown.png")), (self.player_size, self.player_size))
        self.text_power_up = None
        self.text_finish = None

    def draw_powerup_icons(self):
        for power_up_icon in self.power_up_icons:
            if power_up_icon.active:
                window.blit(power_up_icon.image, power_up_icon.rect.topleft)
            if power_up_icon.collided:
                power_up_icon.active = False
                if power_up_icon.timer > 0:
                    power_up_icon.timer -= 1
                    window.blit(power_up_icon.image, power_up_icon.rect.topleft)


    def draw_players(self):
        for player in self.players:
            window.blit(player.current_image, (player.x, player.y))

    def create_players(self):
        if bg.length == 2:
            self.players = [Player(0, bg.height - bg.image.get_height() +  85*i,
                        pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/Set {self.num_player_set}", f"{i+1}.png")), (self.player_size, self.player_size)),
                        pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/Set {self.num_player_set}", f"{i+1}.png")), (self.player_size, self.player_size)), True, False)
                        )
                    for i in range(self.num_players)]
        
        elif bg.length > 2:
            self.players = [Player(0, bg.height - bg.image.get_height() +  65*i,
                        pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/Set {self.num_player_set}", f"{i+1}.png")), (self.player_size, self.player_size)),
                        pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/Set {self.num_player_set}", f"{i+1}.png")), (self.player_size, self.player_size)), True, False)
                        )
                    for i in range(self.num_players)]
        
        else:   
            self.players = [Player(0, bg.height - bg.image.get_height() +  102*i,
                        pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/Set {self.num_player_set}", f"{i+1}.png")), (self.player_size, self.player_size)),
                        pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/Set {self.num_player_set}", f"{i+1}.png")), (self.player_size, self.player_size)), True, False)
                        )
                    for i in range(self.num_players)]
        
        # Save y-coordinate of all players for later use
        self.all_y_coordinates = [player.y for player in self.players]
        # create a copy
        self.available_y_coordinates = [player.y for player in self.players]

    def create_power_up_icons(self):
        self.power_up_icons = []

    def add_random_power_up_icon(self):
        # stop adding creating power-up when exceeding the limit number
        if len(self.power_up_icons) >= self.num_power_up_icons:
            return

        # Check if the list of available y-coordinates is empty
        if not self.available_y_coordinates:
            # If empty, reset it to the initial state
            self.available_y_coordinates = self.all_y_coordinates.copy()

        # choose a random y-coordinate
        y = random.choice(self.available_y_coordinates)
        self.available_y_coordinates.remove(y)

        x = random.randint(200, self.width - 100)

        # power-ups will not appear behind the last player
        if x > min(player.x for player in self.players if player.y == y):
            icon = PowerUpIcon(x, y, None, self.mystery_icon)
            self.power_up_icons.append(icon)
        

    def apply_power_up(self, player):
        player_rect = pygame.Rect(player.x, player.y, self.player_size, self.player_size)
        if player.power_up == "SpeedUp":
            player.speed_multiplier = 2.0
        elif player.power_up == "SlowDown":
            player.speed_multiplier = 0.5
        elif player.power_up == "TurnAround":
            player.speed_multiplier = -1.0
            player.current_image = player.turnaround_image
        elif player.power_up == "Restart":
            player.x -= self.width - self.player_size
        elif player.power_up == "StraightToFinish":
            player.x = self.width - self.player_size
        elif player.power_up == "Teleport":
            player.x = random.randint(0, self.width // 2 - self.player_size)
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
                    player.x += random.uniform(2, 4)  # Tốc độ ngẫu nhiên

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
                        power_up_type = random.choices(self.power_ups, weights = self.power_up_probabilities)[0]
                        power_up_icon.type = power_up_type
                        power_up_icon.image = self.power_up_images[power_up_type]  # Change the icon to the actual power-up icon
                        power_up_icon.collided = True
                        power_up_icon.timer = 30
                        
                        player.power_up = power_up_type
                        player.power_up_timer = random.randint(60, 80)  # Power-up duration
                        
                        self.text_power_up = f"Player {self.players.index(player) + 1} got a power-up: {power_up_type}"
                        print(f"Player {self.players.index(player) + 1} got a power-up: {power_up_type}")

    def check_finish(self):
        for player in self.players:
            if not player.finished and player.x >= self.width - self.player_size:
                player.current_image = player.normal_image
                player.finished = True
                player.order = sum(p.finished for p in self.players)  # Thứ tự kết thúc
                self.text_finish = f"Player {self.players.index(player) + 1} finished the race at rank: {player.order}"
                print(f"Player {self.players.index(player) + 1} finished the race at rank: {player.order}")
                
    def show_rankings(self):
        bg.draw_background(window)
        RankingImg = pygame.image.load("assets/BG-pic/leaderboard.png")

        # Calculate the scaling factors to fit the image on the screen
        width_ratio = bg.width / RankingImg.get_width()
        height_ratio = bg.height / RankingImg.get_height()
        min_ratio = min(width_ratio, height_ratio)

        # Resize the image while maintaining the aspect ratio
        rankingImg = pygame.transform.scale(RankingImg, (int(RankingImg.get_width() * min_ratio), int(RankingImg.get_height() * min_ratio)))

        # Calculate the position to center the image on the screen
        img_x = (bg.width - rankingImg.get_width()) // 2
        img_y = (bg.height - rankingImg.get_height()) // 2

        # Draw the ranking image
        window.blit(rankingImg, (img_x, img_y))

        # Initialize font
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        
        # Sort players based on their order
        self.players.sort(key=lambda player: player.order)

        # Display player rankings
        for i, player in enumerate(self.players):
            rankText = myfont.render('Rank {0}:'.format(player.order), False, (255, 0, 0))
            window.blit(rankText, (300 + 150, 100 + 180 + i * 50))
            carsImg = pygame.transform.scale(player.normal_image, (50, 50))
            window.blit(carsImg, (300 + 500, 100 + 170 + i * 50))

            

    def countdown(self):
        running = True
        music = pygame.mixer.Sound('assets\sfx/race-countdown.mp3')
        music.play()
        time_sec = 3
        bg.draw_background(window)
        self.draw_players()
        pygame.display.update()
        
        # Tạo đối tượng Font
        font = pygame.font.Font(None, 50)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            bg.draw_background(window)
            self.draw_players()

            if time_sec > -1:
                mins, secs = divmod(time_sec, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)

                # Tạo Surface chứa văn bản
                text = font.render(timeformat, True, (255, 255, 255))

                # Vẽ văn bản lên màn hình
                window.blit(text, (10, 10))

                time.sleep(1)
                time_sec -= 1
            else:
                pygame.time.delay(500) # delay 0.5s
                self.run()

            pygame.display.update()

    def run(self):

        # Main game loop
        clock = pygame.time.Clock()
        running = True
        
        music = pygame.mixer.Sound('assets\musics\cars-and-bikes-mokkkamusic.mp3')
        music.play()
        
        announce1 = Announcement() 
        announce2 = Announcement()
    
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            finished_players = [player for player in self.players if player.finished]
            
            # Move players
            self.move_players()
            
            # Check if any player has collided with a power-up icon
            self.check_power_up_collided()
            

            # Check for boundaries
            self.check_boundaries()

            # Add a randon power-up if a random number created < 0.03 and nobody's finished the line yet
            if random.random() < 0.03 and len(finished_players) == 0:  
                self.add_random_power_up_icon()

            

            # Check for winners
            
            if len(finished_players) == self.num_players:
                print("All players reached the finish line!")
                pygame.time.delay(1000)
                self.show_rankings()
                pygame.display.update()
                pygame.time.delay(10000)
                
                 # exit main loop

            # Check for players reaching the finish line
            self.check_finish()
            
            # Draw background
            bg.draw_background(window)

            # Draw power-up icons
            self.draw_powerup_icons()
            # Draw players
            self.draw_players()
            
            # Update announcements
            announce1.update_power_up(self.text_power_up)
            announce2.update_finish(self.text_finish)
            
            # Draw announcements
            announce1.draw_power_up()
            announce2.draw_finish()

            # Update display
            pygame.display.flip()

            # Set frames per second
            clock.tick(60)  # 60 fps

        # Quit Pygame
        pygame.quit()
        sys.exit()

bg = Background(length = 2, width = 1280, height = 720, bg_type = 2)
bg.draw_background(window)

# Initialize the game
game = Game(num_player_set = 3, num_power_up_icons = 20)

# Create players and power-up icons
game.create_players()
game.create_power_up_icons()

# Run the game
game.countdown()