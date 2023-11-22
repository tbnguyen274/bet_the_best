import pygame, sys

def display_intro(screen):
    intro_image = pygame.image.load('./assets/icons/brand.png').convert_alpha()  # Replace 'studio_logo.png' with your image filename
    intro_rect = intro_image.get_rect()
    intro_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    clock = pygame.time.Clock()
    intro_duration = 4000  # Intro duration in milliseconds (3 seconds)
    fade_duration = 1000  # Fade duration in milliseconds (1 second)
    fade_in_start = 0
    fade_out_start = intro_duration - fade_duration
    elapsed_time = 0
    running = True

    while running:
        screen.fill((0, 0, 0))  # Fill the screen with black (you can change the color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        elapsed_time += clock.tick(60)  # Limit frame rate to 60 FPS

        if elapsed_time < fade_in_start:
            # Before fade-in starts, keep the image transparent
            intro_image.set_alpha(0)
        elif elapsed_time < fade_out_start:
            # Fade-in effect
            alpha = min(255, (elapsed_time - fade_in_start) * 255 // fade_duration)
            intro_image.set_alpha(alpha)
        else:
            # Fade-out effect
            alpha = max(0, 255 - ((elapsed_time - fade_out_start) * 255 // fade_duration))
            intro_image.set_alpha(alpha)

        screen.blit(intro_image, intro_rect)

        if elapsed_time > intro_duration:
            running = False

        pygame.display.flip()