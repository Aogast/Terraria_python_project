import os
import sys
import random

import pygame

FPS = 40
mapp = 0
pygame.init()
size = WIDTH, HEIGHT = 1024, 576
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
GRAVITY = 5


def load_image(name, colorkey=None):
    """"This function allows you to load images from the data folder."""
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


def terminate():
    """Еhis function forces the game to end."""
    pygame.quit()
    sys.exit()


def start_screen():
    """This function is responsible for the start screen and for the selection of maps."""
    global mapp
    intro_text = ['выбрать карту 1', 'выбрать карту 2', 'выбрать карту 3']
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
                if 565 <= x <= 735:
                    if 170 <= y <= 220:
                        mapp = 1
                        return
                    elif 300 <= y <= 350:
                        mapp = 2
                        return
                    elif 430 <= y <= 480:
                        mapp = 3
                        return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    """This function loads map information from a txt file."""
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


player_image = [load_image('trump.png'), load_image('trump_run (1).png'), load_image('trump_run (2).png'),
                load_image('trump_run (4).png'), load_image('trump_run (5).png'), load_image('trump_run (6).png'),
                load_image('trump_run (7).png'), load_image('trump_run (8).png'), load_image('trump_run (9).png'),
                load_image('trump_run (11).png'), load_image('trump_run (13).png'), load_image('trump_run (15).png')]
day_image = [pygame.transform.scale(load_image('day.png'), (WIDTH, HEIGHT)),
             pygame.transform.scale(load_image('night.jpg'), (WIDTH, HEIGHT))]
tile_width = tile_height = 39
enemy_image = pygame.transform.scale(load_image('slime.jpg'), (tile_width, tile_height))
game_over_image = pygame.transform.scale(load_image('gameover.png'), (WIDTH, HEIGHT))
tile_images = {'#': pygame.transform.scale(load_image('grow.png'), (tile_width, tile_height)),
               '%': pygame.transform.scale(load_image('grass.jpg'), (tile_width, tile_height)),
               'pech': pygame.transform.scale(load_image('pech.jpg'), (tile_width, tile_height)),
               'verstac': pygame.transform.scale(load_image('verstac.jpg'), (tile_width, tile_height)),
               '{': pygame.transform.scale(load_image('stone.jpg'), (tile_width, tile_height)),
               'stone2': pygame.transform.scale(load_image('stone2.jpg'), (tile_width, tile_height)),
               '*': pygame.transform.scale(load_image('listva.png'), (tile_width, tile_height)),
               '/': pygame.transform.scale(load_image('tree.png'), (tile_width, tile_height)),
               '^': pygame.transform.scale(load_image('sand.jpg'), (tile_width, tile_height)),
               '$': pygame.transform.scale(load_image('snow.png'), (tile_width, tile_height)),
               'sword': load_image('sword.jpg')}


class Tile(pygame.sprite.Sprite):
    """This sprite class contains all map blocks."""
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
    """This class is responsible for updating the map: structure and destruction."""
    def __init__(self, level):
        self.map = []
        for i in level:
            self.map.append(list(i))
        self.info_destroy = [0, 0, 0]
        self.info_create = [0, 0, 0]
        self.ly = len(self.map)
        self.lx = len(self.map[0])

    def generete_new_level(self):
        """Update function"""
        global tiles_group, all_sprites, player_group, player, \
            enemy, enemy_group, inventory_group, walls_group
        cout = 0
        coords = []

        player_info = [player.rect.x, player.rect.y,
                       player.cur_frame_left, player.cur_frame_right]
        if enemy:
            p_x, p_y = enemy.rect.x, enemy.rect.y
        new_player, x, y = None, None, None
        coords_invent = []
        for i_sprite in inventory_group:
            coords_invent.append([i_sprite.rect.x, i_sprite.rect.y])
        for m_sprite in tiles_group:
            coords.append([m_sprite.rect.x, m_sprite.rect.y, m_sprite.pos_x, m_sprite.pos_y])
        walls_group = pygame.sprite.Group()
        inventory_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        if enemy:
            enemy = Enemy()
            enemy.normal = 0
            enemy.rect.x = p_x
            enemy.rect.y = p_y
        for y in range(self.ly):
            for x in range(self.lx):
                if self.info_destroy[2] == 1 and y == self.info_destroy[0] and x == self.info_destroy[1]:
                    cout += 1
                if self.info_create[-1] == 1 and y == self.info_create[0] and x == self.info_create[1]:
                    Tile(self.map[y][x], self.info_create[-2], self.info_create[-3],
                         self.info_create[-4], self.info_create[-5], 1)
                    continue
                if self.map[y][x] in tile_images.keys():
                    Tile(self.map[y][x], coords[cout][0], coords[cout][1], coords[cout][2], coords[cout][3], 1)
                    cout += 1
                elif self.map[y][x] == '@':
                    new_player = Player(player_info[0], player_info[1], 1)
        self.info_destroy = [0, 0, 0]
        self.info_create = [0, 0, 0]
        Walls(coords[0][0], 0, coords[0][0], len(self.map) * tile_width)
        Walls(coords[-1][0], 0, coords[-1][0], len(self.map) * tile_width)
        Walls(coords[0][0], coords[-1][1], coords[-1][0], coords[-1][1])
        player.cur_frame_left = player_info[2]
        player.cur_frame_right = player_info[3]
        return new_player, tiles_group, all_sprites, player_group, coords_invent

    def destroy_or_creating(self, pos):
        """Construction and demolition function"""
        a = list(player.inventory.keys())
        for m_sprite in tiles_group:
            if m_sprite.rect.x < pos[0] < m_sprite.rect.x + tile_width:
                if m_sprite.rect.y < pos[1] < m_sprite.rect.y + tile_height:
                    if self.map[m_sprite.pos_y][m_sprite.pos_x] != '.':
                        if self.map[m_sprite.pos_y][m_sprite.pos_x] in a:
                            player.inventory[self.map[m_sprite.pos_y][m_sprite.pos_x]] += 1
                        elif len(player.inventory) < 10:
                            player.inventory[self.map[m_sprite.pos_y][m_sprite.pos_x]] = 1
                            player.make_inventary(
                                tile_images[self.map[m_sprite.pos_y][m_sprite.pos_x]])
                        self.map[m_sprite.pos_y][m_sprite.pos_x] = '.'
                        self.info_destroy = [m_sprite.pos_y, m_sprite.pos_x, 1]
            if player.number_bloc != 0 and self.info_destroy[2] != 1:
                if m_sprite.rect.x + tile_width > pos[0] > m_sprite.rect.x:
                    if m_sprite.rect.y - tile_height < pos[1] < m_sprite.rect.y:
                        if self.map[m_sprite.pos_y - 1][m_sprite.pos_x] == '.':
                            self.map[m_sprite.pos_y - 1][m_sprite.pos_x] = a[player.number_bloc]
                            player.inventory[a[player.number_bloc]] -= 1
                            self.info_create = [m_sprite.pos_y - 1, m_sprite.pos_x,
                                                m_sprite.rect.y - tile_height, m_sprite.rect.x, 1]
                    elif m_sprite.rect.y + 2 * tile_height > pos[1] > m_sprite.rect.y + tile_height:
                        if self.map[m_sprite.pos_y + 1][m_sprite.pos_x] == '.':
                            self.map[m_sprite.pos_y + 1][m_sprite.pos_x] = a[player.number_bloc]
                            player.inventory[a[player.number_bloc]] -= 1
                            self.info_create = [m_sprite.pos_y + 1, m_sprite.pos_x,
                                                m_sprite.rect.y + tile_height, m_sprite.rect.x, 1]
                            return
                elif m_sprite.rect.y + tile_width > pos[1] > m_sprite.rect.y:
                    if m_sprite.rect.x - tile_height < pos[0] < m_sprite.rect.x:
                        if self.map[m_sprite.pos_y][m_sprite.pos_x - 1] == '.':
                            self.map[m_sprite.pos_y][m_sprite.pos_x - 1] = a[player.number_bloc]
                            player.inventory[a[player.number_bloc]] -= 1
                            self.info_create = [m_sprite.pos_y, m_sprite.pos_x - 1,
                                                m_sprite.rect.y, m_sprite.rect.x - tile_width, 1]
                    elif m_sprite.rect.x + 2 * tile_height > pos[0] > m_sprite.rect.x + tile_height:
                        if self.map[m_sprite.pos_y][m_sprite.pos_x + 1] == '.':
                            self.map[m_sprite.pos_y][m_sprite.pos_x + 1] = a[player.number_bloc]
                            player.inventory[a[player.number_bloc]] -= 1
                            self.info_create = [m_sprite.pos_y, m_sprite.pos_x + 1,
                                                m_sprite.rect.y, m_sprite.rect.x + tile_width, 1]
        if player.inventory[a[player.number_bloc]] == 0:
            del player.inventory[a[player.number_bloc]]
            player.number_bloc -= 1


class Walls(pygame.sprite.Sprite):
    """This is a class of wall sprites so that a person does not go beyond the map"""
    def __init__(self, x1, y1, x2, y2):
        super().__init__(walls_group, all_sprites)
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Player(pygame.sprite.Sprite):
    """Main Player Class"""
    def __init__(self, pos_x, pos_y, f=0):
        super().__init__(player_group, all_sprites)
        self.frames = player_image
        self.image = self.frames[0]
        self.cur_frame_right = 0
        self.number_bloc = 0
        self.cur_frame_left = 0
        self.inventory = {'sword': 1}
        self.pos_x = tile_width * pos_x + 15
        self.pos_y = tile_height * pos_y + 5
        if f:
            self.rect = self.image.get_rect().move(pos_x, pos_y)
        else:
            self.make_inventary()
            self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def make_inventary(self, f=0, coords=None):
        """Player inventory creation"""
        a = list(self.inventory.keys())
        if f == 0:
            for i in range(len(a)):
                Playerinventary(tile_images[a[i]], i * 40, 0, f)
        elif f == 1:
            for i in range(len(a)):
                Playerinventary(tile_images[a[i]], coords[i][0], coords[i][1], f)
        else:
            Playerinventary(f, len(a) * 40, 5, 1)

    def update_right(self):
        self.cur_frame_right = 1 + ((self.cur_frame_right + 1) % 5)
        self.image = self.frames[self.cur_frame_right]

    def update_left(self):
        self.cur_frame_left = 7 + ((self.cur_frame_left + 1) % 5)
        self.image = self.frames[self.cur_frame_left]

    def update(self):
        self.image = self.frames[0]


class Enemy(pygame.sprite.Sprite):
    """Class of an enemy who fights a hero"""
    def __init__(self):
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.normal = 0
        self.rect = self.image.get_rect().move(self.creating_coords(1))
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect = self.image.get_rect().move(self.creating_coords(0))
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.normal = 1

    def creating_coords(self, side):
        if side:
            pos_x = random.randint(player.rect.x - 150, player.rect.x - 100)
        else:
            pos_x = random.randint(player.rect.x + 100, player.rect.x + 150)
        pos_y = player.rect.y - 3
        return pos_x, pos_y

    def update(self):
        move_x = (player.rect.x - self.rect.x) // 20
        self.rect.x += move_x
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.x -= move_x
            if player.rect.y < self.rect.y:
                self.rect.y -= 40
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.y += 40


class Playerinventary(pygame.sprite.Sprite):
    """Hero inventory sprite class"""
    def __init__(self, image, pos_x, pos_y, f=0):
        super().__init__(inventory_group, all_sprites)
        self.image = pygame.transform.scale(image, (40, 40))
        if f:
            self.rect = self.image.get_rect().move(pos_x, pos_y)
        else:
            self.rect = self.image.get_rect().move(10 * pos_x + 5, 10 * pos_y + 5)


player = None
enemy = None

walls_group = pygame.sprite.Group()
inventory_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    """Сreates a map using information from a txt file"""
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in tile_images.keys():
                Tile(level[y][x], x, y, x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    Walls(0, 0, 0, len(level))
    Walls(len(level[0]), 0, len(level[0]), len(level))
    Walls(0, len(level), len(level[0]), len(level))
    return new_player, x, y


class Camera:
    """The class is responsible for finding the hero in the center of the screen"""
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play()
music = ['music.mp3', 'first.mp3']


def play():
    """Main game cycle"""
    global player, level_y, level_x, tiles_group, all_sprites, \
        player_group, enemy, enemy_group, inventory_group, mapp
    if mapp == 1:
        my_map = Map(load_level('map1.txt'))
    elif mapp == 2:
        my_map = Map(load_level('map2.txt'))
    elif mapp == 3:
        my_map = Map(load_level('map3.txt'))
    day_time = [0, 0]
    xp = 100
    x = 0
    y = 0
    camera = Camera()
    count_enemy = [0, 1]
    f = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == \
                        pygame.K_a or event.key == pygame.K_d:
                    q = event.key
                    f = True
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or \
                        event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or \
                        event.key == pygame.K_7 or event.key == pygame.K_8:
                    if len(list(player.inventory.keys())) > event.key - 49:
                        player.number_bloc = event.key - 49
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == \
                        pygame.K_a or event.key == pygame.K_d:
                    q = event.key
                    f = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                me = pygame.mouse.get_pressed()
                if me[0] == 1:
                    my_map.destroy_or_creating(event.pos)
        if f:
            if q == pygame.K_SPACE and pygame.sprite.spritecollideany(player, tiles_group):
                y = 20
            player.rect.y -= 5
            if q == pygame.K_d and not pygame.sprite.spritecollideany(player, tiles_group):
                x += 10
                player.rect.x += x
                if pygame.sprite.spritecollideany(player, tiles_group):
                    player.rect.x -= 10
            if q == pygame.K_a and not pygame.sprite.spritecollideany(player, tiles_group):
                x = -10
                player.rect.x += x
                if pygame.sprite.spritecollideany(player, tiles_group):
                    player.rect.x += 10
            player.rect.y += 5
        if not pygame.sprite.spritecollideany(player, tiles_group):
            player.rect.y += GRAVITY
        screen.fill((0, 0, 0))
        pl_inv = player.inventory, player.number_bloc, player.cur_frame_left, player.cur_frame_right
        player, tiles_group, all_sprites, player_group, coords_invent = my_map.generete_new_level()
        player.inventory, player.number_bloc, player.cur_frame_left, player.cur_frame_right = pl_inv
        player.make_inventary(1, coords_invent)
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
        if count_enemy[0] == 500 and count_enemy[1]:
            count_enemy[1] = 0
            enemy = Enemy()
            if enemy.normal:
                enemy = None
                enemy_group = pygame.sprite.Group()
                count_enemy = [0, 1]
            else:
                enemy.update()
        else:
            count_enemy[0] += 1
        if enemy:
            enemy.update()
            enemy.rect.y += 5
            if not pygame.sprite.spritecollideany(enemy, tiles_group):
                enemy.rect.y += GRAVITY
            enemy.rect.y -= 5
            enemy_group.draw(screen)
            if pygame.sprite.spritecollideany(enemy, player_group):
                if player.number_bloc == 0:
                    enemy = None
                    count_enemy = [0, 1]
                else:
                    xp -= 10
                    player.rect.x += 40
                    player.rect.y -= 5
                    if pygame.sprite.spritecollideany(player, tiles_group):
                        player.rect.x -= 80
                        if pygame.sprite.spritecollideany(player, tiles_group):
                            player.rect.x += 40
                    player.rect.y += 5
        day_time[0] += 1
        if day_time[0] % 1000 == 0:
            day_time[1] += 1
            pygame.mixer.music.load(music[day_time[1] % 2])
            pygame.mixer.music.play()
        screen.blit(day_image[day_time[1] % 2], (0, 0))
        xp_text = 'ХP:' + str(xp) + '%'
        font = pygame.font.Font(None, 30)
        text_coord = 50
        string_rendered = font.render(xp_text, 1, pygame.Color('White'))
        xp_text = string_rendered.get_rect()
        xp_text.top = text_coord
        xp_text.x = 925
        xp_text.y = 10
        screen.blit(string_rendered, xp_text)
        camera.update(player)
        for sprite in tiles_group:
            camera.apply(sprite)
        for sprite in player_group:
            camera.apply(sprite)
        for sprite in enemy_group:
            camera.apply(sprite)
        all_sprites.draw(screen)
        player_group.draw(screen)
        tiles_group.draw(screen)
        inventory_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        if xp == 0 or pygame.sprite.spritecollideany(player, walls_group):
            return


def game_over():
    """This function is responsible for the end of the game"""
    i = 0
    running = True
    color = pygame.Color('blue')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(color)
        screen.blit(game_over_image, (-1024 + i, 0))
        if i < 1024:
            i += 8
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

if mapp == 1:
    player, level_x, level_y = generate_level(load_level('map1.txt'))
elif mapp == 2:
    player, level_x, level_y = generate_level(load_level('map2.txt'))
elif mapp == 3:
    player, level_x, level_y = generate_level(load_level('map3.txt'))

play()
game_over()
