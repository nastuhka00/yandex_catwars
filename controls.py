import pygame


def move_player(keys, player):
    if keys[pygame.K_LEFT]:
        if keys[pygame.K_UP]:
            player.move_up_left()
        elif keys[pygame.K_DOWN]:
            player.move_down_left()
        else:
            player.move_left()
    elif keys[pygame.K_RIGHT]:
        if keys[pygame.K_UP]:
            player.move_up_right()
        elif keys[pygame.K_DOWN]:
            player.move_down_right()
        else:
            player.move_right()
    elif keys[pygame.K_UP]:
        player.move_up()
    elif keys[pygame.K_DOWN]:
        player.move_down()


