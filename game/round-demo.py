import pygame

# Initialize Pygame
pygame.init()

# Set window dimensions
window_width = 1280
window_height = 720

# Create the Pygame window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Horizontal Image Loop')  # Set the window title

Length = 1
race_scale = 1
if Length == 1:
    race_scale = 1
elif Length == 2:
    race_scale = 0.7
else:
    race_scale = 0.5

# Load the image to be looped
background = pygame.image.load('./assets/BG-pic/galaxy.jpg')
image = pygame.image.load('./assets/race/race-mid.png')
image.set_alpha(200)
image_width = image.get_width()
image_height = image.get_height()
image = pygame.transform.scale(image,(int(race_scale*image_width),int(race_scale*image_height)))
image_width = image.get_width()
image_height = image.get_height()
race_start = pygame.image.load('./assets/race/race-start.png')
race_start.set_alpha(200)
race_s_w = race_start.get_width()
race_s_h = race_start.get_height()
race_start = pygame.transform.scale(race_start,(int(race_scale*race_s_w),int(race_scale*race_s_h)))
race_s_w = race_start.get_width()
race_s_h = race_start.get_height()
race_end = pygame.image.load('./assets/race/race-end.png')
race_end.set_alpha(200)
race_e_w = race_end.get_width()
race_e_h = race_end.get_height()
race_end = pygame.transform.scale(race_end,(int(race_scale*race_e_w),int(race_scale*race_e_h)))
race_e_w = race_end.get_width()
race_e_h = race_end.get_height()
end_width = race_end.get_width()




# Calculate the number of repetitions needed to fill the window horizontally
num_repetitions = window_width // image_width + 1  # Add 1 to ensure the whole window is filled

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the tiled image horizontally
    window.blit(background,(0,0))
    for i in range(num_repetitions):
        window.blit(image, (race_s_w + i * image_width, 100))  # Render the image at each multiple of image width
    window.blit(race_start, (0, 100))
    window.blit(race_end, (window_width - end_width, 100))
    pygame.display.flip()  # Update the display

# Quit Pygame properly
pygame.quit()
