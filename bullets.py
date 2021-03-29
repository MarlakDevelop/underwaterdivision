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


class DefaultBullet(AbstractBullet):
    pass


class BulletLvl2(AbstractBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 3  # px
        self.damage = 12
        self.direction = {
            'x_cof': 0,
            'y_cof': -1
        }