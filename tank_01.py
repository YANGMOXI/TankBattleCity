# -*- coding: utf-8 -*-
# date: 2021/2/9 21:26

"""
坦克大战 —— 基础框架搭建

# 基于面向对象的分析
1.有哪些类？不同类对应的功能：
	1.主逻辑类
    	开始游戏
        结束游戏
    2.坦克类（a.我方坦克 b.敌方坦克）
    	移动
        射击
        展示坦克
    3.子弹类
    	移动
    4.爆炸效果类
    	展示爆炸效果
    5.墙壁类
    	属性：是否可以通过
    6.音效类
    	播放音乐
"""

import pygame

class MainGame:
    """主逻辑"""
    def __init__(self):
        pass

    def startGame(self):
        pass

    def stopGame(self):
        pass


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