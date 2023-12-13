from PIL import Image
import pytesseract
import os

# Đường dẫn đến thư mục chứa tesseract.exe (điều này cần thiết nếu không thêm vào biến môi trường PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def convert_image_to_text(image_path, output_file='output.txt'):
    image = Image.open(image_path)

    # Sử dụng pytesseract để nhận diện ký tự
    text = pytesseract.image_to_string(image)

    # Ghi nội dung text vào file
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(text + "\n\n")  # Thêm dòng trống giữa các nội dung từ ảnh để phân biệt

    print(f"Nội dung ảnh {image_path} đã được thêm vào file '{output_file}'.")

if __name__ == "__main__":
    # Thay đổi đường dẫn đến ảnh của bạn và tên file output nếu cần thiết
    image_paths = [
        "../assets/BG-pic/leaderboard.png",
        "../assets/screenshots/screenshot_181004_03122023.png"
    ]
    output_file = "output.txt"

    for image_path in image_paths:
        convert_image_to_text(image_path, output_file)
