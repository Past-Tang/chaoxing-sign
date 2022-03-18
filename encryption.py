def encryption():
    while True:
        username = input('输入用户名')
        serial = input('输入激活码:')
        username = list(username)
        for i in username:
            i = i + 1
        if serial == username:
            print('激活成功')
            return 1
        else:
            print('激活失败')
            return -1
