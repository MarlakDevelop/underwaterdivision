class AbstractPlayer:
    def __init__(self, x, y):
        self.radius = 30
        self.cords = {
            'x': x,
            'y': y
        }


class TennoBathyscaphePlayer(AbstractPlayer):
    pass
