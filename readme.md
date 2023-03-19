# Ayaki

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Bill-Haku/Ayakibot?include_prereleases) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Bill-Haku/AyakiBot) ![GitHub issues](https://img.shields.io/github/issues/Bill-Haku/Ayakibot) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django) ![GitHub](https://img.shields.io/github/license/Bill-Haku/Ayakibot) [![Python application](https://github.com/Bill-Haku/AyakiBot/actions/workflows/python-app.yml/badge.svg)](https://github.com/Bill-Haku/AyakiBot/actions/workflows/python-app.yml)

## 项目说明

Ayaki是我编写的一个QQ Bot。Ayaki是我给她取的名字，日语名あやき，没有对应的汉字。当然，如果你学过日语，你就能知道，这三个假名可以拼成很多汉字，你们可以叫她“彩木”，“绫纪”，“绫绮”等等。每个人心中都可以有属于自己的Ayaki。

Ayaki的出生日期是2022年4月20日。

Ayaki的头像是我使用AI画的。

![Ayaki-Watermark.png](http://nas.hakubill.tech:1234/images/2022/02/27/Ayaki-Watermark.png)

## 安装部署

本程序是Python脚本，可以在任何安装了Python环境的服务器上运行。

### 获取源代码

你可以使用以下命令获取最新的源代码：

```bash
git clone https://github.com/Bill-Haku/AyakiBot.git
```

但我更加推荐你使用最新的发行版，这可能更加稳定：

```bash
git clone -b <tag name> https://github.com/Bill-Haku/AyakiBot.git
```

或者在[GitHub的Release页面](https://github.com/Bill-Haku/AyakiBot/releases)找到最新的发行版并下载源码后解压。

### 安装依赖

本程序使用到了腾讯官方提供的SDK和一些其他的库。在使用前，你可以使用以下命令安装本程序所需要的库。

```bash
cd AyakiBot
pip install -r requirements.txt
```

### 配置个性化参数

在使用之前，需要配置一些个性化的参数。我提供了`./private_config_sample.yaml`文件作为样例。你需要根据注释将你的相关信息填入对应的位置。如果你单纯只为了运行该脚本，必填的只有前三项。后面的可能会用到，也可能不会用到。你需要根据你的实际情况使用。如果你还要获取Pixiv每日日榜，那么你还需要填入Pixiv相关的access token.相关的获取方法将在另外的文档中说明。

**然后，你需要将该文件的文件名中的`sample`字样删除，即修改为`private_config.yaml`，如此在部署时和程序运行时能免除许多不必要的麻烦。**

### 部署代码

如果你跟我一样，开发用的计算机并不是提供服务运行程序的服务器的话，你需要通过某种方式讲你的代码上传到服务器上。

在`./tools/upload.sh`中，我提供了一个简易的脚本程序用于完成这一操作。该脚本使用`scp`的方式安全地传输文件。我建议你在使用前首先在服务器上配置好你的ssh公钥，以便该脚本运行。

首先打开该脚本，将第3～7行中的内容修改为你的实际配置。然后运行以下命令：

```bash
cd tools
./upload.sh
```

如果提示缺少运行权限，请执行以下命令后重新运行：

```bash
chmod 755 upload.sh
```

### 关于二进制文件

我使用[GitHub Actions](https://github.com/Bill-Haku/AyakiBot/actions)自动打包本程序的适用于macOS, Linux和Windows平台的二进制文件。但是这些二进制文件的可用性未经过测试。

## 使用

### 启动

使用以下命令即可启动：

```bash
cd Ayaki
python3 main.py
```

### 日志

本程序使用`botqq`库中的日志模块实现日志，同时会将日志信息显示到终端和保存到文件中。前日日志会自动重命名为日期并单独保存。

### 功能

#### 打招呼`/hello`

打招呼。同时可用于检测Ayaki的可用状态。Ayaki同时会返回图库的库存量。

#### 签到`/signin`

每日用户可以使用该功能签到一次。同时Ayaki会随机完成抽签工作返回用户的运势和黄历宜忌。后台Ayaki会将所有已签到的用户ID存储到基于日期命名的文件中以检测重复签到。

#### 涩涩`/sese`

Ayaki自动从图库中返回第一张未发出的图片。关于图库的运行方式详见其他文档。

#### 摸鱼`/moyu`

Ayaki返回今日的摸鱼日历。摸鱼日历由公众号moyurili提供[API](https://api.vvhan.com/moyu.html)。

同时Ayaki会在每日的早上9点自动在指定的子频道发送摸鱼日历。

#### 每日老婆`/waifu`

每日用户可以使用该功能获取每日老婆。老婆从配置文件的`waifu_list`项随机读取，并发送相关图片。每个用户每日只能使用一次，相关实现方法与[签到](####签到`/signin`)功能类似。

#### 聊天模式

Ayaki启动时默认开启聊天模式。可以通过`/chat`指令打开或关闭聊天模式。聊天模式启用时，Ayaki会将未找到相关命令的at消息的最后一个空格后的内容解析为与Ayaki对话的语句，并返回对话结果。此外，还可以使用该功能查询天气、歌词、IP归属地、电话号码归属地、讲笑话等功能。

#### 帮助`/help`

Ayaki返回相关功能列表和说明。

## 相关项目

- QQ频道机器人SDK：[tencent-connect/botpy](https://github.com/tencent-connect/botpy)

- [QQ频道机器人API文档](https://bot.q.qq.com/wiki/develop/api/)
- [QQ频道机器人Python SDK文档](https://bot.q.qq.com/wiki/develop/pythonsdk/)
- Python Pixiv爬取库：[upbit/pixivpy](https://github.com/upbit/pixivpy)

## 更新记录

- 5.1.0 - 2023.3.19 - Newest

    修复了使用ChatGPT时消息存在多个空格时只有最后一个单词的内容会被发送到后端的问题

- 5.0.1 - 2023.3.3

    新增连接ChatGPT对话的功能

- 4.3.0 - 2022.7.28

    修复了GitHub Actions中的若干问题。

- 4.3.0-RC.2

    修复了`private_config_sample.yaml`中的错误

- 4.3.0-RC.1 - 2022.7.26 

    更新和重构部分代码逻辑

    修复了获取剩余图库数量失败的问题

- 4.2.1 - 2022.7.24

    修复了错误显示{br}的问题

- 4.2.0

    新增聊天模式。可以与Ayaki对话了。

- 4.1.3

    调整了tutu老婆特别优化的启动方式

- 4.1.2 - 2022.7.21

    修复了tutu老婆特别优化应用失败的问题

- 4.1.1 - 2022.7.20

    新增针对tutu老婆的特别优化

- 4.1.0

    新增`/waifu`指令，支持新增的每日老婆功能

- 4.0.11

    修复了每日发送摸鱼日历发送失败的问题

- 4.0.10

    将表面上的@发送人改为内嵌的@格式

- 4.0.9

    增加了消息发送失败时重新发送原因

- 4.0.8 - 2022.7.17

    恢复`4.0.7`中下线的功能

- 4.0.7 - 2022.7.15

    由于NAS服务器网络问题，为减少损失和维护其他正常模块，下线与NAS服务器相关的功能。

- 4.0.6 - 2022.7.14

    增加了`config.yaml`配置文件，程序改用从配置文件读取常量

- 4.0.5

    删除对私信消息的支持

    调整多线程逻辑

    增加上传服务器脚本的shell脚本

- 4.0.4 - 2022.7.13

    修复了可能重复发送图片的问题

- 4.0.3

    将其他已有功能迁移到新SDK中

- 4.0.2

    关机和开机指令增加操作用户锁，只有管理员列表中的用户可以使用这两个命令

- 4.0.1

    新增关机和开机指令，支持关机模式功能

- 4.0.0

    更新SDK，并更换至`botpy`库提供服务。

- 3.5.6 - 2022.7.12

    新增了`/help`指令，用于提供帮助信息。

- 3.5.5 - 2022.7.5 - Stable

    更新优化了消息重发的机制

- 3.5.4 - 2022.7.4 

    新增了与`🍬🍬`和`土土`有关的表情包

- 3.5.3

    更新了"诸事不宜"的算法阈值

    修复了每日宜忌中可能出现重复内容的问题

- 3.5.2 - 2022.7.3

    更新了对于画师信息的获取和支持

- 3.5.1

    更新“诸事不宜”的算法

- 3.5.0

    新增签到和运势功能

- 3.4.4 - 2022.7.2

    更新图库域名

    更改图片压缩格式为`png`

- 3.4.3 - 2022.5.26

    `/info`指令返回的信息中增加运行平台的信息

    改进了部分日志记录的内容

- 3.4.2

    增加`shutdown`指令关机

- 3.4.1

    增加`/moyu`指令手动发送当天的摸鱼日历

- 3.4.0 - 2022.5.24

    每天上午9点自动发送每日摸鱼日历

    不再支持不包含`/`的指令

    取消对`seremain`指令的支持，使用`/info`指令替代

- 3.3.1

    修复了获取图库修改日期失败的问题

- 3.3.0

    对接官方指令API，可以直接在对话框输入`/`调出机器人指令列表

    增加`/info`指令显示当前程序相关的信息（仅管理员可用）

    增加`/ver`指令显示程序版本和图库版本（仅管理员可用）

    增加`/hello`指令发送打招呼内容，缺省状态下不再发送打招呼内容

- 3.2.2 - 2022.5.23

    修复了由于引入了图片标题导致的无法继续发送图片的问题

- 3.2.1  - 2022.5.15

    修复了日志中出现过多Title发现为空的提示的问题

- 3.2.0

    升级SDK版本到0.8.2，修复3.1.2中的问题

    筛选插画内容添加到图库

    发送图片时添加图片标题

    筛选已经在图库中的图片

    增加读取图库信息的模块

- 3.1.6 - 2022.5.10

    修复了当图片含有alpha通道时压缩失败的问题

- 3.1.5 - 2022.5.9

    增加了上传图片压缩失败的异常处理

- 3.1.4 - 2022.5.5

    改进了上传图片的压缩标准

    增加了上传图片的异常处理

- 3.1.3 - 2022.5.4

    增加了发送图片失败时的重传机制

    调整日志记录内容和格式

    回滚3.1.2的修复：Tencent提供的SDK（版本0.7.9）有问题，已经提交Issue

- 3.1.2 - 2022.5.2

    增大API的timeout响应时间，修复由于响应时间过长造成的消息发送失败

- 3.1.1

    完善日志记录

    修复了正常情况下使用`seremain`指令时返回异常的问题

- 3.1.0

    增加`seremain`指令用于返回图库剩余图片数量

    默认回复中添加当前版本信息

- 3.0.0 - 2022.5.1

    重写发送pixiv图片的逻辑，优化使用体验

- 2.0.0 - 2022.4.23

    支持使用`sese`指令返回pixiv上的日榜图片

- 1.0.2

    被动回复添加图片

    修改回复语言为中文

- 1.0.1 - 2022.4.22

    所有子频道中均可使用

    被动回复增加了回复msg_id

    增加了对私信的处理

- 1.0.0 - 2022.4.20

    在群聊中at后可以回复“Hello”和简单的自我介绍

## License 许可证

本项目以[MIT协议](https://github.com/Bill-Haku/AyakiBot/blob/master/LICENSE)授权许可开源。

© 2022 Bill Haku

