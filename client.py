from socket import *

BUFFER_SIZE = 1024 * 5
addr = ()
choice = 0

while True:
    choice = int(input('1.创建房间:\n2.加入房间\n请输入您的选择:'))
    if choice == 1:
        addr = ("106.14.187.13", 22222)  # 公网地址
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
        if "加入房间" in data and choice == 1:
            choice = '1\n'
            conn.send((choice.encode(encoding='utf_8')))
            continue
        elif "加入房间" in data and choice == 2:
            choice = '2\n'
            conn.send((choice.encode(encoding='utf_8')))
            continue
        elif "输入姓名准备开始游戏" in data:
            name = str(input())
            name = name + '\n'
            conn.send(name.encode(encoding='utf_8'))
            continue
        elif "开始游" in data:
            choice = str(input('请输入是否开始游戏:'))
            choice = choice + '\n'
            conn.send((choice.encode(encoding='utf_8')))
            continue
        elif "开始吹牛" in data:
            break

    reply = ""
    while True:
        tmp = str(input('请输入:'))
        if tmp == 'open':
            print("您选择开上家:")
            reply = '0\n'
            break
        else:
            tmpList = tmp.split(' ')
            # print(tmpList)
            if len(tmpList) != 2:
                print("重新输入")
            else:
                flag = 0
                for i in tmpList:

                    if int(i) < 1 or int(i) > 6:
                        flag = 1
                        print('重新输入')
                        break
                if flag == 0:
                    reply = tmp + '\n'
                    break

    conn.send(reply.encode(encoding='utf_8'))
