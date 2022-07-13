import botpy
from botpy.message import *
from botpy.client import *

class MessageReply():
    def __init__(self, message, reply):
        self.message = message
        self.reply = reply


class AyakiFeaturesHandler():
    robot_version = "4.0.0"
    reply_message = MessageReply()
    online = True

    def hello_handler(self, message: Message):
        self.reply_message.content = "你好%s! 我是Ayaki，请多指教了哦! 当前版本：%s" % (message.author.username, self.robot_version)
        self.reply_message.image = "http://nas.hakubill.tech:1234/images/2022/02/27/Ayaki-Watermark.png"
        return self.reply_message