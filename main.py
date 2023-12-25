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
                                 back_color=[153] * 3)

        button_guide = Button((20, 20, 280, 80), "Гайд", fsize=75, roading=6, is_italic=True,
                              back_color=[153] * 3)

        while True:
            self.w.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    pass

            [Spark(self.all_sprites, (350, 1000), (700, 500)) for _ in range(3)]

            self.all_sprites.draw(self.w)
            self.all_sprites.update()

            button_play.draw(self.w)
            button_settings.draw(self.w)
            button_guide.draw(self.w)

            pygame.display.update()
            clock.tick(FPS)

MainGame(window)
