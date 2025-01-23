import pygame
import sys
from classes.constants import WIDTH, HEIGHT, BLACK, RED, WHITE

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def music_background():
    pygame.mixer.music.load('game_sounds/background_music.mp3')
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(loops=-1)


def show_game_over(score):
    font = pygame.font.SysFont('Impact', 50)
    font_small = pygame.font.SysFont('Impact', 30)
    text = font.render("GAME OVER", True, (139, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))

    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)

    flag = True
    play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)


    font = pygame.font.SysFont('Comic Sans MS', 40)
    text = font.render("Try again", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = play_button_rect.center
    screen.blit(text, text_rect)

    pygame.display.flip()
    pygame.mixer.music.load('game_sounds/gameover.mp3')
    pygame.mixer.music.play()

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_button_rect.collidepoint(x, y):
                    flag = False
                    break

    music_background()
