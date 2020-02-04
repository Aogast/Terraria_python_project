import os
import sys
import random

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
    intro_text = ['выбрать карту 1', 'выбрать карту 2', 'выбрать кату 3']
    fon = pygame.transform.scale(load_image('ds.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    color = pygame.Color(50, 150, 50)
    pygame.draw.rect(screen, color, (565, 170, 170, 50), 0)

    color = pygame.Color(50, 150, 50)
    pygame.draw.rect(screen, color, (565, 300, 170, 50), 0)

    color = pygame.Color(50, 150, 50)
    pygame.draw.rect(screen, color, (565, 430, 170, 50), 0)

    font = pygame.font.Font(None, 30)
    text_coord = 60
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 115
        intro_rect.top = text_coord
        intro_rect.x = 570
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                map = 0
                if x >= 565 and x <= 735:
                    if y >= 170 and y <= 220:
                        map = 1
                        return map
                    elif y >= 300 and y <= 350:
                        map = 2
                        return map
                    elif y >= 430 and y<= 480:
                        map = 3
                        return map
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


player_image = [load_image('trump.png'), load_image('trump_run (1).png'), load_image('trump_run (2).png'),
                load_image('trump_run (4).png'), load_image('trump_run (5).png'), load_image('trump_run (6).png'),
                load_image('trump_run (7).png'), load_image('trump_run (8).png'), load_image('trump_run (9).png'),
                load_image('trump_run (11).png'), load_image('trump_run (13).png'), load_image('trump_run (15).png')]

tile_width = tile_height = 39
tile_images = {'grow': pygame.transform.scale(load_image('grow.png'), (tile_width, tile_height)),
               'grass': pygame.transform.scale(load_image('grass.jpg'), (tile_width, tile_height)),
               'pech': pygame.transform.scale(load_image('pech.jpg'), (tile_width, tile_height)),
               'verstac': pygame.transform.scale(load_image('verstac.jpg'), (tile_width, tile_height)),
               'stone': pygame.transform.scale(load_image('stone.jpg'), (tile_width, tile_height)),
               'stone2': pygame.transform.scale(load_image('stone2.jpg'), (tile_width, tile_height)),
               'tree': pygame.transform.scale(load_image('tree.png'), (tile_width, tile_height))}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, x, y, f=0):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.pos_x = x
        self.pos_y = y
        if f:
            self.rect = self.image.get_rect().move(pos_x, pos_y)
        else:
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Map:
    def __init__(self, level):
        self.map = []
        for i in level:
            self.map.append(list(i))
        self.info_destroy = [0, 0, 0]

    def generete_new_level(self):
        global tiles_group, all_sprites, player_group, player
        cout = 0
        coords = []
        new_player, x, y = None, None, None
        for m_sprite in all_sprites:
            coords.append([m_sprite.rect.x, m_sprite.rect.y, m_sprite.pos_x, m_sprite.pos_y])
        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.info_destroy[2] == 1 and y == self.info_destroy[0] and x == self.info_destroy[1]:
                    cout += 1
                if self.map[y][x] == '%':
                    Tile('grass', coords[cout][0], coords[cout][1], coords[cout][2], coords[cout][3], 1)
                    cout += 1
                elif self.map[y][x] == '@':
                    new_player = Player(coords[cout][0], coords[cout][1], 1)
                    cout += 1
                elif self.map[y][x] == '*':
                    Tile('tree', coords[cout][0], coords[cout][1], coords[cout][2], coords[cout][3], 1)
                    cout += 1
                elif self.map[y][x] == '{':
                    Tile('stone', coords[cout][0], coords[cout][1], coords[cout][2], coords[cout][3], 1)
                    cout += 1
                elif self.map[y][x] == '#':
                    Tile('grow', coords[cout][0], coords[cout][1], coords[cout][2], coords[cout][3], 1)
                    cout += 1
                elif self.map[y][x] == '/':
                    Tile('tree', coords[cout][0], coords[cout][1], coords[cout][2], coords[cout][3], 1)
                    cout += 1
        self.info_destroy = [0, 0, 0]
        return new_player, x, y, tiles_group, all_sprites, player_group

    def destroy(self, pos):
        for m_sprite in tiles_group:
            if m_sprite.rect.x > pos[0] > m_sprite.rect.x - tile_width:
                if m_sprite.rect.y > pos[1] > m_sprite.rect.y - tile_height:
                    print(self.map[m_sprite.pos_y - 1][m_sprite.pos_x - 1])
                    if self.map[m_sprite.pos_y - 1][m_sprite.pos_x - 1] != '.':
                        self.map[m_sprite.pos_y - 1][m_sprite.pos_x - 1] = '.'
                        self.info_destroy = [m_sprite.pos_y - 1, m_sprite.pos_x - 1, 1]
                    else:
                        print(self.map[m_sprite.pos_y - 1][m_sprite.pos_x - 1])


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, f=0):
        super().__init__(player_group, all_sprites)
        self.frames = player_image
        self.image = self.frames[0]
        self.cur_frame_right = 0
        self.cur_frame_left = 0
        self.pos_x = tile_width * pos_x + 15
        self.pos_y = tile_height * pos_y + 5
        if f:
            self.rect = self.image.get_rect().move(pos_x, pos_y)
        else:
            self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update_right(self):
        self.cur_frame_right = 1 + ((self.cur_frame_right + 1) % 5)
        self.image = self.frames[self.cur_frame_right]

    def update_left(self):
        self.cur_frame_left = 7 + ((self.cur_frame_left + 1) % 5)
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
                Tile('grass', x, y, x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '*':
                Tile('tree', x, y, x, y)
            elif level[y][x] == '{':
                Tile('stone', x, y, x, y)
            elif level[y][x] == '#':
                Tile('grow', x, y, x, y)
            elif level[y][x] == '/':
                Tile('tree', x, y, x, y)
    return new_player, x, y

class Enemy(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        width = 30
        height = 30
        self.image = pygame.Surface([width, height])
        self.image.fill(red)

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = random.randint(0, 576)
        self.change_y = 600

    def update(self):

        self.rect.centerx += self.change_x
        if self.rect.right <= 0 or self.rect.left >= 100:
            self.change_x *= -1


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
    global player, level_y, level_x, tiles_group, all_sprites, player_group, map
    if map == 1:
        pass
    elif map == 2:
        my_map = Map(load_level('map2.txt'))
    elif map == 3:
        pass

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                me = pygame.mouse.get_pressed()
                if me[0] == 1:
                    my_map.destroy(event.pos)

        if f:
            if q == pygame.K_SPACE and pygame.sprite.spritecollideany(player, tiles_group):
                y = 20
            player.rect.y -= 5
            if q == pygame.K_RIGHT and not pygame.sprite.spritecollideany(player, tiles_group):
                x += 10
                player.rect.x += x
                if pygame.sprite.spritecollideany(player, tiles_group):
                    player.rect.x -= 10
            if q == pygame.K_LEFT and not pygame.sprite.spritecollideany(player, tiles_group):
                x = -10
                player.rect.x += x
                if pygame.sprite.spritecollideany(player, tiles_group):
                    player.rect.x += 10
            player.rect.y += 5
        if not pygame.sprite.spritecollideany(player, tiles_group):
            player.rect.y += GRAVITY
        screen.fill((0, 0, 0))
        player, level_x, level_y, tiles_group, all_sprites, player_group = my_map.generete_new_level()
        if x > 0:
            player.update_right()
        if x < 0:
            player.update_left()
        if x == 0:
            player.update()
        y -= 1
        player.rect.y -= 5
        if not pygame.sprite.spritecollideany(player, tiles_group):
            player.rect.y -= y
            if pygame.sprite.spritecollideany(player, tiles_group):
                player.rect.y += y
                y = 0
        player.rect.y += 5
        if y < 15:
            y = 0
        x = 0
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        player_group.draw(screen)
        tiles_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if map == 2:
    player, level_x, level_y = generate_level(load_level('map2.txt'))

start_screen()
play()
