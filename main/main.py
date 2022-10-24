from threading import Thread
from socket import *

import PlayerUtils

addr = ("0.0.0.0", 22222)
buffer_size = 1024
tcpClientSockets = []


def main():
    tcp_server = socket(AF_INET, SOCK_STREAM)
    tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcp_server.bind(addr)
    tcp_server.listen(10)

    while True:
        print("Waiting for connecting!")
        tcp_client_sock, remote_addr = tcp_server.accept()
        print("Remote Addr is:", remote_addr)
        tcpClientSockets.append(tcp_client_sock)
        print("A new client has appended to list:")
        Thread(target=process, args=(tcp_client_sock,)).start()


def process(conn: socket):
    print("Enter child process:")
    print(tcpClientSockets)
    conn.send("Have connected server successfully!".encode(encoding="utf_8"))
    # data = conn.recv(buffer_size)
    # print(data.decode('utf8'))
    li = PlayerUtils.Player("li_wei_jun", 6, conn)  # 创建一个有6个骰子的玩家
    li.shook_dices()
    li.show_dices()


if __name__ == '__main__':
    main()
