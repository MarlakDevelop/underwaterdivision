import math
import pygame
from random import choice
from player import FirstShipPlayer, SecondShipPlayer, ThirdShipPlayer
from enemies import DemonZombieEnemy, CacoDemonEnemy, UberDemonEnemy, SatanEnemy
from particles import Bubble
from data_controller import DataController
import settings


pygame.mixer.pre_init(44100, -16, 1, 2**12)


class Menu:
    def __init__(self, size):
        global dataController

        self.width, self.height = size
        self.bg = pygame.image.load('assets/sprites/bg/1.jpg')
        self.shop_page = True
        self.profile_page = False
        self.shopShipsById = {}
        for elem in dataController.ships:
            image = pygame.transform.scale(pygame.image.load(elem['sprite']), (100, 100))
            self.shopShipsById[str(elem['id'])] = image

    def handleEvents(self, events):
        global running

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.shop_page:
                    self._handleShopPageClickEvent(event)
                elif self.profile_page:
                    self._handleProfilePageClickEvent(event)
                else:
                    self._handleTitlePageClickEvent(event)

    def _handleTitlePageClickEvent(self, event):
        global gameState

        if event.pos[1] < self.height - 100:
            gameState = {
                'menu': False,
                'isPlaying': True,
                'over': False
            }
        elif event.pos[0] in range(self.width - 260, self.width - 60) and event.pos[1] in range(self.height - 70, self.height - 20):
            self.profile_page = True
            self.shop_page = False

        elif event.pos[0] in range(60, 260) and event.pos[1] in range(self.height - 70, self.height - 20):
            self.profile_page = False
            self.shop_page = True

    def _handleShopPageClickEvent(self, event):
        if event.pos[0] in range(100, 100 + 400) and event.pos[1] in range(self.height - 70, self.height - 70 + 50):
            self.profile_page = False
            self.shop_page = False

    def _handleProfilePageClickEvent(self, event):
        if event.pos[0] in range(100, 100 + 400) and event.pos[1] in range(self.height - 70, self.height - 70 + 50):
            self.profile_page = False
            self.shop_page = False

    def render(self):
        if self.shop_page:
            self._renderShopPage()
        elif self.profile_page:
            self._renderProfilePage()
        else:
            self._renderTitlePage()

    def _renderTitlePage(self):
        screen.blit(self.bg, (0, 0))
        titleFont = pygame.font.Font(None, 72)
        title = titleFont.render('Underwater Division', True, (0, 180, 0))
        descFont = pygame.font.Font(None, 36)
        desc = descFont.render('Нажмите, что-бы начать', True, (255, 255, 255))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 190))
        screen.blit(desc, (self.width // 2 - desc.get_width() // 2, 200 + title.get_height()))

        shopFont = pygame.font.Font(None, 40)
        shop = shopFont.render('Магазин', True, (255, 255, 255))
        pygame.draw.rect(screen, pygame.Color(0, 180, 0), (60, self.height - 70, 200, 50))
        screen.blit(shop, (80, self.height - 60))

        profileFont = pygame.font.Font(None, 40)
        profile = profileFont.render('Статистика', True, (255, 255, 255))
        pygame.draw.rect(screen, pygame.Color(0, 180, 0), (self.width - 260, self.height - 70, 200, 50))
        screen.blit(profile, (self.width - profile.get_width() - 80, self.height - 60))

    def _renderShopPage(self):
        global dataController

        screen.blit(self.bg, (0, 0))

        vault = dataController.personal['powerPointsTotalCollected'] - dataController.personal['powerPointsSold']

        vaultFont = pygame.font.Font(None, 32)
        vaultText = vaultFont.render(f'Очков силы: {vault}', True, (180, 180, 0))
        screen.blit(vaultText, (10, 10))

        titleFont = pygame.font.Font(None, 72)
        title = titleFont.render('Магазин', True, (255, 255, 255))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 40))
        ships = dataController.ships
        for i in range(len(ships)):
            screen.blit(self.shopShipsById[str(ships[i]['id'])], (100, 160 * (i + 1)))
            if ships[i]['isBought'] is False:
                color = pygame.Color(180, 180, 0)
                text = f'{ships[i]["cost"]} очк.'
            elif ships[i]['isUsing']:
                color = pygame.Color(180, 0, 180)
                text = 'Используется'
            else:
                color = pygame.Color(0, 180, 0)
                text = 'Использовать'
            pygame.draw.rect(screen, color, (240, 160 * (i + 1) + 20, 260, 60))
            pygame.draw.rect(screen, (80, 80, 80), (240, 160 * (i + 1) + 20, 260, 60), 5)
            textFont = pygame.font.Font(None, 30)
            textText = textFont.render(text, True, (255, 255, 255))
            screen.blit(textText, (260, 160 * (i + 1) + 40))
        menuFont = pygame.font.Font(None, 40)
        menu = menuFont.render('Обратно', True, (255, 255, 255))
        pygame.draw.rect(screen, pygame.Color(0, 180, 0), (100, self.height - 70, 400, 50))
        screen.blit(menu, (self.width // 2 - menu.get_width() // 2, self.height - 60))

    def _renderProfilePage(self):
        global dataController

        screen.blit(self.bg, (0, 0))
        titleFont = pygame.font.Font(None, 72)
        title = titleFont.render('Личная статистика', True, (255, 255, 255))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 200))

        totalPowerPointsFont = pygame.font.Font(None, 30)
        totalPowerPoints = totalPowerPointsFont.render(f'Очков силы собрано за всё время: {dataController.personal["powerPointsTotalCollected"]}', True, (255, 255, 255))
        screen.blit(totalPowerPoints, (50, 280))

        maxPowerPointsFont = pygame.font.Font(None, 30)
        maxPowerPoints = maxPowerPointsFont.render(f'Максимум очков силы собрано за раунд: {dataController.personal["maxPowerPointsCollected"]}', True, (255, 255, 255))
        screen.blit(maxPowerPoints, (50, 330))

        powerPointsSoldFont = pygame.font.Font(None, 30)
        powerPointsSold = powerPointsSoldFont.render(f'Потрачено очков силы: {dataController.personal["powerPointsSold"]}', True, (255, 255, 255))
        screen.blit(powerPointsSold, (50, 380))

        menuFont = pygame.font.Font(None, 40)
        menu = menuFont.render('Обратно', True, (255, 255, 255))
        pygame.draw.rect(screen, pygame.Color(0, 180, 0), (100, self.height - 70, 400, 50))
        screen.blit(menu, (self.width // 2 - menu.get_width() // 2, self.height - 60))


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
        self.bg = pygame.image.load('assets/sprites/bg/1.jpg')
        self.width, self.height = size
        self.spawnPlayer()
        self.bullet_delay = 0
        self.enemies = []
        self.bullets = []
        self.particles = {
            'bubbles': []
        }
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
        global dataController

        try:
            ship_id = list(filter(lambda x: x['isUsing'] is True, dataController.ships))[0]['id']
            if ship_id == 1:
                self.player = FirstShipPlayer(self.width // 2, self.height - 250)
            elif ship_id == 2:
                self.player = SecondShipPlayer(self.width // 2, self.height - 250)
            elif ship_id == 3:
                self.player = ThirdShipPlayer(self.width // 2, self.height - 250)
            else:
                raise Exception
        except Exception:
            self.player = FirstShipPlayer(self.width // 2, self.height - 250)

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
                    bubbles = []
                    bubblesNum = choice(range(10, 20))
                    for j in range(bubblesNum):
                        bubbles.append(Bubble(choice(range(2, 4)),
                                              choice(range(self.player.cords['x'] - round(self.player.radius * 1.5) + 10,
                                                           self.player.cords['x'] + round(self.player.radius * 1.5) - 10)),
                                              choice(range(self.player.cords['y'] + self.player.radius // 3,
                                                           self.player.cords['y'] + self.player.radius))))
                    self.particles['bubbles'] += bubbles
                    if ((self.player.cords['x'] > self.player.radius or x - self.state['mouseCords'][0] > 0) and
                            (self.player.cords['x'] < self.width - self.player.radius or x - self.state['mouseCords'][0] < 0)):
                        if x - self.state['mouseCords'][0] > 0:
                            self.player.rotation_angle -= 1
                            self.player.rotation_angle = max(self.player.rotation_angle, -40)
                        else:
                            self.player.rotation_angle += 1
                            self.player.rotation_angle = min(self.player.rotation_angle, 40)
                        self.player.cords['x'] += x - self.state['mouseCords'][0]
                    if (self.player.cords['y'] > self.player.radius or y - self.state['mouseCords'][1] > 0) and (self.player.cords['y'] < self.height - self.player.radius or y - self.state['mouseCords'][1] < 0):
                        self.player.cords['y'] += y - self.state['mouseCords'][1]

                self.state['mouseCords'] = x, y

    def handleForGameOver(self):
        global gameState

        for enemy in self.enemies:
            if enemy.cords['y'] + enemy.radius > self.height:
                gameState = {
                    'menu': False,
                    'isPlaying': False,
                    'over': True
                }
                self.gameOver()

    def handleEnemiesConnectWithPlayer(self):
        global gameState

        for enemy in self.enemies:
            len1 = abs(enemy.cords['y'] - self.player.cords['y'])
            len2 = abs(enemy.cords['x'] - self.player.cords['x'])
            d = (len1 ** 2 + len2 ** 2) ** 0.5
            flag = False
            if d < enemy.radius + self.player.radius:
                flag = True
                self.player.death()
            elif d == self.player.radius + enemy.radius:
                flag = True
                self.player.death()
            elif d + self.player.radius == enemy.radius:
                flag = True
                self.player.death()
            elif d < enemy.radius - self.player.radius or d + self.player.radius < enemy.radius:
                flag = True
                self.player.death()
            if flag:
                gameState = {
                    'menu': False,
                    'isPlaying': False,
                    'over': True
                }
                self.gameOver()

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
            else:
                bubbles = []
                bubblesNum = 1
                for j in range(bubblesNum):
                    bubbles.append(Bubble(choice(range(1, 3)),
                                          choice(range(self.bullets[i].cords['x'] - self.bullets[i].radius,
                                                       self.bullets[i].cords['x'] + self.bullets[i].radius)),
                                          choice(range(self.bullets[i].cords['y'] - self.bullets[i].radius,
                                                       self.bullets[i].cords['y'] + self.bullets[i].radius))))
                    bubbles[-1].beforeDestroy = 10
                self.particles['bubbles'] += bubbles
        for i in indexes:
            try:
                del self.bullets[i]
            except Exception:
                pass
        for bullet in self.bullets:
            bullet.cords['x'] += int(bullet.speed * bullet.direction['x_cof'])
            bullet.cords['y'] += int(bullet.speed * bullet.direction['y_cof'])
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

    def updateParticles(self):
        indexes = []
        for i in range(len(self.particles['bubbles'])):
            self.particles['bubbles'][i].beforeDestroy -= 1
            if self.particles['bubbles'][i].beforeDestroy <= 0:
                indexes.append(i)
        for i in indexes:
            try:
                del self.particles['bubbles'][i]
            except Exception:
                pass

    def render(self):
        screen.blit(self.bg, (0, 0))
        for bubble in self.particles['bubbles']:
            screen.blit(bubble.sprite, (bubble.cords['x'] - bubble.radius, bubble.cords['y'] - bubble.radius, bubble.radius * 2, bubble.radius * 2))
        for bullet in self.bullets:
            screen.blit(bullet.sprite, (bullet.cords['x'] - bullet.radius, bullet.cords['y'] - bullet.radius, bullet.radius * 2, bullet.radius * 2))
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
        screen.blit(self.player.rotated_sprite, (self.player.cords['x'] - self.player.rotated_sprite.get_width() // 2,
                                                 self.player.cords['y'] - self.player.radius,
                                                 self.player.radius * 2, self.player.radius * 2))
        # hellLight = pygame.Surface()
        scoreFont = pygame.font.Font(None, 36)
        score = scoreFont.render(f'Очки силы: {game.score}', True, (255, 255, 255))
        scoreSurface = pygame.Surface((self.width - 100, 20 + score.get_height()))
        scoreSurface.set_alpha(200)
        pygame.draw.rect(scoreSurface, pygame.Color(0, 180, 0), (0, 0, scoreSurface.get_width(), scoreSurface.get_height()))
        scoreSurface.blit(score, (scoreSurface.get_width() // 2 - score.get_width() // 2, 10))
        screen.blit(scoreSurface, (50, 80))

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

    def gameOver(self):
        global dataController

        dataController.personal["powerPointsTotalCollected"] += self.score
        if self.score > dataController.personal["maxPowerPointsCollected"]:
            dataController.personal["maxPowerPointsCollected"] = self.score

    def handleGameOverEvents(self, events):
        global running, gameState

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.restart()
                gameState = {
                    'menu': False,
                    'isPlaying': True,
                    'over': False
                }

    def gameOverRender(self):
        self.render()


dataController = DataController()
dataController.load_personal_data()
dataController.load_ships_data()
pygame.init()
pygame.display.set_caption('')
clock = pygame.time.Clock()
size = width, height = 600, 800
screen = pygame.display.set_mode(size)
running = True
gameState = {
    'menu': True,
    'over': False,
    'isPlaying': False
}
menu = Menu(size)
game = Game(size)
while running:
    if gameState['menu']:
        menu.handleEvents(pygame.event.get())
        menu.render()
    if gameState['isPlaying']:
        game.handleEvents(pygame.event.get())
        game.updateEnemies()
        game.updateBullets()
        game.updateParticles()
        game.handleEnemiesConnectWithPlayer()
        game.handleBulletsConnectWithEnemies()
        game.render()
        game.player.update()
        game.tryShoot()
        game.handleForGameOver()
    if gameState['over']:
        game.handleGameOverEvents(pygame.event.get())
        game.gameOverRender()
    pygame.display.flip()
    clock.tick(settings.FPS)
    screen.fill('#000000')
dataController.dump_personal_data()
dataController.dump_ships_data()
