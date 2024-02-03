import pygame


class GameRect:
    def __init__(self, color, rect, spanel):
        self.color, self.rect, self.spanel = color, pygame.rect.Rect(*rect), spanel

    def draw(self, window, alpha=255):
        pygame.draw.rect(window, self.color, self.rect)
        pygame.draw.rect(window, self.spanel, self.rect, 3)

    def move(self, *args):
        self.rect = self.rect.move(*args)

    def data(self):
        print(f"C - {self.color},\t\tR - {self.rect},\t\tS - {self.spanel}")
