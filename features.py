import botpy
import random
import datetime
import os
from botpy import *
from botpy.message import *
from botpy.types.message import *


_log = logging.get_logger()


class MessageReply():
    def __init__(self, content=None, image=None, reference=None):
        self.content = content
        self.image = image
        self.reference = reference


class AyakiFeaturesHandler():
    robot_version = "4.0.2"
    reply_message = MessageReply()
    admin_list = ["14862092315735810791"]
    unsei_list = ["★★★大吉★★★", "★★中吉★★", "★小吉★", "吉", "末吉", "凶", "大凶"]
    liuhantangtang_url = "http://image.hakubill.tech:1234/images/2022/07/04/IMG_2641.jpg"
    liuhantutu_url = "http://image.hakubill.tech:1234/images/2022/07/04/IMG_2642.jpg"
    baochaoaoao_url = "http://image.hakubill.tech:1234/images/2022/07/04/IMG_2643.jpg"
    online = True

    def hello_handler(self, message: Message):
        self.reply_message.content = "你好%s! 我是Ayaki，请多指教了哦! 当前版本：%s" % (message.author.username, self.robot_version)
        self.reply_message.image = "http://nas.hakubill.tech:1234/images/2022/02/27/Ayaki-Watermark.png"
        return self.reply_message

    def shutdown_handler(self, message: Message):
        if message.author.id in self.admin_list:
            self.reply_message.content = "Byebye~"
            self.online = False
        else:
            self.reply_message.content = "<@14862092315735810791>，有人想对我做坏坏的事情！"
        return self.reply_message

    def turnon_handler(self, message: Message):
        self.reply_message.content = "Ayaki回来了哦！"
        self.online = True
        return self.reply_message

    def signin_handler(self, message: Message):
        # 读取今日签到列表
        today = datetime.date.today()
        sign_in_list_name = "sign_in_list_%s" % today
        sign_in_list = []
        if os.path.exists(sign_in_list_name):
            with open(sign_in_list_name, mode='r') as list:
                for line in list.readlines():
                    sign_in_list.append(line.replace('\n', ''))
            if message.author.id in sign_in_list:
                # 用户ID已签到
                self.reply_message.content = "%s，你今天已经签到了哦QAQ！" % message.author.username
            else:
                # 签到
                self.reply_message.content = self.sign_in_op_handler(message)
                # 将ID添加到今日签到列表中
                with open(sign_in_list_name, mode="a") as list_file:
                    list_file.write(message.author.id + '\n')
        else:
            with open(sign_in_list_name, mode='w') as ff:
                _log.info("Create today's sign in list success")
            # 签到
            self.reply_message.content = self.sign_in_op_handler(message)
            # 将ID添加到今日签到列表中
            with open(sign_in_list_name, mode="a") as list_file:
                list_file.write(message.author.id + '\n')
        if self.reply_message.content.find("流汗糖豆") != -1:
            self.reply_message.image = self.liuhantangtang_url
        elif self.reply_message.content.find("爆炒🍬🍬") != -1:
            self.reply_message.image = self.liuhantangtang_url
        elif self.reply_message.content.find("流汗土豆") != -1:
            self.reply_message.image = self.liuhantutu_url
        elif self.reply_message.content.find("爆炒土土") != -1:
            self.reply_message.image = self.liuhantutu_url
        elif self.reply_message.content.find("爆炒奥奥") != -1:
            self.reply_message.image = self.baochaoaoao_url
        msg_reference = Reference(message_id=message.id)
        self.reply_message.message_reference = msg_reference
        return self.reply_message

    # 签到请求处理，返回签到结果
    def sign_in_op_handler(self, message: Message):
        # 随机获得吉等级
        unsei_index = random.randint(0, 6)
        unsei = self.unsei_list[unsei_index]
        _log.info("Get unsei_index success: %s" % unsei_index)
        # 读取并获得宜忌事件列表
        events_list = []
        with open("events.txt", mode='r') as events_file:
            events_list = events_file.readlines()
        # 根据等级返回宜忌事件
        good = "宜："
        bad = "忌："
        threshold = 90
        threshold2 = 20
        manshi_rand = random.randint(0, 100)
        if unsei_index == 0:
            threshold = 50
            threshold2 = -1
        elif unsei_index == 1:
            threshold = 70
            threshold2 = 3
        elif unsei_index == 2:
            threshold = 80
            threshold2 = 5
        elif unsei_index == 3:
            threshold = 90
            threshold2 = 7
        elif unsei_index >= 4:
            threshold = 101
            threshold2 = 10
        if manshi_rand >= threshold:
            good += "万事皆宜"
            bad += "万事皆宜"
        elif manshi_rand < threshold2:
            good += "诸事不宜"
            bad += "诸事不宜"
        else:
            # 随机获取宜和忌的事件的数量
            good_num = 3
            bad_num = 3
            if unsei_index == 0:
                good_num = random.randint(4, 5)
                bad_num = random.randint(1, 2)
            elif unsei_index == 1:
                good_num = random.randint(3, 4)
                bad_num = random.randint(2, 3)
            elif unsei_index == 2:
                good_num = random.randint(3, 4)
                bad_num = random.randint(2, 3)
            elif unsei_index == 3:
                good_num = random.randint(2, 4)
                bad_num = random.randint(2, 4)
            elif unsei_index == 4:
                good_num = random.randint(2, 4)
                bad_num = random.randint(2, 4)
            elif unsei_index == 5:
                good_num = random.randint(2, 3)
                bad_num = random.randint(3, 4)
            elif unsei_index == 6:
                good_num = random.randint(1, 2)
                bad_num = random.randint(3, 5)
            index_dict = {}
            # 获得宜事件
            for i in range(good_num):
                while True:
                    index = random.randint(0, len(events_list) - 1)
                    if index not in index_dict:
                        index_dict[index] = True
                        break
                good += events_list[index].replace('\n', '')
                good += "  "
            # 获得忌事件
            for i in range(bad_num):
                while True:
                    index = random.randint(0, len(events_list) - 1)
                    if index not in index_dict:
                        index_dict[index] = True
                        break
                bad += events_list[index].replace('\n', '')
                bad += "  "

        message = "@%s 签到成功!\n" % message.author.username
        today = datetime.date.today()
        message += "今天是%s\n" % today
        message += "今日运势: %s\n" % unsei
        message += good + "\n"
        message += bad
        _log.info("Get all luck success")
        return message
