from socket import *

BUFFER_SIZE = 1024 * 5
addr = ()

while True:
    choice = int(input('1.创建房间:\n2.加入房间\n请输入您的选择:'))
    if choice == 1:
        addr = ("106.14.187.13", 22222) # 公网地址
        break
    elif choice == 2:
        port = int(input('请输入房间号:'))
        print('输入的port:', port, type(port))
        addr = ("106.14.187.13", port)
        break
    else:
        print('您的输入有误，请重新输入:')

conn = socket(AF_INET, SOCK_STREAM)
conn.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
conn.connect(addr)

while True:
    while True:
        data = conn.recv(BUFFER_SIZE).decode('utf8')
        print(data)
        if "加入房间" in data:
            break
        elif "输入姓名准备开始游戏" in data:
            break
        elif "开始游" in data:
            break
        elif "开始吹牛" in data:
            break

    reply = str(input('请输入:')) + "\n"
    conn.send(reply.encode(encoding='utf_8'))
