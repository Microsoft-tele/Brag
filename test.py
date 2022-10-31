# while True:
#     tmp = str(input('请输入:'))
#     if tmp == 'open':
#         print("您选择开上家:")
#         reply = '0\n'
#         break
#     else:
#         tmpList = tmp.split(' ')
#         print(tmpList)
#         if len(tmpList) != 2:
#             print("重新输入")
#         else:
#             flag = 0
#             for i in tmpList:
#
#                 if int(i) < 1 or int(i) > 6:
#                     flag = 1
#                     print('重新输入')
#                     break
#             if flag == 0:
#                 break
