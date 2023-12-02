import pygame
from sys import exit

pygame.init()

# Hàm xử lý sự kiện nhập liệu
def handle_input():
    global input_text, input_active, target_money, error_message, current_money, show_notification, play_minigame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_active:
                    try:
                        # Chuyển đổi giá trị nhập từ chuỗi sang số nguyên
                        target_money = int(input_text)

                        if 50 <= target_money <= current_money:
                            # Lưu lịch sử giao dịch
                            save_transaction(current_money, target_money)

                            # Kết thúc quá trình nhập
                            input_active = False
                            show_notification = True  # Đặt là True để hiển thị thông báo
                            error_message = ""

                            # Lưu giá trị vào tệp hoặc thực hiện các thao tác cần thiết
                            with open('target_money.txt', 'w') as file:
                                file.write(str(target_money))

                            print(f"Value saved: {target_money}")

                            # Chuyển sang bước tiếp theo (đặt code thắng hay thua cược ở đây)
                            print("Next step...")
                        else:
                            error_message = "Error: Please enter again."
                            # Thiết lập lại trạng thái nhập để người chơi có thể nhập lại
                            input_text = ""
                    except ValueError:
                        error_message = "Error: Please enter an integer."
                        # Thiết lập lại trạng thái nhập để người chơi có thể nhập lại
                        input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_notification and notification_rect.collidepoint(event.pos):
                # Kiểm tra nếu người chơi nhấp vào hộp thông báo, tắt hộp thông báo
                show_notification = False

def save_transaction(previous_money, new_money):
    # Ghi vào lịch sử giao dịch
    with open('money_history.txt', 'a') as file:
        file.write(f"Transaction: ${previous_money} -> ${new_money}\n")

# Khởi tạo cửa sổ Pygame
screen = pygame.display.set_mode((760, 406))
pygame.display.set_caption("Notification")
clock = pygame.time.Clock()
test_surface = pygame.image.load('../assets/BG-pic/nền.png').convert()

font = pygame.font.Font('../assets/font/game.ttf', 28)  # Chọn font và kích thước

current_money = 100  # Số tiền hiện có
target_money = 0  # Số tiền mục tiêu ban đầu
input_text = ""  # Biến lưu trữ giá trị nhập từ bàn phím
error_message = ""  # Biến lưu trữ thông báo lỗi
show_notification = False  # Biến kiểm soát việc hiển thị thông báo
play_minigame = False  # Biến chỉ định liệu có chơi mini-game hay không

input_active = True  # Biến kiểm soát việc nhập dữ liệu
input_rect = pygame.Rect(550, 200, 100, 40)  # Khu vực nhập dữ liệu

# Tạo hộp thông báo với ảnh nền
notification_rect = pygame.Rect(200, 10, 400, 200)  # Hộp thông báo
notification_image = pygame.image.load('../assets/BG-pic/space.jpg').convert()

while True:
    handle_input()

    screen.blit(test_surface, (10, 10))

    # Hiển thị thông báo với số tiền hiện có
    text = font.render(f"You currently have ${current_money}", True, (255, 255, 255))
    screen.blit(text, (100, 150))

    # Hiển thị hướng dẫn nhập số tiền mục tiêu
    instruction_text = font.render("Enter the target amount of money :", True, (255, 255, 255))
    screen.blit(instruction_text, (100, 200))

    # Hiển thị khu vực nhập dữ liệu
    pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)

    # Giới hạn độ dài của văn bản và cập nhật vị trí hiển thị
    input_surface = font.render(input_text, True, (255, 255, 255))
    screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

    # Hiển thị thông báo lỗi
    if error_message:
        error_text = font.render(error_message, True, (255, 0, 0))
        screen.blit(error_text, (100, 250))

    # Hiển thị hộp thông báo với ảnh nền
    if show_notification:
        screen.blit(notification_image, notification_rect)
        # Hiển thị số tiền hiện có trong hộp thông báo
        notification_text = font.render(f"Current Money: ${current_money}", True, (255, 255, 255))
        screen.blit(notification_text, (notification_rect.x + 10, notification_rect.y + 10))

        # Kiểm tra nếu số tiền còn lại dưới 50 để kích hoạt mini-game
        if current_money < 50 and not play_minigame:
            play_minigame = True
            print("Play Mini-Game!")

    pygame.display.update()
    clock.tick(60)
