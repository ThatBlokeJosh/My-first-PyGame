import pygame
from sys import exit
import os
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Variables:
WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.display.set_caption("First Game")
background = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'hell.png')), (WIDTH, HEIGHT)).convert_alpha()
surface_image = pygame.image.load(os.path.join('Assets', 'funny.png')).convert_alpha()
surface = pygame.transform.rotate(pygame.transform.scale(surface_image, (70, 50)), 90)
surface_rect = surface.get_rect(center=(500, 250))
surface_screen = pygame.transform.rotate(pygame.transform.scale(surface_image, (150, 100)), 90)
surface_screen_rect = surface_screen.get_rect(center=(-100, 100))

projectile_image = pygame.transform.scale(pygame.image.load(
        os.path.join('Assets', 'projectile.png')), (50, 35)).convert_alpha()
music = pygame.mixer.Sound(os.path.join('Assets', 'music.mp3'))
fire_sound = pygame.mixer.Sound(os.path.join('Assets', 'firing.mp3'))
hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))
one_up = pygame.mixer.Sound(os.path.join('Assets', '1up.mp3'))
game_over_sound = pygame.mixer.Sound(os.path.join('Assets', 'gameover.mp3'))
animation_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'animation.png')), (70, 50)).convert_alpha(), 270)

hit = pygame.USEREVENT + 1
hit2 = pygame.USEREVENT + 2
boss_hit = pygame.USEREVENT + 3
font = pygame.font.SysFont('arialnova', 40)
screen_font = pygame.font.SysFont('arialnova', 100)
pause_font = pygame.font.SysFont('arialnova', 80)
VEL = 5


def draw(
        animation, animation_amount, animation2, animation_amount2, max_projectiles, kills,
        lives):
    enemy_vel = 3
    if lives >= 10:
        enemy_vel = 4

    if lives >= 20:
        enemy_vel = 5

    if lives >= 30:
        enemy_vel = 6

    if lives >= 40:
        enemy_vel = 7

    if lives >= 50:
        enemy_vel = 8

    if lives >= 60:
        enemy_vel = 9

    if lives >= 70:
        enemy_vel = 10

    if lives >= 80:
        enemy_vel = 11

    if lives >= 90:
        enemy_vel = 12

    if lives >= 100:
        enemy_vel = 13

    for animation in animation_amount:
        WIN.blit(animation_image, animation)
    animation.x -= enemy_vel
    for animation2 in animation_amount2:
        WIN.blit(animation_image, animation2)
    animation2.x -= enemy_vel

    projectile_text = font.render('Bullets: ' + str(max_projectiles), True, WHITE)
    WIN.blit(projectile_text, (10, 10))
    kills_text = font.render('Kills: ' + str(kills), True, WHITE)
    WIN.blit(kills_text, (890, 10))
    lives_text = font.render('Level: ' + str(lives), True, WHITE)
    WIN.blit(lives_text, (410, 10))
    pygame.display.update()


def draw_text(screen_text, kills_text):
    screen_text_render = screen_font.render(screen_text, True, WHITE)
    kills_text_render = font.render(kills_text, True, WHITE)
    WIN.blit(
        screen_text_render, (
            WIDTH//2 - screen_text_render.get_width()//2, HEIGHT//2 - screen_text_render.get_height()//2))
    WIN.blit(kills_text_render, (50, 450))
    pygame.display.update()


def main():
    run = True
    projectile_amount = []
    animation_amount = []
    animation_amount2 = []
    animation = animation_image.get_rect(center=(900, 400))
    animation_amount.append(animation)
    animation2 = animation_image.get_rect(center=(900, 100))
    animation_amount2.append(animation2)
    max_projectiles = 5
    clock = pygame.time.Clock()
    kills = 0
    total_kills = 0
    lives = 3
    music.play(1000000)
    damage = 1
    projectile_regen = 1
    if max_projectiles > 5:
        max_projectiles -= 1
    game_active = False
    game_paused = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(total_kills)
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and max_projectiles > 0:
                fire_sound.play()
                projectile = pygame.Rect(
                    surface_rect.x + surface_rect.width, surface_rect.y + surface_rect.height//2 - 17, 50, 35)
                projectile_amount.append(projectile)
                max_projectiles -= projectile_regen

            if event.type == hit:
                hit_sound.play()
                animation_amount.remove(animation)
                animation.x = 1000
                animation_amount.append(animation)
                max_projectiles += projectile_regen
                kills += 1
                total_kills += 1

            if event.type == hit2:
                hit_sound.play()
                animation_amount2.remove(animation2)
                animation2.x = 1000
                animation_amount2.append(animation2)
                max_projectiles += projectile_regen
                kills += 1
                total_kills += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active is not True:
                    game_active = True
                    animation.x = 900
                    animation2.x = 900
                    surface_rect.x = 500
                    surface_rect.y = 250
                    lives = 3
                    total_kills = 0
                    kills = 0
                    max_projectiles = 5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if game_active:
                        game_active = False
                        game_paused = True
                    else:
                        game_active = True
                        game_paused = False

        if game_active:
            WIN.blit(background, (0, 0))

            for projectile in projectile_amount:
                WIN.blit(projectile_image, projectile)
                if animation.colliderect(projectile):
                    pygame.event.post(pygame.event.Event(hit))
                    projectile_amount.remove(projectile)
                if animation2.colliderect(projectile):
                    pygame.event.post(pygame.event.Event(hit2))
                    projectile_amount.remove(projectile)
                if projectile.x > WIDTH:
                    try:
                        projectile_amount.remove(projectile)
                        max_projectiles += projectile_regen
                    except ValueError:
                        projectile_amount.append(projectile)
                        max_projectiles -= 1

            for projectile in projectile_amount:
                projectile.x += 5

            if animation.x < 0:
                animation.x += 900
                lives -= damage

            if animation2.x < 0:
                animation2.x += 900
                lives -= damage
            if lives >= 10:
                damage = 1
            if lives >= 20:
                damage = 2
            if lives >= 30:
                damage = 2
            if lives >= 40:
                damage = 3
            if lives >= 50:
                damage = 3
            if lives >= 60:
                damage = 4
            if lives >= 70:
                damage = 4
            if lives >= 80:
                damage = 5
            if lives >= 90:
                damage = 5
            if lives >= 100:
                damage = 6

            WIN.blit(surface, surface_rect)

            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_a] and surface_rect.x - VEL > 0:
                surface_rect.x -= VEL
            if keys_pressed[pygame.K_d] and surface_rect.x + VEL + surface_rect.width < WIDTH:
                surface_rect.x += VEL
            if keys_pressed[pygame.K_w] and surface_rect.y - VEL > 0:
                surface_rect.y -= VEL
            if keys_pressed[pygame.K_s] and surface_rect.y + VEL + surface_rect.height < HEIGHT - 15:
                surface_rect.y += VEL

            if kills >= 10:
                one_up.play()
                lives += 1
                kills -= 10
            if lives <= 0:
                game_active = False
            draw(
                animation, animation_amount, animation2, animation_amount2, max_projectiles, kills,
                lives)

        else:
            if game_paused:
                WIN.blit(background, (0, 0))
                pause_text = 'Paused'
                pause_text_render = pause_font.render(pause_text, True, WHITE)
                WIN.blit(pause_text_render, (
                    WIDTH // 2 - pause_text_render.get_width() // 2,
                    HEIGHT // 2 - pause_text_render.get_height() // 2))
            if game_paused is not True:
                WIN.blit(background, (0, 0))
                WIN.blit(surface_screen, surface_screen_rect)
                surface_screen_rect.x += 7
                if surface_screen_rect.x > 1000:
                    surface_screen_rect.x = -100
                screen_text = 'PRESS SPACE TO START'
                draw_text(screen_text, kills_text='Kills last game: ' + str(total_kills))

        pygame.display.update()
        clock.tick(60)

    main()


if __name__ == '__main__':
    main()
