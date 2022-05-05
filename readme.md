# Ayaki

## 说明

Ayaki是我编写的一个QQ Bot。Ayaki是我给她取的名字，日语名あやき，没有对应的汉字。当然，如果你学过日语，你就能知道，这三个假名可以拼成很多汉字，你们可以叫她“彩木”，“绫纪”，“绫绮”等等。每个人心中都可以有属于自己的Ayaki。

Ayaki的出生日期是2022年4月20日。

Ayaki的头像是我使用AI画的。

![Ayaki-Watermark.png](http://billdc.synology.me:1234/images/2022/02/27/Ayaki-Watermark.png)

## 更新记录&版本规划

- 3.3.0

    增加每天提供的图库数量

- 3.2.1

    增加`shutdown`指令关机

-   3.2.0

    将消息的响应逻辑改为异步执行，提高响应能力

- 3.1.4 - 2022.5.5 - Newest

    改进了上传图片的压缩标准

    增加了上传图片的异常处理

- 3.1.3 - 2022.5.4 - Stable

    增加了发送图片失败时的重传机制

    调整日志记录内容和格式

    回滚3.1.2的修复：Tencent提供的SDK有问题，已经提交Issue

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

    在群聊中at后可以回复“Hello”和简单的自我介绍。

    