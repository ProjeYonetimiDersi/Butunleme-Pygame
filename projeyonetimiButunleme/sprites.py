import pygame
from settings import *
from random import choice

vector = pygame.math.Vector2

class Spritesheet:
    def __init__(self,resimler):
        self.spritesheet = pygame.image.load(resimler)

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width//2, height//2))
        image.set_colorkey((0, 0, 0))
        return image

class Player(pygame.sprite.Sprite):
    def __init__(self, oyun):
        super().__init__()
        self.oyun = oyun
        self.load_images()
        self.sonZaman = 0
        self.sayac = 0
        self.jumping = False
        self.walking = False
        self.image = self.beklemeler[0]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.hiz = vector(0, 0)
        self.ivme = vector(0, 0.5)

    def load_images(self):
        self.beklemeler = [self.oyun.spritesheet.get_image(614, 1063, 120, 191),
                      self.oyun.spritesheet.get_image(690, 406, 120, 201)]

        self.sag_yurumeler = [self.oyun.spritesheet.get_image(678, 860, 120, 201),
                      self.oyun.spritesheet.get_image(692, 1458, 120, 207)]

        self.sol_yurumeler = []

        for yurume in self.sag_yurumeler:
            self.sol_yurumeler.append(pygame.transform.flip(yurume, True, False))

    def zipla(self):
        self.rect.y += 1
        temasVarmi = pygame.sprite.spritecollide(self, self.oyun.platforms, False)
        if temasVarmi and self.jumping:
            self.oyun.ziplamaSesi.play()
            self.hiz.y -= 15
            self.jumping = False


    def update(self, *args):

        self.animasyon()

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

        if abs(self.hiz.x) < 0.2:
            self.hiz.x = 0

        self.rect.x += self.hiz.x
        self.rect.y += self.hiz.y


        if self.rect.x > WIDTH:
            self.rect.x = 0 - self.rect.width

        if self.rect.right < 0:
            self.rect.right = WIDTH + self.rect.width

        self.mask = pygame.mask.from_surface(self.image)

    def animasyon(self):
        simdikiZaman = pygame.time.get_ticks()

        if self.hiz.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if simdikiZaman - self.sonZaman > 250:
                self.sonZaman = simdikiZaman
                if self.hiz.x > 0:
                    bottom = self.rect.midbottom
                    self.image = self.sag_yurumeler[self.sayac % 2]
                    self.rect = self.image.get_rect()
                    self.rect.midbottom = bottom
                    self.sayac += 1
                else:
                    bottom = self.rect.midbottom
                    self.image = self.sol_yurumeler[self.sayac % 2]
                    self.rect = self.image.get_rect()
                    self.rect.midbottom = bottom
                    self.sayac += 1

        if not self.walking:
            if simdikiZaman - self.sonZaman > 250:
                self.sonZaman = simdikiZaman
                bottom = self.rect.midbottom
                self.image = self.beklemeler[self.sayac % 2]
                self.rect = self.image.get_rect()
                self.rect.midbottom = bottom
                self.sayac += 1

class Platform(pygame.sprite.Sprite):
    def __init__(self, oyun, x, y):
        super().__init__()
        self.oyun = oyun
        self.image = choice([self.oyun.spritesheet.get_image(0, 768, 380, 94),
                      self.oyun.spritesheet.get_image(213, 1764, 201, 100)])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, oyun, platform):
        super().__init__()
        self.oyun = oyun
        self.platform = platform
        self.image = self.oyun.spritesheet.get_image(820, 1805, 71, 70)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.platform.rect.midtop

    def update(self, *args):
        self.rect.midbottom = self.platform.rect.midtop

        if not self.oyun.platforms.has(self.platform):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, oyun, platform):
        super().__init__()
        self.oyun = oyun
        self.platform = platform
        self.upload_images()

        self.image = self.bekleme
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.platform.rect.midtop
        self.hareketSonZaman = 0
        self.sayac = 0

        self.vx = 3

    def upload_images(self):
        self.bekleme = self.oyun.spritesheet.get_image(814, 1417, 90, 155)

        self.sag_yurumeler = [self.oyun.spritesheet.get_image(704, 1256, 120, 159),
                              self.oyun.spritesheet.get_image(812, 296, 90, 155)]
        self.sol_yurumeler = []

        for yurume in self.sag_yurumeler:
            self.sol_yurumeler.append(pygame.transform.flip(yurume, True, False))

    def update(self, *args):
        self.rect.bottom = self.platform.rect.top

        if not self.oyun.platforms.has(self.platform):
            self.kill()

        self.rect.x += self.vx

        if self.rect.right + 4 > self.platform.rect.right or self.rect.x - 4 < self.platform.rect.left:
            kayitvx = self.vx
            self.vx = 0

            bottom = self.rect.midbottom
            self.image = self.bekleme
            self.rect = self.image.get_rect()
            self.rect.midbottom = bottom

            self.vx = kayitvx * -1

        if self.vx > 0:
            simdi = pygame.time.get_ticks()
            if simdi - self.hareketSonZaman > 250:
                self.hareketSonZaman = simdi
                bottom = self.rect.midbottom
                self.image = self.sag_yurumeler[self.sayac % 2]
                self.rect = self.image.get_rect()
                self.rect.midbottom = bottom
                self.sayac += 1
        else:
            simdi = pygame.time.get_ticks()
            if simdi - self.hareketSonZaman > 250:
                self.hareketSonZaman = simdi
                bottom = self.rect.midbottom
                self.image = self.sol_yurumeler[self.sayac % 2]
                self.rect = self.image.get_rect()
                self.rect.midbottom = bottom
                self.sayac += 1

        self.mask = pygame.mask.from_surface(self.image)
