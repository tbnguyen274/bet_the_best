import pygame
import login
import speed

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up display
# Kích thước cửa sổ
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    
if __name__ == "__main__":
    login.display_intro(pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)))
    speed.run_race()
    

