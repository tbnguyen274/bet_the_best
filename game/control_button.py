import cv2
import sys
import pygame
import random
import datetime
import time
pygame.init()

exitSelect = False
running = True
from mainmenu import isFullscreen
if isFullscreen:
    screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((1280, 720))
close_button = pygame.image.load('assets/icons/close.png')
close_button = pygame.transform.scale(close_button, (50, 50))
close_button_rect = close_button.get_rect(topleft = (1220, 10))
Fullscreen = False
class VideoPlayer:
    def __init__(self, video_path):
        self.video_capture = cv2.VideoCapture(video_path)
        pygame.init()

    def loop_background(self):
        ret, frame = self.video_capture.read()
        if not ret:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video_capture.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (1280, 720))
        pygame_frame = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
        screen.blit(pygame_frame, (0, 0))


class ToggleButton:
    def __init__(self, x, y, image_path, scale=1.0 ):
        self.x = x
        self.y = y
        self.image_path = image_path
        self.original_image = pygame.image.load(self.image_path)
        self.scale = scale
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale),
                                                                  int(self.original_image.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.click_sound = pygame.mixer.Sound('assets/sfx/pop-click-sound.mp3')
        self.click_sound.set_volume(0.2)

    def draw(self, screen):
        border_size = 3  # Kích thước viền

        # Tạo hình chữ nhật viền lớn hơn nút
        border_rect = pygame.Rect(self.rect.x - border_size, self.rect.y - border_size,
                                  self.rect.width + border_size * 2, self.rect.height + border_size * 2)

        if self.clicked:
            # Vẽ viền gradient màu xanh lá
            gradient_rect = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
            gradient = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
            for alpha in range(0, 255, 10):  # Tăng dần alpha để tạo gradient
                gradient.fill((255, 255, 51, alpha), (0, alpha, border_rect.width, 10))
            gradient_rect.blit(gradient, (0, 0))
            screen.blit(gradient_rect, (border_rect.x, border_rect.y))

        screen.blit(self.image, self.rect.topleft)

    @staticmethod
    def check_click(event, buttons):
        for button in buttons:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.rect.collidepoint(event.pos):
                    button.clicked = not button.clicked  # Toggle button state
                    button.click_sound.play()  # Play click sound

                    # Disable other buttons when a button is clicked
                    if button.clicked:
                        for other_button in buttons:
                            if other_button != button:
                                other_button.clicked = False

    @staticmethod
    def turn_off_all(buttons):
        for button in buttons:
            button.clicked = False

class ToggleButton2:
    def __init__(self, x, y, image_path, scale=1.0):
        self.x = x
        self.y = y
        self.image_path = image_path
        self.original_image = pygame.image.load(self.image_path)
        self.scale = scale
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale),
                                                                  int(self.original_image.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked_image = self.darken_image(self.original_image)  # Tạo hình ảnh sậm đi khi nút được nhấn
        self.rect_clicked = self.clicked_image.get_rect(topleft=(x, y))
        self.clicked = False
        self.click_sound = pygame.mixer.Sound('assets/sfx/pop-click-sound.mp3')
        self.click_sound.set_volume(0.2)

    def darken_image(self, image):
        # Tạo bản sao của hình ảnh gốc với màu sậm đi (ở đây tôi chọn màu đen nhẹ)
        darkened_image = image.copy()
        darkened_image.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_SUB)  # Điều chỉnh mức độ sậm màu
        return darkened_image

    def draw(self, screen):
        if self.clicked:
            screen.blit(self.clicked_image, self.rect_clicked.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)

    @staticmethod
    def check_click(event, buttons):
        for button in buttons:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.rect.collidepoint(event.pos):
                    button.clicked = not button.clicked  # Toggle button state
                    button.click_sound.play()  # Play click sound

                    # Disable other buttons when a button is clicked
                    if button.clicked:
                        for other_button in buttons:
                            if other_button != button:
                                other_button.clicked = False
    
    @staticmethod
    def turn_off_all(buttons):
        for button in buttons:
            button.clicked = False


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image_rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.action = False
        self.image_alpha = self.image.copy()
        self.image_alpha.set_alpha(160)

    def draw(self, screen):
        click_sound = pygame.mixer.Sound('assets/sfx/pop-click-sound.mp3')
        click_sound.set_volume(0.2)
        cursor_pos = pygame.mouse.get_pos()
        if self.image_rect.collidepoint(cursor_pos):
            screen.blit(self.image_alpha, (self.image_rect.x, self.image_rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                click_sound.play()
                self.action = True
        else:
            screen.blit(self.image, (self.image_rect.x, self.image_rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
#random ten
random_name = [
    "Kai", "Zara", "Cleo", "Hiro", "Aiko", "Ezra", "Luna", "Zain", "Nala", "Remy",
    "Enzo", "Faye", "Idris", "Kato", "Zola", "Azra", "Niam", "Orla", "Ziva", "Zayd",
    "Kiran", "Rohan", "Ida", "Veda", "Kato", "Cian", "Tari", "Ilya", "Soren", "Ozra"
]

class TextInput:
    def __init__(self, x, y, width, height, font_size, color_inactive, color_active, font_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color = self.color_inactive
        self.font_color = font_color
        self.font = pygame.font.Font(None, font_size)
        self.text = ""
        self.txt_surface = self.font.render(self.text, True, self.font_color)
        self.active = False
        self.error_message = ""  # Add this line to store the error message
        self.error_time = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_SPACE:
                    if self.text == "":
                        self.text = random.choice(random_name)
                        random_name.remove(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_DELETE:
                    random_name.append(self.text)
                    self.text = ''
                else:
                    temp_text = self.text + event.unicode
                    temp_surface = self.font.render(temp_text, True, self.font_color)
                    if temp_surface.get_width() < self.rect.w and len(temp_text) <= 6:  # Add length check here
                        self.text = temp_text
                self.txt_surface = self.font.render(self.text, True, self.font_color)
            if event.key == pygame.K_SPACE :
                if self.text == "":
                    self.text = random.choice(random_name)
                    random_name.remove(self.text)
                self.txt_surface = self.font.render(self.text, True, self.font_color)

    def handle_event2(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_DELETE:
                    self.text = ''
                else:
                    temp_text = self.text + event.unicode
                    temp_surface = self.font.render(temp_text, True, self.font_color)
                    if temp_surface.get_width() < self.rect.w:
                        self.text = temp_text
                self.txt_surface = self.font.render(self.text, True, self.font_color)

    def validate_input(self, current_money):
        if self.text.isdigit():
            number = int(self.text)
            if number > current_money:
                self.set_error_message("Not enough money!")
            elif number < 100:
                self.set_error_message("Minimum bet is 100!")
            else:
                now = datetime.datetime.now()  # Get the current date and time
                # with open('spending_history.txt', 'a') as f:
                #     f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {str(number)}\n")  # Write the date, time, and number to the file
        elif self.text != "":
            self.set_error_message("Invalid number!")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)  # Fill the rectangle with color
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        # Only draw the error message if it's been less than 1.5 seconds
        if time.time() - self.error_time < 1.5:
            error_surface = self.font.render(self.error_message, True, pygame.Color('firebrick2'))
            screen.blit(error_surface, (self.rect.x, self.rect.y + self.rect.h + 20))

    def set_error_message(self, message):
        self.error_message = message
        self.error_time = time.time()

    def naming_character(self):
        return self.text

clock = pygame.time.Clock()


class selector:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.shortRace = ToggleButton2(280, 600, 'assets/icons/buttons/button_short.png')
        self.midRace = ToggleButton2(530, 600, 'assets/icons/buttons/button_medium.png')
        self.longRace = ToggleButton2(780, 600, 'assets/icons/buttons/button_long.png')

        # Ô ĐẶT TÊN
        self.namebox = [
            TextInput(50, 300, 140, 40, 35, pygame.color.Color('#2F3C7E'), pygame.color.Color('#4831D4'), pygame.color.Color('#CCF381')),
            TextInput(250, 300, 140, 40, 35, pygame.color.Color('#2F3C7E'), pygame.color.Color('#4831D4'), pygame.color.Color('#CCF381')),
            TextInput(450, 300, 140, 40, 35, pygame.color.Color('#2F3C7E'), pygame.color.Color('#4831D4'), pygame.color.Color('#CCF381')),
            TextInput(650, 300, 140, 40, 35, pygame.color.Color('#2F3C7E'), pygame.color.Color('#4831D4'), pygame.color.Color('#CCF381')),
            TextInput(850, 300, 140, 40, 35, pygame.color.Color('#2F3C7E'), pygame.color.Color('#4831D4'), pygame.color.Color('#CCF381')),
            TextInput(1050, 300, 140, 40, 35, pygame.color.Color('#2F3C7E'), pygame.color.Color('#4831D4'), pygame.color.Color('#CCF381')),
        ]
        self.bet_box = TextInput(450, 495, 200, 35, 35, 'grey70', 'grey80', 'black')
        self.bet = 0
        #uw la underwater, j la jungle, g la galaxy
        self.set1 = ToggleButton(450, 330, 'assets/sets/Set 1/1.png', 0.3)
        self.set2 = ToggleButton(640, 330, 'assets/sets/Set 2/1.png', 0.3)
        self.set3 = ToggleButton(470, 330, 'assets/sets/Set 3/1.png', 0.3)
        self.set4 = ToggleButton(660, 360, 'assets/sets/Set 4/1.png', 0.3)
        self.set5 = ToggleButton(370, 330, 'assets/sets/Set 5/1.png', 0.3)
        self.set6 = ToggleButton(560, 330, 'assets/sets/Set 6/1.png', 0.3)
        self.set7 = ToggleButton(770, 330, 'assets/sets/Set 7/2.png', 0.3)

        self.set1_char = [
            ToggleButton(20, 130, 'assets/sets/Set 1/1.png', 0.22),
            ToggleButton(210, 130, 'assets/sets/Set 1/2.png', 0.22),
            ToggleButton(460, 130, 'assets/sets/Set 1/3.png', 0.22),
            ToggleButton(650, 130, 'assets/sets/Set 1/4.png', 0.22),
            ToggleButton(850, 130, 'assets/sets/Set 1/5.png', 0.22),
            ToggleButton(1050, 130, 'assets/sets/Set 1/6.png', 0.22),
        ]
        self.set2_char = [
            ToggleButton(20, 130, 'assets/sets/Set 2/1.png', 0.2),
            ToggleButton(210, 130, 'assets/sets/Set 2/2.png', 0.2),
            ToggleButton(440, 130, 'assets/sets/Set 2/3.png', 0.2),
            ToggleButton(660, 130, 'assets/sets/Set 2/4.png', 0.2),
            ToggleButton(800, 130, 'assets/sets/Set 2/5.png', 0.2),
            ToggleButton(1030, 130, 'assets/sets/Set 2/6.png', 0.2),
        ]

        self.set3_char = [
            ToggleButton(50, 130, 'assets/sets/Set 3/1.png', 0.3),
            ToggleButton(250, 130, 'assets/sets/Set 3/2.png', 0.3),
            ToggleButton(450, 130, 'assets/sets/Set 3/3.png', 0.3),
            ToggleButton(680, 130, 'assets/sets/Set 3/4.png', 0.3),
            ToggleButton(850, 130, 'assets/sets/Set 3/5.png', 0.3),
            ToggleButton(1050, 130, 'assets/sets/Set 3/6.png', 0.3),
        ]
        self.set4_char = [
            ToggleButton(50, 130, 'assets/sets/Set 4/1.png', 0.3),
            ToggleButton(250, 130, 'assets/sets/Set 4/2.png', 0.3),
            ToggleButton(450, 130, 'assets/sets/Set 4/3.png', 0.3),
            ToggleButton(650, 130, 'assets/sets/Set 4/4.png', 0.3),
            ToggleButton(850, 130, 'assets/sets/Set 4/5.png', 0.3),
            ToggleButton(1050, 130, 'assets/sets/Set 4/6.png', 0.2),

        ]
        self.set5_char = [
            ToggleButton(50, 130, 'assets/sets/Set 5/1.png', 0.25),
            ToggleButton(250, 130, 'assets/sets/Set 5/2.png', 0.2),
            ToggleButton(450, 130, 'assets/sets/Set 5/3.png', 0.2),
            ToggleButton(650, 130, 'assets/sets/Set 5/4.png', 0.25),
            ToggleButton(850, 130, 'assets/sets/Set 5/5.png', 0.25),
            ToggleButton(1050, 130, 'assets/sets/Set 5/6.png', 0.25),
        ]

        self.set6_char = [
            ToggleButton(50, 130, 'assets/sets/Set 6/1.png', 0.3),
            ToggleButton(250, 130, 'assets/sets/Set 6/2.png', 0.3),
            ToggleButton(450, 130, 'assets/sets/Set 6/3.png', 0.3),
            ToggleButton(650, 130, 'assets/sets/Set 6/4.png', 0.3),
            ToggleButton(850, 130, 'assets/sets/Set 6/5.png', 0.3),
            ToggleButton(1050, 130, 'assets/sets/Set 6/6.png', 0.3),
        ]

        self.set7_char = [
            ToggleButton(50, 130, 'assets/sets/Set 7/1.png', 0.3),
            ToggleButton(250, 130, 'assets/sets/Set 7/2.png', 0.3),
            ToggleButton(450, 130, 'assets/sets/Set 7/3.png', 0.3),
            ToggleButton(650, 130, 'assets/sets/Set 7/4.png', 0.3),
            ToggleButton(850, 130, 'assets/sets/Set 7/5.png', 0.3),
            ToggleButton(1050, 130, 'assets/sets/Set 7/6.png', 0.3),
        ]

        self.set_char = [self.set1_char, self.set2_char, self.set3_char, self.set4_char, self.set5_char, self.set6_char,
                         self.set7_char]

        self.underwater = ToggleButton(80, 70, 'assets/BG-pic/underwater.jpg', 0.25)
        self.jungle = ToggleButton(480, 70, 'assets/BG-pic/jungle.jpg', 0.25)
        self.galaxy = ToggleButton(880, 70, 'assets/BG-pic/space.jpg', 0.25)

        self.next_img = pygame.image.load('assets/icons/return.png')
        self.next_img = pygame.transform.flip(self.next_img, True, False)
        self.next = Button(1120, 600, self.next_img, 0.2)
        self.next1 = Button(1120, 600, self.next_img, 0.2)
        self.back = Button(50, 600, pygame.image.load('assets/icons/return.png'), 0.2)
        self.back1 = Button(50, 600, pygame.image.load('assets/icons/return.png'), 0.2)
        self.player = -1

        self.bg_default = 'assets/videos/diffselectbg.mp4'
        self.bg_default_loop = VideoPlayer(self.bg_default)
        self.bg_uw = 'assets/videos/underwater_background.mp4'
        self.bg_uw_loop = VideoPlayer(self.bg_uw)
        self.bg_j = 'assets/videos/jungle_background.mp4'
        self.bg_j_loop = VideoPlayer(self.bg_j)
        self.bg_g = 'assets/videos/galaxy_background.mp4'
        self.bg_g_loop = VideoPlayer(self.bg_g)

        # List bao gồm: [0] là background, [1] là set nhân vật, [2] là độ dài đường đua
        self.activated_buttons = []

        # Dict lưu các nhân vật và tên tương ứng: key là số thứ tự nhân vật, value là tên nhân vật
        self.char_dict = {}

        self.check_j = False
        self.check_uw = False
        self.check_g = False

        self.popup_message = ""
        self.popup_time = 0

        self.state = 0

    def select_bgnset(self):
        global exitSelect
        self.state = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and Fullscreen:
                if close_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
            if self.next.clicked:

                ToggleButton.turn_off_all(self.set1_char)
                ToggleButton.turn_off_all(self.set2_char)
                ToggleButton.turn_off_all(self.set3_char)
                ToggleButton.turn_off_all(self.set4_char)
                ToggleButton.turn_off_all(self.set5_char)
                ToggleButton.turn_off_all(self.set6_char)
                ToggleButton.turn_off_all(self.set7_char)
                
                button_map = {

                    self.jungle: 'jungle',
                    self.underwater: 'underwater',
                    self.galaxy: 'galaxy',

                    self.set1: 'set1',
                    self.set2: 'set2',
                    self.set3: 'set3',
                    self.set4: 'set4',
                    self.set5: 'set5',
                    self.set6: 'set6',
                    self.set7: 'set7',

                    self.midRace: 'mid',
                    self.longRace: 'long',
                    self.shortRace: 'short'
                }

                map_button = None
                set_button = None
                race_track_button = None

                for button, value in button_map.items():
                    if button.clicked:
                        if value in ['jungle', 'underwater', 'galaxy']:
                            map_button = value
                        elif value in ['set1', 'set2', 'set3', 'set4', 'set5', 'set6', 'set7']:
                            set_button = value
                        elif value in ['mid', 'long', 'short']:
                            race_track_button = value

                self.activated_buttons = [map_button, set_button, race_track_button]

                
                
                if None in self.activated_buttons:
                    self.popup_message = "  Please choose all options"
                    self.popup_time = time.time()
                else:
                    self.check_next = True  # Mark as next clicked
                    self.state = 2
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back1.image_rect.collidepoint(pygame.mouse.get_pos()):
                    exitSelect = True
                    
        
            ToggleButton.check_click(event, [self.underwater, self.jungle, self.galaxy])
            if self.jungle.clicked:
                self.check_j = True
                ToggleButton.check_click(event, [self.set3, self.set4])
            else:
                self.check_j = False

            if self.galaxy.clicked:
                self.check_g = True
                ToggleButton.check_click(event, [self.set5, self.set6, self.set7])
            else:
                self.check_g = False

            if self.underwater.clicked:
                self.check_uw = True
                ToggleButton.check_click(event, [self.set1, self.set2])
            else:
                self.check_uw = False

            ToggleButton2.check_click(event, [self.midRace, self.longRace, self.shortRace])

        # CÁC HÀM VẼ PHẢI ĐƯỢC ĐẶT NGOÀI VÒNG EVENT
        self.bg_default_loop.loop_background()

        if self.check_j:
            ToggleButton.turn_off_all([self.set1, self.set2, self.set5, self.set6, self.set7])
            self.bg_j_loop.loop_background()
            self.set3.draw(screen)
            self.set4.draw(screen)
        if self.check_g:
            ToggleButton.turn_off_all([self.set1, self.set2, self.set3, self.set4])
            self.bg_g_loop.loop_background()
            self.set5.draw(screen)
            self.set6.draw(screen)
            self.set7.draw(screen)
        if self.check_uw:
            ToggleButton.turn_off_all([self.set3, self.set4, self.set5, self.set6, self.set7])
            self.bg_uw_loop.loop_background()
            self.set1.draw(screen)
            self.set2.draw(screen)

        self.underwater.draw(screen)
        self.galaxy.draw(screen)
        self.jungle.draw(screen)
        self.longRace.draw(screen)
        self.midRace.draw(screen)
        self.shortRace.draw(screen)
        self.next.draw(screen)
        self.back1.draw(screen)
        if time.time() - self.popup_time < 1.5:
            popup_surface = pygame.Surface((400, 50), pygame.SRCALPHA)
            popup_surface.fill((255, 255, 255, 160))
            popup_text = pygame.font.Font(None, 40).render(self.popup_message, True, pygame.Color('firebrick2'))
            popup_surface.blit(popup_text, (10, 10))
            screen.blit(popup_surface, (440, 510)) 
        if Fullscreen:
            screen.blit(close_button, close_button_rect)

        pygame.display.update()
        self.clock.tick(60)


    def select_player_n_bet(self, usermoney):
        pygame.surface.Surface.fill(screen, 'white')
        self.state = 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button_rect.collidepoint(pygame.mouse.get_pos()) and Fullscreen:
                    pygame.quit()
                    sys.exit()
            for box in self.namebox:
                box.handle_event(event)
                
            self.bet_box.handle_event2(event)

            if self.activated_buttons[1] == 'set2':
                ToggleButton.check_click(event, self.set2_char)
            if self.activated_buttons[1] == 'set1':
                ToggleButton.check_click(event, self.set1_char)
            if self.activated_buttons[1] == 'set5':
                ToggleButton.check_click(event, self.set5_char)
            if self.activated_buttons[1] == 'set6':
                ToggleButton.check_click(event, self.set6_char)
            if self.activated_buttons[1] == 'set3':
                ToggleButton.check_click(event, self.set3_char)
            if self.activated_buttons[1] == 'set4':
                ToggleButton.check_click(event, self.set4_char)
            if self.activated_buttons[1] == 'set7':
                ToggleButton.check_click(event, self.set7_char)

        if self.activated_buttons[0] == 'jungle':
            self.bg_j_loop.loop_background()
            if self.activated_buttons[1] == 'set3':
                for b in self.set3_char:
                    b.draw(screen)
            elif self.activated_buttons[1] == 'set4':
                for b in self.set4_char:
                    b.draw(screen)

        elif self.activated_buttons[0] == 'underwater':
            self.bg_uw_loop.loop_background()
            if self.activated_buttons[1] == 'set2':
                for b in self.set2_char:
                    b.draw(screen)
            elif self.activated_buttons[1] == 'set1':
                for b in self.set1_char:
                    b.draw(screen)

        elif self.activated_buttons[0] == 'galaxy':
            self.bg_g_loop.loop_background()
            if self.activated_buttons[1] == 'set5':
                for b in self.set5_char:
                    b.draw(screen)
            if self.activated_buttons[1] == 'set6':
                for b in self.set6_char:
                    b.draw(screen)
            if self.activated_buttons[1] == 'set7':
                for b in self.set7_char:
                    b.draw(screen)

        for box in self.namebox:
            box.draw(screen)

        for i in range(1, 7):
            self.char_dict[i] = self.namebox[i - 1].naming_character()

        

        self.next1.draw(screen)


        pygame.draw.rect(screen, 'white', (320, 425, 640, 170), border_radius=20)

        font = pygame.font.Font(None, 60)

        self.bet_box.draw(screen)
        current_money = usermoney
        self.bet_box.validate_input(current_money)
        update_money = font.render(f"You currently have: {current_money}", True, 'black')
        screen.blit(update_money, (350, 440))
        instruction_text = font.render("Bet: ", True, 'black')
        screen.blit(instruction_text, (350, 495))  # Điều chỉnh vị trí hiển thị hướng dẫn

        
        

        self.back.draw(screen)
        if self.back.clicked:
            print("back")
            self.state = 1

            for box in self.namebox:
                box.text = ""
                box.active = False
                box.color = box.color_inactive
                box.txt_surface = box.font.render(box.text, True, box.font_color)

        if self.next1.clicked:
            self.player = -1

            for i in range(7):
                for j in range(6):
                    if self.set_char[i][j].clicked:
                        self.player = j + 1
            if not all(self.char_dict.values()):
                self.bet_box.set_error_message("Please enter the characters names!")
            elif self.bet_box.text == "":
                self.bet_box.set_error_message("Please enter your bet!")
            elif self.player == -1:
                self.bet_box.set_error_message("Please choose your character!")
        
                
            elif self.bet_box.text != "" and all(self.char_dict.values()):
                self.state = 3
        if Fullscreen:
            screen.blit(close_button, close_button_rect)

        
        pygame.display.update()
        self.clock.tick(60)

sel = selector()
def run_test(usermoney, isFullscreen):
    global screen, Fullscreen
    global running, exitSelect, close_button, close_button_rect
    if isFullscreen:
        screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        Fullscreen = True
    else:
        screen = pygame.display.set_mode((1280, 720))
        Fullscreen = False
    exitSelect = False
    sel.state = 1
    while running:
        if sel.state == 1:
            sel.select_bgnset()
        elif sel.state == 2:
            sel.select_player_n_bet(usermoney)
        else:
            sel.state = 1
            import loading
            loading.run(2)
            import speed
            return speed.run_race(usermoney, isFullscreen)
        if exitSelect:
            return ["","", 0]      

if __name__ == '__main__':
    run_test(1000)