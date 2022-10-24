import random
import socket


class Box:
    # dice_box
    dices = []

    def __init__(self, num: int):
        for i in range(num):
            self.dices.append(0)


class Player:
    # Player Class
    # @name:姓名
    # @dice_num:骰子数量
    # conn:sock连接对象
    def __init__(self, name: str, dice_num: int, conn: socket):
        self.name = name  # 玩家姓名
        box = Box(dice_num)
        self.box = box

    def shook_dices(self):
        for i in range(6):
            self.box.dices[i] = random.randint(1, 6)

    def show_dices(self) -> Box.dices:
        print(self.box, "的骰子:", self.box.dices)
        return self.box.dices
