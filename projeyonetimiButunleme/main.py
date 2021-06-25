import pygame,random,sys
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.spritesheet = Spritesheet(SPRITESHEET)
        self.running = True
        self.platformsayac = 0
        self.sayac = 0
        self.skor = 0
        self.maksimumSkor = 0

        self.ziplamaSesi = pygame.mixer.Sound("muzik/zipla.wav")
        self.ziplamaSesi.set_volume(0.1)

    def new(self):
        pygame.mixer.music.load("muzik/mainmusic.mp3")
        pygame.mixer.music.set_volume(0.5)

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.powerUps = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        p1 = Platform(self, 0, HEIGHT-30)
        p2 = Platform(self, WIDTH/2-50, 500)
        p3 = Platform(self, 400, 300)
        p4 = Platform(self, 300, 200)
        p5 = Platform(self, 100, 200)
        p6 = Platform(self, 50, 500)

        self.platforms.add(p1)
        self.platforms.add(p2)
        self.platforms.add(p3)
        self.platforms.add(p4)
        self.platforms.add(p5)
        self.platforms.add(p6)


        self.player = Player(self)


        self.all_sprites.add(self.player)
        self.all_sprites.add(p1)
        self.all_sprites.add(p2)
        self.all_sprites.add(p3)
        self.all_sprites.add(p4)
        self.all_sprites.add(p5)
        self.all_sprites.add(p6)



        self.run()

    def run(self):
        self.playing = True
        pygame.mixer.music.play()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update()
        pygame.mixer.music.fadeout(1000)

    def draw(self):
        self.screen.fill((135, 206, 250))
        self.ustyazi("Skor: {}".format(self.skor))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)

    def update(self):
        self.all_sprites.update()

        if self.player.hiz.y > 0:
            carpismalar = pygame.sprite.spritecollide(self.player, self.platforms, dokill = False)
            if carpismalar:
                durum = self.player.rect.midbottom[0] <= carpismalar[0].rect.left - 10 or self.player.rect.midbottom[0] >= carpismalar[0].rect.right + 10
                if carpismalar[0].rect.center[1] + 7 > self.player.rect.bottom and not durum:
                    self.player.jumping = True
                    self.player.hiz.y = 0
                    self.player.rect.bottom = carpismalar[0].rect.top

        if self.player.rect.top < HEIGHT/4:
            self.player.rect.y += max(abs(self.player.hiz.y), 3)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.hiz.y), 3)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.skor += 10

        powerGain = pygame.sprite.spritecollide(self.player, self.powerUps, True)
        if powerGain:
            self.player.hiz.y = -35

        dusmanTemasi = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
        if dusmanTemasi:
            try:
                with open("skor.txt", "r") as dosya:
                    kayitliSkor = int(dosya.read())
                    if self.skor > kayitliSkor:
                        with open("skor.txt", "w") as dosya:
                            dosya.writelines(str(self.skor))
                        self.maksimumSkor = self.skor
                    else:
                        with open("skor.txt","r") as dosya:
                            skor = str(dosya.read())
                            self.maksimumSkor = skor
            except FileNotFoundError:
                with open("skor.txt", "w") as dosya:
                    dosya.writelines(str(self.skor))
                    self.maksimumSkor = skor

            self.skor = 0
            self.playing = False

        if self.player.rect.top > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.hiz.y, 15)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            try:
                with open("skor.txt", "r") as dosya:
                    kayitliSkor = int(dosya.read())
                    if self.skor > kayitliSkor:
                        with open("skor.txt", "w") as dosya:
                            dosya.writelines(str(self.skor))
                        self.maksimumSkor = self.skor
                    else:
                        with open("skor.txt","r") as dosya:
                            skor = str(dosya.read())
                            self.maksimumSkor = skor
            except FileNotFoundError:
                with open("skor.txt", "w") as dosya:
                    dosya.writelines(str(self.skor))
                    self.maksimumSkor = skor

            self.skor = 0
            self.playing = False


        while len(self.platforms) < 6:
            if self.platformsayac == 0:
                genislik = random.randrange(50, 100)
                p = Platform(self, random.randrange(0, WIDTH - genislik), random.randrange(-2, 0))
            else:
                genislik = random.randrange(50, 100)
                p = Platform(self, random.randrange(0, WIDTH - genislik), random.randrange(-42, -2))

            self.platformsayac += 1

            if len(self.platforms) == 5:
                self.platformsayac = 0


            self.platforms.add(p)
            self.all_sprites.add(p)

            if random.randint(1, 10) == 1:
                powerup = PowerUp(self, p)
                self.powerUps.add(powerup)
                self.all_sprites.add(powerup)

            if p.rect.width > 100:
                if random.randint(1, 10) == 1:
                    enemy = Enemy(self, p)
                    self.enemies.add(enemy)
                    self.all_sprites.add(enemy)

        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.zipla()

    def girisEkrani(self):
        pygame.mixer.music.load("muzik/giris_ekrani.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        resim = pygame.image.load("baslangic.jpg")
        self.screen.blit(resim, resim.get_rect())
        pygame.display.update()
        self.tusBekleme()
        pygame.mixer.music.fadeout(500)

    def bitisEkrani(self):
        resim = pygame.image.load("gover.jpg")
        self.screen.blit(resim, resim.get_rect())

        font = pygame.font.SysFont("Century Gothic", 25)
        text = font.render("En Yüksek Skor: {}".format(self.maksimumSkor), True, (0, 0, 0))
        self.screen.blit(text, (WIDTH/2-(text.get_size() [0]/2), 480))

        pygame.display.update()
        self.tusBekleme()

    def tusBekleme(self):
        bekleme = True
        while bekleme:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    bekleme = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    bekleme = False

    def ustyazi(self, yazi="Zıpla!"):
        font = pygame.font.SysFont("Century Gothic", 25)
        text = font.render(yazi, True, (255, 255, 255))
        self.screen.blit(text, (WIDTH/2-(text.get_size() [0]/2), 0))

game = Game()
game.girisEkrani()

while game.running:
    game.new()
    game.bitisEkrani()