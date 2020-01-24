import os
import sys

import pygame

FPS = 40

pygame.init()
size = WIDTH, HEIGHT = 1024, 576
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
GRAVITY = 5


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey:
        print(colorkey)
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        print(colorkey)
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('loading....png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == 13:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def choose_level():
    fon = pygame.transform.scale(load_image('ds.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'grow': load_image('grow.png'), 'grass': load_image('grass.jpg'),
               'pech': load_image('pech.jpg'), 'verstac': load_image('verstac.jpg'),
               'stone': load_image('stone.jpg'), 'tree': load_image('tree.png')}
player_image = [load_image('trump.png'), load_image('trump_run (1).png'), load_image('trump_run (2).png'),
                load_image('trump_run (4).png'), load_image('trump_run (5).png'), load_image('trump_run (6).png'),
                load_image('trump_run (7).png'), load_image('trump_run (8).png'), load_image('trump_run (9).png'),
                load_image('trump_run (11).png'), load_image('trump_run (13).png'), load_image('trump_run (15).png')]

tile_width = tile_height = 39


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = player_image
        self.image = self.frames[0]
        self.cur_frame_right = 0
        self.cur_frame_left = 0
        self.pos_x = tile_width * pos_x + 15
        self.pos_y = tile_height * pos_y + 5
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update_right(self):
        self.cur_frame_right = 1 + ((self.cur_frame_right + 1) % 5)
        self.image = self.frames[self.cur_frame_right]

    def update_left(self):
        self.cur_frame_left = 7 \
                              + ((self.cur_frame_left + 1) % 5)
        self.image = self.frames[self.cur_frame_left]

    def update(self):
        self.image = self.frames[0]


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '%':
                Tile('grass', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '*':
                Tile('tree', x, y)
            elif level[y][x] == '{':
                Tile('stone', x, y)
            elif level[y][x] == '#':
                Tile('grow', x, y)
            elif level[y][x] == '/':
                Tile('tree', x, y)
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


pygame.mixer.music.load('first.mp3')
pygame.mixer.music.play()


def play():
    x = 0
    y = 0
    camera = Camera()
    f = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == \
                        pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    q = event.key
                    f = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == \
                        pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    q = event.key
                    f = False
        if f:
            if q == pygame.K_SPACE and y == 0 and pygame.sprite.spritecollideany(player, tiles_group):
                y = 25
            player.rect.y -= 5
            player_group.draw(screen)
            if q == pygame.K_RIGHT and not pygame.sprite.spritecollideany(player, tiles_group):
                x += 5
            if q == pygame.K_LEFT and not pygame.sprite.spritecollideany(player, tiles_group):
                x = -5
            player.rect.y += 5
            player_group.draw(screen)
        if not pygame.sprite.spritecollideany(player, tiles_group):
            player.rect.y += GRAVITY
        screen.fill((0, 0, 0))
        player.rect.x += x
        player.rect.y -= y
        if x > 0:
            player.update_right()
        if x < 0:
            player.update_left()
        if x == 0:
            player.update()

        y -= 1
        if y < 20:
            y = 0
        x = 0
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        player_group.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


player, level_x, level_y = generate_level(load_level('map.txt'))

start_screen()
play()
