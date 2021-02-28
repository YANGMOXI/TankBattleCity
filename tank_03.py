# -*- coding: utf-8 -*-
# date: 2021/2/9 22:39

"""
坦克大战 v1.03

新增功能：
    事件处理：
        点击关闭按钮，退出程序的事件
        方向控制
        子弹发射
"""


import pygame

_display = pygame.display
COLOR_GRAY = pygame.Color(125,125,125)
VERSION = 'v1.03'

class MainGame:
    """主逻辑"""
    window = None # 游戏主窗口
    SCREEN_WIDTH = 800
    SCREEN_HIGHT = 500

    def __init__(self):
        pass

    def startGame(self):
        """开始游戏"""
        pygame.display.init()
        # 创建窗口，加载窗口 -> surface
        MainGame.window = _display.set_mode(size=(MainGame.SCREEN_WIDTH, MainGame.SCREEN_HIGHT))
        # 设置游戏标题
        _display.set_caption('坦克大战%s' %VERSION)
        # 让窗口持续刷新操作
        while True:
            MainGame.window.fill(COLOR_GRAY)  # 给窗口 纯色填充
            self.getEvent()  # 持续完成事件的获取
            _display.update()

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
                elif event.key == pygame.K_RIGHT:
                    print("坦克向右")
                elif event.key == pygame.K_UP:
                    print("坦克向上")
                elif event.key == pygame.K_DOWN:
                    print("坦克向下")
                elif event.key == pygame.K_SPACE:
                    print("发射子弹")


    def endGame(self):
        """结束游戏"""
        print("正在退出游戏...")
        exit()


class Tank:
    """坦克基类"""
    def __init__(self):
        pass

    def move(self):
        """移动"""
        pass

    def shoot(self):
        """射击"""
        pass

    def displayTank(self):
        """展示坦克"""
        pass


class MyTank(Tank):
    """我方坦克"""
    def __init__(self):
        pass


class EnemyTank(Tank):
    """敌方坦克"""
    def __init__(self):
        pass


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
