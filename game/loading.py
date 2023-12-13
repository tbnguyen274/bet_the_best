import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loading Screen")

# Function to draw loading screen
def draw_loading_screen(progress):
    screen.fill(BLACK)
    bar_width = 1000  # Adjusted bar width
    bar_height = 50
    bar_x = (WIDTH - bar_width) // 2
    bar_y = (HEIGHT - bar_height) // 2 + 30

    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)  # Outline of the bar
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, progress * (bar_width // 100), bar_height))  # Progress bar
    font = pygame.font.Font(None, 60)
    text = font.render("Loading...", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(text, text_rect)
    pygame.display.update()

# Simulation of loading process
def run(speed):
    progress = 0
    while progress <= 100:
        pygame.time.delay(20)  # Adjusted loading time delay for faster progress
        progress += speed  # Increased increment for faster progress
        draw_loading_screen(min(progress,100))
  # When loading is completed, switch to the main menu or the game

# Function to display main menu (placeholder)
# Main function

if __name__ == "__main__":
    run(1)
