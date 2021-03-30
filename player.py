import pygame
import attacks


class AbstractPlayer:
    def __init__(self, x, y):
        self.radius = 30
        self.cords = {
            'x': x,
            'y': y
        }
        self.attack = attacks.AbstractAttack()
        self.deathSound = pygame.mixer.Sound('assets/sounds/player_killed.wav')

    def death(self):
        self.deathSound.play()

    def update(self):
        self.attack.x, self.attack.y = self.cords['x'], self.cords['y'] - self.radius


class FirstShipPlayer(AbstractPlayer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.attack = attacks.FirstShipAttack()


class SecondShipPlayer(AbstractPlayer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.attack = attacks.SecondShipAttack()


class ThirdShipPlayer(AbstractPlayer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.attack = attacks.ThirdShipAttack()
