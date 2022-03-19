# 修改列表
### author：Wildpointe
### Date:2022-03-19:22:44
## 增加二维码签到
要有一位内应（哈哈哈），用微信扫签到码，之后得到enc码，输入到程序中即可成功。（这次签到中过期的二维码也可以）   
``` js
response = requests.get('https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId='+str(id)+'&uid='+uid+'&enc='+enc, headers=headers,cookies= okcookie)
```  
相比于普通签到，多一个enc码    
## 不回显密码
使用```passwd = getpass.getpass("密码：")#密码，必填```
## 做了一个简单的定时器来设置程序运行的时间         
每隔几秒查看一下有没有新的签到活动  
但是存在间隔太短，请求过于频繁的问题  
## 运行日志
增加了一个运行日志的输出功能，可以查看程序的运行情况。   
