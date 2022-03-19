def encryption():
    username = input('输入用户名:')
    serial = input('输入激活码:')
    key = []
    username = list(username)
    index = 0
    for i in username:
        i = ord(i) + 1
        key.append(i)
        index +=1
    key.append(index)
    index = 0
    for j in key:
        j+=key[index]
        index +=1
    key = j
    # print('key:',key)
    # print('serial:',serial)
    if key == int(serial):
        print('激活成功')
        return 1
    else:
        print('激活失败')
        return -1
