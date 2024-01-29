import pygame

pygame.init()


class Switch:
    def __init__(self, main_rect: pygame.rect.Rect | tuple[int] | list[int],
                 back_color: pygame.color.Color | tuple[int] | list[int],
                 text1: str,
                 text2: str,
                 option_rects: tuple[pygame.rect.Rect,
                 pygame.rect.Rect] | tuple[tuple[int]] | list[tuple[int]] | list[list[int]] | tuple[list[int]],
                 option_color: pygame.color.Color | tuple[int] | list[int] = (255, 0, 0),
                 rounding: int = 5,
                 font_name: str = None,
                 font: pygame.font.Font = None,
                 fsize: int = 20,
                 second_option_color: pygame.color.Color | tuple[int] | list[int] = None):
        self.main_rect = main_rect if type(main_rect) not in (tuple, list) else pygame.rect.Rect(*main_rect)
        self.back_color = back_color

        self.text1, self.text2 = text1, text2

        self.option_rects = option_rects if (type(option_rects[0]) not in
                                             (list, tuple)) else [pygame.rect.Rect(*rect) for rect in option_rects]

        self.rounding = rounding

        self.font_name = font_name
        self.font = font

        self.selected = 0

        self.option_color = option_color

        self.fsize = fsize

        self.sec_c = second_option_color

        self.id = 1

    def get_selected(self) -> int:
        return self.selected

    def set_selected(self):
        self.selected = (self.selected + 1) % 2

    def collide_point(self, pos: tuple[int, int] | list[int, int]) -> bool:
        return self.main_rect.collidepoint(*pos)

    def collide_rect(self, rect: pygame.rect.Rect | tuple[int, int, int, int] | list[int, int, int, int]) -> bool:
        return self.main_rect.colliderect(rect)

    def check_click(self, pos: tuple[int, int] | list[int, int]):
        if self.collide_point(pos):
            self.set_selected()

    def draw(self, window):
        pygame.draw.rect(window, self.back_color, self.main_rect, border_radius=self.rounding)

        pygame.draw.rect(window,
                         self.sec_c if self.sec_c and self.selected else self.option_color,
                         self.option_rects[self.selected], border_radius=self.rounding)

        font = pygame.font.SysFont(self.font_name, self.fsize) if not self.font else self.font

        image1 = font.render(self.text1, True, (0, 0, 0))
        image2 = font.render(self.text2, True, (0, 0, 0))

        window.blit(image1,
                    (
                        self.option_rects[0].centerx - image1.get_width() // 2,
                        self.option_rects[0].centery - image1.get_height() // 2
                    ))

        window.blit(image2,
                    (
                        self.option_rects[1].centerx - image2.get_width() // 2,
                        self.option_rects[1].centery - image2.get_height() // 2
                    ))

    def set_text(self, text1: str, text2: str):
        self.text1 = text1
        self.text2 = text2
