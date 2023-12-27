from random import randint, choice
import pygame
import json
from data.widgets.button import *
from data.widgets.switch import *
from data.widgets.label import *
from data.effects.petal import *
from data.effects.spark import *
from data.effects.particle import *
from data.documentation.guide.guide_en import *
from data.documentation.guide.guide_ru import *
import webbrowser


pygame.init()

with open("data/levels.json") as file_json:
    levels_json = json.load(file_json)

window = pygame.display.set_mode((700, 500))

clock = pygame.time.Clock()

FPS = 40


def customize_sizes(size1: tuple[int] | list[int], size2: tuple[int] | list[int]) -> tuple[int]:
    x1, y1 = size1
    x2, y2 = size2
    z = min([x1 / x2, y1 / y2])
    return (int(x2 * z), int(y2 * z))


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

        button_play = Button((230, 280, 240, 100),
                             {0: "Играть", 1: "Play"}[self.language],
                             is_bold=True, fsize=90, rounding=7, function=self.to_select_level)

        button_settings = Button((400, 20, 280, 80),
                                 {0: "Настройки", 1: "Settings"}[self.language],
                                 fsize=55, rounding=7, is_italic=True,
                                 function=self.to_settings)

        button_guide = Button((20, 20, 280, 80),
                              {0: "Гайд", 1: "Guide"}[self.language],
                              fsize=75, rounding=6, is_italic=True, function=self.guide)

        while True:
            self.all_sprites = pygame.sprite.Group()

            self.w.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    [button.check_click(e.pos)
                        for button in [button_play, button_settings, button_guide]]
            [button.draw(self.w)
                for button in [button_play, button_settings, button_guide]]

            pygame.display.update()
            clock.tick(FPS)

    def to_settings(self):
        self.all_sprites = pygame.sprite.Group()

        switch_mode = Switch((25, 25, 650, 150), [153] * 3,
                             {0: "Нормальный Режим", 1: "Normal Mode"}[self.language],
                             {0: "Сложный Режим", 1: "Hard Mode"}[self.language],
                             [
            [50, 50, 275, 100],
            [375, 50, 275, 100]
        ], rounding=30, option_color=(0, 255, 0), second_option_color=(255, 0, 0), fsize={0: 37, 1: 58}[self.language])

        switch_mode.selected = self.mode

        switch_lang = Switch((25, 200, 650, 150), [153] * 3, "Русский", "English", [
            [50, 225, 275, 100],
            [375, 225, 275, 100]
        ], rounding=30, option_color=(0, 255, 0), second_option_color=(255, 0, 0), fsize=75)

        switch_lang.selected = self.language

        button_menu = Button((25, 380, 650, 70),
                             {0: "В Меню", 1: "To Menu"}[self.language],
                             fsize=62, rounding=10, function=self.to_menu)

        while True:
            switch_mode.set_text({0: "Нормальный Режим", 1: "Normal Mode"}[self.language],
                                 {0: "Сложный Режим", 1: "Hard Mode"}[self.language])

            switch_mode.fsize = {0: 38, 1: 58}[self.language]

            button_menu.set_text({0: "В Меню", 1: "To Menu"}[self.language])

            self.w.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    switch_mode.check_click(e.pos)
                    switch_lang.check_click(e.pos)
                    button_menu.check_click(e.pos)

            self.language = switch_lang.get_selected()
            self.mode = switch_mode.get_selected()

            switch_mode.draw(self.w)
            switch_lang.draw(self.w)

            button_menu.draw(self.w)

            pygame.display.update()
            clock.tick(FPS)

    def guide(self):
        app = QApplication([])
        if self.language:
            guide = GuideEn()
        else:
            guide = GuideRu()
        guide.show()
        app.exec()

    def to_select_level(self):
        button_prev = Button([25, 380, 200, 60],
                             {0: "Предыдущий Уровень", 1: "Previous Level"}[self.language],
                             fsize={0: 23, 1: 31}[self.language],
                             function=self.minus_id_level,
                             rounding=12
                             )
        button_next = Button([475, 380, 200, 60],
                             {0: "Следующий Уровень", 1: "Next Level"}[self.language],
                             fsize={0: 26, 1: 41}[self.language],
                             function=self.plus_id_level,
                             rounding=12
                             )
        button_menu = Button([250, 375, 200, 70],
                             {0: "В Меню", 1: "To Menu"}[self.language],
                             fsize=60,
                             rounding=14,
                             function=self.to_menu)

        button_copy = Button([235, 315, 230, 40], {0: "Открыть URL", 1: "Open URL"}[self.language],
                             fsize={0: 38, 1: 40}[self.language],
                             function=self.open_level_url,
                             rounding=8)

        level_icon_path = levels_json[f"level{self.levelID + 1}"]["icon"]
        level_icon = pygame.image.load(level_icon_path)
        level_icon = pygame.transform.scale(level_icon,
                                            customize_sizes((600, 200), (level_icon.get_size())))

        label_name = Label((350, 280),
                           levels_json[f"level{self.levelID + 1}"]["data"]["name"][str(self.language)],
                           text_color=(255, 255, 255),
                           fsize={0: 40, 1: 30}[self.language])

        while True:
            self.w.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    [button.check_click(e.pos) for button in [button_prev, button_next, button_menu, button_copy]]
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        self.minus_id_level()
                    if e.key == pygame.K_RIGHT:
                        self.plus_id_level()

            [widget.draw(self.w) for widget in [button_prev, button_next, button_menu, label_name, button_copy]]

            self.w.blit(level_icon, (350 - level_icon.get_width() // 2, 105 - level_icon.get_height() // 2))

            pygame.display.update()
            clock.tick(FPS)

    def minus_id_level(self):
        self.levelID = max([0, min([self.levelID - 1, len(levels_json) - 1])])
        self.to_select_level()

    def plus_id_level(self):
        self.levelID = max([0, min([self.levelID + 1, len(levels_json) - 1])])
        self.to_select_level()

    def open_level_url(self):
        webbrowser.open(levels_json[f"level{self.levelID + 1}"]["data"]["link"])


MainGame(window)
