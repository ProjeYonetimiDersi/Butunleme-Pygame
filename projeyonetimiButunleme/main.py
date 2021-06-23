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
        self.sayac = 0
        self.skor = 0
        self.maksimumSkor = 0

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        p1 = Platform(0, HEIGHT-30, WIDTH, 40)
        p2 = Platform(WIDTH/2-50, 500, 100, 30)
        p3 = Platform(400, 300, 50, 30)
        p4 = Platform(300, 200, 30, 30)
        p5 = Platform(100, 200, 70, 30)
        p6 = Platform(50, 500, 100, 30)

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
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update()

    def draw(self):
        self.screen.fill((135, 206, 250))
        self.ustyazi("Skor: {}".format(self.skor))
        self.all_sprites.draw(self.screen)

    def update(self):
        self.all_sprites.update()

        if self.player.hiz.y > 0:
            carpismalar = pygame.sprite.spritecollide(self.player, self.platforms, dokill = False)
            if carpismalar:
                self.player.hiz.y = 0
                self.player.rect.bottom = carpismalar[0].rect.top

        if self.player.rect.top < HEIGHT/4:
            self.player.rect.y += abs(self.player.hiz.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.hiz.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.skor += 10

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
            genislik = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH-genislik), random.randrange(-75, -20), genislik, 30)
            self.platforms.add(p)
            self.all_sprites.add(p)

        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.zipla()

    def girisEkrani(self):
        resim = pygame.image.load("baslangic.jpg")
        self.screen.blit(resim, resim.get_rect())
        pygame.display.update()
        self.tusBekleme()

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