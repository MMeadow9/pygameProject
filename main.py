from random import randint, choice
import pygame
import json

pygame.init()

with open("data/levels.json") as file_json:
    levels_json = json.load(file_json)



window = pygame.display.set_mode((700, 500))


class MainGame:
    def __init__(self):
        pass