from random import randint, choice
import pygame
import json
from data.widgets.button import *
from data.widgets.switch import *
from data.widgets.label import *
from data.effects.petal import *
from data.effects.spark import *
from data.effects.particle import *


pygame.init()

with open("data/levels.json") as file_json:
    levels_json = json.load(file_json)

window = pygame.display.set_mode((700, 500))


clock = pygame.time.Clock()

FPS = 40


class MainGame:
    def __init__(self, window: pygame.surface.Surface):
        self.w = window

        self.levelID = 0
        self.mode = 0
        self.language = 0

        self.rect_alpha = 0

        self.all_sprites = pygame.sprite.Group()

        self.to_menu()

    def to_menu(self):

        button_play = Button((230, 280, 240, 100), "Играть", is_bold=True, fsize=90, roading=7,
                             back_color=[153] * 3)

        button_settings = Button((400, 20, 280, 80), "Настройки", fsize=55, roading=7, is_italic=True,
                                 function=self.to_settings)

        button_guide = Button((20, 20, 280, 80), "Гайд", fsize=75, roading=6, is_italic=True,
                              back_color=[153] * 3)

        while True:
            self.all_sprites = pygame.sprite.Group()

            self.w.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    button_settings.check_click(e.pos)

            [Spark(self.all_sprites, (350, 1000), (700, 500)) for _ in range(3)]

            self.all_sprites.draw(self.w)
            self.all_sprites.update()

            button_play.draw(self.w)
            button_settings.draw(self.w)
            button_guide.draw(self.w)

            pygame.display.update()
            clock.tick(FPS)

    def to_settings(self):
        self.all_sprites = pygame.sprite.Group()

        mode_switch = Switch((25, 25, 650, 150), [153] * 3,
                             {0: "Нормальный Режим", 1: "Normal Mode"}[self.language],
                             {0: "Сложный Режим", 1: "Hard Mode"}[self.language],
                             [
            [50, 50, 275, 100],
            [375, 50, 275, 100]
        ], rounding=30, option_color=(0, 255, 0), second_option_color=(255, 0, 0), fsize={0: 35, 1 :55}[self.language])

        lang_switch = Switch((25, 225, 650, 150), [153] * 3, "Русский", "English", [
            [50, 250, 275, 100],
            [375, 250, 275, 100]
        ], rounding=30, option_color=(0, 255, 0), second_option_color=(255, 0, 0), fsize=75)

        while True:
            mode_switch = Switch((25, 25, 650, 150), [153] * 3,
                                 {0: "Нормальный Режим", 1: "Normal Mode"}[self.language],
                                 {0: "Сложный Режим", 1: "Hard Mode"}[self.language],
                                 [
                                     [50, 50, 275, 100],
                                     [375, 50, 275, 100]
                                 ], rounding=30, option_color=(0, 255, 0), second_option_color=(255, 0, 0),
                                 fsize={0: 35, 1: 55}[self.language])

            self.w.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mode_switch.check_click(e.pos)
                    lang_switch.check_click(e.pos)

            self.language = lang_switch.get_selected()

            self.all_sprites.draw(self.w)
            self.all_sprites.update()

            mode_switch.draw(self.w)
            lang_switch.draw(self.w)

            pygame.display.update()
            clock.tick(FPS)

MainGame(window)
