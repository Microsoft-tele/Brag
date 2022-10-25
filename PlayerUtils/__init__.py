import random
import socket

from RoomUtils import DICE_NUM


class Box:
    # dice_box
    dices = list()

    def __init__(self, num: int):
        # 要输入每个盒子离得骰子数
        for i in range(num):
            self.dices.append(0)


class Player:
    # Player Class
    # @name:姓名
    # @dice_num:骰子数量
    # conn:sock连接对象
    def __init__(self, name: str, dice_num: int, conn: socket):
        # 输入 姓名 骰子数 sock连接对象
        self.name = name  # 玩家姓名
        self.dice_num = dice_num
        box = Box(dice_num)
        self.box = box
        self.conn: socket = conn

    def shook_dices(self):
        for i in range(self.dice_num):
            self.box.dices[i] = random.randint(1, 6)

    def show_dices(self) -> Box.dices:
        # print(self.name[:-1], "的骰子:", self.box.dices[:DICE_NUM])
        return self.box.dices[:DICE_NUM]
