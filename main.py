import math
import pygame
from random import choice
from player import FirstShipPlayer, SecondShipPlayer, ThirdShipPlayer
from enemies import DemonZombieEnemy, CacoDemonEnemy, UberDemonEnemy, SatanEnemy
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
        self.bullet_delay = 0
        self.enemies = []
        self.bullets = []
        self.sounds = {
            'bullet_collide_with_enemies': [
                pygame.mixer.Sound('assets/sounds/bullet_collide_with_flesh/1.wav'),
                pygame.mixer.Sound('assets/sounds/bullet_collide_with_flesh/2.wav')
            ],
            'demon_killed': [
                pygame.mixer.Sound('assets/sounds/demon_killed/1.wav'),
                pygame.mixer.Sound('assets/sounds/demon_killed/2.wav')
            ],
            'boss_awaken': [
                pygame.mixer.Sound('assets/sounds/boss_awaken/uber.wav'),
                pygame.mixer.Sound('assets/sounds/boss_awaken/satan.wav')
            ]
        }
        self.sounds['boss_awaken'][1].set_volume(1.5)

    def spawnEnemy(self):
        spawnByLvlChance = {
            '1': ['zombie'],
            '2': ['zombie', 'zombie', 'zombie', 'zombie', 'caco'],
            '3': ['zombie', 'zombie', 'caco', 'caco', 'caco'],
            '4': ['zombie', 'zombie', 'caco', 'caco', 'caco', 'caco', 'uber'],
            '5': ['zombie', 'caco', 'caco', 'caco', 'caco', 'uber', 'uber'],
            '6': ['zombie', 'caco', 'caco', 'uber', 'uber', 'uber', 'satan']
        }
        lvl = self.getCurrentLvl()
        enemyType = choice(spawnByLvlChance[str(lvl)])
        enemy_ = None
        if enemyType == 'zombie':
            enemy_ = DemonZombieEnemy(choice(range(50, self.width - 50)), -50)
        elif enemyType == 'caco':
            enemy_ = CacoDemonEnemy(choice(range(50, self.width - 50)), -50)
        elif enemyType == 'uber':
            enemy_ = UberDemonEnemy(choice(range(50, self.width - 50)), -80)
            self.sounds['boss_awaken'][0].play()
            self.enemy_delay = round(600 / lvl)
        elif enemyType == 'satan':
            enemy_ = SatanEnemy(choice(range(50, self.width - 50)), -150)
            self.sounds['boss_awaken'][1].play()
            self.enemy_delay = round(1200 / lvl)
        self.enemies = self.enemies + [enemy_]

    def spawnPlayer(self):
        self.player = FirstShipPlayer(self.width // 2, self.height - 50)

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
                self.player.death()
            elif d == self.player.radius + enemy.radius:
                gameOver = True
                self.player.death()
            elif d + self.player.radius == enemy.radius:
                gameOver = True
                self.player.death()
            elif d < enemy.radius - self.player.radius or d + self.player.radius < enemy.radius:
                gameOver = True
                self.player.death()

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
                choice(self.sounds['bullet_collide_with_enemies']).play()
            except Exception:
                pass

    def getCurrentLvl(self):
        if self.score < 500:
            return 1
        elif self.score < 1500:
            return 2
        elif self.score < 4500:
            return 3
        elif self.score < 13500:
            return 4
        elif self.score < 50500:
            return 5
        else:
            return 6

    def tryShoot(self):
        if self.state['mousePressed']:
            if self.bullet_delay <= 0:
                attackByLvl = {
                    '1': lambda _: self.player.attack.lvl1(),
                    '2': lambda _: self.player.attack.lvl2(),
                    '3': lambda _: self.player.attack.lvl3(),
                    '4': lambda _: self.player.attack.lvl4(),
                    '5': lambda _: self.player.attack.lvl5(),
                    '6': lambda _: self.player.attack.lvl6(),
                }
                lvl = self.getCurrentLvl()
                result = attackByLvl[str(lvl)]('_')
                self.bullets += result[0]
                self.bullet_delay = result[1]

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
                choice(self.sounds['demon_killed']).play()
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
        scoreFont = pygame.font.Font(None, 36)
        score = scoreFont.render(f'Очки силы: {game.score}', True, (0, 180, 0))
        pygame.draw.rect(screen, pygame.Color('green'), (0, 0, self.width, 20 + score.get_height()))
        screen.blit(score, (self.width // 2 - score.get_width() // 2, 10))

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
        self.bullet_delay = 0
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
        game.player.update()
        game.tryShoot()
        game.handleForGameOver()
    else:
        game.handleGameOverEvents(pygame.event.get())
        game.gameOverRender()
    pygame.display.flip()
    clock.tick(settings.FPS)
    screen.fill('#000000')
