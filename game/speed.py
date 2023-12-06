import pygame
import random
import sys
import os
import time
from PIL import Image
from control_button import selector, run_test, sel
from firework import BulletFlyUp, FireWork, Random

def run_race():
    # Set up display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bet the Best - Racing Game")

    class Background:
        def __init__(self, width, height):
            self.length = sel.activated_buttons[2]
            self.width = width
            self.height = height
            self.race_scale = 0.8 if self.length == 'long' else 1 if self.length == 'mid' else 1.2
            self.bg_type = sel.activated_buttons[0] # can be modified to meet up with player's choice
            self.load_images()
            
        def load_images(self):
            # Set background based on player's choice in control_button.py
            self.background = pygame.image.load('./assets/BG-pic/galaxy.jpg' if self.bg_type == 'galaxy' else
                                                './assets/BG-pic/jungle.jpg' if self.bg_type == 'jungle' else
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
        def __init__(self, x, y, normal_image, turnaround_image, name):
            self.x = x  # player's x-coordinate
            self.y = y  # player's y-coordinate
            self.speed = random.uniform(1, 3)  # take out a random float number from 1 to 3 and assign to player's speed
            self.speed_multiplier = 1.0 # Use to change player's speed when experiencing powerup's effect
            self.power_up_timer = 0 # time that powerup takes effect
            self.normal_image = normal_image    #update normal_image of each player
            self.turnaround_image = turnaround_image    # update reverse image of each player, used for TurnAround power-up
            self.current_image = normal_image   # work as a temporary image to switch between normal and reverse images
            self.order = 0  # update each player's finish order, initialized at 0
            self.finished = False   # update each player's finish status, initialized at False
            self.name = name    # update each player's name, for later use

        @staticmethod    
        def draw_players():
            for player in game.players:
                window.blit(player.current_image, (player.x, player.y))

    class PowerUpIcon:
        
        def __init__(self, x, y, type, image):
            self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())    # the rectangular area surrounding the power-ups
            self.type = type    # power-up's type
            self.image = image  # power-up's image
            self.timer = 0  # power-up's real image existing time
            self.active = True  # used to draw mystery power-ups on screen, set to False when the real ones appear
            self.collided = False   # check if players meet the power-ups, set to False if they meet
            self.power_up_size = 40 if bg.length == 'long' else 50 if bg.length == 'mid' else 60
            self.power_ups = ["SpeedUp", "SlowDown", "TurnAround", "Restart", "StraightToFinish", "Teleport"]   # list of power-ups
            self.power_up_probabilities = [0.1, 0.04, 0.03, 0.02, 0.005, 0.02] #The corresponding probabilities of power-ups in the list
            # Update and process power-ups' images
            self.power_up_images = {power_up: pygame.transform.scale(pygame.image.load(os.path.join("assets/icons/buff", f"powerup{i+1}.png")), (self.power_up_size, self.power_up_size)) for i, power_up in enumerate(self.power_ups)}

        @staticmethod    
        def create_power_up_icons():
            game.power_up_icons = []

        @staticmethod
        # Create randon power-ups on the race
        def add_random_power_up_icon():
            
            # stop adding creating power-up when exceeding the limit number
            if len(game.power_up_icons) >= game.num_power_up_icons:
                return

            # Check if the list of available y-coordinates is empty
            if len(game.available_y_coordinates) == 0:
                # If empty, reset it to the initial state
                game.available_y_coordinates = game.all_y_coordinates.copy()

            x = random.randint(200, width - 150)
            # choose a random y-coordinate
            y = random.choice(game.available_y_coordinates)
            game.available_y_coordinates.remove(y)

            # power-ups will not appear behind the last player
            if x > min(player.x for player in game.players if player.y == y):
                power_up_size = 40 if bg.length == 'long' else 50 if bg.length == 'mid' else 60
                mystery_icon = pygame.transform.scale(pygame.image.load(os.path.join("assets/icons/buff", f"unknown.png")), (power_up_size, power_up_size))
                # create a mystery power-up and add to the power_up_icons list
                icon = PowerUpIcon(x, y, None, mystery_icon)
                game.power_up_icons.append(icon)
                
        @staticmethod
        def draw_powerup_icons():
            # loop through each power-up in the list
            for power_up_icon in game.power_up_icons:
                
                #check if player meets the power-up
                if power_up_icon.collided:
                    power_up_icon.active = False    # stop displaying the mystery one
                    if power_up_icon.timer > 0:
                        power_up_icon.timer -= 1
                        window.blit(power_up_icon.image, power_up_icon.rect.topleft)    # display real power-up until timer countdown ends
                
                # check if mystery power-up still active then display it
                elif power_up_icon.active:
                    window.blit(power_up_icon.image, power_up_icon.rect.topleft)
                    
    class Announcement:
        def __init__(self):
            self.announce_font = pygame.font.Font('assets/font/#9Slide03 Roboto Condensed Bold.ttf', 30)
            self.announce_render = None
            self.announce_position = None
            
        def update_power_up(self, text):
            self.announce_render = self.announce_font.render(text, True, (22, 27, 33))
            self.announce_position = self.center_text(310, 15, 660, 50)
            
        def update_finish(self, text):
            self.announce_render = self.announce_font.render(text, True, (244, 169, 80))
            self.announce_position = self.center_text(310, 66, 660, 50)
        
        def center_text(self, x, y, width, height):
            text_width, text_height = self.announce_render.get_size()
            return (x + (width - text_width) // 2, y + (height - text_height) // 2)
        
        def draw_power_up(self):
            board_1 = pygame.Rect(310, 15, 660, 50)     
            pygame.Surface.fill(window, (248,248,255), board_1)
            pygame.draw.rect(window, (30,144,255),board_1 , 3)

            if self.announce_render is not None and self.announce_position is not None:
                window.blit(self.announce_render, self.announce_position)
                
        def draw_finish(self):
            board_2 = pygame.Rect(310, 66, 660, 50)
            pygame.Surface.fill(window, (22, 27, 33), board_2)
            pygame.draw.rect(window, (30,144,255),board_2 , 3)
            
            if self.announce_render is not None and self.announce_position is not None:
                window.blit(self.announce_render, self.announce_position)

    class Game:
        def __init__(self, num_power_up_icons):
            self.width = 1280
            self.height = 720
            self.num_players = 6
            # update set character based on what player choooses
            self.num_player_set = 'Set 1' if sel.activated_buttons[1] == 'set1' else \
                      'Set 2' if sel.activated_buttons[1] == 'set2' else \
                      'Set 3' if sel.activated_buttons[1] == 'set3' else \
                      'Set 4' if sel.activated_buttons[1] == 'set4' else \
                      'Set 5' if sel.activated_buttons[1] == 'set5' else \
                      'Set 6' if sel.activated_buttons[1] == 'set6' else \
                      'Set 7'
            
            self.num_power_up_icons = num_power_up_icons    # modify the number of power-ups
            self.players = []
            self.finished_players = []
            self.power_up_icons = []
            self.player_size = 40 if bg.length == 'long' else 50 if bg.length == 'mid' else 60
            self.power_up_size = 40 if bg.length == 'long' else 50 if bg.length == 'mid' else 60
            self.all_y_coordinates = [] # the set of player.y so that the power-ups can appear on their races
            self.available_y_coordinates = []   #the set of player.y but it instantly changes to create power-ups
            self.text_power_up = None   # text on board 1
            self.text_finish = None # text on board 2
            
        def create_players(self):
            player_size = 40 if bg.length == 'long' else 50 if bg.length == 'mid' else 60
            if bg.length == 'mid':
                self.players = [Player(0, bg.height - bg.image.get_height() +  85*i,
                            pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/{self.num_player_set}", f"{i+1}.png")), (player_size, player_size)),
                            pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/{self.num_player_set}", f"{i+1}.png")), (player_size, player_size)), True, False),
                            sel.char_dict[i+1]
                            )
                        for i in range(self.num_players)]
            
            elif bg.length == 'long':
                self.players = [Player(0, bg.height - bg.image.get_height() +  65*i,
                            pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/{self.num_player_set}", f"{i+1}.png")), (player_size, player_size)),
                            pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/{self.num_player_set}", f"{i+1}.png")), (player_size, player_size)), True, False),
                            sel.char_dict[i+1]
                            )
                        for i in range(self.num_players)]
            
            else:   
                self.players = [Player(0, bg.height - bg.image.get_height() +  102*i,
                            pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/{self.num_player_set}", f"{i+1}.png")), (player_size, player_size)),
                            pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(f"assets/sets/{self.num_player_set}", f"{i+1}.png")), (player_size, player_size)), True, False),
                            sel.char_dict[i+1]
                            )
                        for i in range(self.num_players)]
            
            # Save y-coordinate of all players for later use
            self.all_y_coordinates = [player.y for player in self.players]
            # create a copy
            self.available_y_coordinates = [player.y for player in self.players]
            
        def create_power_up_icons(self):
            PowerUpIcon.create_power_up_icons()

        def add_random_power_up_icon(self):
            # Add a randon power-up if a random number created < 0.03 and nobody's finished the line yet
            if random.random() < 0.04 and len(self.finished_players) == 0: 
                PowerUpIcon.add_random_power_up_icon()
    
        def apply_power_up(self, player):
            
            if player.power_up == "SpeedUp":
                player.speed_multiplier = 2.0
                pygame.mixer.Sound('assets\sfx\speedup.mp3').play()
                
            elif player.power_up == "SlowDown":
                player.speed_multiplier = 0.5
                pygame.mixer.Sound('assets\sfx\slow.mp3').play()
                
            elif player.power_up == "TurnAround":
                player.speed_multiplier = -1.0
                player.current_image = player.turnaround_image
                pygame.mixer.Sound('assets\sfx/reverse.mp3').play()
                
            elif player.power_up == "Restart":
                player.x = 0
                pygame.mixer.Sound('assets\sfx/reset.mp3').play()            
                
            elif player.power_up == "StraightToFinish":
                player.x = self.width - self.player_size
                pygame.mixer.Sound('assets\sfx\stun.mp3').play()
                
            elif player.power_up == "Teleport":
                player.x = random.randint(0, self.width - self.player_size - 100)
                pygame.mixer.Sound('assets\sfx/teleport.mp3').play() 
                
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
                            power_up_type = random.choices(power_up_icon.power_ups, weights = power_up_icon.power_up_probabilities)[0]
                            power_up_icon.type = power_up_type
                            power_up_icon.image = power_up_icon.power_up_images[power_up_type]  # Change the icon to the actual power-up icon
                            power_up_icon.collided = True
                            power_up_icon.timer = 30
                            
                            player.power_up = power_up_type
                            player.power_up_timer = random.uniform(60,90)  # Power-up duration
                            
                            self.text_power_up = f"{player.name} (p.{self.players.index(player) + 1}) got a power-up: {power_up_type}"
                            print(f"{player.name} (p.{self.players.index(player) + 1}) got a power-up: {power_up_type}")

        def check_finish(self):
            for player in self.players:
                if not player.finished and player.x >= self.width - self.player_size:
                    player.current_image = player.normal_image
                    player.finished = True
                    player.order = sum(p.finished for p in self.players)  # Thứ tự kết thúc
                    if player.order == 1:
                        pygame.mixer.Sound('assets\sfx\winner.mp3').play()
                    self.text_finish = f"{player.name} (p.{self.players.index(player) + 1}) finished the race at rank: {player.order}"
                    print(f"{player.name} (p.{self.players.index(player) + 1}) finished the race at rank: {player.order}")

        def draw_players(self):
            Player.draw_players()
                        
        def draw_powerup_icons(self):
            PowerUpIcon.draw_powerup_icons()
            
        def firework(self):
            clock = pygame.time.Clock()
            running = True
            
            fireWorks = []
            time_create = 30 # Khoảng thời gian liên tiếp giữa 2 lần bắn
            bulletFlyUps = []
            display_timer = 300 # Khoảng thời gian bắn pháo hoa
   
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                # draw background
                bg.draw_background(window)
                
                # Draw players
                self.draw_players()
                
                announce1.draw_power_up()
                announce2.draw_finish()
                        
                if (display_timer > -1):

                    if time_create == 30: # Tạo (những) viên đạn bay lên sau khoảng thời gian xác đinh
                        for i in range(Random.num_fireworks()):
                            bulletFlyUps.append(BulletFlyUp(Random.randomBulletFlyUp_speed(), Random.randomBulletFlyUp_x(), window))

                    for bulletFlyUp in bulletFlyUps:
                        bulletFlyUp.draw()
                        bulletFlyUp.update()

                    for fireWork in fireWorks:
                        fireWork.draw()
                        fireWork.update()

                    for bulletFlyUp in bulletFlyUps:
                        if bulletFlyUp.speed <= 0: # Viên đạn bay lên đạt độ cao tối đa
                            fireWorks.append(FireWork(bulletFlyUp.x, bulletFlyUp.y, window)) # Tạo quả pháo ngay vị trí viên đạn
                            bulletFlyUps.pop(bulletFlyUps.index(bulletFlyUp)) # Xoá viên đạn đó

                    # Xoá quả pháo hoa khi kích thước những viên đạn <= 0
                    for fireWork in fireWorks:
                        if fireWork.bullets[0].size <= 0:
                            fireWorks.pop(fireWorks.index(fireWork))

                    # Đếm khoảng thời gian bắn
                    if time_create <= 30:
                        time_create += 1
                    else:
                        time_create = 0
                        
                    display_timer -= 1
     
                    pygame.display.flip()
                    clock.tick(60)
                
                else:
                    pygame.display.flip()
                    running = False
        
        
        def show_rankings(self):
            bg.draw_background(window)

            # Load RankingImg
            RankingImg = Image.open("assets/BG-pic/leaderboard.png")

            # Calculate the dimensions of the frame
            frame_width = RankingImg.width // 4 + 10
            frame_height = RankingImg.height // 4 + 10
            frame = pygame.Surface((frame_width, frame_height))

            # Calculate the dimensions of the image display area
            image_width = RankingImg.width // 4
            image_height = RankingImg.height // 4

            # Resize and center the image
            RankingImg = RankingImg.resize((image_width, image_height), Image.Resampling.LANCZOS)
            scaled_image = pygame.image.fromstring(RankingImg.tobytes(), RankingImg.size, RankingImg.mode)
            image_rect = scaled_image.get_rect(center=(frame_width // 2, frame_height // 2))

            # Blit the image onto the frame
            frame.blit(scaled_image, image_rect.topleft)

            # Sort players based on their order
            self.players.sort(key=lambda player: player.order)

            # Render and display ranking information
            myfont = pygame.freetype.Font('assets/font/#9Slide03 Roboto Condensed Bold.ttf', 30)
            for i, player in enumerate(self.players):
                # Render the text onto a new Surface
                rank_text_surface, rank_text_rect = myfont.render('{0}'.format(player.name), (255, 255, 255))

                # Calculate the position of the text to center it in the frame
                rank_text_position = ((frame_width - rank_text_rect.width) // 2, image_rect.top + 197 + i * 55)
                player_postion = (535, image_rect.top + 185 + i * 55)

                # Draw the text onto the frame
                frame.blit(rank_text_surface, rank_text_position)
                
                player_img = pygame.transform.scale(player.normal_image, (50, 50))
                frame.blit(player_img, player_postion)

            # Calculate the position of the frame on the main window
            frame_rect = frame.get_rect(center=(self.width // 2, self.height // 2))

            # Draw the frame onto the main window
            window.blit(frame, frame_rect.topleft)
            
            # Get the current time and format it as a string
            current_time = time.strftime("%H%M%S_%d%m%Y") 

            # Save the entire window to a file with the current time in the filename
            pygame.image.save(window, os.path.join("assets/screenshots", "screenshot_" + current_time + ".png"))  

            pygame.display.flip()


        def countdown(self):
            running = True
            countdown_music = pygame.mixer.Sound('assets\sfx/race-countdown.mp3')
            countdown_music.play()
            
            bg.draw_background(window)
            Player.draw_players()
            pygame.display.update()
            time_sec = 3
            
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
                    pygame.time.delay(800) # delay 0.5s
                    self.run()  # start run() - main game

                pygame.display.update()
            
            # Quit Pygame
            pygame.quit()
            sys.exit()

        def run(self):
            global announce1, announce2
            
            # Main game loop
            clock = pygame.time.Clock()
            running = True
            
            race_music = pygame.mixer.Sound('assets\musics/round.mp3')
            race_music.play()
            
            race_noise = pygame.mixer.Sound('assets\sfx/racing-noise.mp3')
            pygame.mixer.Sound.set_volume(race_noise, 0.4)
            race_noise.play()
            
            announce1 = Announcement() 
            announce2 = Announcement()
        
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                self.finished_players = [player for player in self.players if player.finished]
                
                # Move players
                self.move_players()
                
                # Check if any player has collided with a power-up icon
                self.check_power_up_collided()
                
                # Check for boundaries
                self.check_boundaries()

                self.add_random_power_up_icon()
                
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
                
                # Check for winners
                if len(self.finished_players) == self.num_players:
                    print("All players reached the finish line!")
                    race_noise.stop()
                    self.firework()
                    race_music.stop()
                    
                    # show leaderboard
                    self.show_rankings()
                    pygame.mixer.Sound('assets\sfx/victory.mp3').play()
                    pygame.time.delay(4000)
                    running = False
                    # exit main loop

                # Update display
                pygame.display.flip()

                # Set frames per second
                clock.tick(60)  # 60 fps

            # Quit Pygame
            pygame.quit()
            sys.exit()

    
    bg = Background(width = 1280, height = 720)
    bg.draw_background(window)

    # Initialize the game
    game = Game(num_power_up_icons = 20)

    # Create players and power-up icons
    game.create_players()
    game.create_power_up_icons()

    # Run the game
    game.countdown()
    
if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    run_test()
    run_race()