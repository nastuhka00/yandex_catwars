import pygame
import sys
from classes.constants import WIDTH, HEIGHT, BLACK
screen = pygame.display.set_mode((WIDTH, HEIGHT))


#  окно при смерти
def show_game_over(score):
    font = pygame.font.SysFont('arial black', 90)
    font_small = pygame.font.SysFont('arial black', 60)
    text = font.render("ВЫ ПРОИГРАЛИ(", True, '#b30000')
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
    score_text = font_small.render(f"Ваш счет: {score}", True, 'white')
    score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 35))

    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)

    flag = True
    again_button_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 120, 400, 100)
    font = pygame.font.SysFont('arial black', 60)
    text = font.render("Еще раз", True, 'white')
    pygame.draw.rect(screen, BLACK, again_button_rect, border_radius=10)
    pygame.draw.rect(screen, 'white', again_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = again_button_rect.center
    screen.blit(text, text_rect)

    pygame.display.flip()

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if again_button_rect.collidepoint(x, y):
                    flag = False
                    break


# окно при победе
def win():
    font = pygame.font.SysFont('arial black', 90)
    text = font.render("ПОБЕДА!!!", True, '#b30000')
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
    screen.blit(text, text_rect)

    flag = True
    again_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 100)
    font = pygame.font.SysFont('arial black', 60)
    text = font.render("Ура", True, 'white')
    pygame.draw.rect(screen, BLACK, again_button_rect, border_radius=10)
    pygame.draw.rect(screen, 'white', again_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = again_button_rect.center
    screen.blit(text, text_rect)

    pygame.display.flip()

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if again_button_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()
