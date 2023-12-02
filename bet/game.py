import pygame, cv2, math, sys
import intro

pygame.init()


#Tao cua so tro choi
window_width = 1280
window_height = 720
screen = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Bet for Best")
icon = pygame.image.load('./assets/icons/game-icon.png')
pygame.display.set_icon(icon)

#Tao bien tro choi
gold = 10000000

# Lam background loop
video_capture = cv2.VideoCapture('./assets/videos/background.mp4')
fps = video_capture.get(cv2.CAP_PROP_FPS)
video_loop = True
clock = pygame.time.Clock()
def loop_background():
    ret, frame = video_capture.read()
    if not ret:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video_capture.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (window_width, window_height))
    pygame_frame = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
    screen.blit(pygame_frame, (0, 0))

#Tao nut bam
play_button_img = pygame.image.load('./assets/icons/buttons/1.png').convert_alpha()
arcade_button_img = pygame.image.load('./assets/icons/buttons/6.png').convert_alpha()
setting_button_img = pygame.image.load('./assets/icons/buttons/4.png').convert_alpha()
shop_button_img = pygame.image.load('./assets/icons/buttons/2.png').convert_alpha()
logout_button_img = pygame.image.load('./assets/icons/logout.png').convert_alpha()
logout_button_img = pygame.transform.scale(logout_button_img,(67,67))
help_button_img = pygame.image.load('./assets/icons/help.png').convert_alpha()
help_button_img = pygame.transform.scale(help_button_img,(80,80))

click_sound = pygame.mixer.Sound('./assets/sfx/pop-click-sound.mp3')
click_sound.set_volume(0.3)

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

        
play_button = Button(850,200,play_button_img,1)
arcade_button = Button(850,320,arcade_button_img,1)
setting_button = Button(850,440,setting_button_img,1)
shop_button = Button(850,560,shop_button_img,1)
logout_button = Button(window_width-570,26.5,logout_button_img,1)
help_button = Button(window_width-480,20,help_button_img,1)


#Tao thanh tai khoan
bar_height = 120
bar_width = window_width
semi_transparent_bar = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
semi_transparent_bar.fill((0, 0, 0, 100))  # Adjust the alpha value (4th parameter) for transparency
user_font = pygame.font.SysFont(None, 60, bold=False, italic=True)
current_user = user_font.render("User: Bew test", True, (255, 255, 255))
user_illustrate = pygame.image.load('./assets/icons/user.png').convert_alpha()
user_illustrate = pygame.transform.scale(user_illustrate,(80,80))
gold_icon = pygame.image.load('./assets/icons/coin.png')
gold_icon = pygame.transform.scale(gold_icon,(82,82))

#hien thi tien

variable_text = user_font.render(": " + str(gold), True, (255,255,255))

#Ham hien thi giao dien game
def game_menu():
    #cac nut bam
    play_button.draw()
    arcade_button.draw()
    setting_button.draw()
    shop_button.draw()

    #phan user
    screen.blit(semi_transparent_bar, (0, 0))  #thanh tai khoan
    screen.blit(current_user, (130, 39))
    screen.blit(user_illustrate,(30,20))
    logout_button.draw()
    help_button.draw()

    screen.blit(gold_icon,(window_width-370,19))
    screen.blit(variable_text, (window_width-280, 40))

#Chay intro
intro.display_intro(screen)

#Tao va chay am nhac
music_files = ['./assets/musics/gone-fishing-shandr.mp3','./assets/musics/tech-aylex.mp3', './assets/musics/cyberpunk-alexproduction.mp3', ]
music_files_name = ['Shandr - Gone fishing','Aylex - Tech','Alexproduction - Cyberpunk']

new_volume = 0.15

for file in music_files: #chinh tat ca am luong cua nhac thanh gia tri nay
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(new_volume)

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

#Tao thanh hien thi am nhac
font = pygame.font.Font(None, 40)
text_color = (255, 255, 255)
angle = 0

def music_bar():
    global angle
    r = int(127 + 127 * math.sin(math.radians(angle)))
    g = int(127 + 127 * math.sin(math.radians(angle + 120)))
    b = int(127 + 127 * math.sin(math.radians(angle + 240)))

    current_track_text = font.render("Now Playing: " + music_files_name[current_track_index], True, (r, g, b))
    screen.blit(current_track_text, (20, 680))

    angle += 1
#ket thuc thanh hien thi nhac

#lam thanh help
help_pop = pygame.image.load('./assets/BG-pic/help.png').convert()
pygame.transform.scale(help_pop,(window_width,window_height))
help_running = False


lobby_running = True
def lobby():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            play_next_track()

    loop_background() #chay nen
    game_menu() #chay giao dien
    music_bar() #chay thanh hien thi nhac

    pygame.display.update() #cap nhat man hinh game
    clock.tick(fps)



#Chay game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if lobby_running:
        lobby()
    



     