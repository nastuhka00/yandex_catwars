import pygame

from .constants import WIDTH, HEIGHT



class ExtraScore(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.speed = 2
        self.rect.x = x
        self.rect.y = y
        self.direction_x = 0
        self.direction_y = 1

    def update(self):
        self.rect.y += self.speed * self.direction_y

        if self.rect.bottom >= HEIGHT + 100:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)