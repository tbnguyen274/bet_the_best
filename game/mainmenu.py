import pygame, cv2, math, sys, json, os
import loading

DATABASE_DIRECTORY = 'db'
DATABASE = os.path.join(DATABASE_DIRECTORY, "user_data.json")
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def save_to_database(data):
    with open(DATABASE, 'w') as file:
        json.dump(data, file, indent=4)

def save_coins(username, coin):
    with open(DATABASE, "r") as file:
        data = json.load(file)
        data[username]['coin'] = coin
    save_to_database(data)

def save_avatar(username, index):
    with open(DATABASE, "r") as file:
        data = json.load(file)
        data[username]['avatar'] = index
    save_to_database(data)

def update_history_values(username, new_history_value):
    with open(DATABASE, "r") as file:
        user_data = json.load(file)
        
        # Check if the user exists in the database
        if username in user_data:
            # Update history5 with the value of history4
            user_data[username]["history5"] = user_data[username]["history4"]
            user_data[username]["history4"] = user_data[username]["history3"]
            user_data[username]["history3"] = user_data[username]["history2"]
            user_data[username]["history2"] = user_data[username]["history1"]
            user_data[username]["history1"] = new_history_value
            
            # Save the updated data to the database
            save_to_database(user_data)

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
            self.clickable = True
        
        def hover_effect(self, image):
            # Tạo bản sao của hình ảnh gốc với màu sậm đi (ở đây tôi chọn màu đen nhẹ)
            hover_image = image.copy()
            hover_image.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_SUB)  # Điều chỉnh mức độ sậm màu
            return hover_image

        def display(self):
            if self.visible:
                cursor_pos = pygame.mouse.get_pos()
                window.blit(self.image,(self.image_rect.x,self.image_rect.y)) 
                if self.clickable:
                    if self.image_rect.collidepoint(cursor_pos):
                        window.blit(self.hover_image,(self.image_rect))
                        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                            self.clicked = True
                            self.click_sound.play()
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

            self.avatar_list = ['./assets/icons/avatars/1.png','./assets/icons/avatars/2.png','./assets/icons/avatars/3.png','./assets/icons/avatars/4.png','./assets/icons/avatars/5.png','./assets/icons/avatars/6.png','./assets/icons/avatars/7.png','./assets/icons/avatars/8.png','./assets/icons/avatars/9.png']
            self.avatar_index = 0
            self.current_avatar = self.avatar_list[self.avatar_index]
            self.avatar = pygame.image.load(self.current_avatar).convert_alpha()
            self.avatar = pygame.transform.scale(self.avatar,(80,80))
            self.avatar_rect = self.avatar.get_rect(topleft = (30,(self.height-self.avatar.get_height())//2))

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
            self.avatar_index = json.load(open(DATABASE,"r"))[username].get('avatar')   
            self.current_avatar = self.avatar_list[self.avatar_index]
            self.avatar = pygame.image.load(self.current_avatar).convert_alpha()
            self.avatar = pygame.transform.scale(self.avatar,(80,80))
            window.blit(self.avatar,self.avatar_rect)

            window.blit(self.username_text, (self.avatar_rect.x + self.avatar.get_width() + 10, self.username_text_y))

            window.blit(self.coin_icon, (self.coin_icon_x, self.coin_icon_y))
            self.coin = user_coin
            self.coin_value = self.font.render(": " + self.numdisplay(self.coin), True, (255,255,255))
            window.blit(self.coin_value, (self.coin_icon_x + self.coin_icon.get_width() + 10, self.coin_value_y))
            window.blit(self.tips, (10, self.height+ 10))

    class avatar_select():
        def __init__(self):
            self.display = False
            
            self.width = 570
            self.height = int(self.width*545/620)
            self.x = (WINDOW_WIDTH - self.width)//2
            self.y = (WINDOW_HEIGHT - self.height)//2
            self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
            self.frame = pygame.image.load('assets/icons/frame3.png')
            self.frame = pygame.transform.scale(self.frame, (600,int(600*545/620)))
            self.frame_rect = self.frame.get_rect(center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            self.background.fill((0,0,0,170))

            self.ava1 = self.avatars('assets/icons/avatars/1.png',1,1)
            self.ava2 = self.avatars('assets/icons/avatars/2.png',2,1)
            self.ava3 = self.avatars('assets/icons/avatars/3.png',3,1)
            self.ava4 = self.avatars('assets/icons/avatars/4.png',1,2)
            self.ava5 = self.avatars('assets/icons/avatars/5.png',2,2)
            self.ava6 = self.avatars('assets/icons/avatars/6.png',3,2)
            self.ava7 = self.avatars('assets/icons/avatars/7.png',1,3)
            self.ava8 = self.avatars('assets/icons/avatars/8.png',2,3)
            self.ava9 = self.avatars('assets/icons/avatars/9.png',3,3)

        class avatars():
            def __init__(self, image, posx, posy):
                self.width = 620
                self.height = 545
                self.mother_x = (WINDOW_WIDTH - self.width)//2
                self.mother_y = (WINDOW_HEIGHT - self.height)//2
                self.image = pygame.image.load(image).convert_alpha()
                self.image = pygame.transform.scale(self.image,(100,100))
                self.hover_image = self.hover_effect(self.image)
                if posx == 1:
                    self.x = self.mother_x + self.width//4
                elif posx == 2:
                    self.x = self.mother_x + self.width//2
                elif posx == 3:
                    self.x = self.mother_x + self.width*3//4
                if posy == 1:
                    self.y = self.mother_y + self.height//4
                elif posy == 2:
                    self.y = self.mother_y + self.height//2
                elif posy == 3:
                    self.y = self.mother_y + self.height*3//4
                self.rect = self.image.get_rect(center=(self.x,self.y))
                self.clicked = False
                self.click_sound = pygame.mixer.Sound('./assets/sfx/pop-click-sound.mp3')
                self.click_sound.set_volume(0.2)

            def hover_effect(self, image):
                # Tạo bản sao của hình ảnh gốc với màu sậm đi (ở đây tôi chọn màu đen nhẹ)
                hover_image = image.copy()
                hover_image.fill((70, 70, 70), special_flags=pygame.BLEND_RGB_SUB)  # Điều chỉnh mức độ sậm màu
                return hover_image
            
            def display(self):
                window.blit(self.image, self.rect)
                mousepos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mousepos):
                    window.blit(self.hover_image,(self.rect))
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                        self.clicked = True
                        self.click_sound.play()
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
        def disable_buttons(self):
            button_credit.clickable = button_help.clickable = button_history.clickable = button_logout.clickable = button_minigame.clickable = button_play.clickable = False
        
        def enable_buttons(self):
            button_credit.clickable = button_help.clickable = button_history.clickable = button_logout.clickable = button_minigame.clickable = button_play.clickable = True

        def run(self):
            if self.display:
                window.blit(self.background, (0,0))
                pygame.draw.rect(window, (221, 230, 237), self.rect)
                window.blit(self.frame, self.frame_rect)

                self.ava1.display()
                self.ava2.display()
                self.ava3.display()
                self.ava4.display()
                self.ava5.display()
                self.ava6.display()
                self.ava7.display()
                self.ava8.display()
                self.ava9.display()
                self.disable_buttons()
            elif not history.display and not help.display:
                self.enable_buttons()


    class history():
        def __init__(self):
            self.update_history()
            self.display = False

            self.width = 620
            self.height = 545
            self.x = (WINDOW_WIDTH - self.width)//2
            self.y = (WINDOW_HEIGHT - self.height)//2
            self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
            self.frame = pygame.image.load('assets/icons/frame2.png')
            self.frame = pygame.transform.scale(self.frame, (690,int(690*545/620)))
            self.frame_rect = self.frame.get_rect(center=(WINDOW_WIDTH//2,WINDOW_HEIGHT//2))
            self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            self.background.fill((0,0,0,170))

            self.big_font = pygame.font.SysFont(None, 80)
            self.normal_font = pygame.font.Font(None, 50)

            self.history_label = self.big_font.render('HISTORY', True, (45, 67, 86))
            self.history_label_rect = self.history_label.get_rect(topleft = (self.x + (self.width - self.history_label.get_width())//2 - 140, self.y + 40))
            self.empty = self.normal_font.render("", True, (0,0,0))
            
        def update_history(self):
            self.history_1 = json.load(open(DATABASE,"r"))[username]['history1']
            self.history_2 = json.load(open(DATABASE,"r"))[username]['history2']
            self.history_3 = json.load(open(DATABASE,"r"))[username]['history3']
            self.history_4 = json.load(open(DATABASE,"r"))[username]['history4']
            self.history_5 = json.load(open(DATABASE,"r"))[username]['history5']

        def numdisplay(self, num):
            if num / 1000000000 >= 1:
                return str(num//1000000000) + "." + str(num%1000000000)[0] + "B"
            elif num / 1000000 >= 1:
                return str(num//1000000) + "." + str(num%1000000)[0] + "M"
            elif num / 1000 >= 1:
                return str(num//1000) + "." + str(num%1000)[0] + "K"
            return str(num)

        def history_value(self, number):
            if number == 0:
                return ""
            elif number > 0:
                return f"+ {self.numdisplay(number)}"
            else:
                return f"- {self.numdisplay(abs(number))}"
        
        def history_color(self, number):
            if number == 0:
                return (0,0,0)
            elif number > 0:
                return (101, 183, 65)
            else:
                return (190, 49, 68)
        
        class history_values():
            def __init__(self, text, color, position, y):
                self.text = text
                self.color = color
                self.position = position
                self.normal_font = pygame.font.Font(None, 50)
                self.text_surface = self.normal_font.render(self.text, True, self.color)
                self.y = y
                if position == 1:
                    self.x = (WINDOW_WIDTH - 620)//2 + 60
                elif position == 2:
                    self.x = (WINDOW_WIDTH - self.text_surface.get_width())//2 - 20
                elif position == 3:
                    self.x = (WINDOW_WIDTH - 620)//2 + 620 - 60 - self.text_surface.get_width()
                self.rect = self.text_surface.get_rect(topleft = (self.x, self.y))
            
            def display(self):
                window.blit(self.text_surface,(self.x,self.y))

        def display_history(self):
            window.blit(self.history_label, self.history_label_rect)
            window.blit(self.frame, self.frame_rect)

            history1_1 = self.history_values(self.history_value(self.history_1[2]), self.history_color(self.history_1[2]), 1, self.history_label_rect.y + self.history_label.get_height()+ 40)
            history1_2 = self.history_values(self.history_1[1],  self.history_color(self.history_1[2]), 2, self.history_label_rect.y + self.history_label.get_height()+ 40)
            history1_3 = self.history_values(self.history_1[0],  self.history_color(self.history_1[2]), 3, self.history_label_rect.y + self.history_label.get_height()+ 40)

            history2_1 = self.history_values(self.history_value(self.history_2[2]), self.history_color(self.history_2[2]), 1, history1_1.y + 40 + history1_1.text_surface.get_height())
            history2_2 = self.history_values(self.history_2[1],  self.history_color(self.history_2[2]), 2, history1_1.y + 40 + history1_1.text_surface.get_height())
            history2_3 = self.history_values(self.history_2[0],  self.history_color(self.history_2[2]), 3, history1_1.y + 40 + history1_1.text_surface.get_height())

            history3_1 = self.history_values(self.history_value(self.history_3[2]), self.history_color(self.history_3[2]), 1, history2_1.y + 40 + history1_1.text_surface.get_height())
            history3_2 = self.history_values(self.history_3[1],  self.history_color(self.history_3[2]), 2, history2_1.y + 40 + history1_1.text_surface.get_height())
            history3_3 = self.history_values(self.history_3[0],  self.history_color(self.history_3[2]), 3, history2_1.y + 40 + history1_1.text_surface.get_height())

            history4_1 = self.history_values(self.history_value(self.history_4[2]), self.history_color(self.history_4[2]), 1, history3_1.y + 40 + history1_1.text_surface.get_height())
            history4_2 = self.history_values(self.history_4[1],  self.history_color(self.history_4[2]), 2, history3_1.y + 40 + history1_1.text_surface.get_height())
            history4_3 = self.history_values(self.history_4[0],  self.history_color(self.history_4[2]), 3, history3_1.y + 40 + history1_1.text_surface.get_height())

            history5_1 = self.history_values(self.history_value(self.history_5[2]), self.history_color(self.history_5[2]), 1, history4_1.y + 40 + history1_1.text_surface.get_height())
            history5_2 = self.history_values(self.history_5[1],  self.history_color(self.history_5[2]), 2, history4_1.y + 40 + history1_1.text_surface.get_height())
            history5_3 = self.history_values(self.history_5[0],  self.history_color(self.history_5[2]), 3, history4_1.y + 40 + history1_1.text_surface.get_height())

            if self.history_1[2] == 0:
                window.blit(self.empty, (self.x + (self.width - self.empty.get_width())//2, history1_1.y))
            else:
                history1_1.display()
                history1_2.display()
                history1_3.display()
            if self.history_2[2] == 0:
                window.blit(self.empty, (self.x + (self.width - self.empty.get_width())//2, history2_1.y))
            else:
                history2_1.display()
                history2_2.display()
                history2_3.display()
            if self.history_3[2] == 0:
                window.blit(self.empty, (self.x + (self.width - self.empty.get_width())//2, history3_1.y))
            else:
                history3_1.display()
                history3_2.display()
                history3_3.display()
            if self.history_4[2] == 0:
                window.blit(self.empty, (self.x + (self.width - self.empty.get_width())//2, history4_1.y))
            else:
                history4_1.display()
                history4_2.display()
                history4_3.display()
            if self.history_5[2] == 0:
                window.blit(self.empty, (self.x + (self.width - self.empty.get_width())//2, history5_1.y))
            else:
                history5_1.display()
                history5_2.display()
                history5_3.display()

        def disable_buttons(self):
            button_credit.clickable = button_help.clickable = button_history.clickable = button_logout.clickable = button_minigame.clickable = button_play.clickable = False
        
        def enable_buttons(self):
            button_credit.clickable = button_help.clickable = button_history.clickable = button_logout.clickable = button_minigame.clickable = button_play.clickable = True
        
        def run(self):
            if self.display:
                window.blit(self.background, (0,0))
                pygame.draw.rect(window, (221, 230, 237), self.rect)

                self.update_history()
                self.display_history()
                self.disable_buttons()
            else:
                self.enable_buttons()
    
    class help_page():
        def __init__(self):
            self.display = False

            self.width = 960
            self.height = int(960*9/16)
            self.x = (WINDOW_WIDTH - self.width)//2
            self.y = (WINDOW_HEIGHT - self.height)//2
            self.frame = pygame.image.load('assets/icons/frame.png').convert_alpha()
            self.frame = pygame.transform.scale(self.frame, (1035,int(1035*9/16)))
            self.frame_rect = self.frame.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
            self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            self.background.fill((0,0,0,170))
            self.instructions = [
                "Welcome to Bet The Best!",
                "Start with 300 coins. Bet wisely!",
                "Coins are everything—win or play mini-games!",
                "Race effects are unpredictable—brace yourself!",
                "Finish top 3 for coins; lose otherwise!",
                "",
                "Get ready for excitement! Let's race!"
            ]
            self.big_font = pygame.font.Font(None, 80)
            self.normal_font = pygame.font.Font(None, 50)

            self.help_label = self.big_font.render('GAME INSTRUCTIONS', True, (24, 61, 61))
            self.help_label_rect = self.help_label.get_rect(topleft = (self.x + (self.width - self.help_label.get_width())//2, self.y + 50))

            self.text_x = self.x + 80
            self.text_y = self.help_label_rect.y + self.help_label.get_height() + 40
            

        def disable_buttons(self):
            button_credit.clickable = button_help.clickable = button_history.clickable = button_logout.clickable = button_minigame.clickable = button_play.clickable = False
        
        def enable_buttons(self):
            button_credit.clickable = button_help.clickable = button_history.clickable = button_logout.clickable = button_minigame.clickable = button_play.clickable = True

        def run(self):
            if self.display:
                window.blit(self.background, (0,0))
                pygame.draw.rect(window, (221, 230, 237), self.rect)
                window.blit(self.frame, self.frame_rect)
                window.blit(self.help_label, self.help_label_rect)
                for line in self.instructions:
                    text = self.normal_font.render(line, True, (4, 28, 50))
                    text_rect = text.get_rect(topleft = (self.text_x, self.text_y))
                    window.blit(text, text_rect)
                    self.text_y += 43
                self.text_y = self.help_label_rect.y + self.help_label.get_height() + 40
                self.disable_buttons()
            elif not history.display:
                self.enable_buttons()



    background = background()
    music = music(['./assets/musics/gone-fishing-shandr.mp3','./assets/musics/tech-aylex.mp3', './assets/musics/cyberpunk-alexproduction.mp3'], ['Shandr - Gone fishing','Aylex - Tech','Alexproduction - Cyberpunk'], 0.3, 20, 680)
    user_status = user_status()

    button_play = button(740,170,'./assets/icons/buttons/play.png',1, True)
    button_minigame = button(740,170,'./assets/icons/buttons/minigame.png',1, False)
    button_credit = button(740,390,'./assets/icons/buttons/credit.png',1, True)
    button_history = button(740,280,'./assets/icons/buttons/history.png',1, True)
    button_help = button(740,500,'./assets/icons/buttons/help.png',1, True)
    button_logout = button(740,610,'./assets/icons/buttons/logout.png',1, True)
    history = history()
    help = help_page()
    avatar_selection = avatar_select()

    def GUI():
        background.display()
        music.bar()
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
        button_credit.display()
        button_history.display()
        button_help.display()
        button_logout.display()
        history.run()
        help.run()
        avatar_selection.run()

    while isRunning:
        pygame.time.Clock().tick(60)

        music.play() if isRunning else None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_coins(username, user_coin)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                if button_logout.image_rect.collidepoint(mousepos) and button_logout.clickable:
                    pygame.mixer.music.stop()
                    save_coins(username, user_coin)
                    loading.run(4)
                    isRunning = False
                elif button_minigame.image_rect.collidepoint(mousepos) and button_minigame.visible and button_minigame.clickable:
                    pygame.mixer.music.stop()
                    loading.run(3)
                    import minigame
                    user_coin += minigame.run()
                    save_coins(username, user_coin)
                elif button_play.image_rect.collidepoint(mousepos) and button_play.visible and button_play.clickable:
                    import control_button
                    pygame.mixer.music.stop()
                    new_value = control_button.run_test(user_coin)
                    if new_value == ["","",0]:
                        pass
                    else:
                        user_coin += new_value[2]
                        update_history_values(username, new_value)
                        save_coins(username, user_coin)
                elif button_history.image_rect.collidepoint(mousepos) and history.display == False and button_history.clickable:
                    history.display = True
                elif not history.rect.collidepoint(mousepos) and history.display == True and not button_history.clickable:
                    history.display = False
                elif button_help.image_rect.collidepoint(mousepos) and help.display == False and button_help.clickable:
                    help.display = True
                elif not help.rect.collidepoint(mousepos) and help.display == True and not button_history.clickable:
                    help.display = False
                elif user_status.avatar_rect.collidepoint(mousepos) and avatar_selection.display == False:
                    avatar_selection.display = True
                elif avatar_selection.display:
                    if avatar_selection.ava1.rect.collidepoint(mousepos):
                        save_avatar(username, 0)
                    elif avatar_selection.ava2.rect.collidepoint(mousepos):
                        save_avatar(username, 1)
                    elif avatar_selection.ava3.rect.collidepoint(mousepos):
                        save_avatar(username, 2)
                    elif avatar_selection.ava4.rect.collidepoint(mousepos):
                        save_avatar(username, 3)
                    elif avatar_selection.ava5.rect.collidepoint(mousepos):
                        save_avatar(username, 4)
                    elif avatar_selection.ava6.rect.collidepoint(mousepos):
                        save_avatar(username, 5)
                    elif avatar_selection.ava7.rect.collidepoint(mousepos):
                        save_avatar(username, 6)
                    elif avatar_selection.ava8.rect.collidepoint(mousepos):
                        save_avatar(username, 7)
                    elif avatar_selection.ava9.rect.collidepoint(mousepos):
                        save_avatar(username, 8)
                    elif not avatar_selection.rect.collidepoint(mousepos):
                        avatar_selection.display = False

        user_coin = json.load(open(DATABASE,"r"))[username].get('coin')     
        GUI()
        
        pygame.display.update() #cap nhat man hinh game
        

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    mainmenu("bew")