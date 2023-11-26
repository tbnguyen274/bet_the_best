import pygame, json, os, sys, cv2, face_recognition, numpy as np

#####################################################   DATABASE   ################################################################
# Xây dựng Database
DATABASE_DIRECTORY = './db'
DATABASE = os.path.join(DATABASE_DIRECTORY, "user_data.json")

def initialize_database():
    #Nếu chưa có database thì tạo và ghi vào đó: "{}" để chứa dữ liệu
    if not os.path.exists(DATABASE) or os.stat(DATABASE).st_size == 0:
        with open(DATABASE, 'w') as file:
            json.dump({}, file)

    # load dữ liệu có sẵn từ database trước khi chạy
    try:
        with open(DATABASE, "r") as database:
            return json.load(database)
    except FileNotFoundError:
        return {}

# Lưu dữ liệu từ database vào biến 'user_data' 
user_data = initialize_database()

# Hàm để lưu thông tin vào database
def save_to_database(data):
    with open(DATABASE, 'w') as file:
        json.dump(data, file, indent=4)

# Hàm kiếm tra chuỗi rỗng (Để check input password và username có trống hay không)
def isempty(s):
    return len(s.strip()) == 0

# Hàm đăng kí tài khoản
def register_user(username, password):
    user_data[username] = {
        'password': password, 
        'face_encoding': [], 
        'coin': 0}
    save_to_database(user_data)

# Hàm đăng kí tài khoản dành cho nhận diện khuôn mặt
def register_user_facerecognition(username, face_encoding):
    user_data[username] = {
        "password": '', 
        "face_encoding": face_encoding.tolist(), 
        "coin": 0
        }
    save_to_database(user_data)

# Hàm đánh giá mật khẩu đăng nhập
def validate_login(username, password):
    with open(DATABASE, "r") as file: #cập nhật lại database rồi mới kiểm
        user_data = json.load(file)
    if username in user_data and user_data[username]['password'] == password:
        return True
    return False

######################################################   PYGAME   ###################################################################

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

pygame.init() 

# Tao cua so trinh dang nhap
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
login_icon = pygame.image.load('./assets/icons/lock.png')
pygame.display.set_caption('Bet the Best - Login')
pygame.display.set_icon(login_icon)

# loop bacground
background = cv2.VideoCapture('./assets/videos/tunnel.mp4')

def login_loop_background():
    ret, frame = background.read()
    if not ret:
        background.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = background.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame_frame = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
    window.blit(pygame_frame, (0, 0))

# Tạo form đăng nhập
form_width, form_height = 700, 500
form_x, form_y = (WINDOW_WIDTH - form_width) // 2, (WINDOW_HEIGHT - form_height) // 2
form_color = (255,255,255)
form_alpha = 240 # Điều chỉnh độ trong suốt của form
form = pygame.Surface((form_width, form_height), pygame.SRCALPHA)
form.fill((255,255,255, form_alpha))
form_indent = 50 # Khoảng đẹm lề để căn chỉnh thành phần bên trong form

# Chuỗi Chứa nội dung được nhập
username = ''
password = ''
fr_username = ''
input_active = {'username': True, 'password': False, 'fr_username': False}

facerecognition_button_y =  form_y + 340
facerecognition_button_x = form_x + form_indent
facerecognition_button_width = form_width - form_indent*2
facerecognition_rect = pygame.Rect(facerecognition_button_x, facerecognition_button_y, facerecognition_button_width, 50)  # Register button

#Hàm để in ra chữ
def display_text(x, y, text, color, size):
    font_model = pygame.font.Font(None, size)
    text_surface = font_model.render(text, True, color)
    text_rect = text_surface.get_rect(topleft = (x,y))
    window.blit(text_surface, text_rect)

#Hàm xuất giao diện đăng nhập
def password_login_GUI():

    # Vẽ labels
    display_text(form_x + 50, form_y +36, 'Username:', BLACK, 36)
    display_text(form_x + 50, form_y + 126, 'Password:', BLACK, 36)

    # Tạo ô nhập chữ
    if input_active['username']:
        pygame.draw.rect(window, BLACK, (form_x + 48, form_y + 68, form_width - form_indent*2 + 4, 34))  # Username input box
    elif input_active['password']:
        pygame.draw.rect(window, BLACK, (form_x + 48, form_y + 158, form_width - form_indent*2 + 4, 34))  # Password input box
    pygame.draw.rect(window, GRAY, (form_x + 50, form_y + 70, form_width - form_indent*2, 30))  # Username input box
    pygame.draw.rect(window, GRAY, (form_x + 50, form_y + 160, form_width - form_indent*2, 30))  # Password input box

    # In ra chữ dc nhập
    if input_active['username']:
        display_text(form_x + 55, form_y + 73, username+'|', BLACK, 32)
    else:
        display_text(form_x + 55, form_y + 73, username, BLACK, 32)
    display_text(form_x + 55, form_y + 164, '*' * len(password) if password else password, BLACK, 32)
    display_text(form_x + 50, form_y + 210, "*Tips: Press tab to toggle between the input boxes", DARKGRAY, 28)
    
    # Kích thước và tọa độ nút
    button_gap = 20
    button_width = (form_width - form_indent*2 - button_gap)//2
    button_height = 50
    login_button_x = form_x + form_indent
    register_button_x = login_button_x + button_width + button_gap
    button_y = form_y + 270
    
    login_font = pygame.font.Font(None,32)
    # Vẽ nút Login
    login_rect = pygame.Rect(login_button_x, button_y, button_width, button_height)  # Login button
    pygame.draw.rect(window, BLACK, login_rect)  
    if login_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, DARKGRAY, login_rect)
    login_text_surface = login_font.render('Login', True, WHITE)
    window.blit(login_text_surface, (login_rect.x + button_width//2 - login_text_surface.get_width() // 2, login_rect.y + button_height//2 - login_text_surface.get_height() // 2))
    
    # Vẽ nút đăng ký
    border_register_rect = pygame.Rect(register_button_x, button_y, button_width, button_height)  # Register button
    register_rect = pygame.Rect(register_button_x+3, button_y+3, button_width-6, button_height-6)  # Register button
    pygame.draw.rect(window, BLACK, border_register_rect)
    pygame.draw.rect(window, WHITE, register_rect)  
    register_text_surface = login_font.render('Register', True, BLACK)
    register_text_hover = login_font.render('Register', True, WHITE)
    window.blit(register_text_surface, (register_rect.x + button_width//2 - register_text_surface.get_width() // 2, register_rect.y-2 + button_height//2 - login_text_surface.get_height() // 2))
    if border_register_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, DARKGRAY, border_register_rect)
        window.blit(register_text_hover, (register_rect.x + button_width//2 - register_text_surface.get_width() // 2, register_rect.y-2 + button_height//2 - login_text_surface.get_height() // 2))
    
    #Vẽ nút Nhận diện gương mặt
    global facerecognition_rect
    pygame.draw.rect(window, DARKBLUE, facerecognition_rect)  
    if facerecognition_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, DARKGRAY, facerecognition_rect)  
    facerecognition_text_surface = login_font.render('Login with Face recognition', True, WHITE)
    window.blit(facerecognition_text_surface, (facerecognition_rect.x + facerecognition_button_width//2 - facerecognition_text_surface.get_width() // 2, facerecognition_rect.y + button_height//2 - login_text_surface.get_height() // 2))

    return login_rect, register_rect

#Tao pop-up dang nhap
class login_pop_up():
    def __init__(self, text, color, x ,y):
        self.text = text
        self.color = color
        self.login_pop_font = pygame.font.Font(None, 34)
        self.text_surface = self.login_pop_font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(topleft = (x,y))

    def pop(self):
        window.blit(self.text_surface, self.text_rect)

# Chữ nổi lên khi đăng nhập bằng mật khẩu
pop_loginfail = login_pop_up("Login failed!", RED, 340, 520)
pop_loginsuccess = login_pop_up("Welcome " + username + "!, entering the game...", GREEN, 340, 520)
pop_regsuccess = login_pop_up("Account created!", GREEN, 340, 520)
pop_regexist = login_pop_up("Account already existed", ORANGE, 340, 520)
pop_empty = login_pop_up("Please fill in the input boxes!", NEONPURPLE, 340, 520)

# Chỉ hiện chữ khi biến của nó là True
pop_loginfail_display = pop_loginsuccess_display = pop_regexist_display = pop_regsuccess_display = pop_empty_display = fr_pop_empty_display = fr_pop_regsuccess_display = fr_pop_noface_display = fr_pop_regexist_display = fr_pop_loginfail_display = False

###################################################  facerecognition SYSTEM  ###############################################################

cam_capture = cv2.VideoCapture(0)  # 0 is the default camera index

#Thiết lập kích thước, vị trí các nút bấm cho giao diện nhận diện khuôn mặt
fr_button_gap = 20
return_button = pygame.image.load('./assets/icons/return2.png').convert_alpha()
return_button = pygame.transform.scale(return_button,(70,70))
return_button_rect = return_button.get_rect(topleft = (form_x + form_indent, form_y+form_indent))

# Thiết lập độ dài, tọa độ các nút
facerecognition_register_button_w = (form_width - form_indent*2) // 3
facerecognition_button_width = form_width - form_indent*2
facerecognition_button_height = 40
facerecognition_login_button_h = 50
fr_register_button_rect = pygame.Rect(form_x + form_indent, form_y + form_height - 160, facerecognition_register_button_w, facerecognition_button_height)
fr_login_button_rect = pygame.Rect(form_x + form_indent, form_y + form_height - 100, facerecognition_button_width, facerecognition_login_button_h)

# Khung hiển thị Camera
cam_width = (form_width - form_indent*6)
cam_height = (cam_width*9)//16
cam_x = form_x+ form_indent*3
cam_y = form_y+form_indent
cam_border = pygame.Rect(cam_x-2, cam_y-2 , cam_width+4, cam_height+4)  # Register button

# Hien thi chu trong face recognition
fr_pop_empty = login_pop_up("Enter username!", ORANGE, form_x + form_width - 330, fr_register_button_rect.y - 40)
fr_pop_regsuccess = login_pop_up("Account created!", GREEN, form_x + form_width - 330, fr_register_button_rect.y - 40)
fr_pop_noface = login_pop_up("No face detected!", RED, form_x + form_width - 330, fr_register_button_rect.y - 40)
fr_pop_regexist = login_pop_up("User already exist!", PURPLE, form_x + form_width - 330, fr_register_button_rect.y - 40)
fr_pop_loginfail = login_pop_up("User doesn't exist!", NEONGREEN, form_x + form_width - 330, fr_register_button_rect.y - 40)

# nút và hiển thị chữ của nhận diện km
def facerecognition_login_GUI():
    # Vẽ nút
    window.blit(return_button,return_button_rect)
    pygame.draw.rect(window, SDARKGRAY, fr_register_button_rect)
    pygame.draw.rect(window, SDARKGRAY, fr_login_button_rect)
    if fr_register_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, DARKGRAY, fr_register_button_rect)
    elif fr_login_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, DARKGRAY, fr_login_button_rect)

    # Hiện chữ cho nút
    fr_button_font = pygame.font.Font(None, 36)
    fr_register_text = fr_button_font.render('Register', True, WHITE)
    fr_login_text = fr_button_font.render('Login with Face recognition', True, WHITE)
    window.blit(fr_register_text, (fr_register_button_rect.x + facerecognition_register_button_w // 2 - fr_register_text.get_width() // 2, fr_register_button_rect.y + facerecognition_button_height // 2 - fr_register_text.get_height() //2))
    window.blit(fr_login_text, (fr_login_button_rect.x + facerecognition_button_width // 2 - fr_login_text.get_width() // 2, fr_login_button_rect.y + facerecognition_login_button_h // 2 - fr_login_text.get_height() // 2))
    display_text(form_x + 50, fr_register_button_rect.y - 40, "*Tips: Press tab to toggle input", DARKGRAY, 28)
    
    # Vẽ viền nếu đang không nhập chữ
    if input_active['fr_username']:
        pygame.draw.rect(window, BLACK, (form_x + form_indent + fr_button_gap + facerecognition_register_button_w - 2, fr_register_button_rect.y - 2, form_width - form_indent*2 -fr_button_gap - facerecognition_register_button_w + 4, facerecognition_button_height+4))  # Username input box
    pygame.draw.rect(window, GRAY, (form_x + form_indent + fr_button_gap + facerecognition_register_button_w, fr_register_button_rect.y, form_width - form_indent*2 -fr_button_gap - facerecognition_register_button_w, facerecognition_button_height))
    
    # Nếu chưa nhập gì thì hiện placeholder
    if isempty(fr_username):
        display_text(form_x + form_indent + fr_button_gap + facerecognition_register_button_w + 10, fr_register_button_rect.y + 10, 'Username', DARKGRAY, 32)
    elif input_active['fr_username']:
        display_text(form_x + form_indent + fr_button_gap + facerecognition_register_button_w + 10, fr_register_button_rect.y + 10, fr_username+'|', BLACK, 32)
    else:
        display_text(form_x + form_indent + fr_button_gap + facerecognition_register_button_w + 10, fr_register_button_rect.y + 10, fr_username, BLACK, 32)

###############################################   HIỂN THỊ ĐĂNG NHẬP BẰNG MẬT KHẨU###########################################################
start_time = 0
def display_password_state():
    global start_time, pop_loginfail_display, pop_regexist_display, pop_regsuccess_display, pop_empty_display, username, password, input_active, state_login_password, state_login_facerec
    
    # Vẽ giao diện password
    fr_login_button_rect, fr_register_button_rect = password_login_GUI()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos() # Lấy vị trí chuột
            if facerecognition_rect.collidepoint(mouse_pos) and not state_login_facerec: # Nếu nhấn nút này, chuyển sang giao diện đăng nhập khuôn mặt
                state_login_password = False
                state_login_facerec = True
                username = ''
                password = ''
            elif fr_login_button_rect.collidepoint(mouse_pos):
                if isempty(username) or isempty(password): # Chừa trống, cảnh báo
                    pop_empty_display = True
                    start_time = pygame.time.get_ticks()
                elif validate_login(username, password): # Nếu đúng mật khẩu, vào game
                    login_success()
                else:
                    pop_loginfail_display = True # Nếu sai thì thông báo
                    start_time = pygame.time.get_ticks()
            elif fr_register_button_rect.collidepoint(mouse_pos):
                if isempty(username) or isempty(password): # Chừa trống, cảnh báo
                    pop_empty_display = True
                    start_time = pygame.time.get_ticks()
                elif username in user_data: # Nếu tên ng chơi đã tồn tại, thông báo
                    pop_regexist_display = True
                    start_time = pygame.time.get_ticks()
                else: # Nếu không bị gì, đky
                    register_user(username,password)
                    username = ''
                    password = ''
                    pop_regsuccess_display = True
                    start_time = pygame.time.get_ticks()
        elif event.type == pygame.KEYDOWN: # Cập nhật chuỗi nhận kí tự để in ra màn hình
            if event.key == pygame.K_TAB:
                input_active['username'] = not input_active['username']
                input_active['password'] = not input_active['password']
            elif input_active['username']:
                if event.key == pygame.K_RETURN:
                    input_active['username'] = False
                    input_active['password'] = True
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            elif input_active['password']:
                if event.key == pygame.K_RETURN: # Sau khi đã nhập mật khẩu vào ô thứ 2, nhấn enter để vào game cũng dc
                    if validate_login(username, password):
                        login_success()
                elif event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    password += event.unicode
    
    # Chữ hiển thị trạng thái đăng nhập trong 1,5s
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    
    if elapsed_time < 1500:
        if pop_loginfail_display:
            pop_loginfail.pop()
        elif pop_regsuccess_display:
            pop_regsuccess.pop()
        elif pop_regexist_display:
            pop_regexist.pop()
        elif pop_empty_display:
            pop_empty.pop()
    else:
        pop_loginfail_display = pop_empty_display = pop_regexist_display = pop_regsuccess_display = False

###############################################   HIỂN THỊ ĐĂNG NHẬP BẰNG KHUÔN MẶT  ###########################################################

# Các biến để thực hiện chức năng trong giao diện khuôn mặt
process_facerecognition = False
fr_register_button_clicked = False
fr_login_button_clicked = False

def display_state_facerecognition():
    global start_time, process_facerecognition, fr_register_button_clicked, fr_login_button_clicked, input_active, fr_username, state_login_facerec, state_login_password, fr_pop_empty_display, fr_pop_noface_display, fr_pop_regsuccess_display, fr_pop_regexist_display, fr_pop_loginfail_display
    ret, frame = cam_capture.read()

    # Tạo khung để chiếu lên màn hình trực quan (Camera feed)
    frame = cv2.resize(frame, (cam_width,cam_height))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.image.frombuffer(frame.flatten(), (cam_width,cam_height), 'RGB')
    
    pygame.draw.rect(window, BLACK, cam_border) #Ve vien
    window.blit(frame_surface, (cam_x, cam_y))  # Display camera feed in the square
    facerecognition_login_GUI() #Chay ham ve nut

    #Cam nhan trang thai
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if return_button_rect.collidepoint(mouse_pos) and not state_login_password:  # Chuyển giao diện nếu ấn nút này
                state_login_password = True
                state_login_facerec = False
                fr_username = ''
            elif fr_register_button_rect.collidepoint(mouse_pos):
                fr_register_button_clicked = True
                process_facerecognition = True # Chỉ thực hiện gương mặt khi nhấn nút -> tối ưu cho hiệu suất, tránh gây nặng cpu, tương tự với nút đăng nhập
            elif fr_login_button_rect.collidepoint(mouse_pos):
                fr_login_button_clicked = True
                process_facerecognition = True
        elif event.type == pygame.KEYDOWN: # Cập nhật chuỗi username
            if event.key == pygame.K_TAB:
                input_active['fr_username'] = not input_active['fr_username']
            elif input_active['fr_username']:
                if event.key == pygame.K_BACKSPACE:
                    fr_username = fr_username[:-1]
                else:
                    fr_username += event.unicode
    
    if process_facerecognition:
        #face recognition logic
        big_frame = cv2.resize(frame, (720,720))
        big_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(big_frame)

        if len(face_locations) > 0: # Kiểm tra có detect dc khuôn mặt không
            face_encodings = face_recognition.face_encodings(big_frame, face_locations)
            for face_encoding in face_encodings:
                if fr_register_button_clicked:
                    face_encodings_from_db = []
                    with open(DATABASE) as file:
                        data = json.load(file)
                        for user_data in data.values():
                            face_encodings_from_db.append(np.array(user_data['face_encoding']))

                        # Check if the new face encoding matches any face encoding in the database
                    face_encoding_exists = False
                    for known_face_encoding in face_encodings_from_db:
                        if known_face_encoding.shape == (0,):  # Skip empty face encodings
                            continue
                        match = face_recognition.compare_faces([known_face_encoding], face_encoding)
                        if match[0]:
                            face_encoding_exists = True
                            break

                    if face_encoding_exists: # Nếu tồn tại rồi thì ko cho đăng kí
                        fr_pop_regexist_display = True
                        start_time = pygame.time.get_ticks()
                    elif isempty(fr_username): # Chừa trống, không cho đki
                        fr_pop_empty_display = True
                        start_time = pygame.time.get_ticks()
                    else: # Không có vấn đề gì thì đky
                        register_user_facerecognition(fr_username, face_encoding)
                        fr_pop_regsuccess_display = True
                        start_time = pygame.time.get_ticks()
                    fr_register_button_clicked = False
                elif fr_login_button_clicked:
                    face_encodings_from_db = []
                    with open(DATABASE) as file:
                        data = json.load(file)
                        for user_data in data.values():
                            face_encodings_from_db.append(np.array(user_data['face_encoding']))

                    # Check if the new face encoding matches any face encoding in the database
                    face_encoding_exists = False
                    for known_face_encoding in face_encodings_from_db:
                        if known_face_encoding.shape == (0,):  # Skip empty face encodings
                            continue
                        match = face_recognition.compare_faces([known_face_encoding], face_encoding)
                        if match[0]:
                            face_encoding_exists = True
                            break

                    if face_encoding_exists:
                        login_success()
                    else:
                        fr_pop_loginfail_display = True
                        start_time = pygame.time.get_ticks()
                    fr_login_button_clicked = False
        elif fr_register_button_clicked or fr_login_button_clicked:
            fr_pop_noface_display = True
            start_time = pygame.time.get_ticks()
            fr_register_button_clicked = False
            fr_login_button_clicked = False

    process_facerecognition = False # Dừng nhận diện sau khi chạy xong

    # Hiển thị chữ thông báo 1,5s
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    if elapsed_time < 1500:
        if fr_pop_empty_display:
            fr_pop_empty.pop()
        elif fr_pop_noface_display:
            fr_pop_noface.pop()
        elif fr_pop_regsuccess_display:
            fr_pop_regsuccess.pop()
        elif fr_pop_regexist_display:
            fr_pop_regexist.pop()
        elif fr_pop_loginfail_display:
            fr_pop_loginfail.pop()
    else:
        fr_pop_empty_display = fr_pop_noface_display = fr_pop_regsuccess_display = fr_pop_regexist_display = fr_pop_loginfail_display = False

# khối lệnh sẽ dc thực hiện khi đăng nhập thành công
def login_success():
    print("entering the game...")
    pygame.mixer.music.stop()
    

##################################################  CHAY GAME  #########################################################

# Chạy nhạc nền
login_music = ('./assets/musics/login_music.mp3')
pygame.mixer.music.load(login_music)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

# Trạng thái hiển thị
state_login_password = True
state_login_facerec = False

# Chạy game
while True:
    # Set FPS
    pygame.time.Clock().tick(60)
    # chay nen
    login_loop_background()
    # in nền form
    window.blit(form,(form_x,form_y))

    # Hien thi cac state dang nhap 
    if state_login_password:
        display_password_state()
    if state_login_facerec:
        display_state_facerecognition()
    
    # Cập nhật màn hình
    pygame.display.update()

# Thoát game hoàn toàn
cam_capture.release()
pygame.quit()
sys.exit()