# -*- coding: utf-8 -*-
# date: 2021/2/9 21:26

"""
坦克大战 v1.02

新增功能：
    创建游戏窗口 —— pygame中模块使用
"""

import pygame

_display = pygame.display
COLOR_GRAY = pygame.Color(125,125,125)

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
        _display.set_caption('坦克大战v1.02')
        # 让窗口持续刷新操作
        while True:
            MainGame.window.fill(MainGame.COLOR_GRAY) # 给窗口 纯色填充
            _display.update()


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
    MainGame().startGame()