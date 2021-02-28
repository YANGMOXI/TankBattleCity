# -*- coding: utf-8 -*-
# date: 2021/2/9 22:39

"""
坦克大战 v1.24

新增功能：
    1.音效处理（pygame.mixer.music模块）
        我方坦克出生
        发生子弹
        爆炸
"""

import pygame
import time
import random

_display = pygame.display
COLOR_GRAY = pygame.Color(125, 125, 125)
COLOR_BLACK = pygame.Color(0, 0, 0)
VERSION = 'v1.24'
P1_TANK_SIZE = pygame.image.load('img/p1tankU.gif').get_size()


class MainGame:
    """主逻辑"""
    window = None  # 游戏主窗口
    SCREEN_HIGHT = 500
    SCREEN_WIDTH = 800
    # 创建我方坦克
    TANK_P1 = None
    # 创建敌方坦克
    EnemyTank_list = []
    EnemyTank_count = 4
    # 我方子弹 — 存储列表
    Bullet_list = []
    # 敌方子弹 — 存储列表
    Enemy_bullet_list = []
    # 爆炸效果列表
    Explode_list = []
    # 墙壁列表
    Wall_list = []

    def startGame(self):
        """开始游戏"""
        pygame.display.init()
        # 创建窗口，加载窗口 -> surface（画布）
        MainGame.window = _display.set_mode(size=(MainGame.SCREEN_WIDTH, MainGame.SCREEN_HIGHT))
        # 出场音乐
        music = Music('img/start.wav')
        music.play()
        # 创建我方坦克
        self.createMyTank()
        # 创建敌方坦克
        self.createEnemyTank()
        # 创建墙壁
        self.createWalls()

        # 设置游戏标题
        _display.set_caption('坦克大战%s' % VERSION)

        # 让窗口持续刷新操作
        while True:
            MainGame.window.fill(COLOR_BLACK)  # 给窗口 纯色填充
            self.getEvent()  # 持续完成事件的获取
            # 调用展示墙壁的方法
            self.blitWalls()
            # 将绘制文字的画布 展示到窗口中
            MainGame.window.blit(self.getTextSurface('剩余敌方坦克%d辆' % len(MainGame.EnemyTank_list)), (10, 10))  # 小画布; 坐标
            # 我方坦克 —— 在窗口中显示
            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                MainGame.TANK_P1.displayTank()
            # 敌方坦克 —— 在窗口中显示
            self.blitEnemyTank()
            # 根据tank移动开关状态进行移动
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                # 坦克碰撞墙壁 - 还原坐标
                MainGame.TANK_P1.hitwalls()
                MainGame.TANK_P1.hitEnemyTank()
            # 我方 - 渲染子弹列表方法
            self.blitBullet()
            # 敌方 - 渲染子弹列表方法
            self.blitEnemyBullet()
            # 爆炸效果 - 我方子弹碰撞敌方坦克
            self.displayExplodes()

            time.sleep(0.02)
            # 窗口刷新
            _display.update()

    def createMyTank(self):
        MainGame.TANK_P1 = MyTank((MainGame.SCREEN_WIDTH - P1_TANK_SIZE[0]) / 2,
                                  MainGame.SCREEN_HIGHT - P1_TANK_SIZE[1])  # 初始位置


    def createEnemyTank(self):
        """敌方坦克 —— 创建坦克"""
        # 生成位置范围
        top = 0
        for i in range(MainGame.EnemyTank_count):
            speed = random.randint(3, 5)  # 每辆坦克速度不一样
            left = random.randint(1, 7)  # 横坐标区间 —— 允许重复
            eTank = EnemyTank(left * 100, top, speed)
            MainGame.EnemyTank_list.append(eTank)

    def createWalls(self):
        """随机创建 - 简易版 - y轴固定"""
        for i in range(1, 6):
            for j in range(2, 4):
                wall = Wall(i*130, j*60)
                MainGame.Wall_list.append(wall)

    def blitWalls(self):
        """墙壁 —— 加入到窗口中"""
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.Wall_list.remove(wall)


    def blitEnemyTank(self):
        """敌方坦克 —— 加入到窗口中"""
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()
                eTank.randomMove()
                eTank.hitwalls()
                eTank.hitMyTank()
                # 射击（随机性）—— 产生子弹
                eBullet = eTank.shoot()
                if eBullet:  # 子弹 存储到敌方子弹列表
                    MainGame.Enemy_bullet_list.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)

    def blitBullet(self):
        """我方子弹 —— 加入到窗口中"""
        for bullet in MainGame.Bullet_list:
            if bullet.live:
                bullet.displayBullet()  # 展示子弹
                bullet.bulletMove()  # 子弹移动
                # 调用碰撞 —— 我方子弹 碰撞 敌方坦克
                bullet.hitEnemyTank()
                # 调用碰撞 - 我方子弹 是否碰撞 墙壁
                bullet.hitWalls()
            else:
                MainGame.Bullet_list.remove(bullet)

    def blitEnemyBullet(self):
        """敌方子弹 —— 加入到窗口中"""
        for eBullet in MainGame.Enemy_bullet_list:
            if eBullet.live:
                eBullet.displayBullet()
                eBullet.bulletMove()  # 子弹移动
                eBullet.hitWalls()  # 子弹是否撞墙
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    # 敌方子弹是否碰撞我方坦克
                    eBullet.hitMyTank()
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)  # 从列表中 删除子弹

    # 新增方法 —— 渲染爆炸列表方法
    def displayExplodes(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                print(self)
                explode.displayExplode()
                music = Music('music/blast.wav')
                music.play()
            else:
                MainGame.Explode_list.remove(explode)

    def getEvent(self):
        """获取程序期间所有事件（鼠标事件、键盘事件）"""
        # 获取所有事件
        # 对事件判断处理1.鼠标事件
        eventList = pygame.event.get()
        for event in eventList:
            # 点击关闭按钮（鼠标事件）
            if event.type == pygame.QUIT:
                self.endGame()
            # 按键判断
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not MainGame.TANK_P1.live:
                    # 坦克重生方法 —— 按Esc键
                    music = Music('music/add.wav')
                    music.play()
                    self.createMyTank()

                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    if event.key == pygame.K_LEFT:
                        print("坦克向左")
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'L'
                        # 移动操作
                        # MainGame.TANK_P1.move()
                        MainGame.TANK_P1.stop = False  # 打开开关
                    elif event.key == pygame.K_RIGHT:
                        print("坦克向右")
                        MainGame.TANK_P1.direction = 'R'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_UP:
                        print("坦克向上")
                        MainGame.TANK_P1.direction = 'U'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_DOWN:
                        print("坦克向下")
                        MainGame.TANK_P1.direction = 'D'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        print("发射子弹")
                        if len(MainGame.Bullet_list) < 5:
                            # 产生一颗子弹
                            m = Bullet(MainGame.TANK_P1)
                            # 将子弹加入子弹列表
                            MainGame.Bullet_list.append(m)
                            music = Music('music/fire.wav')
                            music.play()
                        else:
                            print("当前子弹数量不足")

                        print("当前子弹数量:%d" % len(MainGame.Bullet_list))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN and MainGame.TANK_P1.live:
                    MainGame.TANK_P1.stop = True  # 关闭开关——tank停止

    def getTextSurface(self, text):
        """绘制文字"""
        # 初始化字体模块
        pygame.font.init()
        # 选择字体样式
        # fontList = pygame.font.get_fonts()  # 获取系统上所有的字体
        font = pygame.font.SysFont(name='microsoftyaheimicrosoftyaheiui', size=16)
        # 文字内容绘制
        textSurface = font.render(text, True, COLOR_GRAY)  # 内容，抗锯齿，字颜色
        return textSurface

    def endGame(self):
        """结束游戏"""
        print("正在退出游戏...")
        exit()


class BasicItem(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)


class Tank(BasicItem):
    """坦克基类"""
    def __init__(self, left, top):
        self.images = {  # 坦克图片集
            'U': pygame.image.load('img/p1tankU.gif'),
            'D': pygame.image.load('img/p1tankD.gif'),
            'L': pygame.image.load('img/p1tankL.gif'),
            'R': pygame.image.load('img/p1tankR.gif'),
        }
        self.direction = 'U'  # 当前朝向
        self.image = self.images[self.direction]  # 当前坦克图片,从图集中获取 —— 与朝向相关联
        # 坦克所在位置（相对窗口） Rect ->
        self.rect = self.image.get_rect()
        # 指定初始化位置
        self.rect.left = left
        self.rect.top = top
        self.speed = 8  # 速度/单位位移
        self.stop = True  # 坦克移动开关
        self.live = True  # 记录坦克是否存活
        self.oldLeft = self.rect.left  # 记录坦克移动墙的坐标（用于坐标还原时使用）
        self.oldTop = self.rect.top

    def move(self):
        """移动"""
        # 先记录移动之前的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HIGHT:
                self.rect.top += self.speed

    def stay(self):
        """还原坐标"""
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    def hitwalls(self):
        """坦克碰撞墙壁"""
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()

    def shoot(self):
        """射击"""
        return Bullet(self)

    def displayTank(self):
        """
        展示坦克：将坦克surface绘制到窗口中
        实时刷新（调头）
        """
        # 1.重置坦克图片
        self.image = self.images[self.direction]
        # 2.将坦克加入到窗口
        MainGame.window.blit(self.image, self.rect)


class MyTank(Tank):
    """我方坦克"""
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)

    def hitEnemyTank(self):
        """主动碰撞敌方坦克"""
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(self, eTank):
                self.stay()


class EnemyTank(Tank):
    """敌方坦克"""
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)
        # 图片集合
        self.images = {  # 敌方坦克图片集
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif'),
        }
        self.direction = self.randomDirection()  # 随机方向
        self.image = self.images[self.direction]  # 当前坦克图片,从图集中获取 —— 与朝向相关联
        # 坦克所在位置（相对窗口） Rect ->
        self.rect = self.image.get_rect()
        # 指定初始化位置
        self.rect.left = left
        self.rect.top = top
        self.speed = speed  # 速度
        self.stop = True  # 移动开关
        self.step = 50  # 步数，控制随机移动

    def randomDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    def randomMove(self):
        """随机移动"""
        if self.step <= 0:
            # 每20步重置
            self.direction = self.randomDirection()
            self.step = 50
        else:
            self.move()
            self.step -= 1
        time.sleep(0.02)

    def shoot(self):
        """随机产生子弹 —— 重写父类"""
        num = random.randint(1, 30)
        if num == 1:
            return Bullet(self)

    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
            self.stay()


class Bullet(BasicItem):
    """子弹类"""
    def __init__(self, tank):
        # 图片
        self.image = pygame.image.load('img/tankmissile.gif')
        # 方向（坦克的方向）
        self.direction = tank.direction
        # 速度
        self.speed = MainGame.TANK_P1.speed * 1.5
        # 坐标
        self.rect = self.image.get_rect()
        # 初始化位置需根据坦克的方向进行调整
        if self.direction == 'U':
            # self.rect.left += (坦克宽度的一半 - 子弹宽度的一半)
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.width / 2
        # 标签 - 记录子弹是否撞到墙壁
        self.live = True

    def bulletMove(self):
        """子弹移动"""
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:  # 撞墙消失
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False

    def displayBullet(self):
        """展示子弹 - 在窗口中显示"""
        MainGame.window.blit(self.image, self.rect)

    def hitEnemyTank(self):
        """我方子弹 碰撞 敌方坦克的方法"""
        for eTank in MainGame.EnemyTank_list:
            # 碰撞算法(rect：2矩形是否有交集) -> bool
            if pygame.sprite.collide_rect(self, eTank):
                # 产生一个爆炸效果； 加入爆炸效果列表
                explode = Expolde(eTank)
                MainGame.Explode_list.append(explode)
                self.live = False
                eTank.live = False

    def hitMyTank(self):
        """我方子弹 碰撞 敌方坦克的方法"""
        if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
            # 产生一个爆炸效果； 加入爆炸效果列表
            explode = Expolde(MainGame.TANK_P1)
            MainGame.Explode_list.append(explode)
            self.live = False
            MainGame.TANK_P1.live = False

    def hitWalls(self):
        """子弹与墙壁的碰撞"""
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.live = False  # 子弹消失
                music = Music('music/hit.wav')
                music.play()
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live = False


class Expolde:
    """爆炸效果 - 多张图：从小到大，最后消失"""
    def __init__(self, tank):
        self.step = 0  # 爆炸阶段
        self.images = [  # 爆炸效果图片集
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif'),
            pygame.image.load('img/blast5.gif')
        ]
        self.image = self.images[self.step]
        self.rect = self.image.get_rect()
        self.rect.top = tank.rect.top - (self.rect.height / 2 - tank.rect.height / 2)
        self.rect.left = tank.rect.left - (self.rect.width / 2 - tank.rect.width / 2)
        self.live = True

    def displayExplode(self):
        """展示爆炸"""
        if self.step < len(self.images):
            MainGame.window.blit(self.image, self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.live = False
            self.step = 0


class Wall:
    """墙壁类"""
    def __init__(self, left, top):
        self.image = pygame.image.load('img/walls.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 1 # 记录墙壁的生命值

    def displayWall(self):
        """展示墙壁（障碍物）"""
        MainGame.window.blit(self.image, self.rect)



class Music:
    """音效"""
    def __init__(self, fileName):
        self.fileName = fileName
        # 初始化混响器
        pygame.mixer.init()
        pygame.mixer.music.load(fileName)

    def play(self):
        """开始播放音乐"""
        pygame.mixer.music.play(loops=0)  # loops播放次数  -1循环
        pass


if __name__ == '__main__':
    MainGame().startGame()
