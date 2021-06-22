import pygame,random,sys
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

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
        self.screen.fill((0, 0, 0))
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


game = Game()

while game.running:
    game.new()