'''
Author: 过往 Past
改 Author：Wildpointer
Date: 2022-02-22 21:12:32
改 Date:2022-3-18 23:26
'''
import encryption
import datetime
from asyncio.windows_events import NULL
import requests
import json
import time
import os
import random
from lxml import etree
import getpass 
import log
itime="4"#基础延时
token=''#push+ token，选填
classini=[]#课程信息
#用户区结束
#全局区开始
headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; M2007J3SC Build/RKQ1.200826.002) (device:M2007J3SC) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_5.1.3_android_phone_613_74 '}#超星app原生ua
#全局区结束
#第一个函数 实现登录，验证cookie，保存cookie，获取cookie各功能
def login():#使用超星app登录api，测试多次获取没遇到过验证，比较稳定
    print("登录模块启动")
    data = {'uname': name,'code': passwd,'loginType': '1','roleSelect': 'true'}
    r = requests.post('https://passport2-api.chaoxing.com/v11/loginregister', headers=headers, data=data)
    load_cookies = requests.utils.dict_from_cookiejar(r.cookies)
    #转换为字符串保存到文件
    fo = open("cookie.txt", "w")
    fo.write(str(json.dumps(load_cookies)))
    print("cookie保存成功")
    fo.close()
    print("请重启程序")
#第二个函数 实现验证cookie，如果失效便启动再次登录获取新cookie
def cookie_check():
    if os.path.exists("cookie.txt") == True:
        f=open('cookie.txt','r',encoding="utf-8")
        dic = json.loads(f.read())
        response = requests.get('https://mooc1-api.chaoxing.com/mycourse/backclazzdata', headers=headers,cookies=dic)
        if '成功' in response.text:
                return [True,dic,dic['UID']]
                #get_class()
        else:
            print("cookie好像失效了,启动重新获取")
            login()
    else:
        print("未找到cookie文件呀启动登录")
        login()
#第三个函数 实现获取待查询是否有签到的课程，这个api也没有发现请求次数限制
#课程的选择：
#1.  ‘-1’这个是跟目录下
#2.  ‘目录参数’ 可以填写你的目录参数过滤掉其他的课程：浏览器f12即可
def is_succeeded(response):
    if 'succ' in response.text:
        print("\n\n"+"*"*5+"签到成功"+"*"*5+"\n\n")
        cur = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        # 输出结果到日志
        log.log_write(cur+'----'+"签到成功"+'----'+'\n')
        if token ==NULL:
            return
        response = requests.get("https://www.pushplus.plus/send?token="+token+"&title="+str(random.randint(0,100))+"您的学习通&content=成功签到")
        print(response.text)
    else:
        print("\n\n"+"*"*5+"签到失败"+"*"*5+"\n\n")
        cur = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        log.log_write(cur+'----'+"签到失败"+'----'+'\n')
    return
def get_class():
    r = requests.get('https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&mcode=', headers=headers, cookies= okcookie)
    classinfo =json.loads(r.text)
    for i in classinfo['channelList']:
        if "course" not in str(i):
            continue
        if str("-1") in str(i["cfid"]):#这里可以实现对课程的选择
            classini.append([i['content']['course']['data'][0]['name'],i['content']['course']['data'][0]['id'],i['key']])
    print("\n\n"+"*"*5+"课程获取成功"+"*"*5+"\n\n")
    return classinfo
def common_sign(id):#第四个函数，发出签到请求，推送push+
    response = requests.get('https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId='+str(id)+'&uid='+uid, headers=headers,cookies= okcookie)
    is_succeeded(response)
def location_sign(id):
    response = requests.get('https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId='+str(id)+'&uid='+uid, headers=headers,cookies= okcookie)
    is_succeeded(response)
    return 0
def Qrcode_sign(id):
    response = requests.get('https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId='+str(id)+'&uid='+uid+'&enc=', headers=headers,cookies= okcookie)
    is_succeeded(response)
    return 0
def get_active_one():#第五个函数 实现查询活动(核心)，这个超星api有访问次数限制，这里用网页版和app版的活动获取两种api，交替并演示使用
    for i in classini:
        print("查询"+i[0]+"....")
        r = requests.get('https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId='+str(i[1])+'&classId='+str(i[2]), headers=headers, cookies=okcookie)
        a =json.loads(r.text)
        #print(a)
        if str("频繁") in str(a):
                print("\n\n\n出现频繁自动跳转备用接口\n\n\n")
                get_active_two()
                break
        if str("进行中(0)") in str(a["groupList"][0]['name']):
                print("无活动跳过\n")
                continue
        for o in a['activeList']:
            if str("1") not in str(o["status"]):
                print("不是进行中的跳过\n")
                continue        
            if str("2") not in str(o["activeType"]):
                print("不是进行中的签到任务\n")
                continue
            else:
                print("监听到签到\n")
                if o["nameOne"] == "签到码签到" or o["nameOne"]=="签到" or o["nameOne"]=="手势签到":
                    print("监听到:签到码签到或普通签到或手势签到\n")
                    location_sign(o["id"])
                elif o["nameOne"] == "位置签到":
                    print("监听到:位置签到\n")
                    common_sign(o["id"])
                elif o["nameOne"] == "二维码签到":
                    print("监听到:二维码签到\n")
                    Qrcode_sign(o["id"])
        time.sleep(random.randint(2,10))      
def get_active_two():#备用网页端接口
        for i in classini:
            print("查询"+i[0]+"....")
            r = requests.get('https://mobilelearn.chaoxing.com/widget/pcpick/stu/index?courseId='+str(i[1])+'&jclassId='+str(i[2]), headers=headers, cookies=okcookie)
            if str("频繁") in r.text:
                print("\n\n\n出现频繁\n\n\n")
                return
            html = etree.HTML(r.text)
            act=html.xpath('//*[@id="startList"]/div/div/@onclick')
            if len(act)==0:
                print("无活动跳过\n")
                continue
            if str(",2,") not in str(act):
                print("不是进行中的签到任务\n")
                continue
            for i in act:
                go=i
                go=go.replace('activeDetail(','')
                go=go.replace(',2,null)','')
                common_sign(go)
                time.sleep(random.randint(2,10))
def main():
    if cookie_check()[0] ==True:
        print("cookie检测成功")
        global okcookie
        okcookie=cookie_check()[1]
        global uid
        uid=cookie_check()[2]
        while 1:
            print("进入课程获取")
            global classlist
            classlist = get_class()
            get_active_one()
bit = encryption.encryption()
if bit == 1:
    global name
    global passwd
    name = input("账号:")#用户名，必填
    # 不回显输入密码
    passwd = getpass.getpass("密码：")#密码，必填
    main()
elif bit == -1:
    exit(-1)
# 一。https://mobilelearn.chaoxing.com/widget/sign/pcTeaSignController/endSign?activeId=4000016512062&classId=53789806&fid=18078&courseId=223932923&isTeacherViewOpen=1
# 二维码签到，二维码页面的url
# https://mobilelearn.chaoxing.com/widget/sign/pcTeaSignController/endSign?activeId=+str(id)+'&classId'=+''+'fid='+''+'&courseId'=''+'&isTeacherViewOpen=1'
# 二。https://mobilelearn.chaoxing.com/page/sign/endSign?courseId=223932923&classId=53789806&activeId=4000016514053&fid=0&cpi=154183194&showOnScreenShare=true
