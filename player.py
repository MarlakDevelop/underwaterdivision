import math
import pygame
import attacks


class AbstractPlayer:
    def __init__(self, x, y):
        self.radius = 60
        self.cords = {
            'x': x,
            'y': y
        }
        self.attack = attacks.AbstractAttack()
        self.deathSound = pygame.mixer.Sound('assets/sounds/player_killed.wav')
        self.deathSound.set_volume(5)
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/ship/1.png'), (self.radius, self.radius))
        self.sprite.set_colorkey((255, 255, 255))
        self.rotation_angle = 0
        self.dead = False
        self.rotated_sprite = self.sprite

    def respawn(self):
        self.dead = False

    def death(self):
        self.dead = True
        pygame.mixer.Channel(0).play(self.deathSound)

    def update(self):
        self.attack.x, self.attack.y = self.cords['x'], self.cords['y'] - self.radius // 2
        if self.rotation_angle < 0:
            self.rotation_angle += 0.5
        elif self.rotation_angle > 0:
            self.rotation_angle -= 0.5
        self.rotated_sprite = pygame.transform.scale(self.sprite, (round(self.sprite.get_width() * (90 - abs(self.rotation_angle)) / 90), self.sprite.get_height()))


class FirstShipPlayer(AbstractPlayer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.attack = attacks.FirstShipAttack()
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/ship/1.png'), (self.radius * 2, self.radius * 2))


class SecondShipPlayer(AbstractPlayer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.attack = attacks.SecondShipAttack()
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/ship/2.png'), (self.radius * 2, self.radius * 2))


class ThirdShipPlayer(AbstractPlayer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.attack = attacks.ThirdShipAttack()
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/ship/3.png'), (self.radius * 2, self.radius * 2))
