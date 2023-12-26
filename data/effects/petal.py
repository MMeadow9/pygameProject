import pygame
from random import randint, choice

pygame.init()


class Petal(pygame.sprite.Sprite):
    def __init__(self, group, color, pos, d="D", rl="RL", ud="DDDU", ws=(700, 500)):
        super().__init__(group)

        size = randint(5, 10)

        self.angle = randint(0, 359)

        self.rotate = randint(-2, 10)

        self.fimage = pygame.surface.Surface((size + 3, size), pygame.SRCALPHA)

        pygame.draw.ellipse(self.fimage, color, (0, 0, size, size))
        pygame.draw.polygon(self.fimage, color, [(size // 2, 0), (size // 2, size), (size + 3, size // 2)])

        self.image = pygame.transform.rotate(self.fimage, self.angle)

        self.rect = pygame.rect.Rect(*pos, size + 3, size)

        self.vx = (randint(3, 20) - size // 5) * (-1 if d == "L" else 1)
        self.vy = (randint(3, 20) - size // 5) * (-1 if d == "U" else 1)

        self.d = d

        self.rl, self.ud = rl, ud
        self.ws = ws

    def update(self):
        if self.d == "D":
            if not self.vx:
                self.d = choice(self.rl)
            else:
                self.vy += 1
                self.vx += 1 if self.vx < 0 else -1
            self.angle = (self.rotate + self.angle) % 360

        elif self.d == "U":
            if not self.vx:
                self.d = choice("RL")
            else:
                self.vy -= 1
                self.vx += 1 if self.vx < 0 else -1
            self.angle = (self.rotate + self.angle) % 360

        elif self.d == "R":
            if not self.vy:
                self.d = choice(self.ud)
            else:
                self.vx += 1
                self.vy += 1 if self.vy < 0 else -1
            self.angle = (self.rotate + self.angle) % 360

        elif self.d == "L":
            if not self.vy:
                self.d = choice(self.ud)
            else:
                self.vx -= 1
                self.vy += 1 if self.vy < 0 else -1
            self.angle = (self.rotate + self.angle) % 360

        self.rect = self.rect.move(self.vx, self.vy)

        self.image = pygame.transform.rotate(self.fimage, self.angle)

        if self.rect.x < -100 or self.rect.x > self.ws[0] + 100 or self.rect.y > self.ws[1] + 20:
            self.kill()

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
