import pygame, cv2, math, sys, json, os

DATABASE_DIRECTORY = 'db'
DATABASE = os.path.join(DATABASE_DIRECTORY, "user_data.json")
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def save_user_info(username, coin):
    with open(DATABASE, "r") as file:
        data = json.load(file)
        data[username]['coin'] = coin
    with open(DATABASE, "w") as file:
        json.dump(data,file, indent=4)

def mainmenu(loggedinuser):
    pygame.init()
    username = loggedinuser
    user_coin = json.load(open(DATABASE,"r"))[username].get('coin')
    isRunning = True

    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

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

    class music():
        def __init__(self, music_file_paths, music_name_list, volume, bar_x, bar_y):
            self.music_file_path = music_file_paths
            self.music_name_list = music_name_list
            self.volume = volume
            self.current_track_index = 0
            self.angle = 0
            self.bar_x = bar_x
            self.bar_y = bar_y
            self.current_display_index = 0
        
        def play(self):
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.music_file_path[self.current_track_index])
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()
                self.current_track_index = (self.current_track_index + 1) % len(self.music_file_path)
                self.current_display_index = (self.current_track_index - 1) % len(self.music_file_path)

        def bar(self):
            r = int(127 + 127 * math.sin(math.radians(self.angle)))
            g = int(127 + 127 * math.sin(math.radians(self.angle + 120)))
            b = int(127 + 127 * math.sin(math.radians(self.angle + 240)))

            current_track_text = pygame.font.Font(None, 40).render("Now Playing: " + self.music_name_list[self.current_display_index], True, (r, g, b))
            window.blit(current_track_text, (self.bar_x, self.bar_y))

            self.angle += 1
            
        

    #Tao nut bam
    class button():
        def __init__(self,x,y,image,scale, visible):
            self.image = pygame.image.load(image)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.x = x
            self.y = y
            self.image = pygame.transform.scale(self.image,(int(self.width*scale), int(self.height*scale)))
            self.image_rect = self.image.get_rect(topleft = (x, y))
            self.clicked = False
            self.hover_image = self.hover_effect(self.image)  # Tạo hình ảnh sậm đi khi nút được nhấn
            self.click_sound = pygame.mixer.Sound('./assets/sfx/pop-click-sound.mp3')
            self.click_sound.set_volume(0.2)
            self.visible = visible
            

        
        def hover_effect(self, image):
            # Tạo bản sao của hình ảnh gốc với màu sậm đi (ở đây tôi chọn màu đen nhẹ)
            hover_image = image.copy()
            hover_image.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_SUB)  # Điều chỉnh mức độ sậm màu
            return hover_image

        def display(self):
            if self.visible:
                cursor_pos = pygame.mouse.get_pos()
                if self.image_rect.collidepoint(cursor_pos):
                    window.blit(self.hover_image,(self.image_rect))
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                        self.clicked = True
                        self.click_sound.play()
                else:
                    window.blit(self.image,(self.image_rect.x,self.image_rect.y))   

                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
            else:
                pass

    #Tao thanh tai khoan
    class user_status():
        global username, user_coin
        def __init__(self):
            # Set up bar
            self.height = 120
            self.width = WINDOW_WIDTH
            self.alpha = 150
            self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.surface.fill((0,0,0, self.alpha))
            self.font = pygame.font.Font(None, 60)
            self.minifont = pygame.font.Font(None, 28)

            # User info
            self.username = username
            self.coin = user_coin

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

            self.tips_list = ['','When you have less than 100 coins, you have to play minigame', 'Click on the avatar to change it', 'You can change the music by clicking next and previous button']
            self.tips_index = 0
            self.tips = self.minifont.render(self.tips_list[self.tips_index], True, (255, 85, 187))

        def numdisplay(self, num):
            if num / 1000000000 >= 1:
                return str(num//1000000000) + "." + str(num%1000000000)[0] + "B"
            elif num / 1000000 >= 1:
                return str(num//1000000) + "." + str(num%1000000)[0] + "M"
            return str(num)

        def display(self):
            window.blit(self.surface,(0,0))
            window.blit(self.avatar,(30,self.avatar_y))

            window.blit(self.username_text, (self.avatar_x + 10, self.username_text_y))

            window.blit(self.coin_icon, (self.coin_icon_x, self.coin_icon_y))
            self.coin = user_coin
            self.coin_value = self.font.render(": " + self.numdisplay(self.coin), True, (255,255,255))
            window.blit(self.coin_value, (self.coin_icon_x + self.coin_icon.get_width() + 10, self.coin_value_y))
            window.blit(self.tips, (10, self.height+ 10))

    background = background()
    music = music(['./assets/musics/gone-fishing-shandr.mp3','./assets/musics/tech-aylex.mp3', './assets/musics/cyberpunk-alexproduction.mp3'], ['Shandr - Gone fishing','Aylex - Tech','Alexproduction - Cyberpunk'], 0.3, 20, 680)
    user_status = user_status()

    button_play = button(740,170,'./assets/icons/buttons/play.png',1, True)
    button_minigame = button(740,170,'./assets/icons/buttons/minigame.png',1, False)
    button_shop = button(740,280,'./assets/icons/buttons/shop.png',1, True)
    button_history = button(740,390,'./assets/icons/buttons/history.png',1, True)
    button_help = button(740,500,'./assets/icons/buttons/help.png',1, True)
    button_logout = button(740,610,'./assets/icons/buttons/logout.png',1, True)

    def display_text(x, y, text, color, size):
        font_model = pygame.font.Font(None, size)
        text_surface = font_model.render(text, True, color)
        text_rect = text_surface.get_rect(topleft = (x,y))
        window.blit(text_surface, text_rect)

    def GUI():
        background.display()
        user_status.display()

        if user_status.coin < 100:
            user_status.tips_index = 1
            button_minigame.visible = True
            button_play.visible = False
        else:
            button_minigame.visible = False
            button_play.visible = True
            user_status.tips_index = 2

        button_minigame.display()          
        button_play.display()
        button_shop.display()
        button_history.display()
        button_help.display()
        button_logout.display()

        music.bar()

    while isRunning:
        pygame.time.Clock().tick(60)

        music.play() if isRunning else None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_user_info(username, user_coin)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                if button_logout.image_rect.collidepoint(mousepos):
                    pygame.mixer.music.stop()
                    save_user_info(username, user_coin)
                    isRunning = False
                elif button_minigame.image_rect.collidepoint(mousepos) and button_minigame.visible:
                    pygame.mixer.music.stop()
                    import minigame
                    user_coin += minigame.run()
                    save_user_info(username, user_coin)
                elif button_play.image_rect.collidepoint(mousepos) and button_play.visible:
                    pass

        user_coin = json.load(open(DATABASE,"r"))[username].get('coin')       
        GUI()
        
        pygame.display.update() #cap nhat man hinh game
        



     