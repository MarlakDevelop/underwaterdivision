class AbstractEnemy:
    def __init__(self, x, y):
        self.hp = 0
        self.max_hp = 0
        self.speed = 2  # per frame
        self.radius = 20  # from center in pixels
        self.damage = 50  # damage to player
        self.cords = {
            'x': x,
            'y': y
        }
        self.direction = {
            'x_cof': 0,
            'y_cof': 0
        }


class DemonZombieEnemy(AbstractEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = 50
        self.max_hp = 50
        self.reward = 50
        self.speed = 0.7
        self.radius = 20
        self.damage = 40
        self.direction = {
            'x_cof': 0,
            'y_cof': 1
        }


class CacoDemonEnemy(AbstractEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = 200
        self.max_hp = 200
        self.reward = 200
        self.speed = 0.3
        self.radius = 50
        self.damage = 100
        self.direction = {
            'x_cof': 0,
            'y_cof': 1
        }

