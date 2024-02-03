def play(path=""):

    import pygame
    from random import randint, choice

    pygame.init()

    window = pygame.display.set_mode((1000, 725))

    class Asteroid1:
        def __init__(self, filename=path + "data/images/asteroid1"):
            size = choice([
                (59, 49),
                (42, 36),
                (46, 40),
                (50, 43),
                (54, 46)
            ])

            self.angle = randint(0, 359)

            self.fimage = pygame.transform.scale(pygame.image.load(f"{filename}.png"), size)

            self.image = pygame.transform.rotate(self.fimage, self.angle)
            self.rect = pygame.rect.Rect(randint(100, 900), -100, *size)
            self.speedy = randint(3, 15)
            self.speedx = randint(-9, 9)

            self.rotate = randint(-20, 20) / 10

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            self.angle = (360 + self.angle + self.rotate) % 360

            self.image = pygame.transform.rotate(self.fimage, self.angle)

        def collide_rect(self, rect):
            return self.rect.colliderect(rect)

        def draw(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

        def collide_point(self, x, y):
            self.rect.collidepoint(x, y)

    class Asteroid2(Asteroid1):
        def __init__(self, filename=path + "data/images/asteroid2"):
            super().__init__(filename)

        def update(self):
            super().update()

            if self.rect.x <= 0 or self.rect.x >= 1000 - self.rect.width:
                self.speedx *= -1
                self.rotate *= -1

    class Asteroid3(Asteroid1):
        def __init__(self, filename=path + "data/images/asteroid3"):
            super().__init__(filename)

            self.os = False  # on_screen

        def update(self):
            super().update()

            if self.rect.y >= 725 - self.rect.height or (self.rect.y <= 0 and self.os):
                self.speedy *= -1
                self.rotate *= -1

            self.os = self.rect.y > 0

    class Asteroid4(Asteroid1):
        def __init__(self):
            super().__init__(path + "data/images/asteroid4")

            self.os = False  # on_screen

        def update(self):
            super().update()

            if self.rect.x <= 0 or self.rect.x >= 1000 - self.rect.width:
                self.speedx *= -1
                self.rotate *= -1

            if self.rect.y >= 725 - self.rect.height or (self.rect.y <= 0 and self.os):
                self.speedy *= -1
                self.rotate *= -1

            self.os = self.rect.y > 0

    Ey = 600

    class Bolt:
        def __init__(self):
            self.image = pygame.image.load(path + "data/images/magicBolt.png")
            self.rect = pygame.rect.Rect(470, 580, 60, 60)
            self.dx = choice([4, -4])
            self.dy = -4

        def collide_rect(self, rect):
            return self.rect.colliderect(rect)

        def update(self):
            self.rect.x += self.dx
            if self.rect.x <= 0 or self.rect.x >= 940:
                self.dx *= -1
            self.rect.y += self.dy
            if self.rect.y <= 0:
                self.dy = abs(self.dy)

        def draw(self):
            window.blit(self.image, (self.rect.x, self.rect.y))


    y = -1700

    asteroids = []

    timer = 0

    spawn_interval = 35  # 35

    clock = pygame.time.Clock()
    bolt = Bolt()
    back = pygame.image.load(path + "data/images/background.png")
    plat = pygame.image.load(path + "data/images/platform.png")

    earth = pygame.image.load(path + "data/images/earth.png")

    move_r, move_l = False, False
    move_a = False

    x = 445
    pygame.mixer.music.load(path + "data/sounds/sound.mp3")
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RIGHT, pygame.K_d):
                move_r = True
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_a):
                move_l = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                move_a = True
            if event.type == pygame.KEYUP and event.key in (pygame.K_RIGHT, pygame.K_d):
                move_r = False
            if event.type == pygame.KEYUP and event.key in (pygame.K_LEFT, pygame.K_a):
                move_l = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                move_a = False

        x += (move_r - move_l) * (6 + move_a * 3)

        x = -110 if x > 1000 else (1000 if x <= -111 else x)

        window.blit(back, (0, int(y)))
        window.blit(earth, (-50, Ey))
        window.blit(plat, (x, 685))
        bolt.update()
        if bolt.collide_rect(pygame.rect.Rect(x, 685, 110, 35)):
            bolt.dy = -abs(bolt.dy)
        bolt.draw()
        timer += 1
        if timer >= spawn_interval:
            spawn_interval *= 0.995
            timer = 0

            asteroid_type = choice([1] * 84 + [2] * 10 + [3] * 5 + [4])

            if asteroid_type == 1:
                asteroids.append(Asteroid1())
            if asteroid_type == 2:
                asteroids.append(Asteroid2())
            if asteroid_type == 3:
                asteroids.append(Asteroid3())
            if asteroid_type == 4:
                asteroids.append(Asteroid4())

        for asteroid in asteroids[::-1]:
            asteroid.update()
            if asteroid.collide_rect(pygame.rect.Rect(x, 762, 110, 35)):
                print("YOU LOSE!!!")
                return 0

            if asteroid.rect.x < -asteroid.rect.width or asteroid.rect.x > 1000 or asteroid.rect.y > 800 or \
                    asteroid.rect.y < -500:
                asteroids.remove(asteroid)

            elif bolt.collide_rect(asteroid.rect):
                a, b = bolt.rect.x, bolt.rect.y
                a -= bolt.dx
                b -= bolt.dy
                if asteroid.collide_rect(pygame.rect.Rect(a + bolt.dx, b, 60, 60)):
                    bolt.dx *= -1
                if asteroid.collide_rect(pygame.rect.Rect(a, b + bolt.dy, 60, 60)):
                    bolt.dy *= -1

                asteroids.remove(asteroid)

            else:
                asteroid.draw()

        y += 0.1
        Ey += 0.01
        if bolt.rect.y >= 725:
            return 0

        if y >= -10:
            print("YOU WIN!!!")
            return 0

        pygame.display.update()
        clock.tick(35)
