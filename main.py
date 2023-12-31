from random import randint, choice, choices
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

        self.x, self.y = -1, -1

        self.levelID = 0
        self.mode = 0
        self.language = 0

        self.rect_alpha = 0

        self.music = 1

        self.music_is_already_played = 0

        self.all_sprites = pygame.sprite.Group()

        self.to_menu()

    def to_menu(self):
        if not self.music_is_already_played:
            pygame.mixer.music.load("data/sounds/back_music.mp3")
            pygame.mixer.music.play(-1)

            self.music_is_already_played = 1

        button_play = Button((230, 280, 240, 100),
                             {0: "Играть", 1: "Play"}[self.language],
                             is_bold=True, is_italic=True, fsize=90, rounding=7, function=self.to_select_level)

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
                if e.type == pygame.MOUSEMOTION:
                    self.x, self.y = e.pos

            [button.check_on((self.x, self.y)) for button in [button_play, button_settings, button_guide]]

            [button.draw(self.w)
                for button in [button_play, button_settings, button_guide]]

            pygame.display.update()
            clock.tick(FPS)

    def to_settings(self):
        if not self.music_is_already_played:
            pygame.mixer.music.load("data/sounds/back_music.mp3")
            pygame.mixer.music.play(-1)

            self.music_is_already_played = 1

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
                if e.type == pygame.MOUSEMOTION:
                    self.x, self.y = e.pos

            button_menu.check_on((self.x, self.y))


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
        if not self.music_is_already_played:
            pygame.mixer.music.load("data/sounds/back_music.mp3")
            pygame.mixer.music.play(-1)

            self.music_is_already_played = 1

        button_prev = Button([25, 380, 310, 90],
                             {0: "Предыдущий Уровень", 1: "Previous Level"}[self.language],
                             fsize={0: 33, 1: 49}[self.language],
                             function=self.minus_id_level,
                             rounding=17,
                             is_italic=True
                             )
        button_next = Button([365, 380, 310, 90],
                             {0: "Следующий Уровень", 1: "Next Level"}[self.language],
                             fsize={0: 36, 1: 57}[self.language],
                             function=self.plus_id_level,
                             rounding=17,
                             is_italic=True
                             )
        button_menu = Button([25, 255, 220, 95],
                             {0: "В Меню", 1: "To Menu"}[self.language],
                             fsize=67,
                             rounding=16,
                             function=self.to_menu,
                             is_italic=True)

        button_open = Button([270, 265, 405, 75], {0: "Открыть URL в Браузере", 1: "Open URL in Browser"}[self.language],
                             fsize={0: 40, 1: 45}[self.language],
                             function=self.open_level_url,
                             rounding=8,
                             is_italic=True)

        button_play = Button([350, 160, 310, 46],
                             {0: "Играть", 1: "Play"}[self.language],
                             fsize={0: 40, 1: 44}[self.language],
                             rounding=9,
                             is_italic=True,
                             function=self.play)



        image_star = pygame.transform.scale(pygame.image.load("data/images/star.png"), (40, 40))

        image_level_path = levels_json[f"level{self.levelID + 1}"]["icon"]
        image_level = pygame.image.load(image_level_path)
        image_level = pygame.transform.scale(image_level,
                                            customize_sizes((300, 200), (image_level.get_size())))

        label_name = Label((505, 40),
                           levels_json[f"level{self.levelID + 1}"]["data"]["name"][str(self.language)],
                           text_color=(255, 255, 255),
                           fsize={0: 50, 1: 41}[self.language])

        label_duration = Label((505, 90),
                {0: f"Продолжительность: {levels_json['level' + str(self.levelID + 1)]['data']['duration']} сек.",
                 1: f"Duration: {levels_json['level' + str(self.levelID + 1)]['data']['duration']} sec."}[self.language],
                               (255, 255, 255),
                               fsize=31)

        complexity = levels_json[f"level{self.levelID + 1}"]["complexity"]

        while True:
            self.w.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    [button.check_click(e.pos) for button in [button_prev, button_next, button_menu, button_open,
                                                              button_play]]
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        self.minus_id_level()
                    if e.key == pygame.K_RIGHT:
                        self.plus_id_level()
                if e.type == pygame.MOUSEMOTION:
                    self.x, self.y = e.pos

            [button.check_on((self.x, self.y)) for button in [button_play, button_open, button_menu, button_next,
                                                              button_prev]]

            [widget.draw(self.w) for widget in [button_prev, button_next, button_menu, button_open, button_play,
                                                label_name, label_duration]]

            self.w.blit(image_level, (155 - image_level.get_width() // 2, 110 - image_level.get_height() // 2))

            x1 = 490 - (35 * (complexity - 1))

            for _ in range(complexity):
                self.w.blit(image_star, (x1, 105))
                x1 += 65

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

    def play(self):
        self.music_is_already_played = 0

        level = levels_json[f"level{self.levelID + 1}"]
        in_menu = False

        music = level["music"]
        icon = level["icon"]
        back_image = level["background_image"]
        back_color = level["background_color"]

        rects = level["figures"]["rects"]
        ellipses = level["figures"]["ellipses"]

        iters_of_game = 0

        comp = level["complexity"]

        spawns = level["spawn_notes"]

        if self.mode:
            spawns = 0


        button_pause = Button((655, 15, 30, 30), "", None, image="data/images/pause.png",
                              function=self.fill_alpha)

        button_quit_menu = Button((250, 300, 200, 60), {0: "Продолжить", 1: "Continue"}[self.language],
                                  is_italic=True, fsize={0: 40, 1: 50}[self.language], rounding=12)

        button_play_again = Button((255, 200, 190, 60), {0: "Заново", 1: "Play Again"}[self.language],
                                   is_italic=True, fsize=50, rounding=12, function=self.play)

        button_quit_level = Button((260, 100, 180, 60), {0: "Выйти", 1: "Exit"}[self.language],
                                   is_italic=True, fsize=60, rounding=12, function=self.to_select_level)



        on_menu = False

        pygame.mixer.music.load(level["music"])
        pygame.mixer.music.play(1)

        while True:
            self.w.fill(back_color)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if button_pause.collide_point(e.pos):
                        on_menu = True


                    if on_menu:
                        button_quit_level.check_click(e.pos)

                        if button_quit_menu.collide_point(e.pos):
                            on_menu = False
                    else:
                        pass

            self.w.blit(
                pygame.transform.scale(pygame.image.load(back_image), (700, 500))
                (0, 0)) if back_image else 0

            button_pause.draw(self.w)

            if on_menu:
                self.fill_alpha()
                pygame.mixer.music.pause()
                [button.draw(self.w) for button in [button_quit_level, button_quit_menu, button_play_again]]
            else:
                iters_of_game += 1



                pygame.mixer.music.unpause()
            pygame.display.update()
            clock.tick(FPS)

    def fill(self, color: tuple[int, int, int] | list[int, int, int], alpha: int = 255):
        s = pygame.Surface((700, 500))
        s.fill(color)
        s.set_alpha(alpha)

        self.w.blit(s, (0, 0))

    def fill_alpha(self, color: tuple[int, int, int] = (0, 0, 0)):
        self.fill(color, 128)




MainGame(window)
