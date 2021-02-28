# -*- coding: utf-8 -*-
# date: 2021/2/9 22:39

"""
坦克大战 v1.09

新增敌方坦克：
	1.完善敌方坦克类
    2.创建敌方坦克，将敌方坦克展示到窗口中
"""


import pygame
import time
import random

_display = pygame.display
COLOR_GRAY = pygame.Color(125,125,125)
COLOR_BLACK = pygame.Color(0,0,0)
VERSION = 'v1.09'
P1_TANK_SIZE = pygame.image.load('img/p1tankU.gif').get_size()


class MainGame:
    """主逻辑"""
    window = None # 游戏主窗口
    SCREEN_HIGHT = 500
    SCREEN_WIDTH = 800
    # 创建我方坦克
    TANK_P1 = None
    # 创建敌方坦克
    EnemyTank_list = []
    EnemyTank_count = 6

    def __init__(self):
        pass

    def startGame(self):
        """开始游戏"""
        pygame.display.init()
        # 创建窗口，加载窗口 -> surface（画布）
        MainGame.window = _display.set_mode(size=(MainGame.SCREEN_WIDTH, MainGame.SCREEN_HIGHT))
        # 创建我方坦克
        MainGame.TANK_P1 = Tank((MainGame.SCREEN_WIDTH - P1_TANK_SIZE[0])/2, MainGame.SCREEN_HIGHT - P1_TANK_SIZE[1]) # 初始位置
        # 创建敌方坦克
        self.creatEnemyTank()

        # 设置游戏标题
        _display.set_caption('坦克大战%s' %VERSION)


        # 让窗口持续刷新操作
        while True:
            MainGame.window.fill(COLOR_BLACK)  # 给窗口 纯色填充
            self.getEvent()  # 持续完成事件的获取
            # 将绘制文字的画布 展示到窗口中
            MainGame.window.blit(self.getTextSurface('剩余敌方坦克%d辆' %len(MainGame.EnemyTank_list)), (10,10)) # 小画布; 坐标
            # 在窗口中 显示我方坦克
            MainGame.TANK_P1.displayTank()
            # 在窗口中 显示敌方坦克
            self.blitEnemyTnak()
            # 根据tank移动开关状态进行移动
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                time.sleep(0.02)
            # 窗口刷新
            _display.update()

    def creatEnemyTank(self):
        """创建敌方坦克"""
        # 生成位置范围
        top = 120
        speed = random.randint(3, 5)
        for i in range(MainGame.EnemyTank_count):
            left = random.randint(1, 7)  # 横坐标区间 —— 允许重复
            eTank = EnemyTank(left*100, top, speed)
            MainGame.EnemyTank_list.append(eTank)

    # 将坦克加入到窗口中
    def blitEnemyTnak(self):
        for eTank in MainGame.EnemyTank_list:
            eTank.displayTank()

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
                if event.key == pygame.K_LEFT:
                    print("坦克向左")
                    # 修改坦克方向
                    MainGame.TANK_P1.direction = 'L'
                    # 移动操作
                    # MainGame.TANK_P1.move()
                    MainGame.TANK_P1.stop = False # 打开开关

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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
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


class Tank:
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
        self.speed = 5  # 速度/单位位移
        self.stop = True  # 坦克移动开关

    def move(self):
        """移动"""
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

    def shoot(self):
        """射击"""
        pass

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
    def __init__(self):
        pass


class EnemyTank(Tank):
    """敌方坦克"""
    def __init__(self, left, top, speed):
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

    def randomDirection(self):
        num = random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    # def displayEnemyTank(self):
    #     super().displayTank()

class Bullet:
    """子弹类"""
    def __init__(self):
        pass

    def move(self):
        """子弹移动"""
        pass

    def displayBullet(self):
        """展示子弹"""
        pass


class Expolde:
    """爆炸效果"""
    def __init__(self):
        pass

    def displayExpolde(self):
        """展示爆炸"""
        pass


class Wall:
    """爆炸效果"""
    def __init__(self):
        pass

    def displayWall(self):
        """展示墙壁（障碍物）"""
        pass


class Music:
    """音效"""
    def __init__(self):
        pass

    def play(self):
        """开始播放音乐"""
        pass


if __name__ == '__main__':
    game1 = MainGame()
    game1.startGame()