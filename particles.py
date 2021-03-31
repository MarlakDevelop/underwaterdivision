import pygame
from random import choice


class AbstractParticle:
    def __init__(self, x, y):
        self.cords = {
            'x': x,
            'y': y
        }
        self.beforeDestroy = 60  # frames


class Bubble(AbstractParticle):
    def __init__(self, radius, x, y):
        super().__init__(x, y)
        self.radius = radius
        self.maxBeforeDestroy = 40
        self.beforeDestroy = 40
        self.sprite = pygame.transform.scale(pygame.transform.rotate(
            pygame.image.load('assets/sprites/particles/bubble/1.png'), choice(range(360))),
                                             (self.radius * 2, self.radius * 2))


class Fire(AbstractParticle):
    def __init__(self, radius, x, y):
        super().__init__(x, y)
        self.radius = radius
        self.maxBeforeDestroy = 80
        self.beforeDestroy = 80
        self.sprite = pygame.transform.scale(pygame.transform.rotate(
            pygame.image.load('assets/sprites/particles/fire/1.png'), choice(range(360))),
                                             (self.radius * 2, self.radius * 2))


class Flesh(AbstractParticle):
    def __init__(self, radius, x, y):
        super().__init__(x, y)
        self.radius = radius
        self.maxBeforeDestroy = 180
        self.beforeDestroy = 180
        self.sprite = pygame.transform.scale(pygame.transform.rotate(
            pygame.image.load(choice(['assets/sprites/particles/flesh/1.png',
                                      'assets/sprites/particles/flesh/2.png'])), choice(range(360))),
                                             (self.radius * 2, self.radius * 2))
