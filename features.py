import botpy
from botpy import *
from botpy.message import *


_log = logging.get_logger()


class MessageReply():
    def __init__(self, content=None, image=None):
        self.content = content
        self.image = image


class AyakiFeaturesHandler():
    robot_version = "4.0.1"
    reply_message = MessageReply()
    online = True

    def hello_handler(self, message: Message):
        self.reply_message.content = "你好%s! 我是Ayaki，请多指教了哦! 当前版本：%s" % (message.author.username, self.robot_version)
        self.reply_message.image = "http://nas.hakubill.tech:1234/images/2022/02/27/Ayaki-Watermark.png"
        return self.reply_message

    def shutdown_handler(self, message: Message):
        self.reply_message.content = "Byebye~"
        self.online = False
        return self.reply_message

    def turnon_handler(self, message: Message):
        self.reply_message.content = "Ayaki回来了哦！"
        self.online = True
        return self.reply_message
