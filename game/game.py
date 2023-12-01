import pygame, cv2, math, sys, json, os
from intro import display_intro

DATABASE_DIRECTORY = 'db'
DATABASE = os.path.join(DATABASE_DIRECTORY, "user_data.json")

# Tạo databasee nếu chưa có
if not os.path.exists(DATABASE) or os.stat(DATABASE).st_size == 0:
    with open(DATABASE, 'w') as file:
        json.dump({}, file)

#Tao cua so tro choi
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
username = 'bewpass'
coin = json.load(open(DATABASE,"r"))[username].get('coin')

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Bet The Best")
icon = pygame.image.load('./assets/icons/game-icon.png')
pygame.display.set_icon(icon)

class background():
    def __init__(self):
        self.sourceclip = cv2.VideoCapture('./assets/videos/background.mp4')

    def display(self):
        ret, frame = self.sourceclip.read()
        if not ret:
            self.sourceclip.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.sourceclip.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame_frame = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
        window.blit(pygame_frame, (0, 0))
background = background()

#Tao nut bam
class lobby_button():
    def __init__(self,x,y,image,scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image,(int(self.width*scale), int(self.height*scale)))
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
            
play_button_img = pygame.image.load('./assets/icons/buttons/play.png').convert_alpha()
shop_button_img = pygame.image.load('./assets/icons/buttons/shop.png').convert_alpha()
help_button_img = pygame.image.load('./assets/icons/buttons/help.png').convert_alpha()
logout_button_img = pygame.image.load('./assets/icons/buttons/logout.png').convert_alpha()
history_button_img = pygame.image.load('./assets/icons/buttons/history.png').convert_alpha()  

play_button = lobby_button(740,170,play_button_img,1)
shop_button = lobby_button(740,280,shop_button_img,1)
history_button = lobby_button(740,390,history_button_img,1)
help_button = lobby_button(740,500,help_button_img,1)
logout_button = lobby_button(740,610,logout_button_img,1)

#Tao thanh tai khoan
class user_status():
    global username, coin
    def __init__(self):
        # Set up bar
        self.height = 120
        self.width = WINDOW_WIDTH
        self.alpha = 150
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((0,0,0, self.alpha))
        self.font = pygame.font.Font(None, 60)

        # User info
        self.username = username
        self.coin = coin

        self.avatar_list = ['./assets/icons/user.png']
        self.current_avatar = self.avatar_list[0]
        self.avatar = pygame.image.load(self.current_avatar).convert_alpha()
        self.avatar = pygame.transform.scale(self.avatar,(80,80))
        self.avatar_x = 130
        self.avatar_y = (self.height-self.avatar.get_height())//2

        self.username_text = self.font.render(self.username, True, (255,255,255))
        self.username_text_y = (self.height-self.username_text.get_height())//2

        self.coin_icon = pygame.image.load('./assets/icons/coin.png').convert_alpha()
        self.coin_icon = pygame.transform.scale(self.coin_icon,(82,82))
        self.coin_icon_x =  740
        self.coin_icon_y = (self.height-self.coin_icon.get_height())//2
        self.coin_value = self.font.render(": " + str(self.coin), True, (255,255,255))
        self.coin_value_y = (self.height-self.coin_value.get_height())//2
    
    def numdisplay(self, num):
        if num / 1000000000 >= 1:
            return str(num//1000000000) + "." + str(num%100000000)[0] + "B"
        elif num / 1000000 >= 1:
            return str(num//1000000) + "." + str(num%100000)[0] + "M"
        elif num / 1000 >= 1:
            return str(num//1000) + "." + str(num%1000) + "K"
        return str(num)

    def display(self):
        window.blit(self.surface,(0,0))
        window.blit(self.avatar,(30,self.avatar_y))

        window.blit(self.username_text, (self.avatar_x + 10, self.username_text_y))

        window.blit(self.coin_icon, (self.coin_icon_x, self.coin_icon_y))
        self.coin_value = self.font.render(": " + self.numdisplay(self.coin), True, (255,255,255))
        window.blit(self.coin_value, (self.coin_icon_x + self.coin_icon.get_width() + 10, self.coin_value_y))
user_status = user_status()

#Ham hien thi giao dien game
def lobby_GUI():
    user_status.display()

    play_button.draw()
    shop_button.draw()
    history_button.draw()
    help_button.draw()
    logout_button.draw()

    music_bar() #chay thanh hien thi nhac

#Tao va chay am nhac
pygame.mixer.music.stop()
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

    current_track_text = pygame.font.Font(None, 40).render("Now Playing: " + music_list[current_track_index], True, (r, g, b))
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

    background.display() #chay nen
    lobby_GUI() #chay giao dien
            
        #Chay game
while True:

    pygame.time.Clock().tick(60)
    lobby()
    pygame.display.update() #cap nhat man hinh game
        



     