import pygame
from random import choices

pygame.init()

s = pygame.display.set_mode((600, 466))

#pygame.mixer.music.load("data/sounds/sound2.mp3")
pygame.mixer.music.load("data/sounds/sound1.mp3")
pygame.mixer.music.play()

FPS = 40

i = 0

lst = []

clock = pygame.time.Clock()

lst1 = [i for i in
[9, 23, 41, 58, 75, 108, 124, 143, 154, 173, 193, 211, 229, 267, 301, 308, 330, 349, 366, 384, 420, 433, 451, 463, 474, 485, 494, 505, 514, 525, 535, 545, 554, 560, 567, 573, 583, 589, 596, 602, 612, 637, 655, 675, 692, 722, 739, 758, 771, 791, 809, 828, 845, 884, 915, 920, 944, 964, 983, 999, 1033, 1049, 1067, 1079, 1100, 1119, 1149, 1159, 1169, 1180, 1190, 1200, 1209, 1219, 1230, 1238, 1265, 1270, 1292, 1310, 1328, 1345, 1388, 1416, 1421, 1435, 1446, 1455, 1466, 1500, 1540, 1574, 1598, 1617, 1651, 1676, 1686, 1696, 1713, 1731, 1750, 1770, 1848, 1885, 1904, 1926, 1947, 1963, 2003, 2034, 2049, 2059, 2069, 2079, 2152, 2189, 2211, 2233, 2264, 2288, 2299, 2309, 2326, 2346, 2365, 2383, 2445, 2456, 2466, 2483, 2500, 2520, 2541]

]

print(lst1)

key, val = lst1, choices("QWE", k=len(lst1))

dct = dict(zip([str(i) for i in key], val))

print(len(dct))

print([str(dct).replace("'", '"')])

while 1:
    s.fill((0, 0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            print(lst)
            exit()
        if e.type == pygame.KEYDOWN:
            lst.append(i)

    i += 1

    if i in lst1:
        s.fill((255, 100, 0))

    pygame.display.update()
    clock.tick(FPS)
