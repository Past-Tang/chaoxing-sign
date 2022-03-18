import os
def decoding():
    username = input('输入用户名:')
    username = list(username)
    serial = []
    index = 0
    for i in username:
        i = ord(i) + 1
        serial.append(i)
        index += 1
    serial.append(index)
    index = 0
    for j in serial:
        j+=serial[index]
        index += 1
    serial = j
    print('激活码是:',serial)
    os.system("pause")
    return serial
decoding()
