import random
import threading
import time
from socket import *

from typing import Tuple, List

import PlayerUtils
from main import BUFFER_SIZE

DICE_NUM = 5  # @TODO 默认是5个骰子,这里就不让用户进行修改了，如果需要后续再进行拓展
dice_res = []  # 用于存放结果 每个人的骰子数
dice_point_statistic = [0, 0, 0, 0, 0, 0]


def win_or_lose(is_1_activate, dice_num, dice_point_num) -> bool:
    if is_1_activate == 1:  # 赖子生效
        print("玩家骰子数：", dice_num)
        print("玩家骰子点数：", dice_point_num)
        have_dic_point_num = dice_point_statistic[dice_point_num - 1] + dice_point_statistic[0]
        print("本轮骰子数:", have_dic_point_num)
        if have_dic_point_num >= dice_num:
            print("上家赢")
            return True
    else:  # 赖子不生效
        have_dic_point_num = dice_point_statistic[dice_point_num - 1]
        if have_dic_point_num < dice_num:
            print("下家赢")
            return False


def statistic_dices_num():
    global dice_point_statistic
    dice_point_statistic = [0, 0, 0, 0, 0, 0]
    for i in dice_res:
        for j in i:
            if j == 1:
                dice_point_statistic[0] = dice_point_statistic[0] + 1
            elif j == 2:
                dice_point_statistic[1] = dice_point_statistic[1] + 1
            elif j == 3:
                dice_point_statistic[2] = dice_point_statistic[2] + 1
            elif j == 4:
                dice_point_statistic[3] = dice_point_statistic[3] + 1
            elif j == 5:
                dice_point_statistic[4] = dice_point_statistic[4] + 1
            elif j == 6:
                dice_point_statistic[5] = dice_point_statistic[5] + 1
    print("本轮所有玩家骰子统计结果:", dice_point_statistic)


def broadcast_result(players):
    print("有人选择开上家，现在公布本轮骰子结果:")
    for i in players:
        i: PlayerUtils.Player
        i.conn.send("有人选择开上家，现在公布本轮骰子结果:\n".encode(encoding='utf_8'))

    for i in range(len(players)):
        print(f"{players[i].name[:-1]} : {dice_res[i]}")
        for j in range(len(players)):
            players[i].conn.send(f"{players[j].name[:-1]} : {dice_res[j]}\n".encode(encoding='utf_8'))

    for i in range(len(players)):
        players[i].conn.send(
            f"本轮统计结果:[1, 2, 3, 4, 5 ，6]点的数量是:{dice_point_statistic}\n".encode(encoding='utf_8'))


def broadcast_operate(current_player_name, players, operate, dice_num, dice_point_num):
    operate: int  # 0代表吹牛 1代表开上家
    for i in players:
        i: PlayerUtils.Player
        if operate == 0:
            i.conn.send(
                f"[广播]: {current_player_name}  选择的是[吹牛]: 数目是:[{dice_num} 个 {dice_point_num}]\n"
                .encode(encoding='utf_8'))
        elif operate == 1:
            i.conn.send(
                f"[广播]: {current_player_name}  选择的是[开上家]:\n".encode(
                    encoding='utf_8'))


class Room:
    # 房间对象
    room_host_conn: socket  # 房主的连接
    room_id = None  # 顺便充当端口号
    room_conn = None  # 服务器地址
    players_conn_list = list()  # 玩家连接socket
    is_start_game = False
    players = []

    def __init__(self, room_host_conn: Tuple[socket, any]):
        self.room_id = random.randint(10000, 999999)
        self.room_host_conn = room_host_conn[0]

    def create_room(self, player_num: int):  # 需要创建房间的传入本房间的最大人数
        while True:
            addr = ("0.0.0.0", self.room_id)  # 游戏房间的地址
            sock = socket(AF_INET, SOCK_STREAM)
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            try:
                sock.bind(addr)
                sock.listen(player_num)
                break
            except:
                self.room_id = random.randint(10000, 999999)

        self.room_conn = sock
        print("创建新的sock成功：成功创建房间：")
        print(self.room_conn)
        print("当前房间端口号:", self.room_id)
        print("当前连接即将关闭，即将加入游戏房间:")
        self.players_conn_list.append(self.room_host_conn)  # 将房主加入到房间中

        self.room_host_conn.send("请输入姓名准备开始游戏:\n".encode(encoding='utf_8'))
        name = self.room_host_conn.recv(BUFFER_SIZE).decode('utf8')
        print("房主的姓名:", name)
        player_obj = PlayerUtils.Player(name, DICE_NUM, self.room_host_conn)
        self.players.append(player_obj)

        print(self.players_conn_list)
        self.room_host_conn.send(
            f"创建的房间号:  {self.room_id}\n将房间号分享给您的好友即可加入游戏了\n".encode(encoding='utf_8'))

    def accept_players(self):
        # 等待玩家进入房间
        while True:
            player, remote_addr = self.room_conn.accept()
            self.players_conn_list.append(player)  # 加入连接链表中
            print("新加入的用户:", player)
            player.send("请输入姓名准备开始游戏:\n".encode(encoding='utf_8'))
            name = player.recv(BUFFER_SIZE).decode('utf8')
            print(player.getsockname(), "玩家输入的姓名", name)
            player_obj = PlayerUtils.Player(name, DICE_NUM, player)
            self.players.append(player_obj)
            player.send("请等待游戏开始:\n".encode(encoding='utf_8'))

    def play_game(self):
        global dice_point_statistic, dice_res
        for i in self.players:
            i: PlayerUtils.Player
            i.conn.send("游戏开始，其他玩家无法继续加入本房间:\n".encode(encoding='utf_8'))

        player_num = len(self.players)
        print("当前加入房间的人数是:", player_num)
        print("当前玩家对象:")
        for i in self.players:
            print(i)

        # @TODO 可以加一个调换顺序的功能，在这里就不实现了，有兴趣的同学可以加进来
        start: int = 0  # 第一个开始吹牛的人，简称庄家，这里先初始设置成创建房间的人，如果有需求的话需要增加上述功能TODO
        while True:
            del dice_res[:]
            dice_res = []
            for i in range(player_num):  # @TODO 这里要设置循环队列来保证游戏不会结束
                self.players[i].shook_dices()
                self.players[i].conn.send(
                    ("您本轮掷出的点数为:" + str(self.players[i].show_dices()) + "\n").encode(encoding='utf_8'))
                dice_res.append(self.players[i].show_dices())  # 记录结果

            statistic_dices_num()  # 每轮骰子掷完都进行统计
            flag = 0  # 记录本局是否为庄家
            is_over = 0  # 记录当前对局是否结束
            is_1_activate = 1  # 记录1这个赖子点数是否生效
            dice_num = 0  # 记录上一名玩家说出的骰子数
            dice_point_num = 0  # 记录上一名玩家说出的骰子点数

            i = start  # 设置本轮进行操作的玩家的下标
            while True:
                #  for i in range(player_num):  # @TODO 循环列表防止一轮之内没人开
                if i == player_num:
                    i = 0

                if is_over == 1:  # 如果检测到结束标志就结束本次循环
                    break
                if flag == 0:  # 代表庄主，没有开上一个人的选项
                    self.players[i].conn.send(
                        "轮到您吹牛啦:\n输入[骰子数][骰子点数]\n例如：10个3 则输入 10[space]3\n开始吹牛:\n".encode(
                            encoding='utf_8'))
                    num_str: str = self.players[i].conn.recv(BUFFER_SIZE).decode('utf8')
                    num_list = num_str.split(' ')
                    dice_num = int(num_list[0])
                    dice_point_num = int(num_list[1])
                    print(self.players[i].name[:-1], "的输入是:", dice_num, ":", dice_point_num, type(dice_num),
                          type(dice_point_num))
                    # 操作完毕，进行广播操作
                    broadcast_operate(self.players[i].name[:-1], self.players, 0, dice_num, dice_point_num)
                    flag = 1
                    i = i + 1
                else:
                    while True:
                        self.players[i].conn.send("轮到您吹牛啦:\n输入[随意一个数]开上家\n输入[骰子数][骰子点数]自己吹牛\n例如：10个3 则输入 10 3\n"
                                                  "开始吹牛:\n".encode(encoding='utf_8'))
                        num_str = self.players[i].conn.recv(BUFFER_SIZE).decode('utf8')
                        num_list = num_str.split(' ')
                        print(num_list)
                        if len(num_list) == 1:  # 如果玩家输入只有一个数就代表开上家
                            op = int(num_list[0])
                            print(self.players[i].name[:-1], "的输入是:", op, "开上家")
                            broadcast_operate(self.players[i].name[:-1], self.players, 1, 0, 0)  # 广播操作
                            broadcast_result(self.players)
                            # 判断上家的吹牛情况
                            is_win = win_or_lose(is_1_activate, dice_num, dice_point_num)
                            if is_win:
                                # 广播
                                for player in self.players:
                                    player.conn.send(
                                        f"上家[{self.players[(i - 1) % player_num].name[:-1]}]赢！！！本局结束\n\n\n".encode(
                                            encoding='utf_8'))
                                start = i
                            else:
                                for player in self.players:
                                    player.conn.send(
                                        f"下家[{self.players[i].name[:-1]}]赢！！！本局结束\n\n\n".encode(
                                            encoding='utf_8'))
                                start = i - 1

                            is_over = 1  # 记录本局结束
                            break  # 本局结束
                        else:  # 如果玩家输入的不是一个数
                            dice_num_tmp = int(num_list[0])
                            dice_point_num_tmp = int(num_list[1])

                            if dice_num_tmp * dice_point_num_tmp == 0:  # 玩家输入了一个0则判断输入不合法
                                print("骰子数或骰子点数不能输入0，请重新输入:")
                                self.players[i].conn.send(
                                    "骰子数或骰子点数不能输入0，请重新输入:\n".encode(encoding='utf_8'))
                            elif dice_num_tmp != 0 and dice_point_num_tmp == 1:  # 如果有人吹牛的点数是1,则本轮赖子失效
                                self.players[i].conn.send(
                                    "您使用了本轮的特权，赖子1在本轮不再生效:\n".encode(encoding='utf_8'))
                                dice_num = dice_num_tmp
                                dice_point_num = dice_point_num_tmp
                                print("继续吹牛:", dice_num, dice_point_num)
                                broadcast_operate(self.players[i].name[:-1], self.players, 0, dice_num,
                                                  dice_point_num)  # 广播操作
                                is_1_activate = 0
                                break
                            elif dice_num_tmp == dice_num:  # 本轮叫的骰子数和上一人相等的话，骰子点数必须大于上一人叫的点数
                                if dice_point_num_tmp <= dice_point_num:
                                    print("您选择的点数不能小于上家，或您的骰子数应大于上家:")
                                    self.players[i].conn.send(
                                        "您选择的点数不能小于上家，或您的骰子数应大于上家，请重新输入:\n".encode(
                                            encoding='utf_8'))
                                else:
                                    dice_num = dice_num_tmp
                                    dice_point_num = dice_point_num_tmp
                                    print("继续吹牛:", dice_num, dice_point_num)
                                    broadcast_operate(self.players[i].name[:-1], self.players, 0, dice_num,
                                                      dice_point_num)  # 广播操作
                                    break
                            elif dice_num_tmp < dice_num:  # 如果输入的骰子数小于上家则判断输入不合法
                                print("您输入的骰子数应大于上家，请重新输入:")
                                self.players[i].conn.send(
                                    "您输入的骰子数应大于上家，请重新输入:\n".encode(encoding='utf_8'))
                            else:
                                dice_num = dice_num_tmp
                                dice_point_num = dice_point_num_tmp
                                print("继续吹牛:", dice_num, dice_point_num)
                                broadcast_operate(self.players[i].name[:-1], self.players, 0, dice_num,
                                                  dice_point_num)  # 广播操作
                                break
                    i = i + 1
