import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.acc = 0.5
        self.vx = 0

    def update(self, *args):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                if self.vx < 7:
                    self.vx += self.acc
                else:
                    self.vx = 7

            if keys[pygame.K_LEFT]:
                if self.vx > -7:
                    self.vx -= self.acc
                else:
                    self.vx = -7

        else:
            if self.vx > 0:
                self.vx -= 0.3
            if self.vx < 0:
                self.vx += 0.3

        self.rect.x += self.vx


        if self.rect.x > WIDTH:
            self.rect.x = 0

        if self.rect.right < 0:
            self.rect.right = WIDTH