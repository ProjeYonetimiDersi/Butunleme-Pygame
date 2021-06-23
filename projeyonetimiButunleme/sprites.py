import pygame
from settings import *

vector = pygame.math.Vector2

class Spritesheet:
    def __init__(self,resimler):
        self.spritesheet = pygame.image.load(resimler)

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width//2, height//2))
        return image

class Player(pygame.sprite.Sprite):
    def __init__(self, oyun):
        super().__init__()
        self.oyun = oyun
        self.image = self.oyun.spritesheet.get_image(614, 1063, 120, 191)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.hiz = vector(0, 0)
        self.ivme = vector(0, 0.5)

    def zipla(self):
        self.rect.y += 1
        temasVarmi = pygame.sprite.spritecollide(self, self.oyun.platforms, False)
        if temasVarmi:
            self.hiz.y -= 15


    def update(self, *args):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                if self.hiz.x < 7:
                    self.ivme.x = 0.5
                else:
                    self.ivme.x = 0

            if keys[pygame.K_LEFT]:
                if self.hiz.x > -7:
                    self.ivme.x = -0.5
                else:
                    self.ivme.x = 0

            self.hiz.x += self.ivme.x

        else:
            if self.hiz.x > 0:
                self.hiz.x -= 0.5
            if self.hiz.x < 0:
                self.hiz.x += 0.5

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