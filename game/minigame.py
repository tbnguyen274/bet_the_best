import pygame
import sys
from random import randint, choice

def run():
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            walk1 = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
            walk2 = pygame.image.load('assets/graphics/Player/player_walk_2.png').convert_alpha()
            player_walk_1 = pygame.transform.rotozoom(walk1,0,1.6)
            player_walk_2 = pygame.transform.rotozoom(walk2, 0 ,1.6)
            self.player_walk = [player_walk_1, player_walk_2]
            self.player_index = 0
            player_jump = pygame.image.load('assets/graphics/Player/jump.png').convert_alpha()
            self.player_jump = pygame.transform.rotozoom(player_jump,0,1.6)
            self.image = self.player_walk[self.player_index]
            self.rect = self.image.get_rect(midbottom=(120, 500))
            self.gravity = 0
            self.jump_sound = pygame.mixer.Sound('assets/sfx/jumpsound.mp3')
            self.jump_sound.set_volume(0.5)


        def player_input(self):
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 500:
                self.gravity = -20
                self.jump_sound.play()
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right <= 1280:
                self.rect.x += 5
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left >= 0:
                self.rect.x -= 5
        def apply_gravity(self):
            self.gravity += 1
            self.rect.y += self.gravity
            if self.rect.bottom >= 500:
                self.rect.bottom = 500

        def animation_state(self):
            if self.rect.bottom < 500:
                self.image = self.player_jump
            else:
                self.player_index += 0.1
                if self.player_index >= len(self.player_walk): self.player_index = 0
                self.image = self.player_walk[int(self.player_index)]

        def update(self):
            self.player_input()
            self.apply_gravity()
            self.animation_state()


    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, type):
            super().__init__()

            if type == 'fly':
                fly_1 = pygame.image.load('assets/graphics/Fly/Fly1.png').convert_alpha()
                fly_2 = pygame.image.load('assets/graphics/Fly/Fly2.png').convert_alpha()
                fly_1 = pygame.transform.rotozoom(fly_1,0,1.6)
                fly_2 = pygame.transform.rotozoom(fly_2, 0, 1.6)
                self.frames = [fly_1, fly_2]
                y_pos = 250
            else:
                snail_1 = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
                snail_2 = pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()
                snail_1 = pygame.transform.rotozoom(snail_1,0,1.6)
                snail_2 = pygame.transform.rotozoom(snail_2, 0, 1.6)
                self.frames = [snail_1, snail_2]
                y_pos = 500

            self.animation_index = 0
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(midbottom=(randint(1350, 1400), y_pos))

        def animation_state(self):
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

        def update(self):
            self.animation_state()
            self.rect.x -= 6
            self.destroy()

        def destroy(self):
            if self.rect.x <= -100:
                self.kill()


    def display_score():
        current_time = int(pygame.time.get_ticks() / 150) - start_time
        score_surf = test_font.render(f'Score: {current_time}', False, (179, 19, 18))
        score_rect = score_surf.get_rect(center=(640, 50))
        screen.blit(score_surf, score_rect)
        return current_time


    def collision_sprite():
        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
            obstacle_group.empty()
            return False
        else:
            return True


    pygame.init()
    
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    test_font = pygame.font.Font('assets/font/Pixeltype.ttf', 100)
    game_active = False
    start_time = 0
    score = 0
    consecutive_esc_presses = 0
    isRunning = True
    last_esc_time = 0


    # Groups
    player = pygame.sprite.GroupSingle()
    player.add(Player())

    obstacle_group = pygame.sprite.Group()

    sky_surface = pygame.image.load('assets/graphics/background3.jpg').convert()
    ground_surface = pygame.image.load('assets/graphics/ground1.png').convert()

    # Màn hình giới thiệu và kết thúc
    player_stand = pygame.image.load('assets/graphics/Player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 4)
    player_stand_rect = player_stand.get_rect(midbottom=(640,500 ))

    game_name = test_font.render("Reach 100 points to earn coins!" , False, (111, 196, 169))
    game_name_rect = game_name.get_rect(center=(640, 80))

    game_over = test_font.render('Game Over!', False, (111, 196, 169))
    game_over_rect = game_over.get_rect(center=(640, 80))
    
    game_beat = test_font.render('You won!', False, (111, 196, 169))
    game_beat_rect = game_beat.get_rect(center=(640, 80))

    game_message = test_font.render('Press arrow keys to move', False, (111, 196, 169))
    game_message_rect = game_message.get_rect(midtop=(640, 530))

    game_message2 = test_font.render('Press space to start, Esc twice to exit', False, (188, 122, 249))
    game_message2_rect = game_message2.get_rect(midtop=(640, game_message_rect.y + game_message.get_height() + 20))

    game_pass = test_font.render ("Returning to 'Bet the best' in 4 seconds...", False, (188, 122, 249))
    game_pass_rect = game_pass.get_rect(midtop = (640,530))
    # Timer
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)

    #Choi nhac
    pygame.mixer.music.load('assets/musics/Minigame.mp3')
    pygame.mixer.music.play(loops=-1)

    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:
                if event.type == obstacle_timer:
                    obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_esc_time < 1000:  # Check if ESC was pressed within 1 second
                        consecutive_esc_presses += 1
                    else:
                        consecutive_esc_presses = 1
                    
                    last_esc_time = current_time
                    
                    if consecutive_esc_presses >= 2:
                        pygame.mixer.music.stop()
                        return 0
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        start_time = int(pygame.time.get_ticks() / 150)
                    elif event.key == pygame.K_ESCAPE:
                        current_time = pygame.time.get_ticks()
                        if current_time - last_esc_time < 1000:  # Check if ESC was pressed within 1 second
                            consecutive_esc_presses += 1
                        else:
                            consecutive_esc_presses = 1
                        
                        last_esc_time = current_time
                        
                        if consecutive_esc_presses >= 2:
                            pygame.mixer.music.stop()
                            return 0

        if game_active:
            screen.blit(sky_surface, (0, -150))
            screen.blit(ground_surface, (0, 500))
            score = display_score()

            player.draw(screen)
            player.update()

            obstacle_group.draw(screen)
            obstacle_group.update()

            game_active = collision_sprite()
            if score == 100:
                game_active = False
        else:
            screen.fill((48, 129, 208))
            # else: pass
            screen.blit(player_stand, player_stand_rect)

            score_message = test_font.render(f'Your score: {score}/100', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(midtop=(640, 520))

            score_message2 = test_font.render(f'Press Space to try again', False, (188, 122, 249))
            score_message2_rect = score_message2.get_rect(midtop=(640, score_message_rect.y + score_message.get_height() + 20))

            if score == 0:
                screen.blit(game_name, game_name_rect)
                screen.blit(game_message, game_message_rect)
                screen.blit(game_message2,game_message2_rect)
            elif score == 100:
                start_time = pygame.time.get_ticks()
                pygame.mixer.music.stop()
                while pygame.time.get_ticks() - start_time < 4000:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    screen.blit(game_beat,game_beat_rect)
                    screen.blit(game_pass, game_pass_rect)

                    pygame.display.update()

                return 100
            else:
                screen.blit(score_message2,score_message2_rect)
                screen.blit(score_message, score_message_rect)
                screen.blit(game_over,game_over_rect)

        pygame.display.update()
        clock.tick(60)
