import pygame
from sys import exit

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Jump man')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
icon = pygame.image.load('graphics/icon.png')
pygame.display.set_icon(icon)
game_active = False  # Set the game to start in an inactive state
game_start = True  # Added variable to control the start screen

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render('Jump Man', False, (64, 64, 64)).convert()
score_rect = score_surf.get_rect(center=(400, 50))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright=(600, 300))

player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

jump_sound = pygame.mixer.Sound('audio/jump.mp3')
die = pygame.mixer.Sound('audio/die.mp3')

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Jump Man', False, (64, 64, 64))
game_name_rect = game_name.get_rect(center=(400, 130))

press_space = test_font.render('Press space to start', False, (64, 64, 64))
press_space_rect = press_space.get_rect(center=(400, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_start:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_start = False  # Start the game when space is pressed
                game_active = True

        if game_active:
            if event.type == pygame.MOUSEMOTION:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()


        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        pygame.draw.rect(screen, '#d67a7a', score_rect, 6)
        pygame.draw.rect(screen, '#d67a7a', score_rect)
        screen.blit(score_surf, score_rect)
        snail_rect.x -= 4

        if snail_rect.right <= -0:
            snail_rect.left = 800

        screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # Collision
        if snail_rect.colliderect(player_rect):
            jump_sound.play()
            die.play()
            game_active = False
    else:
        screen.fill('#d67a7a')
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(press_space, press_space_rect)

    pygame.display.update()
    clock.tick(60)  # 60 frames per second
