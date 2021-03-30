import pygame


class AbstractBullet:
    def __init__(self, x, y):
        self.speed = 8  # px per frame
        self.radius = 2  # px
        self.damage = 8
        self.cords = {
            'x': x,
            'y': y
        }
        self.direction = {
            'x_cof': 0,
            'y_cof': -1
        }
        self.sprite = pygame.image.load('assets/sprites/bullet/1.png')
        self.collide_with_flesh_sprite = pygame.image.load('assets/sprites/bullet/1.png')


class BulletLvl1(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 4
        self.damage = 6
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/bullet/1.png'), (self.radius * 2, self.radius * 2))


class BulletLvl2(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 4
        self.damage = 8
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/bullet/2.png'), (self.radius * 2, self.radius * 2))


class BulletLvl3(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 4
        self.damage = 10
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/bullet/3.png'), (self.radius * 2, self.radius * 2))


class BulletLvl4(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 4
        self.damage = 12
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/bullet/4.png'), (self.radius * 2, self.radius * 2))


class BulletLvl5(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 4
        self.damage = 14
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/bullet/5.png'), (self.radius * 2, self.radius * 2))


class BulletLvl6(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 4
        self.damage = 16
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/bullet/6.png'), (self.radius * 2, self.radius * 2))
