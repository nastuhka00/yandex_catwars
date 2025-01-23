import sys
import random

import pygame
import pygame.mixer

from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED




pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)
pygame.mixer.set_num_channels(20)
for i in range(20):
    channel = pygame.mixer.Channel(i)
    channel.set_volume(0.25)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load('images/mainmenu.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))



play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)


pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.play(-1)
selected_button = 0
show_menu = True


while show_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if play_button_rect.collidepoint(x, y):
                show_menu = False
                import main
                main.main()
                break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_button = 0
            elif event.key == pygame.K_DOWN:
                selected_button = 1
            elif event.key == pygame.K_RETURN:
                if selected_button == 0:
                    show_menu = False
                    screen.fill(BLACK)
                    import main
                    main.main()
                    break
                elif selected_button == 1:
                    pygame.quit()
                    sys.exit()


    screen.blit(mainmenu_img, (0, 0))


    font = pygame.font.SysFont('Comic Sans MS', 40)
    text = font.render("Play", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = play_button_rect.center
    screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()