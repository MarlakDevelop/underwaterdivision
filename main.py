import pygame
import json
from random import choice
from datetime import datetime
from player import TennoBathyscaphePlayer
from enemies import DemonZombieEnemy, CacoDemonEnemy
from bullets import DefaultBullet, BulletLvl2
import settings


class Game:
    def __init__(self, size):
        self.enemy_delay_down_delay = settings.ENEMY_DELAY_LOWER_DELAY
        self.default_enemy_delay = settings.ENEMY_DELAY
        self.enemy_delay = settings.ENEMY_DELAY
        self.score = 0
        self.state = {
            'mouseCords': (0, 0),
            'mousePressed': False
        }
        self.width, self.height = size
        self.spawnPlayer()
        self.bullet_delay = settings.BULLET_DELAY
        self.enemies = []
        self.bullets = []

    def spawnEnemy(self):
        enemyType = choice(['zombie', 'zombie', 'zombie', 'zombie', 'caco'])
        enemy_ = None
        if enemyType == 'zombie':
            enemy_ = DemonZombieEnemy(choice(range(50, self.width - 50)), -50)
        elif enemyType == 'caco':
            enemy_ = CacoDemonEnemy(choice(range(50, self.width - 50)), -50)
        self.enemies = self.enemies + [enemy_]

    def spawnPlayer(self):
        self.player = TennoBathyscaphePlayer(self.width // 2, self.height - 50)

    def handleEvents(self, events):
        global running

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.state['mousePressed'] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.state['mousePressed'] = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if self.state['mousePressed']:
                    if ((self.player.cords['x'] > self.player.radius or x - self.state['mouseCords'][0] > 0) and
                            (self.player.cords['x'] < self.width - self.player.radius or x - self.state['mouseCords'][0] < 0)):
                        self.player.cords['x'] += x - self.state['mouseCords'][0]
                    if (self.player.cords['y'] > self.player.radius or y - self.state['mouseCords'][1] > 0) and (self.player.cords['y'] < self.height - self.player.radius or y - self.state['mouseCords'][1] < 0):
                        self.player.cords['y'] += y - self.state['mouseCords'][1]
                self.state['mouseCords'] = x, y

    def handleForGameOver(self):
        global gameOver

        for enemy in self.enemies:
            if enemy.cords['y'] + enemy.radius > self.height:
                gameOver = True

    def handleEnemiesConnectWithPlayer(self):
        global gameOver

        for enemy in self.enemies:
            len1 = abs(enemy.cords['y'] - self.player.cords['y'])
            len2 = abs(enemy.cords['x'] - self.player.cords['x'])
            d = (len1 ** 2 + len2 ** 2) ** 0.5
            if d < enemy.radius + self.player.radius:
                gameOver = True
            elif d == self.player.radius + enemy.radius:
                gameOver = True
            elif d + self.player.radius == enemy.radius:
                gameOver = True
            elif d < enemy.radius - self.player.radius or d + self.player.radius < enemy.radius:
                gameOver = True

    def handleBulletsConnectWithEnemies(self):
        bullet_indexes = []
        for i, bullet in enumerate(self.bullets):
            for enemy in self.enemies:
                len1 = abs(enemy.cords['y'] - bullet.cords['y'])
                len2 = abs(enemy.cords['x'] - bullet.cords['x'])
                d = (len1 ** 2 + len2 ** 2) ** 0.5
                if d < enemy.radius + bullet.radius:
                    bullet_indexes.append(i)
                    enemy.hp -= bullet.damage
                elif d == bullet.radius + enemy.radius:
                    bullet_indexes.append(i)
                    enemy.hp -= bullet.damage
                elif d + bullet.radius == enemy.radius:
                    bullet_indexes.append(i)
                    enemy.hp -= bullet.damage
                elif d < enemy.radius - bullet.radius or d + bullet.radius < enemy.radius:
                    bullet_indexes.append(i)
                    enemy.hp -= bullet.damage
        for i in bullet_indexes:
            try:
                del self.bullets[i]
            except Exception:
                pass

    def tryShoot(self):
        if self.state['mousePressed']:
            if self.bullet_delay <= 0:
                if self.score < 500:
                    self.bullets.append(DefaultBullet(self.player.cords['x'], self.player.cords['y'] - self.player.radius))
                elif self.score < 1500:
                    self.bullets.append(DefaultBullet(self.player.cords['x'] - 15, self.player.cords['y'] - self.player.radius))
                    self.bullets.append(DefaultBullet(self.player.cords['x'] + 15, self.player.cords['y'] - self.player.radius))
                elif self.score < 4500:
                    bullet = DefaultBullet(self.player.cords['x'] - 20, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = -0.066
                    self.bullets.append(bullet)
                    self.bullets.append(DefaultBullet(self.player.cords['x'], self.player.cords['y'] - self.player.radius))
                    bullet = DefaultBullet(self.player.cords['x'] + 20, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = 0.066
                    self.bullets.append(bullet)
                elif self.score < 11500:
                    bullet = DefaultBullet(self.player.cords['x'] - 30, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = -0.1
                    self.bullets.append(bullet)
                    bullet = DefaultBullet(self.player.cords['x'] - 15, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = -0.05
                    self.bullets.append(bullet)
                    self.bullets.append(DefaultBullet(self.player.cords['x'], self.player.cords['y'] - self.player.radius))
                    bullet = DefaultBullet(self.player.cords['x'] + 15, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = 0.066
                    self.bullets.append(bullet)
                    bullet = DefaultBullet(self.player.cords['x'] + 30, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = 0.1
                    self.bullets.append(bullet)
                elif self.score < 18500:
                    bullet = BulletLvl2(self.player.cords['x'] - 30, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = -0.1
                    self.bullets.append(bullet)
                    bullet = BulletLvl2(self.player.cords['x'] - 15, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = -0.05
                    self.bullets.append(bullet)
                    self.bullets.append(BulletLvl2(self.player.cords['x'], self.player.cords['y'] - self.player.radius))
                    bullet = BulletLvl2(self.player.cords['x'] + 15, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = 0.066
                    self.bullets.append(bullet)
                    bullet = BulletLvl2(self.player.cords['x'] + 30, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = 0.1
                    self.bullets.append(bullet)
                else:
                    bullet = BulletLvl2(self.player.cords['x'] - 30, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = -0.1
                    self.bullets.append(bullet)
                    bullet = BulletLvl2(self.player.cords['x'] - 20, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = -0.066
                    self.bullets.append(bullet)
                    bullet = BulletLvl2(self.player.cords['x'] - 10, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = -0.033
                    self.bullets.append(bullet)
                    self.bullets.append(BulletLvl2(self.player.cords['x'], self.player.cords['y'] - self.player.radius))
                    bullet = BulletLvl2(self.player.cords['x'] + 10, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = 0.033
                    self.bullets.append(bullet)
                    bullet = BulletLvl2(self.player.cords['x'] + 20, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = 0.066
                    self.bullets.append(bullet)
                    bullet = BulletLvl2(self.player.cords['x'] + 30, self.player.cords['y'] - self.player.radius)
                    bullet.direction['x_cof'] = 0.1
                    self.bullets.append(bullet)
                self.bullet_delay = settings.BULLET_DELAY

    def updateBullets(self):
        indexes = []
        for i in range(len(self.bullets)):
            if self.bullets[i].cords['y'] + self.bullets[i].radius <= 0:
                indexes.append(i)
        for i in indexes:
            try:
                del self.bullets[i]
            except Exception:
                pass
        for bullet in self.bullets:
            bullet.cords['x'] += bullet.speed * bullet.direction['x_cof']
            bullet.cords['y'] += bullet.speed * bullet.direction['y_cof']
        self.bullet_delay -= 1

    def updateEnemies(self):
        if self.enemy_delay_down_delay <= 0:
            self.default_enemy_delay -= 1
            if self.default_enemy_delay < 10:
                self.default_enemy_delay = 10
            self.enemy_delay_down_delay = settings.ENEMY_DELAY_LOWER_DELAY
        if self.enemy_delay <= 0:
            self.enemy_delay = self.default_enemy_delay
            self.spawnEnemy()
        self.enemy_delay -= 1
        self.enemy_delay_down_delay -= 1
        for enemy_ in self.enemies:
            enemy_.cords['x'] += enemy_.speed * enemy_.direction['x_cof']
            enemy_.cords['y'] += enemy_.speed * enemy_.direction['y_cof']
        indexes = []
        for i in range(len(self.enemies)):
            if self.enemies[i].hp <= 0:
                indexes.append(i)
        for i in indexes:
            try:
                self.score += self.enemies[i].reward
                del self.enemies[i]
            except Exception:
                pass

    def render(self):
        pygame.draw.circle(
            screen,
            pygame.Color('#FFFFFF'),
            (self.player.cords['x'],
             self.player.cords['y']),
            self.player.radius)
        for enemy_ in self.enemies:
            pygame.draw.circle(screen, pygame.Color('#FFFFFF'), (enemy_.cords['x'], enemy_.cords['y']), enemy_.radius)
            pygame.draw.rect(screen, pygame.Color('#999999'), (
                enemy_.cords['x'] - enemy_.radius,
                enemy_.cords['y'] - enemy_.radius - 15,
                enemy_.radius * 2,
                10
            ))
            pygame.draw.rect(screen, pygame.Color('#0fff83'), (
                enemy_.cords['x'] - enemy_.radius,
                enemy_.cords['y'] - enemy_.radius - 15,
                round(enemy_.radius * 2 * (enemy_.hp / enemy_.max_hp)),
                10
            ))
        for bullet in self.bullets:
            pygame.draw.circle(screen, pygame.Color('#FFFFFF'), (bullet.cords['x'], bullet.cords['y']), bullet.radius)

    def restart(self):
        self.enemy_delay_down_delay = settings.ENEMY_DELAY_LOWER_DELAY
        self.default_enemy_delay = settings.ENEMY_DELAY
        self.enemy_delay = settings.ENEMY_DELAY
        self.score = 0
        self.state = {
            'mouseCords': (0, 0),
            'mousePressed': False
        }
        self.width, self.height = size
        self.spawnPlayer()
        self.bullet_delay = settings.BULLET_DELAY
        self.enemies = []
        self.bullets = []

    def handleGameOverEvents(self, events):
        global running, gameOver

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.restart()
                gameOver = False

    def gameOverRender(self):
        self.render()


pygame.init()
pygame.display.set_caption('')
clock = pygame.time.Clock()
size = width, height = 600, 800
screen = pygame.display.set_mode(size)
running = True
gameOver = False
game = Game(size)
while running:
    if not gameOver:
        game.handleEvents(pygame.event.get())
        game.updateEnemies()
        game.updateBullets()
        game.handleEnemiesConnectWithPlayer()
        game.handleBulletsConnectWithEnemies()
        game.render()
        game.tryShoot()
        game.handleForGameOver()
        scoreFont = pygame.font.Font(None, 36)
        score = scoreFont.render(f'Очки силы: {game.score}', True,
                                 (0, 180, 0))
        screen.blit(score, (10, 10))
    else:
        game.handleGameOverEvents(pygame.event.get())
        game.gameOverRender()
    pygame.display.flip()
    clock.tick(settings.FPS)
    screen.fill('#000000')
