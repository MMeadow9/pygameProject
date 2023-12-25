import pygame
from random import randint, choice

pygame.init()


class Spark(pygame.sprite.Sprite):
    def __init__(self, group, pos, ws=(700, 500)):
        super().__init__(group)

        size = choice([1] * (3 ** 4) + [2] * (3 ** 2) + [3])

        self.rect = pygame.rect.Rect(*pos, *[size] * 2)

        self.color = choice(
            [(255, 183, 3), (255, 194, 41), (255, 202, 69), (247, 75, 32), (255, 0, 0)]
        )

        self.d = "U"

        self.image = pygame.surface.Surface((size, size), pygame.SRCALPHA)
        self.image.fill(self.color)

        self.dx = randint(5, 10) * choice([1, -1])
        self.dy = randint(8, 10) * -1

        self.ws = ws

    def update(self):
        if self.d == "U":
            if not self.dx:
                self.d = choice("RL")
            else:
                self.dy -= 1
                self.dx += 1 if self.dx < 0 else -1
        elif self.d == "R":
            if abs(self.dy) < 5:
                self.d = choice("U")
            else:
                self.dx += 1
                self.dy += 1 if self.dy < 0 else -1
        elif self.d == "L":
            if abs(self.dy) < 5:
                self.d = choice("U")
            else:
                self.dx -= 1
                self.dy += 1 if self.dy < 0 else -1

        self.rect = self.rect.move(self.dx, self.dy)

        if self.rect.x < -100 or self.rect.x > self.ws[0] + 100 or self.rect.y < -50:
            self.kill()

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

