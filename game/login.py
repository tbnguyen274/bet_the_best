import pygame, json, os, sys, cv2, face_recognition, numpy as np, re, smtplib, math
from email.message import EmailMessage
from intro import display_intro
import game

# Xây dựng Database
DATABASE_DIRECTORY = 'db'
DATABASE = os.path.join(DATABASE_DIRECTORY, "user_data.json")

# Tạo databasee nếu chưa có
if not os.path.exists(DATABASE) or os.stat(DATABASE).st_size == 0:
    with open(DATABASE, 'w') as file:
        json.dump({}, file)

# Hàm lưu dữ liệu vào database
def save_to_database(data):
    with open(DATABASE, 'w') as file:
        json.dump(data, file, indent=4)

# Hàm kiếm tra chuỗi rỗng
def isempty(s):
    return len(s.strip()) == 0

# khối lệnh sẽ dc thực hiện khi đăng nhập thành công
def login_success(username):
    pygame.mixer.music.stop()
    game.mainmenu(username)

# Kích thước cửa sổ
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Hằng màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (108, 52, 40)
GRAY = (200, 200, 200)
DARKGRAY = (68, 80, 105)
SDARKGRAY = (39, 55, 77)
GREEN = (0, 255, 0)
LIGHTGREEN = (168, 223, 142)
NEONGREEN = (0, 223, 162)
CYAN = (64, 248, 255)
BLUE = (0, 169, 255)
DARKBLUE = (11, 40, 81)
MOMO = (248, 117, 170)
ORANGE = (245, 134, 52)
RED = (216, 0, 50)
LIGHTRED = (0, 0, 0)
PURPLE = (147, 118, 224)
NEONPURPLE = (147, 54, 180)
SKIN = (255, 242, 204)
MILK = (255, 242, 216)

def start_login():
    pygame.init() 

    # Tao cua so trinh dang nhap
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    login_icon = pygame.image.load('assets/icons/lock.png')
    pygame.display.set_caption('Bet the Best - Login')
    pygame.display.set_icon(login_icon)

    # loop bacground
    class background():
        def __init__(self):
            self.sourceclip = cv2.VideoCapture('assets/videos/tunnel.mp4')

        def display(self):
            ret, frame = self.sourceclip.read()
            if not ret:
                self.sourceclip.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.sourceclip.read()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame_frame = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
            window.blit(pygame_frame, (0, 0))

    def display_text(x, y, text, color, size):
        font_model = pygame.font.Font(None, size)
        text_surface = font_model.render(text, True, color)
        text_rect = text_surface.get_rect(topleft = (x,y))
        window.blit(text_surface, text_rect)

    class music():
        def __init__(self, music_file_paths, music_name_list, volume, bar_x, bar_y):
            self.music_file_path = music_file_paths
            self.music_name_list = music_name_list
            self.volume = volume
            self.music_end = pygame.USEREVENT + 1
            self.current_track_index = 0
            self.angle = 0
            self.bar_x = bar_x
            self.bar_y = bar_y

            pygame.mixer.music.set_endevent(self.music_end)
        
        def play(self):
            for event in pygame.event.get():
                if event.type == self.music_end:
                    self.current_track_index = (self.current_track_index + 1) % len(self.music_file_path)
                    pygame.mixer.music.load(self.music_file_path[self.current_track_index])
                    pygame.mixer.music.set_volume(self.volume)
                    pygame.mixer.music.play()

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.music_file_path[self.current_track_index])
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()

        def bar(self):
            r = int(127 + 127 * math.sin(math.radians(self.angle)))
            g = int(127 + 127 * math.sin(math.radians(self.angle + 120)))
            b = int(127 + 127 * math.sin(math.radians(self.angle + 240)))

            current_track_text = pygame.font.Font(None, 40).render("Now Playing: " + self.music_name_list[self.current_track_index], True, (r, g, b))
            window.blit(current_track_text, (self.bar_x, self.bar_y))

            self.angle += 1

    # Tạo form đăng nhập
    class form():
        def __init__(self):
            self.width, self.height = 700, 500
            self.x, self.y = (WINDOW_WIDTH - self.width) // 2, (WINDOW_HEIGHT - self.height) // 2
            self.color = (255,255,255)
            self.alpha = 240 # Điều chỉnh độ trong suốt của form
            self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.surface.fill((255,255,255, self.alpha))
            self.indent = 50 # Khoảng đẹm lề để căn chỉnh thành phần bên trong form
        
        def display(self):
            window.blit(self.surface, (self.x, self.y))

    class button():
        def __init__(self, x, y, width, height, button_color, text, text_color, font_size, border):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = button_color
            self.text_color = text_color
            self.border = border
            self.rect = None
            self.border_rect = None
            self.click_sound = pygame.mixer.Sound('assets/sfx/pop-click-sound.mp3')
            self.click_sound.set_volume(0.2)
            self.clicked = False
            self.font = pygame.font.Font(None, font_size)
            self.text_surface = self.font.render(text, True, text_color)

        def display(self):
            mousepos = pygame.mouse.get_pos()
            if self.border:
                self.border_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                self.rect = pygame.Rect(self.x + 3, self.y + 3, self.width - 6, self.height - 6)
                if self.rect.collidepoint(mousepos):
                    pygame.draw.rect(window, DARKGRAY, self.border_rect)
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                        self.clicked = True
                        self.click_sound.play()
                else:
                    pygame.draw.rect(window, BLACK, self.border_rect)
                    pygame.draw.rect(window, self.color, self.rect)
            else:
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                if self.rect.collidepoint(mousepos):
                    pygame.draw.rect(window, DARKGRAY, self.rect)
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                        self.clicked = True
                        self.click_sound.play()
                else:
                    pygame.draw.rect(window, self.color, self.rect)
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False     
            
            window.blit(self.text_surface, (self.x + self.width//2 - self.text_surface.get_width()//2, self.y + self.height//2 - self.text_surface.get_height()//2))

    class label():
        def __init__(self, x, y, text, color, font_size):
            self.x = x
            self.y = y
            self.color = color
            self.text = text
            self.font = pygame.font.Font(None, font_size)
            self.text_surface = self.font.render(text, True, color)
        
        def display(self):
            window.blit(self.text_surface, (self.x, self.y))

    class input():
        def __init__(self, x, y, width, height, text_color, font_size, ispassword, placeholder, placeholder_text, input_active):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.box_color = GRAY
            self.box = pygame.rect.Rect(x,y,width,height)
            self.box_border = pygame.rect.Rect(x - 2,y - 2,width + 4,height + 4)
            self.text = ''
            self.active = input_active
            self.font = pygame.font.Font(None, font_size)
            self.ispassword = ispassword
            self.text_color = text_color
            self.text_surface = self.font.render(self.text, True, self.text_color)
            self.indent = (self.height - self.text_surface.get_height())//2
            self.placeholder = placeholder
            self.placeholder_text = placeholder_text
            self.placeholder_surface = self.font.render(self.placeholder_text, True, DARKGRAY)

        def checkmaxreached(self, string):
            temp_surface = self.font.render(string, True, self.text_color)
            if temp_surface.get_width() > self.width:
                return 'Maximum characters reached'
            return string

        def display(self):
            if self.active:
                pygame.draw.rect(window, BLACK, self.box_border)
            pygame.draw.rect(window, self.box_color, self.box)
            if isempty(self.text) and self.placeholder:
                window.blit(self.placeholder_surface, (self.x + self.indent, self.y + self.indent))
            if self.ispassword:
                self.text_surface =  self.font.render(self.checkmaxreached('*'*len(self.text) if self.text else self.text), True, self.text_color)
            elif self.active:
                self.text_surface = self.font.render(self.checkmaxreached(self.text+'|'), True, self.text_color)
            else:
                self.text_surface = self.font.render(self.checkmaxreached(self.text), True, self.text_color)
            window.blit(self.text_surface, (self.x + self.indent, self.y + self.indent))

    class login_pop_up():
        def __init__(self, text, color, x ,y):
            self.text = text
            self.color = color
            self.login_pop_font = pygame.font.Font(None, 34)
            self.text_surface = self.login_pop_font.render(self.text, True, self.color)
            self.text_rect = self.text_surface.get_rect(topleft = (x,y))
            self.display = False

        def pop(self):
            window.blit(self.text_surface, self.text_rect)

    class password():
        def __init__(self):
            self.display = True

            self.label_username = label(form.x + 50, form.y +36, 'Username:', BLACK, 36)
            self.label_password = label(form.x + 50, form.y + 126, 'Password:', BLACK, 36)

            self.input_username = input(form.x + form.indent, form.y + 70, form.width - form.indent*2, 30, BLACK, 32, False, False, None, True)
            self.input_password = input(form.x + form.indent, form.y + 160, form.width - form.indent*2, 30, BLACK, 32, True, False, None, False)

            self.button_login = button(form.x + form.indent, form.y + 270, (form.width - form.indent*2 - 20)//2, 50, BLACK, 'Login', WHITE, 32, False)
            self.button_register = button(self.button_login.x + self.button_login.width + 20, self.button_login.y, self.button_login.width, 50, WHITE, 'Register', BLACK, 32, True)
            self.button_faceid = button(self.button_login.x, self.button_login.y + 70, form.width - form.indent*2, 50, DARKBLUE, "Login with Face ID", WHITE, 32, False)

            self.pop_fail = login_pop_up("Login failed!", RED, form.x + form.indent, self.button_faceid.y + self.button_faceid.height + 30)
            self.pop_empty = login_pop_up("Please fill all the space!", NEONPURPLE, form.x + form.indent, self.button_faceid.y + self.button_faceid.height + 30)
            self.start_time = 0

        def validate_login(self, username, password):
            with open(DATABASE, "r") as file: #cập nhật lại database rồi mới kiểm
                user_data = json.load(file)
                if username in user_data and user_data[username]['password'] == password:
                    return True
            return False

        def GUI(self):
            # Vẽ labels
            self.label_username.display()
            self.label_password.display()
            # Tạo ô nhập chữ
            self.input_username.display()
            self.input_password.display()
            display_text(form.x + 50, form.y + 210, "*Tips: Press tab to toggle between the input boxes", DARKGRAY, 28)
            # Nút
            self.button_login.display()
            self.button_register.display()
            self.button_faceid.display()

            return self.button_login.rect, self.button_register.rect, self.button_faceid.rect

        def run(self):
            # Vẽ giao diện password
            button_login, button_register, button_faceid = self.GUI()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos() # Lấy vị trí chuột
                    if button_faceid.collidepoint(mouse_pos): # Nếu nhấn nút này, chuyển sang giao diện đăng nhập khuôn mặt
                        self.display = False
                        faceid.display = True
                        register.display = False
                        self.input_username.text = self.input_password.text = ''
                    elif button_login.collidepoint(mouse_pos):
                        if isempty(self.input_username.text) or isempty(self.input_password.text): # Chừa trống, cảnh báo
                            self.pop_empty.display = True
                            self.start_time = pygame.time.get_ticks()
                        elif self.validate_login(self.input_username.text, self.input_password.text): # Nếu đúng mật khẩu, vào game
                            login_success(self.input_username.text)
                            self.input_username.text = self.input_password.text = ''
                        else:
                            self.pop_fail.display = True # Nếu sai thì thông báo
                            self.start_time = pygame.time.get_ticks()
                    elif button_register.collidepoint(mouse_pos):
                        self.display = faceid.display = False
                        register.display = True
                        self.input_username.text = self.input_password.text = ''
                elif event.type == pygame.KEYDOWN: # Cập nhật chuỗi nhận kí tự để in ra màn hình
                    if event.key == pygame.K_TAB:
                        self.input_username.active = not self.input_username.active
                        self.input_password.active = not self.input_password.active
                    elif self.input_username.active:
                        if event.key == pygame.K_RETURN:
                            self.input_username.active = False
                            self.input_password.active = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_username.text = self.input_username.text[:-1]
                        else:
                            self.input_username.text += event.unicode
                    elif self.input_password.active:
                        if event.key == pygame.K_RETURN: # Sau khi đã nhập mật khẩu vào ô thứ 2, nhấn enter để vào game cũng dc
                            if self.validate_login(self.input_username.text, self.input_password.text):
                                login_success(self.input_username.text)
                                self.input_username.text = self.input_password.text = ''
                            else:
                                self.pop_fail.display = True # Nếu sai thì thông báo
                                self.start_time = pygame.time.get_ticks()
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_password.text = self.input_password.text[:-1]
                        else:
                            self.input_password.text += event.unicode
                
            # Chữ hiển thị trạng thái đăng nhập trong 1,5s
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time
                
            if elapsed_time < 1500:
                if self.pop_fail.display:
                    self.pop_fail.pop()
                elif self.pop_empty.display:
                    self.pop_empty.pop()
            else:
                self.pop_fail.display = self.pop_empty.display = False

    class faceid():
        def __init__(self):
            self.display = False

            self.cam_capture = cv2.VideoCapture(0)
            self.cam_width = (form.width - form.indent*6)
            self.cam_height = (self.cam_width*9)//16
            self.cam_x = form.x + (form.width - self.cam_width)//2
            self.cam_y = form.y + form.indent
            self.cam_border = pygame.Rect(self.cam_x-2, self.cam_y-2 , self.cam_width+4, self.cam_height+4)

            self.return_button = pygame.image.load('assets/icons/return2.png').convert_alpha()
            self.return_button = pygame.transform.scale(self.return_button,(70,70))
            self.return_button_rect = self.return_button.get_rect(topleft = (form.x + form.indent, form.y+form.indent))

            self.button_register = button(form.x + form.indent, form.y + form.height - 160, (form.width - form.indent*2) // 3, 40, SDARKGRAY, 'Register', WHITE, 36, False)
            self.input_username = input(self.button_register.x + self.button_register.width + 20, self.button_register.y, form.width - (form.indent*2 + self.button_register.width + 20), 40, BLACK, 32, False, True, 'Username', False)
            self.button_login = button(form.x + form.indent, self.button_register.y + 60, form.width - form.indent*2, 50, SDARKGRAY, 'Login with Face ID', WHITE, 36, False)

            self.pop_empty = login_pop_up("Enter username!", ORANGE, form.x + form.width - 330, self.button_register.y - 40)
            self.pop_registersuccess = login_pop_up("Account created!", GREEN, form.x + form.width - 330, self.button_register.y - 40)
            self.pop_noface = login_pop_up("No face detected!", RED, form.x + form.width - 330, self.button_register.y - 40)
            self.pop_exist = login_pop_up("User already exist!", PURPLE, form.x + form.width - 330, self.button_register.y - 40)
            self.pop_loginfail = login_pop_up("User doesn't exist!", NEONGREEN, form.x + form.width - 330, self.button_register.y - 40)

            self.register_clicked = self.login_clicked = False
            self.start_time = 0

        def register_user(self, username, face_encoding):
            with open(DATABASE, "r") as file: #cập nhật lại database rồi mới kiểm
                user_data = json.load(file)
                user_data[username] = {
                    "password": '', 
                    "face_encoding": face_encoding.tolist(), 
                    "coin": 0,
                    'email': ''
                    }
            save_to_database(user_data)

        def GUI(self):
            # Vẽ nút
            self.button_register.display()
            self.input_username.display()
            self.button_login.display()
            window.blit(self.return_button, self.return_button_rect)
            display_text(form.x + 50, self.button_register.y - 40, "*Tips: Press tab to toggle input", DARKGRAY, 28)

        def run(self):
            ret, frame = self.cam_capture.read()

            # Tạo khung để chiếu lên màn hình trực quan (Camera feed)
            frame = cv2.resize(frame, (self.cam_width,self.cam_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.image.frombuffer(frame.flatten(), (self.cam_width,self.cam_height), 'RGB')
            pygame.draw.rect(window, BLACK, self.cam_border) #Ve vien
            window.blit(frame_surface, (self.cam_x, self.cam_y))  # Display camera feed in the square

            self.GUI()

            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.return_button_rect.collidepoint(mouse_pos):  # Chuyển giao diện nếu ấn nút này
                        password.display = True
                        self.display = register.display = False
                        self.input_username.text = ''
                    elif self.button_register.rect.collidepoint(mouse_pos):
                        self.register_clicked = True
                    elif self.button_login.rect.collidepoint(mouse_pos):
                        self.login_clicked = True
                elif event.type == pygame.KEYDOWN: # Cập nhật chuỗi username
                    if event.key == pygame.K_TAB:
                        self.input_username.active = not self.input_username.active
                    elif self.input_username.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.input_username.text = self.input_username.text[:-1]
                        else:
                            self.input_username.text += event.unicode
            
            if self.register_clicked:
                enhanced_frame = frame.copy()
                enhanced_frame = cv2.resize(enhanced_frame, (700,700))
                enhanced_frame = cv2.convertScaleAbs(enhanced_frame, alpha=1.5, beta=50)
                enhanced_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2RGB)
                gray_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2GRAY)

                face_locations = face_recognition.face_locations(gray_frame)

                if len(face_locations) > 0: # Kiểm tra có detect dc khuôn mặt không
                    face_encodings = face_recognition.face_encodings(enhanced_frame, face_locations)
                    face_encodings_from_db = []
                    with open(DATABASE) as file:
                        data = json.load(file)
                        for user_data in data.values():
                            face_encodings_from_db.append(np.array(user_data['face_encoding']))
                    face_encoding_exists = False
                    for face_encoding in face_encodings:
                        # Check if the new face encoding matches any face encoding in the database
                        for known_face_encoding in face_encodings_from_db:
                            if known_face_encoding.shape == (0,):  # Skip empty face encodings
                                continue
                            match = face_recognition.compare_faces([known_face_encoding], face_encoding)
                            if match[0]:
                                face_encoding_exists = True
                                break

                    if face_encoding_exists or self.input_username.text in json.load(open(DATABASE, "r")):
                        self.pop_exist.display = True
                    elif isempty(self.input_username.text): # Chừa trống, không cho đki
                        self.pop_empty.display = True
                    else: # Không có vấn đề gì thì đky
                        self.register_user(self.input_username.text, face_encoding)
                        self.pop_registersuccess.display = True
                        self.input_username.text = ''
                else:
                    self.pop_noface.display = True
                self.start_time = pygame.time.get_ticks()
                self.register_clicked = False
            elif self.login_clicked:
                enhanced_frame = frame.copy()
                enhanced_frame = cv2.resize(enhanced_frame, (700,700))
                enhanced_frame = cv2.convertScaleAbs(enhanced_frame, alpha=1.5, beta=50)
                enhanced_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2RGB)
                gray_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2GRAY)

                face_locations = face_recognition.face_locations(gray_frame)

                if len(face_locations) > 0:
                    face_encodings = face_recognition.face_encodings(enhanced_frame, face_locations)
                    with open(DATABASE, "r") as database:
                        user_data = json.load(database)
                        found_match = False
                        for face_encoding in face_encodings:
                            for face_username, user_info in user_data.items():
                                stored_face_encoding = np.array(user_info.get("face_encoding"))
                                if stored_face_encoding.shape == (0,):  # Skip empty face encodings
                                    continue
                                match = face_recognition.compare_faces([stored_face_encoding], face_encoding)
                                if match[0]:  # If a match is found in the database
                                    found_match = True
                                    login_success(face_username)
                                    break
                            if found_match:
                                break
                        if not found_match:
                            self.pop_loginfail.display = True
                else:
                    self.pop_noface.display = True
                self.start_time = pygame.time.get_ticks()
                self.login_clicked = False

            # Hiển thị chữ thông báo 1s
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time

            if elapsed_time < 1000:
                if self.pop_empty.display:
                    self.pop_empty.pop()
                elif self.pop_noface.display:
                    self.pop_noface.pop()
                elif self.pop_registersuccess.display:
                    self.pop_registersuccess.pop()
                elif self.pop_exist.display:
                    self.pop_exist.pop()
                elif self.pop_loginfail.display:
                    self.pop_loginfail.pop()
            else:
                self.pop_empty.display = self.pop_noface.display = self.pop_registersuccess.display = self.pop_exist.display = self.pop_loginfail.display = False

    class register():
        def __init__(self):
            self.display = False
            self.label_username = label(form.x + form.indent, form.y + form.indent - 10, 'Username:', BLACK, 36)
            self.label_password = label(form.x + 50, self.label_username.y + 75, 'Password:', BLACK, 36)
            self.label_repassword = label(form.x + 50, self.label_password.y + 75, 'Confirm password:', BLACK, 36)
            self.label_email = label(form.x + 50, self.label_repassword.y + 75, 'Email:', BLACK, 36)

            self.input_username = input(form.x + form.indent, self.label_username.y + 30, form.width - form.indent*2, 30, BLACK, 32, False, False, None, True)
            self.input_password = input(form.x + form.indent, self.input_username.y + 75, form.width - form.indent*2, 30, BLACK, 32, True, False, None, False)
            self.input_repassword = input(form.x + form.indent, self.input_password.y + 75, form.width - form.indent*2, 30, BLACK, 32, True, False, None, False)
            self.input_email = input(form.x + form.indent, self.input_repassword.y + 75, form.width - form.indent*2, 30, BLACK, 32, False, False, None, False)

            self.button_returnlogin = button(form.x + form.indent, self.input_email.y + self.input_email.height + 30, (form.width - form.indent*2 - 20)//2, 60, DARKBLUE, 'Return to login', WHITE, 32, False)
            self.button_register = button(self.button_returnlogin.x + self.button_returnlogin.width + 20, self.button_returnlogin.y, self.button_returnlogin.width, 60, BLACK, 'Register Now!', WHITE, 32, False)

            self.pop_empty = login_pop_up("Please fill all the space!", NEONPURPLE, form.x + form.indent, self.button_returnlogin.y + self.button_returnlogin.height + 20)
            self.pop_notmatch = login_pop_up("Passwords do not match", RED, form.x + form.indent, self.button_returnlogin.y + self.button_returnlogin.height + 20)
            self.pop_success = login_pop_up("Account created!", GREEN, form.x + form.indent, self.button_returnlogin.y + self.button_returnlogin.height + 20)
            self.pop_exist = login_pop_up("Account already existed", ORANGE, form.x + form.indent, self.button_returnlogin.y + self.button_returnlogin.height + 20)
            self.pop_validemail = login_pop_up("Please enter a valid email", ORANGE, form.x + form.indent, self.button_returnlogin.y + self.button_returnlogin.height + 20)

            self.start_time = 0

        def is_valid_email(self, email):
            # Regular expression pattern to match a basic email format
            pattern = r"[^@]+@[^@]+\.[^@]+"
            return re.match(pattern, email)

        def send_email_notification(self, receiver_email, username):
            sender_email = 'betthebestn0reply@hotmail.com'
            password = 'Bestthebestmailsender'
            smtp_server = 'smtp.office365.com'
            smtp_port = 587

            message = EmailMessage()
            message['Subject'] = '(Bet the Best) Account registered successfully!'
            message['From'] = sender_email
            message['To'] = receiver_email
            message.set_content('Hello ' + username + ', \n\nThank you for registering! Your account registration was successful. \n\nDare to bet, become the best! \n\nFrom Bet the Best team')

            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, password)
                server.send_message(message)
                server.quit()
                print("Email notification sent successfully")
            except Exception as e:
                print(f"Failed to send email: {str(e)}")

        def register_user(self, username, password, email):
            with open(DATABASE, "r") as file: #cập nhật lại database rồi mới kiểm
                user_data = json.load(file)
                user_data[username] = {
                    'password': password,
                    'face_encoding': [], 
                    'coin': 0,
                    'email': email
                    }
            save_to_database(user_data)

        def GUI(self):
            # Vẽ labels
            self.label_username.display()
            self.label_password.display()
            self.label_repassword.display()
            self.label_email.display()

            # Tạo ô nhập chữ
            self.input_username.display()
            self.input_password.display()
            self.input_repassword.display()
            self.input_email.display()

            # Nút
            self.button_register.display()
            self.button_returnlogin.display()

            return self.button_register.rect, self.button_returnlogin.rect

        def run(self):
            # Vẽ giao diện password
            register_button, return_login_button = self.GUI()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos() # Lấy vị trí chuột
                    if return_login_button.collidepoint(mouse_pos): # Nếu nhấn nút này, chuyển sang giao diện đăng nhập khuôn mặt
                        password.display = True
                        faceid.display = self.display = False
                        self.input_username.text = self.input_password.text = self.input_repassword.text = self.input_email.text = ''
                    elif register_button.collidepoint(mouse_pos):
                        if isempty(self.input_username.text) or isempty(self.input_password.text) or isempty(self.input_repassword.text) or isempty(self.input_email.text): # Chừa trống, cảnh báo
                            self.pop_empty.display = True
                        elif self.input_password.text != self.input_repassword.text:
                            self.pop_notmatch.display = True
                        elif self.input_username.text in json.load(open(DATABASE,"r")): # Nếu tên ng chơi đã tồn tại, thông báo 
                            self.pop_exist.display = True
                        elif self.input_email.text in [user_info.get('email') for user_info in json.load(open(DATABASE,"r")).values()]:
                            self.pop_exist.display = True
                        elif not self.is_valid_email(self.input_email.text):
                            self.pop_validemail.display = True
                        else:
                            self.register_user(self.input_username.text, self.input_password.text, self.input_email.text)
                            self.send_email_notification(self.input_email.text,self.input_username.text)
                            self.input_username.text = self.input_password.text = self.input_repassword.text = self.input_email.text = ''
                            self.pop_success.display = True
                        self.start_time = pygame.time.get_ticks()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        if self.input_username.active:
                            self.input_username.active = False
                            self.input_password.active = True
                            self.input_repassword.active = False
                            self.input_email.active = False
                        elif self.input_password.active:
                            self.input_username.active = False
                            self.input_password.active = False
                            self.input_repassword.active = True
                            self.input_email.active = False
                        elif self.input_repassword.active:
                            self.input_username.active = False
                            self.input_password.active = False
                            self.input_repassword.active = False
                            self.input_email.active = True
                        elif self.input_email.active:
                            self.input_username.active = True
                            self.input_password.active = False
                            self.input_repassword.active = False
                            self.input_email.active = False
                    elif self.input_username.active:
                        if event.key == pygame.K_RETURN:
                            self.input_username.active = False
                            self.input_password.active = True
                            self.input_repassword.active = False
                            self.input_email.active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_username.text = self.input_username.text[:-1]
                        else:
                            self.input_username.text += event.unicode
                    elif self.input_password.active:
                        if event.key == pygame.K_RETURN:
                            self.input_username.active = False
                            self.input_password.active = False
                            self.input_repassword.active = True
                            self.input_email.active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_password.text = self.input_password.text[:-1]
                        else:
                            self.input_password.text += event.unicode
                    elif self.input_repassword.active:
                        if event.key == pygame.K_RETURN:
                            self.input_username.active = False
                            self.input_password.active = False
                            self.input_repassword.active = False
                            self.input_email.active = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_repassword.text = self.input_repassword.text[:-1]
                        else:
                            self.input_repassword.text += event.unicode
                    elif self.input_email.active:
                        if event.key == pygame.K_RETURN: # Sau khi đã nhập mật khẩu vào ô thứ 2, nhấn enter để vào game cũng dc
                            if isempty(self.input_username.text) or isempty(self.input_password.text) or isempty(self.input_repassword.text) or isempty(self.input_email.text): # Chừa trống, cảnh báo
                                self.pop_empty.display = True
                            elif self.input_username.text in json.load(open(DATABASE,"r")): # Nếu tên ng chơi đã tồn tại, thông báo
                                self.pop_exist.display = True
                            elif self.input_password.text != self.input_repassword.text:
                                self.pop_notmatch.display = True
                            elif not self.is_valid_email(self.input_email.text):
                                self.pop_validemail.display = True
                            else: # Nếu không bị gì, đky
                                self.register_user(self.input_username.text, self.input_password.text, self.input_email.text)
                                self.send_email_notification(self.input_email.text, self.input_username.text)
                                self.input_username.text = self.input_password.text = self.input_repassword.text = self.input_email.text = ''
                                self.pop_success.display = True
                            self.start_time = pygame.time.get_ticks()
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_email.text = self.input_email.text[:-1]
                        else:
                            self.input_email.text += event.unicode
            
            # Chữ hiển thị trạng thái đăng nhập trong 1,5s
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time
            
            if elapsed_time < 1500:
                if self.pop_success.display:
                    self.pop_success.pop()
                elif self.pop_exist.display:
                    self.pop_exist.pop()
                elif self.pop_empty.display:
                    self.pop_empty.pop()
                elif self.pop_notmatch.display:
                    self.pop_notmatch.pop()
                elif self.pop_validemail.display:
                    self.pop_validemail.pop()
            else:
                self.pop_validemail.display = self.pop_empty.display = self.pop_notmatch.display = pop_empty_display = self.pop_exist.display = self.pop_success.display = False

    background = background()
    form = form()
    password = password()
    faceid = faceid()
    register = register()
    music = music(['assets/musics/login_music.mp3'],None,0.3,None,None)

    # Main loop
    while True:
        pygame.time.Clock().tick(60)
        background.display()
        form.display()
            # Hien thi cac state dang nhap 
        if password.display:
            password.run()
        elif faceid.display:
            faceid.run()
        elif register.display:
            register.run()    
        
        music.play()
            
        pygame.display.update()

def restart_login():
    pygame.quit()
    start_login()

if __name__ == "__main__":
    pygame.init()
    display_intro(pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)))
    start_login()