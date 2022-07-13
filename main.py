import random

import qqbot    #已废弃
import botpy
import features
import requests
import datetime
import time
import os
import _thread
import platform
import schedule as sch
from qqbot import *
from botpy.message import *
from features import *
from pixivpy3 import *

appid = "102005740"
sandboxid = 4294837189
guildid = "5440859059313954953"  # 之外语文
test_channel_id = "5463311"
sesephoto_channel_id = "3613561"
nichijou_channel_id = "3613272"
access_token = "jIhM72IaFkMZmi8X8KIgxCzr6HbIiEgi"
access_secret = "QSGtIVUIsITWKxLX"
pixiv_access_token = "2xohFPRY2kf16FOuUok9gD16abM2DXQWFXwcOcaB6qI"
pixiv_refresh_token = "XlkWbEVUqVkS_zjpNb64LSD5wl7E-0CTaxmcziKp5rg"
robot_version = "4.0.2"



token = qqbot.Token(appid, access_token)
ayaki_logo_url = "http://nas.hakubill.tech:1234/images/2022/02/27/Ayaki-Watermark.png"




def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)


def get_file_modified_time(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


def send_moyu_cal():
    qqbot.logger.info("Send today's moyu calendar")
    image_api = "https://api.vvhan.com/api/moyu?type=json"
    res = requests.get(image_api)
    res_json = res.json()
    image_url = res_json['url']
    send_message = MessageSendRequest()
    send_message.image = image_url
    today = datetime.date.today()
    send_message.content = "今天是%s，今天也要努力摸鱼鸭！" % today
    msg_api = qqbot.MessageAPI(token, False, timeout=10)
    try:
        msg_api.post_message(nichijou_channel_id, send_message)
        qqbot.logger.info("Send message success")
    except Exception as err:
        qqbot.logger.error("Send message error: %s, now try again" % str(err))
        try:
            msg_api.post_message(nichijou_channel_id, send_message)
            qqbot.logger.info("Send message success")
        except Exception as err2:
            qqbot.logger.error("Send message error: %s, try again fail" % str(err2))


def _moyu_handler():
    sch.every().day.at("09:00").do(send_moyu_cal)
    while True:
        sch.run_pending()
        time.sleep(1)


def _get_seremain():
    cnt = 0
    try:
        with open("pixiv_src.csv", "r") as src:
            for line in src.readlines():
                values = line.split(',')
                have_used = int(values[3])
                if have_used == 0:
                    cnt += 1
    except Exception as err:
        cnt = -1
        qqbot.logger.error("Get seremain fail, " + str(err))
    return cnt


# 群中被at的回复
def _at_message_handler(event, message: Message):
    hello_message = MessageSendRequest()
    # 打印返回信息
    qqbot.logger.info(
        "receive at message %s" % message.content + ", came from %s-%s" % (message.author.id, message.author.username))

    undefined_command = False

    if message.content.find("爱你") != -1 or message.content.find("love you") != -1:
        qqbot.logger.info("Recognized command love you")
        if message.author.username == "水里的碳酸钙":
            hello_message.content = "我也爱你哦"
        else:
            hello_message.content = "对不起，你是个好人。"

    # 发送程序相关信息
    elif message.content.find("/info") != -1:
        qqbot.logger.info("Recognized command info")
        remain = _get_seremain()
        if remain >= 0:
            remain_info = "%d" % remain
            qqbot.logger.info("Get remain success, remain %d" % remain)
        else:
            remain_info = "获取失败"
            qqbot.logger.warning("Get sese image database remain fail")
        hello_message.content = "At_Message_Handler运行正常\nWeb Socket连接正常\n" \
                                "运行平台：%s\n图库图片剩余%s" % (platform.platform(), remain_info)

    # 版本信息功能
    elif message.content.find("/ver") != -1:
        qqbot.logger.info("Recognized command version")
        update_time = get_file_modified_time("pixiv_src.csv")
        hello_message.content = "Script Version: %s\nIllustration Database Update Time: %s" % (robot_version, update_time)

    # 摸鱼日历功能
    elif message.content.find("/moyu") != -1:
        qqbot.logger.info("Recognized command moyu")
        image_api = "https://api.vvhan.com/api/moyu?type=json"
        res = requests.get(image_api)
        res_json = res.json()
        image_url = res_json['url']
        hello_message.image = image_url
        today = datetime.date.today()
        hello_message.content = "今天是%s，今天也要努力摸鱼鸭！" % today

    # 关机功能
    elif message.content.find("shutdown") != -1:
        qqbot.logger.info("Recognized command shutdown")
        exit(0)

    elif message.content.find("/help") != -1:
        qqbot.logger.info("Recognized command help")
        hello_message.content = "欢迎使用Ayaki，以下是我的使用说明：\n" + \
                                "我的主要功能是运势签到和发送一张涩涩图片。图片来自Pixiv日榜前30，图片每日更新通过转存到Bill的图库发送。" + \
                                "图库在更新时，会自动筛选剔除已经发送过的和未被作者标记为插画类型的图片。以下是命令介绍：\n" + \
                                "/hello：打招呼：你可以使用此命令跟我打招呼。\n " + \
                                "/signin：签到与运势：你每天可以通过此命令在我这里打卡，同时会自动抽签，记得每天都来看看你的运势吧！\n " + \
                                "/sese：涩涩！涩涩是人类进步的阶梯！要涩涩的话就来让我发一张涩图吧！\n" + \
                                "/moyu：发送摸鱼日历：再次发送今天的摸鱼日历。人活着就是为了摸鱼。\n " + \
                                "/ver：发送版本信息\n " + \
                                "/info：发送程序相关信息\n "
        msg_reference = MessageReference(message_id=message.id)
        hello_message.message_reference = msg_reference

    else:
        qqbot.logger.info("Undefined command")
        undefined_command = True

    if not undefined_command:
        hello_message.msg_id = message.id
        msg_api = qqbot.MessageAPI(token, False, timeout=10)
        try:
            msg_api.post_message(message.channel_id, hello_message)
            qqbot.logger.info("Send message success")
        except Exception as err:
            qqbot.logger.error("Send message error: %s, now try again" % str(err))
            try:
                msg_api.post_message(message.channel_id, hello_message)
                qqbot.logger.info("Send message success")
            except Exception as err2:
                qqbot.logger.error("Send message error: %s, try again fail" % str(err2))
                try:
                    time.sleep(1)
                    msg_api.post_message(message.channel_id, hello_message)
                    qqbot.logger.info("Send message success")
                except Exception as err3:
                    qqbot.logger.error("Send message error: %s, try again again fail" % str(err3))


# 私信回复
def _direct_message_handler(event, message: Message):
    hello_message = MessageSendRequest()
    # 打印返回信息
    qqbot.logger.info(
        "event %s" % event + ", receive direct message %s" % message.content + ", came from %s-%s" % (message.author.id, message.author.username))
    qqbot.logger.info("Recognized command default")
    hello_message.content = "你好%s! 我是Ayaki，请多指教! 当前版本：%s" % (message.author.username, robot_version)
    hello_message.image = "http://nas.hakubill.tech:1234/images/2022/02/27/Ayaki-Watermark.png"
    hello_message.msg_id = message.id
    dms_api = qqbot.DmsAPI(token, False, timeout=10)
    dms_api.post_direct_message(message.guild_id, hello_message)


_log = logging.get_logger()


class AyakiClient(botpy.Client):
    handler = AyakiFeaturesHandler()

    async def on_ready(self):
        _log.info(f"{self.robot.name} is ready!")

    async def on_at_message_create(self, message: Message):
        _log.info(f"At message {message.content} came from {message.author.username} - {message.author.id}")
        if not self.handler.online:
            _log.info("Bot is offline, ignore at message")
            if "turnon" in message.content:
                _log.info("Recognized command turnon")
                if message.author.id in self.handler.admin_list:
                    reply = self.handler.turnon_handler(message)
                    await self.api.post_message(channel_id=message.channel_id, content=reply.content, msg_id=message.id)
                    return
                else:
                    return
            else:
                return

        reply = MessageReply(content=f"{message.author.username}，你好！SDK正在更新中。")
        if "/hello" in message.content:
            _log.info(f"Recognized command hello")
            reply = self.handler.hello_handler(message=message)
        elif "/signin" in message.content:
            _log.info(f"Recognized command signin")
            reply = self.handler.signin_handler(message=message)
        elif "shutdown" in message.content:
            _log.info(f"Recognized command shutdown")
            reply = self.handler.shutdown_handler(message=message)
        elif "/sese" in message.content:
            _log.info(f"Recognized command sese")
            reply = self.handler.sese_handler(message=message)
        await self.api.post_message(channel_id=message.channel_id,
                                    content=reply.content,
                                    image=reply.image,
                                    message_reference=reply.message_reference,
                                    msg_id=message.id)
        _log.info(f"Replied {reply.content} SUCCESS")

if __name__ == '__main__':
    userApi = qqbot.UserAPI(token, False)
    user = userApi.me()
    # 打印机器人名字
    qqbot.logger.info("Starting %s..." % user.username)
    qqbot.logger.info("Platform: %s" % platform.platform())
    qqbot.logger.info("Python version: %s" % platform.python_version())

    intents = botpy.Intents(public_guild_messages=True)
    client = AyakiClient(intents=intents)
    client.run(appid=appid, token=access_token)

    # ayaki_at_message_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _at_message_handler)
    # ayaki_direct_message_handler = qqbot.Handler(qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _direct_message_handler)
    # qqbot.listen_events(token, False, ayaki_at_message_handler)
    # qqbot.listen_events(token, False, ayaki_direct_message_handler)
    qqbot.logger.info("%s start complete, current version %s" % (user.username, robot_version))
    # _thread.start_new_thread(_moyu_handler())
