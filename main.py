import sys

import pygame
import random

from controls import move_player
from classes.constants import WIDTH, HEIGHT, FPS, SHOOT_DELAY
from functions import show_game_over, win
from menu import show_menu

from classes.player import Player
from classes.bullets import Bullet
from classes.refill import ExtraScore
from classes.explosions import Explosion
from classes.enemies import Enemy1, Meteors2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("SVO")
clock = pygame.time.Clock()
score_logs = open('score_logs.txt', 'w')

explosions = pygame.sprite.Group()
explosions2 = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy1_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
meteor2_group = pygame.sprite.Group()
extra_score_group = pygame.sprite.Group()

bg_y_shift = -HEIGHT
background_img = pygame.image.load('images/bg/background.jpg').convert()
background_img2 = pygame.image.load('images/bg/background2.png').convert()
background_img3 = pygame.image.load('images/bg/background3.png').convert()
background_top = background_img.copy()
current_image = background_img
new_background_activated = False

explosion_images = [pygame.image.load(f"images/explosion/explosion{i}.png") for i in range(8)]

enemy1_img = [
    pygame.image.load('images/enemy/enemy1_1.png').convert_alpha(),
    pygame.image.load('images/enemy/enemy1_3.png').convert_alpha()
]

meteor2_imgs = [
    pygame.image.load('images/camni/meteor2_1.png').convert_alpha(),
    pygame.image.load('images/camni/meteor2_2.png').convert_alpha()
]
extra_score_img = pygame.image.load('images/score/score_coin.png').convert_alpha()

initial_player_pos = (WIDTH // 2, HEIGHT - 100)

score = 0
hi_score = 0
player = Player()
player_life = 200
running = True

if show_menu:
    import menu

    menu.main()

is_shooting = False
last_shot_time = 0

#  основной цикл
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.time.get_ticks() - last_shot_time > SHOOT_DELAY:
                    last_shot_time = pygame.time.get_ticks()
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                is_shooting = True

            elif event.key == pygame.K_ESCAPE:
                sys.exit(0)
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_UP:
                player.move_up()
            elif event.key == pygame.K_DOWN:
                player.move_down()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and player.original_image is not None:
                player.image = player.original_image.copy()
                is_shooting = False

    # чтобы стрелял нормально, не пуля на пуле
    if pygame.time.get_ticks() - last_shot_time > SHOOT_DELAY and is_shooting:
        last_shot_time = pygame.time.get_ticks()
        bullet = Bullet(player.rect.centerx, player.rect.top)
        bullets.add(bullet)

    keys = pygame.key.get_pressed()

    move_player(keys, player)

    screen.blit(current_image, (0, bg_y_shift))
    background_top_rect = background_top.get_rect(topleft=(0, bg_y_shift))
    background_top_rect.top = bg_y_shift + HEIGHT
    screen.blit(background_top, background_top_rect)

    # смена фонов
    bg_y_shift += 1
    if bg_y_shift >= 0:
        bg_y_shift = -HEIGHT

    if score > 3000:
        bg_y_shift += 2

    if score >= 3000 and not new_background_activated:
        current_image = background_img2
        background_top = background_img2.copy()
        new_background_activated = True

    if score >= 10000 and new_background_activated:
        current_image = background_img3
        background_top = background_img3.copy()

    if score >= 15000:
        win()

    if score == 0:
        current_image = background_img
        background_top = background_img.copy()
        new_background_activated = False

    screen.blit(current_image, (0, bg_y_shift))
    background_top_rect = background_top.get_rect(topleft=(0, bg_y_shift))
    background_top_rect.top = bg_y_shift + HEIGHT
    screen.blit(background_top, background_top_rect)

    if score > hi_score:
        hi_score = score
        score_logs.write(f'Лучший счет: {hi_score} \n')

    # спавн врагов
    if random.randint(0, 120) == 0:
        enemy_img = random.choice(enemy1_img)
        enemy_object = Enemy1(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50),
            enemy_img,
        )
        enemy1_group.add(enemy_object)

    if random.randint(0, 60) == 0:
        extra_score = ExtraScore(
            random.randint(50, WIDTH - 50),
            random.randint(-HEIGHT, -50 - extra_score_img.get_rect().height),
            extra_score_img,
        )

        extra_score_group.add(extra_score)

    if random.randint(0, 90) == 0:
        meteor2_img = random.choice(meteor2_imgs)
        meteor2_object = Meteors2(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50 - meteor2_img.get_rect().height),
            meteor2_img,
        )
        meteor2_group.add(meteor2_object)

    #  смерть
    if player_life <= 0:
        show_game_over(score)
        score = 0
        player_life = 200
        player.rect.topleft = initial_player_pos
        bullets.empty()
        extra_score_group.empty()
        meteor_group.empty()
        meteor2_group.empty()
        enemy1_group.empty()
        explosions.empty()

    for extra_score in extra_score_group:
        extra_score.update()
        extra_score.draw(screen)

        if player.rect.colliderect(extra_score.rect):
            score += 20
            extra_score.kill()

    for meteor2_object in meteor2_group:
        meteor2_object.update()
        meteor2_object.draw(screen)

        if meteor2_object.rect.colliderect(player.rect):
            player_life -= 10
            explosion = Explosion(meteor2_object.rect.center, explosion_images)
            explosions.add(explosion)
            meteor2_object.kill()
            score += 20

        bullet_collisions = pygame.sprite.spritecollide(meteor2_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion = Explosion(meteor2_object.rect.center, explosion_images)
            explosions.add(explosion)
            meteor2_object.kill()
            score += 40

        if score >= 3000:
            meteor2_object.speed = 4
        if score >= 10000:
            meteor2_object.speed = 6

    for enemy_object in enemy1_group:
        enemy_object.update(enemy1_group)
        enemy1_group.draw(screen)

        if enemy_object.rect.colliderect(player.rect):
            player_life -= 10
            explosion = Explosion(enemy_object.rect.center, explosion_images)
            explosions.add(explosion)
            enemy_object.kill()
            score += 20

        bullet_collisions = pygame.sprite.spritecollide(enemy_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion = Explosion(enemy_object.rect.center, explosion_images)
            explosions.add(explosion)
            enemy_object.kill()
            score += 50


    player_image_copy = player.image.copy()
    screen.blit(player_image_copy, player.rect)

    for explosion in explosions:
        explosion.update()
        screen.blit(explosion.image, explosion.rect)

    for bullet in bullets:
        bullet.update()
        screen.blit(bullet.image, bullet.rect)

        if bullet.rect.bottom < 0:
            bullet.kill()

    player_life_surface = pygame.Surface((200, 25), pygame.SRCALPHA, 32)
    player_life_surface.set_alpha(216)

    player_life_bar_width = int(player_life / 200 * 200)
    player_life_bar_width = max(0, min(player_life_bar_width, 200))

    player_life_bar = pygame.Surface((player_life_bar_width, 30), pygame.SRCALPHA, 32)
    player_life_bar.set_alpha(216)

    life_bar_image = pygame.image.load("images/life_bar.png").convert_alpha()

    if player_life > 50:
        player_life_bar.fill((152, 251, 152))
    else:
        player_life_bar.fill((0, 0, 0))

    player_life_surface.blit(life_bar_image, (0, 0))
    player_life_surface.blit(player_life_bar, (35, 0))

    life_x_pos = 10
    screen.blit(player_life_surface, (life_x_pos, 10))

    score_surface = pygame.font.SysFont('arial black', 30).render(f'{score}', True, (238, 232, 170))
    score_image_rect = score_surface.get_rect()
    score_image_rect.x, score_image_rect.y = WIDTH - score_image_rect.width - extra_score_img.get_width() - 10, 10

    screen.blit(extra_score_img,
                (score_image_rect.right + 5, score_image_rect.centery - extra_score_img.get_height() // 2))
    screen.blit(score_surface, score_image_rect)

    hi_score_surface = pygame.font.SysFont('arial black', 20).render(f'лучший счет: {hi_score}', True, (255, 255, 255))
    hi_score_surface.set_alpha(128)
    hi_score_x_pos = (screen.get_width() - hi_score_surface.get_width()) // 2
    hi_score_y_pos = 0
    screen.blit(hi_score_surface, (hi_score_x_pos, hi_score_y_pos))

    pygame.display.flip()

    clock.tick(FPS)
score_logs.close()
score_logs = open("score_logs.txt", "r")
print(score_logs.readlines()[-1])
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
