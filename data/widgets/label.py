import pygame

pygame.init()


class Label:
    def __init__(self, center: list[int] | tuple[int],
                 text: str | list[str],
                 text_color: pygame.color.Color | tuple[int] | list[int] | None = (0, 0, 0),
                 font_name: str = None,
                 font: pygame.font.Font = None,
                 fsize: int = 24):
        self.center = center
        self.text = [text] if isinstance(text, str) else text
        self.text_color = text_color
        self.font_name = font_name
        self.font = font
        self.fsize = fsize

    def draw(self, window):
        text = pygame.font.Font(self.font_name, self.fsize).render(self.text, True, self.text_color) \
            if not self.font else self.font

        window.blit(text,
                    (
                        self.center[0] - text.get_width() // 2,
                        self.center[1] - text.get_height() // 2
                    ))
