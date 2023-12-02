import pygame, sys

def display_intro(screen):
    intro_image = pygame.image.load('./assets/icons/brand.png').convert_alpha()  # Replace 'studio_logo.png' with your image filename
    intro_rect = intro_image.get_rect()
    intro_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    clock = pygame.time.Clock()