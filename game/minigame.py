import pygame
import sys
import random
from random import choice

# def run():
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
        self.rect = self.image.get_rect(midbottom=(240, 500))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('assets/sfx/jumpsound.mp3')
        self.jump_sound.set_volume(0.5)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 500:
            self.gravity = -23
            self.jump_sound.play()

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
            self.y_pos = 300
        else:
            snail_1 = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()
            snail_1 = pygame.transform.rotozoom(snail_1,0,1.6)
            snail_2 = pygame.transform.rotozoom(snail_2, 0, 1.6)
            self.frames = [snail_1, snail_2]
            self.y_pos = 500

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom= (1280, self.y_pos))

    def animation_state(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        if self.y_pos == 250:
            self.rect.x -= 15
        else : self.rect.x -= 11
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def generate_points():
    random_number_1 = random.randint(100, 500)
    random_number_2 = random.randint(100, 500)

    # Choose the minimum of the two numbers
    random_number = min(random_number_1, random_number_2)

    return random_number

def display_score():
    current_time = int(pygame.time.get_ticks() / 300) - start_time
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


class displayEvent():
    def displayScore():
        #Lose announcement:
        game_over = test_font.render('Game Over!', False, (111, 196, 169))
        game_over_rect = game_over.get_rect(center=(640, 80))
        screen.blit(game_over,game_over_rect)
        #Losing score
        score_message = test_font.render(f'Your score: {score}/100', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(midtop=(640, 520))
        screen.blit(score_message, score_message_rect)
        #Lose
        lose_instruction = test_font.render(f'Press Space to try again', False, (188, 122, 249))
        lose_instruction_rect = lose_instruction.get_rect(midtop=(640, score_message_rect.y + score_message.get_height() + 20))
        screen.blit(lose_instruction,lose_instruction_rect)
        
        

    def displayRule():
        #Rule
        game_rule = test_font.render("Reach 100 points to earn coins!" , False, (111, 196, 169))
        game_rule_rect = game_rule.get_rect(center=(640, 80))
        screen.blit(game_rule, game_rule_rect)
        #Instruction
        game_instruction = test_font.render('Press "SPACE" to jump', False, (111, 196, 169))
        game_instruction_rect = game_instruction.get_rect(midtop=(640, 530))
        screen.blit(game_instruction,game_instruction_rect)
        #Key
        game_instruction2 = test_font.render('Press "SPACE" to start, "ESC" twice to exit', False, (188, 122, 249))
        game_instruction2_rect = game_instruction2.get_rect(midtop=(640, game_instruction_rect.y + game_instruction.get_height() + 20))
        screen.blit(game_instruction2,game_instruction2_rect)

        
        
        

    def displayGameBeat():
        #Win
        game_beat = test_font.render('You won!', False, (111, 196, 169))
        game_beat_rect = game_beat.get_rect(center=(640, 80))   
        screen.blit(game_beat,game_beat_rect)
        #Loading
        game_passed = test_font.render ('Returning to "Bet the best" in 4 seconds...', False, (188, 122, 249))
        game_passed_rect = game_passed.get_rect(midtop = (640,530))
        screen.blit(game_passed, game_passed_rect)

    def displayBackground():
        #Sky
        sky_surface = pygame.image.load('assets/graphics/background3.jpg').convert()
        screen.blit(sky_surface, (0, -150)) 
        #Ground
        ground_surface = pygame.image.load('assets/graphics/ground1.png').convert()
        screen.blit(ground_surface, (0, 500))



pygame.init()

icon = pygame.image.load('./assets/icons/game-icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Bet the best')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
test_font = pygame.font.Font('assets/font/Pixeltype.ttf', 80)
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



# Starting and ending screen
player_stand = pygame.image.load('assets/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 4)
player_stand_rect = player_stand.get_rect(midbottom=(640,500 ))



# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 800)

#Music
pygame.mixer.music.load('assets/musics/Minigame.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

fail_sound = pygame.mixer.Sound('assets/sfx/minigamefail.mp3')
fail_sound.set_volume(0.5)
fail_sound_play = win_sound_play = False
win_sound = pygame.mixer.Sound('assets/sfx/minigamewin.mp3')
win_sound.set_volume(0.4)

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
                    # return 0
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 300)
                elif event.key == pygame.K_ESCAPE:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_esc_time < 1000:  # Check if ESC was pressed within 1 second
                        consecutive_esc_presses += 1
                    else:
                        consecutive_esc_presses = 1
                    
                    last_esc_time = current_time
                    
                    if consecutive_esc_presses >= 2:
                        pygame.mixer.music.stop()
                        # return 0

    if game_active:
        pygame.mixer.music.set_volume(0.3)
        displayEvent.displayBackground()
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
        fail_sound_play = False
        if score == 100:
            game_active = False
    else:
        screen.fill((48, 129, 208))
        # else: pass
        screen.blit(player_stand, player_stand_rect)

        if score == 0:
            displayEvent.displayRule()
        elif score == 100:
            start_time = pygame.time.get_ticks()
            pygame.mixer.music.stop()
            if not win_sound_play:
                win_sound.play()
                win_sound_play = True
            while pygame.time.get_ticks() - start_time < 4000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                displayEvent.displayGameBeat()

                pygame.display.update()

            # return generate_points()
        else:
            displayEvent. displayScore()
            pygame.mixer.music.set_volume(0)
            if not fail_sound_play:
                fail_sound.play()
                fail_sound_play = True

    pygame.display.update()
    clock.tick(60)
