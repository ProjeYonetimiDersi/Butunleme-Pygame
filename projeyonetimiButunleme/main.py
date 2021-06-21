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

        self.platforms.add(p1)
        self.platforms.add(p2)


        self.player = Player()


        self.all_sprites.add(self.player)
        self.all_sprites.add(p1)
        self.all_sprites.add(p2)


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

        carpismalar = pygame.sprite.spritecollide(self.player, self.platforms, dokill = False)
        if carpismalar:
            self.player.hiz.y = 0
            self.player.rect.bottom = carpismalar[0].rect.top

        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

game = Game()

while game.running:
    game.new()