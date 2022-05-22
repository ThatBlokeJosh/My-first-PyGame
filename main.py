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

projectile_image = pygame.transform.scale(pygame.image.load(
        os.path.join('Assets', 'projectile.png')), (35, 22)).convert_alpha()
music = pygame.mixer.Sound(os.path.join('Assets', 'music.mp3'))
animation_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'animation.png')), (70, 50)).convert_alpha(), 270)

hit = pygame.USEREVENT + 1
hit2 = pygame.USEREVENT + 2
font = pygame.font.SysFont('arialnova', 40)
game_over_font = pygame.font.SysFont('arialnova', 80)
pause_font = pygame.font.SysFont('arialnova', 80)
VEL = 5


def draw(animation, animation_amount, animation2, animation_amount2, max_projectiles, kills, lives):
    enemy_vel = 4
    if lives >= 10:
        enemy_vel += 2
    elif lives >= 25:
        enemy_vel += 2
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


def game_over(game_over_text):
    game_over_text_render = game_over_font.render(game_over_text, True, WHITE)
    WIN.blit(game_over_text_render, (
        WIDTH//2 - game_over_text_render.get_width()//2, HEIGHT//2 - game_over_text_render.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


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
    if max_projectiles > 5:
        max_projectiles -= 1

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and max_projectiles > 0:
                projectile = pygame.Rect(
                    surface_rect.x + surface_rect.width, surface_rect.y + surface_rect.height//2 - 2, 10, 5)
                projectile_amount.append(projectile)
                max_projectiles -= 1

            if event.type == hit:
                animation_amount.remove(animation)
                animation.x = 1000
                animation_amount.append(animation)
                max_projectiles += 1
                kills += 1
                total_kills += 1

            if event.type == hit2:
                animation_amount2.remove(animation2)
                animation2.x = 1000
                animation_amount2.append(animation2)
                max_projectiles += 1
                kills += 1
                total_kills += 1

        if animation.x < 0:
            animation.x += 900
            lives -= 1

        if animation2.x < 0:
            animation2.x += 900
            lives -= 1

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
                    max_projectiles += 1
                except ValueError:
                    projectile_amount.append(projectile)
                    max_projectiles -= 1

        for projectile in projectile_amount:
            projectile.x += 5

        WIN.blit(surface, surface_rect)
        pause_text = 'PAUSED'
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_a] and surface_rect.x - VEL > 0:
            surface_rect.x -= VEL
        if keys_pressed[pygame.K_d] and surface_rect.x + VEL + surface_rect.width < WIDTH:
            surface_rect.x += VEL
        if keys_pressed[pygame.K_w] and surface_rect.y - VEL > 0:
            surface_rect.y -= VEL
        if keys_pressed[pygame.K_s] and surface_rect.y + VEL + surface_rect.height < HEIGHT - 15:
            surface_rect.y += VEL
        if keys_pressed[pygame.K_SPACE]:
            pause_text_render = pause_font.render(pause_text, True, WHITE)
            WIN.blit(pause_text_render, (
                WIDTH // 2 - pause_text_render.get_width() // 2,
                HEIGHT // 2 - pause_text_render.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)


        if kills >= 10:
            lives += 1
            kills -= 10
        game_over_text = 'GAME OVER' \
                         ' YOU GOT ' + str(total_kills) + ' kills.'
        if lives <= 0:
            game_over(game_over_text)
            break
        clock.tick(60)
        draw(animation, animation_amount, animation2, animation_amount2, max_projectiles, kills, lives)


main()


if __name__ == '__main__':
    main()
