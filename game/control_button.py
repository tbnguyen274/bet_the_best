import cv2
import sys
import pygame
pygame.init()
class VideoPlayer:
    def __init__(self, video_path):
        self.video_capture = cv2.VideoCapture(video_path)
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))

    def loop_background(self):
        ret, frame = self.video_capture.read()
        if not ret:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video_capture.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (1280, 720))
        pygame_frame = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
        self.screen.blit(pygame_frame, (0, 0))


class ToggleButton:
    def __init__(self, x, y, image_path, scale=1.0):
        self.x = x
        self.y = y
        self.image_path = image_path
        self.original_image = pygame.image.load(self.image_path)
        self.scale = scale
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale),
                                                                 int(self.original_image.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.click_sound = pygame.mixer.Sound('../assets/sfx/pop-click-sound.mp3')

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
        self.click_sound = pygame.mixer.Sound('../assets/sfx/pop-click-sound.mp3')

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


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.image_rect = self.image.get_rect(topleft = (x, y))
        self.clicked = False
        self.action = False
        self.image_alpha = self.image.copy()
        self.image_alpha.set_alpha(160)

    def draw(self, screen):
        click_sound = pygame.mixer.Sound('../assets/sfx/pop-click-sound.mp3')
        cursor_pos = pygame.mouse.get_pos()
        if self.image_rect.collidepoint(cursor_pos):
            screen.blit(self.image_alpha, (self.image_rect.x,self.image_rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                click_sound.play()
                self.action = True
        else:
            screen.blit(self.image,(self.image_rect.x, self.image_rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


class TextInput:
    def __init__(self, x, y, width, height, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.font_color = pygame.Color('black')  # Add this line to set the font color
        self.font = pygame.font.Font(None, font_size)
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.font_color)  # Change this line
        self.active = False

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
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    temp_text = self.text + event.unicode
                    temp_surface = self.font.render(temp_text, True, self.font_color)
                    if temp_surface.get_width() < self.rect.w:
                        self.text = temp_text
                self.txt_surface = self.font.render(self.text, True, self.font_color)  # Change this line

    def draw(self, screen):
        # Fill the input box with color
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw the text on the filled input box
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

       


WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class selector:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1280, 720))

        self.shortRace = ToggleButton2(280, 600, '../assets/icons/buttons/button_short.png')
        self.midRace = ToggleButton2(530, 600, '../assets/icons/buttons/button_medium.png')
        self.longRace = ToggleButton2(780, 600, '../assets/icons/buttons/button_long.png')

        #Ô ĐẶT TÊN
        self.betbox = [
            TextInput(50, 300, 140, 50, 40),
            TextInput(250, 300, 140, 50, 40),
            TextInput(450, 300, 140, 50, 40),
            TextInput(650, 300, 140, 50, 40),
            TextInput(850, 300, 140, 50, 40),
            TextInput(1050, 300, 140, 50, 40),
        ]
        self.set4_uw = ToggleButton(670, 330, '../assets/sets/Set 4/1.png', 0.3)
        self.set12_uw = ToggleButton(470, 330, '../assets/sets/Set 12/1.png', 0.3)
        self.set13_j = ToggleButton(470, 330, '../assets/sets/Set 13/1.png', 0.3)
        self.set6_j = ToggleButton(660, 330, '../assets/sets/Set 6/1.png', 0.3)
        self.set11_g = ToggleButton(470, 330, '../assets/sets/Set 11/1.png', 0.3)
        self.set10_g = ToggleButton(660, 330, '../assets/sets/Set 10/1.png', 0.3)

        self.set4_char = [
            ToggleButton(20, 130, '../assets/sets/Set 4/1.png', 0.22),
            ToggleButton( 210, 130, '../assets/sets/Set 4/2.png', 0.22),
            ToggleButton(460, 130, '../assets/sets/Set 4/3.png', 0.2),
            ToggleButton(670, 130, '../assets/sets/Set 4/4.png', 0.22),
            ToggleButton(850, 130, '../assets/sets/Set 4/5.png', 0.22),
            ToggleButton(1050, 130, '../assets/sets/Set 4/6.png', 0.22),
            ]
        self.set12_char = [
            ToggleButton(20, 130, '../assets/sets/Set 12/1.png', 0.25),
            ToggleButton(210, 130, '../assets/sets/Set 12/2.png', 0.25),
            ToggleButton(440, 130, '../assets/sets/Set 12/3.png', 0.25),
            ToggleButton(600, 130, '../assets/sets/Set 12/4.png', 0.25),
            ToggleButton(800, 130, '../assets/sets/Set 12/5.png', 0.25),
            ToggleButton(1030, 130, '../assets/sets/Set 12/6.png', 0.25),
            ]

        self.set11_char = [
            ToggleButton(50, 130, '../assets/sets/Set 11/1.png', 0.3),
            ToggleButton(250, 130, '../assets/sets/Set 11/2.png', 0.3),
            ToggleButton(450, 130, '../assets/sets/Set 11/3.png', 0.3),
            ToggleButton(650, 130, '../assets/sets/Set 11/4.png', 0.3),
            ToggleButton(850, 130, '../assets/sets/Set 11/5.png', 0.3),
            ToggleButton(1050, 130, '../assets/sets/Set 11/6.png', 0.3),
        ]
        self.set10_char = [
            ToggleButton(50, 130, '../assets/sets/Set 10/1.png', 0.3),
            ToggleButton(250, 130, '../assets/sets/Set 10/2.png', 0.3),
            ToggleButton(450, 130, '../assets/sets/Set 10/3.png', 0.3),
            ToggleButton(650, 130, '../assets/sets/Set 10/4.png', 0.3),
            ToggleButton(850, 130, '../assets/sets/Set 10/5.png', 0.3),
            ToggleButton(1050, 130, '../assets/sets/Set 10/6.png', 0.3),

        ]
        self.set6_char = [
            ToggleButton(50, 130, '../assets/sets/Set 6/1.png', 0.25),
            ToggleButton(250, 130, '../assets/sets/Set 6/2.png', 0.2),
            ToggleButton(450, 130, '../assets/sets/Set 6/3.png', 0.2),
            ToggleButton(650, 130, '../assets/sets/Set 6/4.png', 0.25),
            ToggleButton(850, 130, '../assets/sets/Set 6/5.png', 0.25),
            ToggleButton(1050, 130, '../assets/sets/Set 6/6.png', 0.25),
        ]

        self.set13_char = [
            ToggleButton(50, 130, '../assets/sets/Set 13/1.png', 0.3),
            ToggleButton(250, 130, '../assets/sets/Set 13/2.png', 0.3),
            ToggleButton(450, 130, '../assets/sets/Set 13/3.png', 0.3),
            ToggleButton(650, 130, '../assets/sets/Set 13/4.png', 0.3),
            ToggleButton(850, 130, '../assets/sets/Set 13/5.png', 0.3),
            ToggleButton(1050, 130, '../assets/sets/Set 13/6.png', 0.3),
        ]



        self.underwater = ToggleButton(80, 70, '../assets/BG-pic/underwater.jpg', 0.25)
        self.jungle = ToggleButton(480, 70, '../assets/BG-pic/jungle.jpg', 0.25)
        self.galaxy = ToggleButton(880, 70, '../assets/BG-pic/galaxy.jpg', 0.25)

        self.next_img = pygame.image.load('../assets/icons/return.png')
        self.next_img = pygame.transform.flip(self.next_img, True, False)
        self.next = Button(1120, 600, self.next_img, 0.2)

        self.back_img = pygame.image.load('../assets/icons/return.png')
        self.back = Button(20, 600, self.back_img, 0.2)

        self.bg_default = '../assets/videos/diffselectbg.mp4'
        self.bg_default_loop = VideoPlayer(self.bg_default)
        self.bg_uw = '../assets/videos/underwater_background.mp4'
        self.bg_uw_loop = VideoPlayer(self.bg_uw)
        self.bg_j = '../assets/videos/jungle_background.mp4'
        self.bg_j_loop = VideoPlayer(self.bg_j)
        self.bg_g = '../assets/videos/galaxy_background.mp4'
        self.bg_g_loop = VideoPlayer(self.bg_g)
        self.activated_buttons = []


    def select(self):
        check_j = False
        check_uw = False
        check_g = False
        check_next = False
        running = True
        self.activated_buttons = []
        self.screen.fill((255, 255, 255))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if self.next.clicked:
                    # LƯU LẠI CÁC THÔNG TIN TRƯỚC KHI CHUYỂN QUA MÀN HÌNH MỚI
                    self.activated_buttons = []
                    if self.jungle.clicked:
                        self.activated_buttons.append('jungle')
                    elif self.underwater.clicked:
                        self.activated_buttons.append('underwater')
                    elif self.galaxy.clicked:
                        self.activated_buttons.append('galaxy')
                    if self.set6_j.clicked:
                        self.activated_buttons.append('set6_j')
                    elif self.set13_j.clicked:
                        self.activated_buttons.append('set13_j')
                    elif self.set10_g.clicked:
                        self.activated_buttons.append('set10_g')
                    elif self.set11_g.clicked:
                        self.activated_buttons.append('set11_g')
                    elif self.set12_uw.clicked:
                        self.activated_buttons.append('set12_uw')
                    elif self.set4_uw.clicked:
                        self.activated_buttons.append('set4_uw')
                    if self.midRace.clicked:
                        self.activated_buttons.append('mid')
                    elif self.longRace.clicked:
                        self.activated_buttons.append('long')
                    elif self.shortRace.clicked:
                        self.activated_buttons.append('short')

                    if len(self.activated_buttons) == 3:
                        check_next = True  # ĐÁNH DẤU LÀ ĐÃ BẤM NEXT
                if self.back.clicked:
                    check_next = False

                if not check_next:
                    ToggleButton.check_click(event, [self.underwater, self.jungle, self.galaxy])
                    if self.jungle.clicked:
                        check_j = True
                        ToggleButton.check_click(event, [self.set6_j, self.set13_j])
                    else:
                        check_j = False

                    if self.galaxy.clicked:
                        check_g = True
                        ToggleButton.check_click(event, [self.set10_g, self.set11_g])
                    else:
                        check_g = False

                    if self.underwater.clicked:
                        check_uw = True
                        ToggleButton.check_click(event, [self.set12_uw, self.set4_uw])
                    else:
                        check_uw = False

                    ToggleButton2.check_click(event, [self.midRace, self.longRace, self.shortRace])

                else:
                    #HIEN THI CAC SET NHAN VAT
                    if self.activated_buttons[1] == 'set4_uw':
                        ToggleButton.check_click(event, self.set4_char)
                    if self.activated_buttons[1] == 'set12_uw':
                        ToggleButton.check_click(event, self.set12_char)
                    if self.activated_buttons[1] == 'set11_g':
                        ToggleButton.check_click(event, self.set11_char)
                    if self.activated_buttons[1] == 'set10_g':
                        ToggleButton.check_click(event, self.set10_char)
                    if self.activated_buttons[1] == 'set6_j':
                        ToggleButton.check_click(event, self.set6_char)
                    if self.activated_buttons[1] == 'set13_j':
                        ToggleButton.check_click(event, self.set13_char)

                    for box in self.betbox:
                        box.handle_event(event)
            if not check_next:
                self.bg_default_loop.loop_background()
                if check_j:
                    self.bg_j_loop.loop_background()
                    self.set6_j.draw(self.screen)
                    self.set13_j.draw(self.screen)
                if check_g:
                    self.bg_g_loop.loop_background()
                    self.set10_g.draw(self.screen)
                    self.set11_g.draw(self.screen)
                if check_uw:
                    self.bg_uw_loop.loop_background()
                    self.set12_uw.draw(self.screen)
                    self.set4_uw.draw(self.screen)

                self.underwater.draw(self.screen)
                self.galaxy.draw(self.screen)
                self.jungle.draw(self.screen)
                self.longRace.draw(self.screen)
                self.midRace.draw(self.screen)
                self.shortRace.draw(self.screen)
                self.next.draw(self.screen)


            else:
                if self.activated_buttons[0] == 'jungle':
                    self.bg_j_loop.loop_background()
                    if self.activated_buttons[1] == 'set6_j':
                        for b in self.set6_char:
                            b.draw(self.screen)
                    elif self.activated_buttons[1] == 'set13_j':
                        for b in self.set13_char:
                            b.draw(self.screen)

                elif self.activated_buttons[0] == 'underwater':
                    self.bg_uw_loop.loop_background()
                    if self.activated_buttons[1] == 'set4_uw':
                        for b in self.set4_char:
                            b.draw(self.screen)
                    elif self.activated_buttons[1] == 'set12_uw':
                        for b in self.set12_char:
                            b.draw(self.screen)

                elif self.activated_buttons[0] == 'galaxy':
                    self.bg_g_loop.loop_background()
                    if self.activated_buttons[1] == 'set10_g':
                        for b in self.set10_char:
                            b.draw(self.screen)
                    if self.activated_buttons[1] == 'set11_g':
                        for b in self.set11_char:
                            b.draw(self.screen)

                for box in self.betbox:
                    box.draw(self.screen)

                self.back.draw(self.screen)

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60)





        sys.exit()
if __name__ == '__main__':
  selector = selector()
  selector.select()