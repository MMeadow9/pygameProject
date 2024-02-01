from random import randint, choice, choices
import pygame
import json

from data.widgets.button import *
from data.widgets.switch import *
from data.widgets.label import *
from data.widgets.big_switch import *

from data.effects.petal import *
from data.effects.spark import *
from data.effects.particle import *

from data.documentation.guide.guide_en import *
from data.documentation.guide.guide_ru import *

from data.game_rect import *

import webbrowser


pygame.init()

with open("data/levels.json") as file_json:
    levels_json = json.load(file_json)

window = pygame.display.set_mode((700, 500))

clock = pygame.time.Clock()

FPS = 40


def customize_sizes(size1: tuple[int] | list[int], size2: tuple[int] | list[int]) -> tuple[int, int]:
    x1, y1 = size1
    x2, y2 = size2
    z = min([x1 / x2, y1 / y2])
    return (int(x2 * z), int(y2 * z))


def get_obj(obj: str | int | None) -> str | int | None:
    result = None  # coordination

    if type(obj) == str:  # Если это строка
        if obj.startswith("choice"):  # Если она начинается с choice
            result = choice(obj.split()[1:])  # Получаем случайный объект из строки
        elif obj.startswith("randint"):  # Если она начинается с randint
            result = randint(int(obj.split()[1]),
                        int(obj.split()[2]))  # Получаем случайное число между 1-ым и 2-ым элементами
        else:  # Если не начинается с choice или randint
            result = obj  # Значит нам нужна вся строка
    else:
        result = obj  # Если это не строка (значит число), то просто сохраняем это в переменную

    return result  # Возвращаем объект



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

        self.volume = 0

        self.to_menu()

    def to_menu(self):
        if not self.music_is_already_played:
            pygame.mixer.music.load("data/sounds/back_music.mp3")
            pygame.mixer.music.play(-1)

            pygame.mixer.music.set_volume(self.volume * 0.2)

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

            self.set_cursor(any([button.collide_point((self.x, self.y)) for button in [
                button_play, button_settings, button_guide
            ]]))

            pygame.display.update()
            clock.tick(FPS)

    def to_settings(self):
        if not self.music_is_already_played:
            pygame.mixer.music.load("data/sounds/back_music.mp3")
            pygame.mixer.music.play(-1)

            self.music_is_already_played = 1

        self.all_sprites = pygame.sprite.Group()

        switch_volume = BigSwitch(
            (25, 30, 650, 100), [153] * 3,
            [{0: "Выкл.", 1: "OFF"}[self.language]] + list("12345"),
            [
                [35, 40, 140, 80], [175 + 28, 60, 70, 60], [245 + 28 * 2, 60, 70, 60], [315 + 28 * 3, 60, 70, 60],
                [385 + 28 * 4, 40, 70, 80], [455 + 28 * 5, 40, 70, 80]
            ],
            [
                (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128)
            ],
            rounding=25,
            fsize=48
        )
        switch_volume.selected = self.volume

        switch_mode = Switch((25, 155, 650, 100), [153] * 3,
                             {0: "Нормальный Режим", 1: "Normal Mode"}[self.language],
                             {0: "Сложный Режим", 1: "Hard Mode"}[self.language],
                             [
                                 [50, 165, 275, 80],
                                 [375, 165, 275, 80]
                             ], rounding=30, option_color=(0, 255, 0), second_option_color=(255, 0, 0),
                             fsize={0: 37, 1: 58}[self.language])

        switch_mode.selected = self.mode

        switch_lang = Switch((25, 280, 650, 100), [153] * 3, "Русский", "English", [
            [50, 290, 275, 80],
            [375, 290, 275, 80]
        ], rounding=30, option_color=(0, 255, 0), second_option_color=(255, 0, 0), fsize=75)

        switch_lang.selected = self.language

        button_menu = Button((25, 405, 650, 70),
                             {0: "В Меню", 1: "To Menu"}[self.language],
                             fsize=62, rounding=10, function=self.to_menu)

        label_volume = Label((336, 25), {0: "Громкость", 1: "Volume"}[self.language], text_color=(255, 255, 255),
                             fsize=40)

        while True:
            pygame.mixer.music.set_volume(self.volume * 0.2)

            self.volume = int(switch_volume.get_selected())

            switch_mode.set_text({0: "Нормальный Режим", 1: "Normal Mode"}[self.language],
                                 {0: "Сложный Режим", 1: "Hard Mode"}[self.language])

            switch_mode.fsize = {0: 38, 1: 58}[self.language]

            button_menu.set_text({0: "В Меню", 1: "To Menu"}[self.language])

            switch_volume.texts[0] = {0: "Выкл.", 1: "OFF"}[self.language]
            switch_volume.fsize = {0: 48, 1: 56}[self.language]

            label_volume.text = {0: "Громкость", 1: "Volume"}[self.language]
            label_volume.fsize = {0: 40, 1: 44}[self.language]

            self.w.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    switch_mode.check_click(e.pos)
                    switch_lang.check_click(e.pos)
                    button_menu.check_click(e.pos)
                    switch_volume.check_click(e.pos)
                if e.type == pygame.MOUSEMOTION:
                    self.x, self.y = e.pos

            button_menu.check_on((self.x, self.y))

            self.language = switch_lang.get_selected()
            self.mode = switch_mode.get_selected()

            switch_volume.draw(self.w)
            switch_mode.draw(self.w)
            switch_lang.draw(self.w)

            button_menu.draw(self.w)

            pygame.draw.rect(self.w, (0, 0, 0), (175 + 28, 0, 266, 50), border_radius=20)

            label_volume.draw(self.w)

            self.set_cursor(max([0] + [obj.id for obj in [
                button_menu, switch_volume, switch_mode, switch_lang, label_volume
            ] if obj.collide_point((self.x, self.y))]))

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

            self.set_cursor(max([0] + [obj.id for obj in [
                button_menu, button_open, button_play, button_next, button_prev, label_duration, label_name
            ] if obj.collide_point((self.x, self.y))]))

            pygame.display.update()
            clock.tick(FPS)

    def minus_id_level(self):
        self.levelID = (self.levelID - 1) % len(levels_json)
        self.to_select_level()

    def plus_id_level(self):
        self.levelID = (self.levelID + 1) % len(levels_json)
        self.to_select_level()

    def open_level_url(self):
        webbrowser.open(levels_json[f"level{self.levelID + 1}"]["data"]["link"])

    def play(self):
        self.all_sprites = pygame.sprite.Group()

        self.music_is_already_played = 0

        level = levels_json[f"level{self.levelID + 1}"]

        level_data = level["data"]
        level_name = level_data["name"][str(self.language)]

        music = level["music"]
        icon = level["icon"]
        back_image = level["background_image"]
        back_color = level["background_color"]

        rects = level["figures"]["rects"]
        ellipses = level["figures"]["ellipses"]

        iters_of_game = 0

        comp = level["complexity"]

        spawns = level["spawn_notes"]

        is_light = level["is_light"]

        spawns_rects = []

        dct_lines = {1: 3, 2: 4, 3: 6, 4: 8, 5: 10}

        game_lines = dct_lines[comp]

        size = 650 / game_lines

        pressed_letters = []


        def draw_stat():
            table = pygame.surface.Surface((50, 500))
            table.fill([(not is_light) * 255] * 3)

            statistic = pygame.surface.Surface((40, 440))
            statistic.fill((0, 255, 0))

            try:
                bad_line = int(490 * (good_res / all_res))
            except ZeroDivisionError:
                bad_line = 0

            table.blit(statistic, (5, 5))

            pygame.draw.rect(statistic, (255, 0, 0), (0, 0, 40, bad_line))

            self.w.blit(table, (650, 50))

        if self.mode:
            for spawn in spawns:
                spawns_rects.append(["QWERTYUIOP"[randint(0, game_lines - 1)], int(spawn) + 30])
        else:
            spawns_rects = [[values, int(key) + 30] for key, values in spawns.items()]  # 1.5 sec

        spawns_rects = sorted(spawns_rects, key=lambda x: x[1])

        button_pause = Button((660, 10, 30, 30), "", None, image="data/images/pause.png",
                              function=self.fill_alpha)

        button_quit_menu = Button((8, 30, 200, 66), {0: "Продолжить", 1: "Continue"}[self.language],
                                  is_italic=True, fsize={0: 40, 1: 50}[self.language], rounding=15)

        button_play_again = Button((229, 30, 190, 66), {0: "Заново", 1: "Play Again"}[self.language],
                                   is_italic=True, fsize=50, rounding=15, function=self.play)

        button_quit_level = Button((450, 30, 180, 66), {0: "Выйти", 1: "Exit"}[self.language],
                                   is_italic=True, fsize=60, rounding=15, function=self.to_select_level)

        switch_volume = BigSwitch(
            (47.5, 180, 260, 290),
            [153 - 26 * is_light] * 3,
            [{0: "Выкл.", 1: "OFF"}[self.language]] + list("12345"),
            [
                [60, 200, 105, 70], [190, 200, 105, 70], [60, 290, 105, 70], [190, 290, 105, 70],
                [60, 380, 105, 70], [190, 380, 105, 70]
            ],
            [
                (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128)
            ],
            fsize={0: 40, 1: 50}[self.language],
            rounding=20
        )

        switch_volume.selected = self.volume

        label_volume = Label(
            (180, 150),
            {0: "Громкость", 1: "Volume"}[self.language],
            [255 - 255 * is_light] * 3, fsize=50
        )

        label_name = Label(
            (475, 350),
            level_name,
            [255 - 255 * is_light] * 3, fsize=40
        )

        image_level = pygame.image.load(icon)
        image_level = pygame.transform.scale(image_level,
                                             customize_sizes((300, 200), (image_level.get_size())))

        image_star = pygame.transform.scale(pygame.image.load("data/images/star.png"), (40, 40))

        on_menu = False

        wait = level["wait"]

        effects = level["effects"]

        particles = effects["particle"]
        petals = effects["petal"]
        sparks = effects["spark"]

        complexity = level["complexity"]

        pygame.mixer.music.load(music)
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(self.volume * 0.2)

        letters_colors = level["letter_colors"]

        game_rects_colors = level["game_rects_colors"]

        good_res, all_res = 0, 0

        ewait = float(effects["wait"]) * 40  # effect wait

        game_rects = []

        lines = [
            [(x + 1) * (650 / game_lines), 0, 1,
             500] for x in range(game_lines)
        ] + [[650, 0, 2, 500]]

        time = 0

        letters = [
            Label([x * size + size / 2, 463], "QWERTYUIOP"[x], fsize=60,
                  text_color=([255] * 3 if is_light else [0] * 3))
            for x in range(game_lines)
        ]

        letters_rects = [
            [letters_colors[x % len(letters_colors)] if letters_colors else
                ([204] * 3 if not is_light else [41] * 3),
             [round(x * size), 425, round(size), 75]]
            for x in range(game_lines)
        ]

        """
        
        spawns_rects    →   list[*list[str, int]]   →   Список с данными для игровых прямоугольников
        
        """

        while True:

            pressed_letters.clear()

            self.w.fill(back_color)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:

                    if button_pause.collide_point(e.pos):
                        on_menu = bool(on_menu - 1)

                    if on_menu:
                        button_quit_level.check_click(e.pos)

                        button_play_again.check_click(e.pos)

                        switch_volume.check_click(e.pos)

                        if button_quit_menu.collide_point(e.pos):
                            on_menu = False

                if e.type == pygame.MOUSEMOTION:
                    self.x, self.y = e.pos

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        pressed_letters.append("Q")
                    if e.key == pygame.K_w:
                        pressed_letters.append("W")
                    if e.key == pygame.K_e:
                        pressed_letters.append("E")
                    if e.key == pygame.K_r:
                        pressed_letters.append("R")
                    if e.key == pygame.K_t:
                        pressed_letters.append("T")
                    if e.key == pygame.K_y:
                        pressed_letters.append("Y")
                    if e.key == pygame.K_u:
                        pressed_letters.append("U")
                    if e.key == pygame.K_i:
                        pressed_letters.append("I")
                    if e.key == pygame.K_o:
                        pressed_letters.append("O")
                    if e.key == pygame.K_p:
                        pressed_letters.append("P")

            self.w.blit(
                pygame.transform.scale(pygame.image.load(back_image), (700, 500))
                (0, 0)) if back_image else 0

            [pygame.draw.rect(self.w, *rect) for rect in rects[::-1]]
            [pygame.draw.ellipse(self.w, *ellips) for ellips in ellipses[::-1]]

            self.all_sprites.draw(self.w)
            draw_stat()

            if on_menu:
                [pygame.draw.rect(self.w, *rect) for rect in letters_rects]

                [label.draw(self.w) for label in letters]

                [pygame.draw.rect(self.w, [(not is_light) * 255] * 3, line) for line in lines]

                pygame.draw.rect(self.w, back_color, (653, 0, 50, 50))

                self.fill_alpha()
                pygame.mixer.music.pause()

                [button.check_on((self.x, self.y)) for button in [button_quit_level, button_quit_menu, button_play_again]]
                [button.draw(self.w) for button in [button_quit_level, button_quit_menu, button_play_again, button_pause]]

                self.volume = switch_volume.get_selected()

                pygame.mixer.music.set_volume(self.volume * 0.2)

                switch_volume.draw(self.w)
                label_volume.draw(self.w)
                label_name.draw(self.w)

                self.set_cursor(max([0] + [obj.id for obj in [
                    button_pause, switch_volume, button_play_again, button_quit_menu, label_volume, button_quit_level,
                    label_name
                ] if obj.collide_point((self.x, self.y))]))

                self.w.blit(image_level, (475 - image_level.get_width() // 2, 225 - image_level.get_height() // 2))

                x1 = 465 - (35 * (complexity - 1))

                for _ in range(complexity):
                    self.w.blit(image_star, (x1, 370))
                    x1 += 65
            else:

                pygame.draw.rect(self.w, back_color, (650, 0, 50, 50))

                time += ewait

                while 1 < time:
                    if particles:  # Создание эффекта-частиц
                        x = get_obj(particles[0])
                        y = get_obj(particles[1])
                        color = get_obj(particles[2]) if len(particles) > 2 else None

                        Particle(self.all_sprites, x, y, color) if color else Particle(self.all_sprites, x, y)

                    if petals:  # Создание эффекта-лепестков
                        color = get_obj(petals[0])
                        pos = (int(get_obj(petals[1][0])), int(get_obj(petals[1][1])))
                        direction = get_obj(petals[2])
                        rl = get_obj(petals[3])
                        ud = get_obj(petals[4])
                        msp = get_obj(petals[5])  # max speed
                        msz = get_obj(petals[6])  # max size

                        Petal(self.all_sprites, color, pos, direction, rl, ud, msp, msz)

                    if sparks:  # Создание эффекта-искр
                        x = get_obj(sparks[0])
                        y = get_obj(sparks[1])

                        Spark(self.all_sprites, (x, y))

                    time -= 1

                for rect in spawns_rects:
                    if iters_of_game == rect[1]:
                        col = {
                            "Q": 0, "W": 1, "E": 2, "R": 3, "T": 4, "Y": 5, "U": 6, "I": 7, "O": 8, "P": 9
                        }[rect[0]]

                        color_data = game_rects_colors[col % len(game_rects_colors)]

                        print(color_data)

                        color = color_data[0]

                        spanel = color_data[1]  # stroke panel

                        gr = GameRect(color, [round(obj) for obj in (col * size, -45, size, 45)], spanel)

                        gr.l = rect[0]

                        game_rects.append(
                            gr
                        )

                        self.fill_alpha()

                for game_rect in game_rects[::-1]:
                    game_rect.move(0, 425 / 60)

                    if game_rect.rect.y >= 500:
                        game_rects.remove(game_rect)

                for game_rect in game_rects:
                    game_rect.draw(self.w)

                [pygame.draw.rect(self.w, *rect) for rect in letters_rects]

                [label.draw(self.w) for label in letters]

                self.all_sprites.update()

                if iters_of_game < wait * 40:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

                [pygame.draw.rect(self.w, [(not is_light) * 255] * 3, line) for line in lines]
                iters_of_game += 1

                button_pause.draw(self.w)

                self.set_cursor(any([button.collide_point((self.x, self.y)) for button in [
                    button_pause
                ]]))

            pygame.display.update()
            clock.tick(FPS)

    def fill(self, color: tuple[int, int, int] | list[int, int, int], alpha: int = 255):
        s = pygame.Surface((700, 500))
        s.fill(color)
        s.set_alpha(alpha)

        self.w.blit(s, (0, 0))

    def fill_alpha(self, color: tuple[int, int, int] = (0, 0, 0)):
        self.fill(color, 92)

    def set_cursor(self, a: bool | int):
        if a == 1:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        elif not a:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        elif a == 2:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_IBEAM))


MainGame(window)
