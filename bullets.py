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


class BulletLvl1(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 2
        self.damage = 6


class BulletLvl2(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 2
        self.damage = 8


class BulletLvl3(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 3
        self.damage = 10


class BulletLvl4(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 3
        self.damage = 12


class BulletLvl5(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 4
        self.damage = 14


class BulletLvl6(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.radius = 4
        self.damage = 16
