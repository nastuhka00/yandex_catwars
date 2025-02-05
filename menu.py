import sys
import pygame
from classes.constants import WIDTH, HEIGHT, BLACK

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load('images/mainmenu.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

play_button_rect = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2 + 120, 280, 90)

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

    font = pygame.font.SysFont('arial black', 190)
    game_name = font.render("CAT WARS", True, '#1c542d')
    game_name_rect = game_name.get_rect()
    game_name_rect.center = (WIDTH // 2, 170)
    font = pygame.font.SysFont('arial black', 60)
    text = font.render("ИГРАТЬ", True, '#1c542d')
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, '#1c542d', play_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = play_button_rect.center
    screen.blit(game_name, game_name_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
