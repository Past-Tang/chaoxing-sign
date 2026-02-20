<div align="center">

<img src="assets/logo.svg" alt="Chaoxing Auto-Sign" width="600">

<br/>
<br/>

**学习通自动签到工具**

*双接口防频繁 | 自动更新 Cookie | 微信推送通知*

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Archived-lightgrey.svg)]()

</div>

---

> **此仓库已归档，不再维护。** 仅作为 Python 网络自动化的学习参考。

## 概述

针对超星学习通平台的自动签到脚本。通过调用学习通 App 端和 Web 端两套 API，实现签到活动的自动检测与完成。当 App 接口触发频率限制时，自动切换到 Web 接口，保证签到成功率。

### 功能特性

- **自动签到** -- 定时轮询课程活动，检测到签到任务后自动完成
- **双接口切换** -- App API 被限频时自动切换 Web API，提高稳定性
- **Cookie 管理** -- 自动登录获取 Cookie，本地持久化，失效后自动重新获取
- **微信推送** -- 通过 PushPlus 将签到结果推送到微信
- **课程过滤** -- 支持指定目录下的课程，避免无关课程干扰

---

## 工作原理

```
登录 (App API)  -->  获取 Cookie  -->  持久化到 cookie.txt
                                          |
                                          v
                                    获取课程列表
                                          |
                                          v
                              轮询每门课的活动列表
                                    /          \
                            App API              Web API (备用)
                           (频繁时自动切换)          |
                                    \          /
                                     检测签到活动
                                          |
                                          v
                                    发送签到请求
                                          |
                                          v
                                  PushPlus 微信通知
```

---

## 使用方法

### 环境要求

| 要求 | 说明 |
|:---|:---|
| Python | >= 3.6 |
| 依赖库 | requests, lxml |

### 安装

```bash
git clone https://github.com/Past-Tang/chaoxing-sign.git
cd chaoxing-sign
pip install requests lxml
```

### 配置

编辑 `chaoxing-sign.py` 顶部的用户区参数：

```python
name = ""       # 学习通账号（手机号）
passwd = ""     # 密码
itime = "4"     # 轮询间隔（秒）
token = ""      # PushPlus Token（可选，用于微信推送）
```

<details>
<summary><b>如何获取 PushPlus Token</b></summary>

1. 访问 [pushplus.plus](https://www.pushplus.plus/)
2. 微信扫码登录
3. 复制 Token 填入 `token` 变量

</details>

### 运行

```bash
python chaoxing-sign.py
```

---

## 技术细节

### 双接口机制

| 接口 | 端点 | 特点 |
|:---|:---|:---|
| App API | `mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist` | 数据完整，但有频率限制 |
| Web API | `mobilelearn.chaoxing.com/widget/pcpick/stu/index` | 备用接口，通过 HTML 解析提取活动 |

当 App API 返回"频繁"提示时，脚本自动切换到 Web API 继续工作。

### Cookie 生命周期

```
首次运行 --> 无 cookie.txt --> 调用登录 API --> 保存 Cookie (有效期 30 天)
后续运行 --> 读取 cookie.txt --> 验证有效性 --> 失效则重新登录
```

---

## 免责声明

本项目仅供技术学习和研究目的。使用自动化脚本可能违反平台服务条款，由此产生的任何后果由使用者自行承担。
