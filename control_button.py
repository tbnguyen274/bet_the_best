import pygame
import sys
import cv2
pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CONTROL')
clock = pygame.time.Clock()

bg1 = cv2.VideoCapture('assets/videos/jungle_background.mp4')

def loop_background(video_capture):
    ret, frame = video_capture.read()
    if not ret:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video_capture.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (WIDTH, HEIGHT))
    pygame_frame = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
    screen.blit(pygame_frame, (0, 0))

class Button():
    def __init__(self,x,y,image,scale):
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
        click_sound = pygame.mixer.Sound('./assets/sfx/pop-click-sound.mp3')
        click_sound.set_volume(0.3)
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

underwater = pygame.image.load('assets/BG-pic/underwater.jpg')
jungle = pygame.image.load('assets/BG-pic/jungle.jpg')
galaxy = pygame.image.load('assets/BG-pic/galaxy.jpg')

# Tạo một list để lưu trữ các hình ảnh
set12_images = []
set6_images = []
set10_images = []
# Load các hình ảnh từ 'Set 12' từ 1 đến 6
for i in range(1, 7):
    image_path = f"assets/sets/Set 12/{i}.png"
    loaded_image = pygame.image.load(image_path)
    set12_images.append(loaded_image)
    image_path = f"assets/sets/Set 6/{i}.png"
    loaded_image = pygame.image.load(image_path)
    set6_images.append(loaded_image)
    image_path = f"assets/sets/Set 10/{i}.png"
    loaded_image = pygame.image.load(image_path)
    set10_images.append(loaded_image)

underwaterButton = Button(80, 70, underwater, 0.25)
jungleButton = Button(480, 70, jungle, 0.25)
galaxyButton = Button (880, 70, galaxy, 0.25)

##Nhan vat set12##
set12_1Button = Button (80, 300, set12_images[0], 0.2)
set12_2Button = Button (250, 300, set12_images[1], 0.2)
set12_3Button = Button (450, 300, set12_images[2], 0.2)
set12_4Button = Button (600, 300, set12_images[3], 0.2)
set12_5Button = Button (770, 300, set12_images[4], 0.2)
set12_6Button = Button (980, 300, set12_images[5], 0.2)
##Nhan vat set6###
set6_1Button = Button (80, 300, set6_images[0], 0.2)
set6_2Button = Button (250, 300, set6_images[1], 0.17)
set6_3Button = Button (450, 300, set6_images[2], 0.17)
set6_4Button = Button (600, 300, set6_images[3], 0.2)
set6_5Button = Button (770, 300, set6_images[4], 0.2)
set6_6Button = Button (980, 300, set6_images[5], 0.2)
##Nhan vat set10###
set10_1Button = Button (80, 300, set10_images[0], 0.2)
set10_2Button = Button (250, 300, set10_images[1], 0.2)
set10_3Button = Button (450, 300, set10_images[2], 0.2)
set10_4Button = Button (600, 300, set10_images[3], 0.2)
set10_5Button = Button (770, 300, set10_images[4], 0.2)
set10_6Button = Button (980, 300, set10_images[5], 0.2)

# Main game loop
# Trong vòng lặp game loop, kiểm tra khi nào người dùng nhấn vào underwaterButton
# Khởi tạo các biến để kiểm soát trạng thái hiển thị của các set Button
show_set12_buttons = False
previous_show_set12_buttons = False
show_set6_buttons = False
previous_show_set6_buttons = False
show_set10_buttons = False
previous_show_set10_buttons = False

def race_select():
    show_set12_buttons = False
    show_set6_buttons = False
    show_set10_buttons = False
    show_set12_1_button_only = False
    show_set6_1_button_only = False
    show_set10_1_button_only = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if underwaterButton.image_rect.collidepoint(event.pos):
                    show_set12_buttons = False
                    show_set6_buttons = False
                    show_set6_1_button_only = False
                    show_set12_1_button_only = True
                    show_set10_1_button_only = False

                elif jungleButton.image_rect.collidepoint(event.pos):
                    show_set12_buttons = False
                    show_set12_1_button_only = False
                    show_set6_1_button_only = True
                    show_set10_1_button_only = False
                    show_set10_buttons = False
                    show_set6_buttons = False

                elif galaxyButton.image_rect.collidepoint(event.pos):
                    show_set12_buttons = False
                    show_set6_buttons = False
                    show_set10_1_button_only = True
                    show_set12_1_button_only = False
                    show_set6_1_button_only = False

                if set12_1Button.image_rect.collidepoint(event.pos):
                    if show_set12_1_button_only:
                        if not show_set12_buttons:
                            show_set12_buttons = True
                        else:
                            show_set12_buttons = False
                            #show_set12_1_button_only = False

                if set6_1Button.image_rect.collidepoint(event.pos):
                    if show_set6_1_button_only:
                        if not show_set6_buttons:
                            show_set6_buttons = True
                        else:
                            show_set6_buttons = False
                            #show_set6_1_button_only = False

                if set10_1Button.image_rect.collidepoint(event.pos):
                    if show_set10_1_button_only:
                        if not show_set10_buttons:
                            show_set10_buttons = True
                        else:
                            show_set10_buttons = False

        loop_background(bg1)
        underwaterButton.draw()
        jungleButton.draw()
        galaxyButton.draw()

        if show_set12_buttons:
            set12_1Button.draw()
            set12_2Button.draw()
            set12_3Button.draw()
            set12_4Button.draw()
            set12_5Button.draw()
            set12_6Button.draw()
        elif show_set12_1_button_only:
            set12_1Button.draw()

        if show_set6_buttons:
            set6_1Button.draw()
            set6_2Button.draw()
            set6_3Button.draw()
            set6_4Button.draw()
            set6_5Button.draw()
            set6_6Button.draw()
        elif show_set6_1_button_only:
            set6_1Button.draw()

        if show_set10_buttons:
            set10_1Button.draw()
            set10_2Button.draw()
            set10_3Button.draw()
            set10_4Button.draw()
            set10_5Button.draw()
            set10_6Button.draw()
        elif show_set10_1_button_only:
            set10_1Button.draw()

        pygame.display.update()
        clock.tick(30)

while True:
    race_select()
