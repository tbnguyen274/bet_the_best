import pygame, cv2, math, sys
from intro import display_intro

pygame.init()

#Tao cua so tro choi
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Bet The Best")
icon = pygame.image.load('./assets/icons/game-icon.png')
pygame.display.set_icon(icon)

# Lam background loop
video_capture = cv2.VideoCapture('./assets/videos/background.mp4')
fps = video_capture.get(cv2.CAP_PROP_FPS)
video_loop = True

def loop_background():
    pygame.time.Clock().tick(60)
    ret, frame = video_capture.read()
    if not ret:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video_capture.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame_frame = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
    window.blit(pygame_frame, (0, 0))

#Tao nut bam
play_button_img = pygame.image.load('./assets/icons/buttons/play.png').convert_alpha()
shop_button_img = pygame.image.load('./assets/icons/buttons/shop.png').convert_alpha()
help_button_img = pygame.image.load('./assets/icons/buttons/help.png').convert_alpha()
logout_button_img = pygame.image.load('./assets/icons/buttons/logout.png').convert_alpha()
history_button_img = pygame.image.load('./assets/icons/buttons/history.png').convert_alpha()

class lobby_button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image,(int(width*scale), int(height*scale)))
        self.image_rect = self.image.get_rect(topleft = (x, y))
        self.clicked = False
        self.hover_image = self.darken_image(self.image)  # Tạo hình ảnh sậm đi khi nút được nhấn
        self.click_sound = pygame.mixer.Sound('./assets/sfx/pop-click-sound.mp3')
        self.click_sound.set_volume(0.2)

        self.action = False
    
    def darken_image(self, image):
        # Tạo bản sao của hình ảnh gốc với màu sậm đi (ở đây tôi chọn màu đen nhẹ)
        darkened_image = image.copy()
        darkened_image.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_SUB)  # Điều chỉnh mức độ sậm màu
        return darkened_image

    def draw(self):
        cursor_pos = pygame.mouse.get_pos()
        if self.image_rect.collidepoint(cursor_pos):
            window.blit(self.hover_image,(self.image_rect))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.click_sound.play()
                self.action = True
        else:
            window.blit(self.image,(self.image_rect.x,self.image_rect.y))   

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False     

play_button = lobby_button(740,170,play_button_img,1)
shop_button = lobby_button(740,280,shop_button_img,1)
history_button = lobby_button(740,390,history_button_img,1)
help_button = lobby_button(740,500,help_button_img,1)
logout_button = lobby_button(740,610,logout_button_img,1)

#Tao thanh tai khoan
STATUS_BAR_HEIGHT = 120
STATUS_BAR_WIDTH = WINDOW_WIDTH
STATUS_BAR_ALPHA = 150
status_bar = pygame.Surface((STATUS_BAR_WIDTH, STATUS_BAR_HEIGHT), pygame.SRCALPHA)
status_bar.fill((0, 0, 0, STATUS_BAR_ALPHA))  # Adjust the alpha value (4th parameter) for transparency
user_font = pygame.font.Font(None, 60)
current_user = user_font.render("Bew test", True, (255, 255, 255))
user_avatar = pygame.image.load('./assets/icons/user.png').convert_alpha()
user_avatar = pygame.transform.scale(user_avatar,(80,80))
coin_icon = pygame.image.load('./assets/icons/coin.png')
coin_icon = pygame.transform.scale(coin_icon,(82,82))
coin_rect = coin_icon.get_rect(topleft = (740, STATUS_BAR_HEIGHT//2 - coin_icon.get_height()//2))
coin = 0
coin_display = user_font.render(": " + str(coin), True, (255,255,255))
coin_display_rect = coin_display.get_rect(topleft = (coin_rect.x + coin_icon.get_width() + 10, STATUS_BAR_HEIGHT//2 - coin_display.get_height()//2))



#Ham hien thi giao dien game
def lobby_GUI():
    #cac nut bam
    play_button.draw()
    shop_button.draw()
    history_button.draw()
    help_button.draw()
    logout_button.draw()

    #phan user
    window.blit(status_bar, (0, 0))  #thanh tai khoan
    window.blit(current_user, (130, 39))
    window.blit(user_avatar,(30,20))
    window.blit(coin_icon, coin_rect)
    window.blit(coin_display, coin_display_rect)

    music_bar() #chay thanh hien thi nhac

display_intro(window)

#Tao va chay am nhac
music_files = ['./assets/musics/gone-fishing-shandr.mp3','./assets/musics/tech-aylex.mp3', './assets/musics/cyberpunk-alexproduction.mp3', ]
music_list = ['Shandr - Gone fishing','Aylex - Tech','Alexproduction - Cyberpunk']

for file in music_files: #chinh tat ca am luong cua nhac thanh gia tri nay
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(0.15)

current_track_index = 0
pygame.mixer.music.load(music_files[current_track_index])
def play_next_track():
    global current_track_index
    current_track_index = (current_track_index + 1) % len(music_files)
    pygame.mixer.music.load(music_files[current_track_index])
    pygame.mixer.music.play()

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)
pygame.mixer.music.play()
#ket thuc phan am nhac

angle = 0

def music_bar():
    global angle
    r = int(127 + 127 * math.sin(math.radians(angle)))
    g = int(127 + 127 * math.sin(math.radians(angle + 120)))
    b = int(127 + 127 * math.sin(math.radians(angle + 240)))

    current_track_text = pygame.font.Font(None, 30).render("Now Playing: " + music_list[current_track_index], True, (r, g, b))
    window.blit(current_track_text, (20, 680))

    angle += 1
#ket thuc thanh hien thi nhac

def lobby():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MUSIC_END:
            play_next_track()

    loop_background() #chay nen
    lobby_GUI() #chay giao dien

    pygame.display.update() #cap nhat man hinh game



#Chay game

while True:
    lobby()
    



     