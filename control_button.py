import cv2
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
        self.click_sound = pygame.mixer.Sound('assets/sfx/pop-click-sound.mp3')

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
        self.click_sound = pygame.mixer.Sound('assets/sfx/pop-click-sound.mp3')

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

class Button():
    def __init__(self,x,y,image, scale):
        width = image.get_width()
        height = image.get_height()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image,(int(width*scale), int(height*scale)))
        self.image_rect = self.image.get_rect(topleft = (x, y))
        self.clicked = False
        self.action = False

        self.image_alpha = self.image.copy()
        self.image_alpha.set_alpha(160)

    def draw(self):
        click_sound = pygame.mixer.Sound('assets/sfx/pop-click-sound.mp3')
        cursor_pos = pygame.mouse.get_pos()
        if self.image_rect.collidepoint(cursor_pos):
            screen.blit(self.image_alpha,(self.image_rect.x,self.image_rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                click_sound.play()
                self.action = True
        else:
            screen.blit(self.image,(self.image_rect.x,self.image_rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

shortRace = ToggleButton2 (280, 600, 'assets/icons/buttons/button_short.png')
midRace = ToggleButton2 (530, 600, 'assets/icons/buttons/button_medium.png')
longRace = ToggleButton2 (780, 600, 'assets/icons/buttons/button_long.png')

set12_uw = ToggleButton(400, 300, 'assets/sets/Set 12/1.png', 0.3)

set13_j = ToggleButton(400, 300, 'assets/sets/Set 13/1.png', 0.3)
set6_j = ToggleButton(600, 300, 'assets/sets/Set 6/1.png', 0.3)

set11_g = ToggleButton(400, 300, 'assets/sets/Set 11/1.png', 0.3)
set10_g = ToggleButton(600, 300, 'assets/sets/Set 10/1.png', 0.3)

underwater = ToggleButton(80, 70, 'assets/BG-pic/underwater.jpg', 0.25)
jungle = ToggleButton(480, 70, 'assets/BG-pic/jungle.jpg', 0.25)
galaxy = ToggleButton(880, 70, 'assets/BG-pic/galaxy.jpg', 0.25)

next_img = pygame.image.load('assets/icons/return.png')
next_img = pygame.transform.flip(next_img, True, False)
next = Button(1120, 600, next_img , 0.2)

bg_default = 'assets/videos/tunnel.mp4'
bg_default_loop = VideoPlayer(bg_default)
bg_uw = 'assets/videos/underwater_background.mp4'
bg_uw_loop = VideoPlayer(bg_uw)
bg_j = 'assets/videos/jungle_background.mp4'
bg_j_loop = VideoPlayer(bg_j)
bg_g = 'assets/videos/galaxy_background.mp4'
bg_g_loop = VideoPlayer(bg_g)

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


check_j = False
check_uw = False
check_g = False
check_next = False
activated_buttons = []
running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if next.clicked:
            check_next = True
        if not check_next:
            ToggleButton.check_click(event, [underwater, jungle, galaxy])
            if jungle.clicked:
                check_j = True
                ToggleButton.check_click(event, [set6_j, set13_j])
            else:
                check_j = False

            if galaxy.clicked:
                check_g = True
                ToggleButton.check_click(event, [set10_g, set11_g])
            else:
                check_g = False

            if underwater.clicked:
                check_uw = True
                ToggleButton.check_click(event, [set12_uw])
            else:
                check_uw = False

            ToggleButton2.check_click(event, [midRace, longRace, shortRace])

            if next.clicked:
                activated_buttons = []
                if jungle.clicked:
                    activated_buttons.append('jungle')
                elif underwater.clicked:
                    activated_buttons.append('underwater')
                elif galaxy.clicked:
                    activated_buttons.append('galaxy')

                if set6_j.clicked:
                    activated_buttons.append('set6_j')
                elif set13_j.clicked:
                    activated_buttons.append('set13_j')
                elif set10_g.clicked:
                    activated_buttons.append('set10_g')
                elif set11_g.clicked:
                    activated_buttons.append('set11_g')

                if midRace.clicked:
                    activated_buttons.append('mid')
                elif longRace.clicked:
                    activated_buttons.append('long')
                elif shortRace.clicked:
                    activated_buttons.append('short')
            else: #PHAN CHON NHAN VAT
                pass

    bg_default_loop.loop_background()

    if not check_next:
        if check_j:
            bg_j_loop.loop_background()
            set6_j.draw(screen)
            set13_j.draw(screen)
        if check_g:
            bg_g_loop.loop_background()
            set10_g.draw(screen)
            set11_g.draw(screen)
        if check_uw:
            bg_uw_loop.loop_background()
            set12_uw.draw(screen)

        underwater.draw(screen)
        galaxy.draw(screen)
        jungle.draw(screen)
        longRace.draw(screen)
        midRace.draw(screen)
        shortRace.draw(screen)
        next.draw()
    else: #PHAN CHON NHAT VAT
        pass

    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
for btn in activated_buttons:
    print(btn)

