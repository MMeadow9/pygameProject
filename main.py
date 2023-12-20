from random import randint, choice
import pygame

pygame.init()


class Particle(pygame.sprite.Sprite):
    def __init__(self, group, x, y, color):
        super().__init__(group)

        size = choice([1] * 81 + [2] * 27 + [3] * 9 + [4] * 3 + [5])

        max_speed = 20

        self.rect = pygame.rect.Rect(x, y, size, size)
        self.color = color

        self.dx, self.dy = randint(-max_speed, max_speed), randint(-max_speed, max_speed)

    def update(self):
        self.rect = self.rect.move(self.dx, self.dy)

        if -10 > self.rect.x or self.rect.x > 700:
            self.kill()

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)