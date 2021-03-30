import pygame


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
        self.beforeDestroy = 40
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/particles/bubble/1.png'),
                                             (self.radius * 2, self.radius * 2))


class Blood:
    pass
