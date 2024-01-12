import pygame

pygame.init()


class BigSwitch:
    def __init__(self, main_rect: pygame.rect.Rect | tuple[int] | list[int],
                 back_color: pygame.color.Color | tuple[int] | list[int],
                 texts: list[str] | tuple[str],
                 option_rects: tuple[pygame.rect.Rect],
                 option_color: tuple[int] | list[tuple[int]],
                 rounding: int = 5,
                 font_name: str = None,
                 font: pygame.font.Font = None,
                 fsize: int = 20):
        self.main_rect = main_rect if type(main_rect) not in (tuple, list) else pygame.rect.Rect(*main_rect)
        self.back_color = back_color

        self.texts = texts

        self.option_rects = option_rects

        self.option_color = option_color

        self.selected = 0

        self.font_name = font_name
        self.font = font

        self.fsize = fsize

        self.rounding = rounding

    def get_selected(self) -> int:
        return self.selected

    def set_selected(self):
        self.selected = (self.selected + 1) % len(self.option_rects)

    def collide_point(self, pos) -> bool:
        return self.main_rect.collidepoint(*pos)

    def check_click(self, pos):
        if self.collide_point(pos):
            self.set_selected()

    def draw(self, window):
        pygame.draw.rect(window, self.back_color, self.main_rect, border_radius=self.rounding)

        pygame.draw.rect(window, self.option_color[self.selected % len(self.option_color)],
                          self.option_rects[self.selected], border_radius=25)

        font = pygame.font.SysFont(self.font_name, self.fsize) if not self.font else self.font

        for index in range(len(self.option_rects)):
            rect, text = pygame.rect.Rect(*self.option_rects[index]), self.texts[index]

            image = font.render(text, True, (0, 0, 0))

            window.blit(image, (
                rect.centerx - image.get_width() // 2,
                rect.centery - image.get_height() // 2
            ))

