import pygame
from settings import *

vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.hiz = vector(0, 0)
        self.ivme = vector(0, 0.3)

    def update(self, *args):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                if self.hiz.x < 7:
                    self.ivme.x = 0.3
                else:
                    self.ivme.x = 0

            if keys[pygame.K_LEFT]:
                if self.hiz.x > -7:
                    self.ivme.x = -0.3
                else:
                    self.ivme.x = 0

            self.hiz.x += self.ivme.x

        else:
            if self.hiz.x > 0:
                self.hiz.x -= 0.3
            if self.hiz.x < 0:
                self.hiz.x += 0.3

        self.hiz.y += self.ivme.y

        self.rect.x += self.hiz.x
        self.rect.y += self.hiz.y


        if self.rect.x > WIDTH:
            self.rect.x = 0

        if self.rect.right < 0:
            self.rect.right = WIDTH

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y