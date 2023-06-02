import pygame
import random


# 初始化pygame
pygame.init()

# 设置游戏窗口大小和标题
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alien Invasion")

# 加载背景音乐和字体
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
font = pygame.font.SysFont(None, 48)

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 定义玩家飞船类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 5
        self.lives = 3

    def update(self):
        # 控制飞船左右移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    def shoot(self):
        # 发射子弹
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# 定义外星人类
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("alien.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

    def update(self):
        # 控制外星人下落
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 3)

# 定义子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        # 控制子弹上升
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# 创建玩家、外星人、子弹等精灵组
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# 创建一些初始的外星人
for i in range(10):
    alien = Alien()
    all_sprites.add(alien)
    aliens.add(alien)

# 设置游戏主循环
clock = pygame.time.Clock()
running = True
while running:
    # 控制游戏帧率
    clock.tick(60)

    # 处理游戏事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 更新游戏状态
    all_sprites.update()

    # 处理碰撞事件
    hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
    for hit in hits:
        alien = Alien()
        all_sprites.add(alien)
        aliens.add(alien)

    hits = pygame.sprite.spritecollide(player, aliens, True)
    for hit in hits:
        player.lives -= 1
        if player.lives == 0:
            running = False
        else:
            alien = Alien()
            all_sprites.add(alien)
            aliens.add(alien)

    # 绘制游戏画面
    screen.fill(black)
    all_sprites.draw(screen)
    lives_text = font.render("Lives: " + str(player.lives), True, white)
    screen.blit(lives_text, (10, 10))
    pygame.display.flip()

# 游戏结束后显示得分和排名
score_text = font.render("Score: " + str(player.score), True, white)
screen.blit(score_text, (screen_width // 2 - 100, screen_height // 2 - 50))
pygame.display.flip()
pygame.time.delay(2000)

# 退出游戏
pygame.quit()