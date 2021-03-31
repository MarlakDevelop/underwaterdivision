import pygame
import bullets


class AbstractAttack:
    def __init__(self):
        self.speed = 1
        self.damage = 1
        self.x = 0
        self.y = 0
        self.sound = pygame.mixer.Sound('assets/sounds/shots/middleshot.wav')

    def playSound(self):
        pygame.mixer.Channel(3).play(self.sound)


class FirstShipAttack(AbstractAttack):
    def __init__(self):
        super().__init__()
        self.sound = pygame.mixer.Sound('assets/sounds/shots/middleshot.wav')
        self.sound.set_volume(0.5)

    def lvl1(self):
        bullet = bullets.BulletLvl1(self.x, self.y)
        self.playSound()
        return [bullet], 10 * (1 / self.speed)

    def lvl2(self):
        bullet1 = bullets.BulletLvl2(self.x + 8, self.y)
        bullet2 = bullets.BulletLvl2(self.x - 8, self.y)
        self.playSound()
        return [bullet1, bullet2], 10 * (1 / self.speed)

    def lvl3(self):
        bullets_ = []
        for i in range(-1, 2):
            bullet = bullets.BulletLvl3(self.x + i * 16, self.y)
            bullet.direction['x_cof'] = (i * 0.16)
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)

    def lvl4(self):
        bullets_ = []
        for i in range(-2, 3):
            bullet = bullets.BulletLvl4(self.x + i * 16, self.y)
            bullet.direction['x_cof'] = (i * 0.16)
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)

    def lvl5(self):
        bullets_ = []
        for i in range(-3, 4):
            bullet = bullets.BulletLvl5(self.x + i * 16, self.y)
            bullet.direction['x_cof'] = (i * 0.12)
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)

    def lvl6(self):
        bullets_ = []
        for i in range(-3, 4):
            bullet = bullets.BulletLvl6(self.x + i * 16, self.y)
            bullet.direction['x_cof'] = (i * 0.1)
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)


class SecondShipAttack(AbstractAttack):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.damage = 0.7
        self.sound = pygame.mixer.Sound('assets/sounds/shots/weakshot.wav')
        self.sound.set_volume(0.5)

    def lvl1(self):
        bullet = bullets.BulletLvl1(self.x, self.y)
        bullet.damage *= self.damage
        bullet.speed *= self.speed * 0.6
        self.playSound()
        return [bullet], 10 * (1 / self.speed)

    def lvl2(self):
        bullet1 = bullets.BulletLvl2(self.x - 8, self.y)
        bullet1.damage *= self.damage
        bullet1.speed *= self.speed * 0.6
        bullet2 = bullets.BulletLvl2(self.x + 8, self.y)
        bullet2.damage *= self.damage
        bullet2.speed *= self.speed * 0.6
        self.playSound()
        return [bullet1, bullet2], 10 * (1 / self.speed)

    def lvl3(self):
        bullets_ = []
        for i in range(-1, 2):
            bullet = bullets.BulletLvl3(self.x + i * 16, self.y)
            bullet.damage *= self.damage
            bullet.speed *= self.speed * 0.6
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)

    def lvl4(self):
        bullets_ = []
        for i in range(-2, 3):
            bullet = bullets.BulletLvl4(self.x + i * 16, self.y)
            bullet.damage *= self.damage
            bullet.speed *= self.speed * 0.6
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)

    def lvl5(self):
        bullets_ = []
        for i in range(-3, 4):
            bullet = bullets.BulletLvl5(self.x + i * 16, self.y)
            bullet.damage *= self.damage
            bullet.speed *= self.speed * 0.6
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)

    def lvl6(self):
        bullets_ = []
        for i in range(-3, 4):
            bullet = bullets.BulletLvl6(self.x + i * 16, self.y)
            bullet.damage *= self.damage
            bullet.speed *= self.speed * 0.6
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)


class ThirdShipAttack(AbstractAttack):
    def __init__(self):
        super().__init__()
        self.speed = 0.5
        self.damage = 3
        self.sound = pygame.mixer.Sound('assets/sounds/shots/strongshot.wav')
        self.sound.set_volume(0.5)

    def lvl1(self):
        bullet = bullets.BulletLvl1(self.x, self.y)
        bullet.damage *= self.damage
        bullet.speed *= self.speed
        self.playSound()
        return [bullet], 10 * (1 / self.speed)

    def lvl2(self):
        bullet1 = bullets.BulletLvl2(self.x - 8, self.y)
        bullet1.damage *= self.damage
        bullet1.speed *= self.speed
        bullet2 = bullets.BulletLvl2(self.x + 8, self.y)
        bullet2.damage *= self.damage
        bullet2.speed *= self.speed
        self.playSound()
        return [bullet1, bullet2], 10 * (1 / self.speed)

    def lvl3(self):
        bullets_ = []
        for i in range(-1, 2):
            bullet = bullets.BulletLvl3(self.x + i * 16, self.y)
            bullet.damage *= self.damage
            bullet.speed *= self.speed
            bullet.direction['x_cof'] = (i * 0.33)
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)

    def lvl4(self):
        bullets_ = []
        for i in range(-2, 3):
            bullet = bullets.BulletLvl4(self.x + i * 16, self.y)
            bullet.damage *= self.damage
            bullet.speed *= self.speed
            bullet.direction['x_cof'] = (i * 0.33)
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)

    def lvl5(self):
        bullets_ = []
        for i in range(-3, 4):
            bullet = bullets.BulletLvl5(self.x + i * 16, self.y)
            bullet.damage *= self.damage
            bullet.speed *= self.speed
            bullet.direction['x_cof'] = (i * 0.25)
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)

    def lvl6(self):
        bullets_ = []
        for i in range(-3, 4):
            bullet = bullets.BulletLvl6(self.x + i * 16, self.y)
            bullet.damage *= self.damage
            bullet.speed *= self.speed
            bullet.direction['x_cof'] = (i * 0.2)
            bullets_.append(bullet)
        self.playSound()
        return bullets_, 10 * (1 / self.speed)
