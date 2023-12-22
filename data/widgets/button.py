import pygame

pygame.init()


window = pygame.display.set_mode((300, 300))


class Button:
    def __init__(self, rect: tuple[int, int, int, int] | list[int, int, int, int],
                 text: str,
                 back_color: pygame.Color | tuple[int, int, int] | list[int, int, int] = (255, 255, 255),
                 text_color: pygame.Color | tuple[int, int, int] | list[int, int, int] = (0, 0, 0),
                 is_antialias: bool | int = True,
                 is_bold: bool | int = False,
                 is_italic: bool | int = False,
                 font: str | None = None,
                 function=None,
                 fsize: int = 24):

        """
        Создание кнопки, для активации которой нужно нажать на неё

        :param rect: Местоположение, длина и высота кнопки
        :param text: Текст, который будет находиться на кнопке
        :param back_color: Цвет кнопки
        :param text_color: Цвет текста на кнопке
        :param is_antialias: Сглаженный ли будет текст
        :param is_bold: Жирный ли будет текст
        :param is_italic: Курсивный ли будет текст
        :param font: Название шрифта для текста
        :param function: Функция, вызываемая при нажатии на кнопку
        :param fsize: Размер текста на кнопке
        """

        self.rect = pygame.rect.Rect(*rect)
        self.text = text

        self.back_color = back_color
        self.text_color = text_color

        self.is_antialias = is_antialias
        self.is_bold = is_bold
        self.is_italic = is_italic

        self.font = font
        self.function = function

        self.fsize = fsize

    def set_rect(self, rect: tuple[int, int, int, int] | list[int, int, int, int]):
        self.rect = pygame.rect.Rect(*rect)

    def set_text(self, text: str):
        self.text = text

    def set_colors(self, back_color: pygame.Color | tuple[int, int, int] | list[int, int, int] = None,
                   text_color: pygame.Color | tuple[int, int, int] | list[int, int, int] = None):
        self.back_color = back_color if back_color is not None else self.back_color
        self.text_color = text_color if text_color is not None else self.text_color

    def set_text_characteristic(self, is_antialias: bool | int = None,
                       is_bold: bool | int = None,
                       is_italic: bool | int = None,
                       fsize: int = None):
        self.is_antialias = is_antialias if is_antialias is not None else self.is_antialias
        self.is_bold = is_bold if is_bold is not None else self.is_bold
        self.is_italic = is_italic if is_italic is not None else self.is_italic
        self.fsize = fsize if fsize is not None else self.fsize

    def set_font(self, font: str):
        self.font = font

    def set_function(self, function):
        self.function = function

    def collide_point(self, pos: tuple[int, int] | list[int, int]) -> bool:
        return self.rect.collidepoint(*pos)

    def collide_rect(self, rect: pygame.rect.Rect | tuple[int, int, int, int] | list[int, int, int]) -> bool:
        return self.rect.colliderect(rect)

    def check_click(self, pos: tuple[int, int] | list[int, int]):
        if self.collide_point(pos):
            self.function()

    def draw(self, window: pygame.surface.Surface):
        pygame.draw.rect(window, self.back_color, self.rect)

        font = pygame.font.SysFont(self.font, self.fsize, self.is_bold, self.is_italic)

        text_image = font.render(self.text, self.is_antialias, self.text_color)

        rect_text_image = text_image.get_rect()

        window.blit(
            text_image,
            (
                self.rect.centerx - rect_text_image.width // 2,
                self.rect.centery - rect_text_image.height // 2
             )
        )


def f():    print(1)


button = Button((20, 20, 260, 260), "Text", (255, 255, 0), (0, 0, 0), True, True, False, None, f, 80)


clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button.check_click(event.pos)

    window.fill((0, 0, 0))

    button.draw(window)

    pygame.display.update()
    clock.tick(30)