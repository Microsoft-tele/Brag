from threading import Thread
from socket import *

import PlayerUtils
import RoomUtils

addr = ("0.0.0.0", 22222)
BUFFER_SIZE = 1024


def main():
    tcp_server = socket(AF_INET, SOCK_STREAM)
    tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcp_server.bind(addr)
    tcp_server.listen(10)

    while True:
        print("Waiting for connecting!")
        tcp_client_sock, remote_addr = tcp_server.accept()
        print("Remote Addr is:", remote_addr)
        print("A new client has appended to list:")
        Thread(target=process, args=(tcp_client_sock, remote_addr)).start()


def process(conn: socket, remote_addr: any):
    print("Enter child process:")
    conn.send("Have connected server successfully!".encode(encoding="utf_8"))
    while True:
        conn.send("欢迎进入吹牛大赛,请选择:\n".encode(encoding="utf_8"))
        conn.send("1.创建房间:\n".encode(encoding="utf_8"))
        conn.send("2.加入房间:\n".encode(encoding="utf_8"))
        data = conn.recv(BUFFER_SIZE)
        choice = int(data.decode('utf8'))
        print("用户输入的选项:", choice)
        if choice == 1:
            print("开始创建房间:")
            conn.send("开始创建房间:\n".encode(encoding="utf_8"))
            room = RoomUtils.Room((conn, remote_addr))
            room.create_room(10)  # @TODO 创建房间，并指定最大接入数量
            Thread(target=room.accept_players).start()  # 等待玩家进入房间
            while True:
                conn.send("房主已经加入房间，请等待其他成员:\n1. 开始游戏\n".encode(encoding='utf_8'))
                is_start_game = int(conn.recv(BUFFER_SIZE).decode('utf8'))  # 接收到1就开始游戏
                print("接收到房主的开始游戏信号:", is_start_game)
                if is_start_game == 1:
                    room.play_game()
                    while True:
                        pass
                else:
                    print("输入有误:")
                    conn.send("您的输入有误，请重新输入:".encode(encoding='utf_8'))

        elif choice == 2:
            print("准备加入房间:")
            conn.send("准备加入房间:\n".encode(encoding="utf_8"))
        else:
            print("输入有误，请重新输入:")
            conn.send("输入有误，请重新输入:\n".encode(encoding="utf_8"))


if __name__ == '__main__':
    main()
