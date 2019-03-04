import pygame
import os
import main_win
from loading_image import load_image
import json
from inventory import *
from inventory_objects import *
from requests import get, Response
import json

screen = None
size = w, h, = 720, 480
pygame.init()
font = pygame.font.Font('11939.ttf', 50)

data = open('../settings/game.json', mode='r').read()
data = json.loads(data)

def load():
    data = open('../settings/game.json', mode='r').read()
    data = json.loads(data)
    return data

inv = Invent(8,5)
inv.cell_size=40
inv.top = 10

items = {
    'Usual_Sword': UsualSword,
    'Secret_Sword': SecretSword
}

def load_settings():
    player_settings = open('../settings/Player.json').read()
    data = json.loads(player_settings)
    # print(data)
    return data

class Menu:
    def __init__(self):
        global screen, data
        data = load()
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self.buttons = Buttons()
        self.mouse = pygame.Rect(*pygame.mouse.get_pos(), 1, 1)
        self.levels = LevelsRender()
        self.settings = Settings()
        self.settings.mountains_val = data['settings']['mountains']
        self.player = PlayerSettings()
        self.all_sprites= pygame.sprite.Group()
        self.search = Search()
        settings = load_settings()
        self.inv_data = [[Hand((0, 0), True), Hand((0, 2), False),
                          Hand((0, 2), False),
                          Hand((0, 3), False), Hand((0, 4), False)],
                         [Hand((1, 0), False), Hand((1, 1), False),
                          Hand((1, 2), False),
                          Hand((1, 3), False), Hand((1, 4), False)],
                         [Hand((2, 0), False), Hand((2, 1), False),
                          Hand((2, 2), False),
                          Hand((2, 3), False), Hand((2, 4), False)],
                         [Hand((3, 0), False), Hand((3, 1), False),
                          Hand((3, 2), False),
                          Hand((3, 3), False), Hand((3, 4), False)],
                         [Hand((4, 0), False), Hand((4, 1), False),
                          Hand((4, 2), False),
                          Hand((4, 3), False), Hand((4, 4), False)],
                         [Hand((5, 0), False), Hand((5, 1), False),
                          Hand((5, 2), False),
                          Hand((5, 3), False), Hand((5, 4), False)],
                         [Hand((6, 0), False), Hand((6, 1), False),
                          Hand((6, 2), False),
                          Hand((6, 3), False), Hand((6, 4), False)],
                         [Hand((7, 0), False), Hand((7, 1), False),
                          Hand((7, 2), False),
                          Hand((7, 3), False), Hand((7, 4), False)]]
        for i in range(40):
            y = i // 8
            x = i % 8
            if settings['inventory'][str(i)]["type"] == 'Hand':
                self.inv_data[x][y] = Hand((x,y), True)
            else:
                print(self.inv_data)
                print(settings['inventory'][str(i)]['type'])
                print()
                print(settings['inventory'][str(i)])
                self.inv_data[x][y] = items[settings['inventory'][str(i)]['type']]((x,y),False,screen, size=(36,36))
                self.inv_data[x][y].power = settings['inventory'][str(i)]['power']
                self.inv_data[x][y].upgrade_cost = settings['inventory'][str(i)]['upgrade_cost']
                self.inv_data[x][y].level = settings['inventory'][str(i)]['level']

        self.screen_update()

    def screen_update(self):
        global data
        self.event = True
        level = None

        while self.event:
            if level is not None:
                self.event = False
                run = main_win.Window(int(level), self.settings.mountains_val)
            screen.fill((0, 0, 0))
            self.mouse = pygame.Rect(*pygame.mouse.get_pos(), 1, 1)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.event = False
                    quit(0)

                if e.type == pygame.MOUSEBUTTONDOWN:
                    level = self.levels.get_lvl(pygame.mouse.get_pos())
                    if self.buttons.show:
                        if self.buttons.levels.colliderect(
                            self.mouse):
                            self.buttons.show = False
                            self.levels.show = True

                        if self.buttons.player_set.colliderect(self.mouse):
                            self.player.show = True
                            self.buttons.show = False

                        if self.buttons.settings.rect.colliderect(self.mouse):
                            self.settings.show = True
                            self.buttons.show = False

                    elif self.player.show:
                        if self.player.back.rect.colliderect(self.mouse):
                            self.player.show = False
                            self.buttons.show = True

                        inv.get_cell(pygame.mouse.get_pos(), screen)

                    elif self.search.show:
                        if self.search.back.rect.colliderect(self.mouse):
                            self.search.show = False
                            self.buttons.show = True

                    elif self.buttons.settings.rect.colliderect(self.mouse) and self.settings.show is False and self.levels.show is False and self.player.show is False:
                        self.settings.show = True
                        self.buttons.show = False

                    elif self.settings.show and self.buttons.show is False and self.levels.show is False and self.player.show is False:
                        if self.settings.back.rect.colliderect(self.mouse):
                            self.settings.show = False
                            self.buttons.show = True

                    elif self.levels.back.rect.colliderect(self.mouse) and self.levels.show and self.buttons.show is False:
                        self.levels.show = False
                        self.buttons.show = True

                    if self.settings.show:
                        if self.settings.mountains_rect.colliderect(self.mouse):
                            self.settings.mountains_val += 1
                            data['settings']['mountains'] = self.settings.mountains_val

                        self.save_settings()

                    elif self.buttons.search.rect.colliderect(self.mouse):
                        self.buttons.show = False
                        self.search.show = True

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        self.search.text = self.search.text[:-1]

                    elif e.key == pygame.K_RETURN:
                        response = get('http://127.0.0.1:8000/current_lvl='+self.search.text+'/get')
                        if response.ok:
                            loaded_level = response.text
                            file = open('../LEVELS/lvl_'+str(self.search.text)+'.txt', mode='w')
                            file.write(loaded_level)
                            file.close()
                        
                    elif self.search.show:
                        self.search.update(e.unicode)

            if self.player.show:
                for i in range(len(self.inv_data)):
                    for j in range(len(self.inv_data[i])):
                        inv_obj = self.inv_data[i][j]
                        if inv_obj.get_type() != 'Hand':
                            inv_obj.draw((inv_obj.place[0] * inv.cell_size + inv.left,
                                          inv_obj.place[1] * inv.cell_size + inv.top), screen)
                        if inv_obj.get_type() != 'Hand' and not self.all_sprites.has(
                                inv_obj.sprite):
                            self.all_sprites.add(inv_obj.sprite)

            else:
                self.all_sprites.empty()

            self.search.draw()
            self.search.online_levels_draw()
            self.buttons.draw()
            self.levels.draw()
            self.settings.draw()
            self.player.draw()
            self.all_sprites.draw(screen)


            pygame.display.flip()

    def save_settings(self):
        save = open('../settings/game.json', mode='w')
        json.dump(data, save)

class Buttons:
    def __init__(self):
        self.show = True
        self.w, self.h = 210, 75
        self.x, self.y = 360 - self.w//2, 240 - self.h//2-self.h
        self.levels = pygame.Rect(self.x, self.y, self.w, self.h)

        self.settings = pygame.sprite.Sprite()
        self.group = pygame.sprite.Group()
        self.settings.image = load_image('settings.png')
        self.settings.image = pygame.transform.scale(self.settings.image, (64,64))
        self.settings.rect = self.settings.image.get_rect()
        self.settings.left, self.settings.top = 0,0

        self.search = pygame.sprite.Sprite()
        self.search.image = load_image('search.png')
        self.search.image = pygame.transform.scale(self.search.image, (64, 64))
        self.search.rect = pygame.Rect(656,0,64,64)

        self.group.add(self.settings)
        self.group.add(self.search)

        self.player_set = pygame.Rect(self.x, self.y+150,self.w,self.h)

    def draw(self):
        if self.show:
            self.levels = pygame.draw.rect(screen, (255, 255, 255),
                                           (self.x, self.y, self.w, self.h), 5)

            self.player_set = pygame.draw.rect(screen, (255,255,255), (self.x, self.y+150, self.w,self.h),5)
            levels = font.render('Levels', 1, (255, 255, 255), 5)
            levels_x = (w / 2) - levels.get_width()//2
            levels_y = self.y
            screen.blit(levels, (levels_x, levels_y))

            player_text = font.render('Player', 1, (255,255,255),5)
            player_x = (w / 2) - player_text.get_width()//2
            player_y = self.y+150
            screen.blit(player_text, (player_x, player_y))
            self.group.draw(screen)


class LevelsRender:
    def __init__(self):
        self.show = False
        self.lvls = os.listdir('../LEVELS')
        self.size = 75
        self.left, self.top = 67, 40
        self.max = 7

        self.back = pygame.sprite.Sprite()
        self.back.image = load_image('cancel.jpg')
        self.back.image = pygame.transform.scale(self.back.image, (64,64))
        self.back.rect = self.back.image.get_rect()
        self.back.rect.left, self.back.rect.top = 0, 0
        self.group = pygame.sprite.Group()
        self.group.add(self.back)

        self.lvls_grid = []
        for lvl in range(len(self.lvls)):
            if 'lvl' and '.txt' in self.lvls[lvl]:
                if lvl % self.max == 0:
                    self.lvls_grid.append([])

                self.lvls_grid[lvl // self.max].append(self.lvls[lvl])
        print(self.lvls_grid)


    def draw(self):
        if self.show == True:
            for i in range(len(self.lvls_grid)):
                for j in range(len(self.lvls_grid[i])):
                    pygame.draw.rect(screen, (255, 255, 255), (
                        j * (self.size + 10) + self.left, i * (self.size + 10) + self.top,
                        self.size,
                        self.size), 0)
                    pygame.draw.rect(screen, (0, 0, 0), (
                        j * (self.size + 10) + 3 + self.left, i * (self.size + 10) + 3 + self.top,
                        self.size - 6, self.size - 6), 0)
                    level = font.render(self.lvls_grid[i][j].split('.')[0].split('_')[-1], 1, (255, 255, 255))
                    level_x = j * (
                            self.size + 10) + self.left + self.size // 2 - level.get_width() // 2
                    level_y = i * (self.size + 10) + self.top
                    screen.blit(level, (level_x, level_y))

            self.group.draw(screen)

    def get_lvl(self, pos):
        if self.show:
            for i in range(len(self.lvls_grid)):
                for j in range(len(self.lvls_grid[i])):
                    if j * (self.size + 10) + self.left < pos[0] < j * (
                            self.size + 10) + self.left + self.size and i * (
                            self.size + 10) + self.top < pos[1] < i * (
                            self.size + 10) + self.top + self.size:
                        return self.lvls_grid[i][j].split('.')[0].split('_')[-1]
        return None

class Settings:
    def __init__(self):
        self.show = False
        self.back = pygame.sprite.Sprite()
        self.back.image = load_image('cancel.jpg')
        self.back.image = pygame.transform.scale(self.back.image, (64,64))
        self.back.rect = self.back.image.get_rect()
        self.back.rect.left, self.back.rect.top = 0,0
        self.group = pygame.sprite.Group()
        self.group.add(self.back)

        self.mountains = font.render('TEXT', 1, (255, 255, 255))
        self.mx = 240
        self.my = 0
        screen.blit(self.mountains, (self.mx, self.my))

        self.mountains_rect = pygame.Rect(350,70,96,48)
        self.mountains_swithcer = pygame.Rect(350,70,48,48)
        self.mountains_val = 1



    def draw(self):
        self.mountains_val = self.mountains_val%2
        if self.show:
            self.back.rect = self.back.image.get_rect()
            self.back.rect.left, self.back.rect.top = 0, 0
            self.group.draw(screen)

            self.mountains = font.render('Mountains', 5, (255, 255, 255))
            self.mx = 200
            self.my = 60
            screen.blit(self.mountains, (self.mx-self.mountains.get_width()/2, self.my))

            self.mountains_rect = pygame.draw.rect(screen,(255,255,255), (350,75,96,48), 1)
            self.mountains_swithcer = pygame.draw.rect(screen,(255,255,255), (350+48*(self.mountains_val),75,48,48), 0)

        else:
            self.back.rect = pygame.Rect(0,0,0,0)


class PlayerSettings:
    def __init__(self):
        self.show = False

        self.back = pygame.sprite.Sprite()
        self.back.image = load_image('cancel.jpg')
        self.back.image = pygame.transform.scale(self.back.image, (64,64))
        self.back.rect = self.back.image.get_rect()
        self.back.rect.left, self.back.rect.top = 0,0
        self.group = pygame.sprite.Group()
        self.group.add(self.back)

        self.player_sprite = pygame.sprite.Sprite()
        self.player_sprite.image = load_image('../textures/entities/Player/Player_1.png')
        self.player_sprite.image = pygame.transform.scale(self.player_sprite.image, (128,256))
        self.player_sprite.rect = self.player_sprite.image.get_rect()
        self.player_sprite.rect.top = 150
        self.player_sprite.rect.left = 10

        self.group.add(self.player_sprite)

    def draw(self):
        if self.show:
            self.group.draw(screen)
            inv.render(screen)

class Search:
    def __init__(self):
        self.show = False
        self.back = pygame.sprite.Sprite()
        self.back.image = load_image('cancel.jpg')
        self.back.image = pygame.transform.scale(self.back.image, (64, 64))
        self.back.rect = self.back.image.get_rect()
        self.back.rect.left, self.back.rect.top = 0, 0
        self.text = ''
        self.max = 8

        self.left=40
        self.top=120
        self.size=50

        self.group = pygame.sprite.Group()
        self.group.add(self.back)

        levels = get('http://127.0.0.1:8000/get_list_of_levels').text

        print(levels.split('\n'))
        self.lvls_grid = []
        for lvl in range(len(levels)):
            if 'lvl' and '.txt' in levels[lvl]:
                if lvl % self.max == 0:
                    self.lvls_grid.append([])

                self.lvls_grid[lvl // self.max].append(levels[lvl])

        

    def draw(self):
        if self.show:
            self.group.draw(screen)

            self.text_draw = font.render(self.text, 1, (255, 255, 255))
            self.tx = 125
            self.ty = 78
            screen.blit(self.text_draw, (self.tx, self.ty))

            pygame.draw.rect(screen, (255, 255, 255),
                             (120, 80, max(320, self.text_draw.get_width()+10), 65), 2)

    def update(self, key):
        self.text += key
        print(self.text)

    def online_levels_draw(self):
        if self.show:
            print(1221)
            for i in range(len(self.lvls_grid)):
                for j in range(len(self.lvls_grid[i])):
                    pygame.draw.rect(screen, (255, 255, 255), (
                        j * (self.size + 10) + self.left, i * (self.size + 10) + self.top,
                        self.size,
                        self.size), 0)
                    pygame.draw.rect(screen, (0, 0, 0), (
                        j * (self.size + 10) + 3 + self.left, i * (self.size + 10) + 3 + self.top,
                        self.size - 6, self.size - 6), 0)
                    level = font.render(self.lvls_grid[i][j].split('.')[0].split('_')[-1], 1, (255, 255, 255))
                    level_x = j * (
                            self.size + 10) + self.left + self.size // 2 - level.get_width() // 2
                    level_y = i * (self.size + 10) + self.top
                    screen.blit(level, (level_x, level_y))



if __name__ == '__main__':
    win = Menu()
    pygame.quit()
