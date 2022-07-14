import random

import qqbot  # 已废弃
import time
import threading
import schedule as sch
from qqbot import *
from botpy.message import *
from features import *
from threading import Thread

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
robot_version = "4.0.3"

token = qqbot.Token(appid, access_token)
ayaki_logo_url = "http://nas.hakubill.tech:1234/images/2022/02/27/Ayaki-Watermark.png"


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


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


def _moyu_handler(thread_name):
    _log.info("Start moyu handler")
    sch.every().day.at("09:00").do(send_moyu_cal)
    cnt = 3
    while True:
        sch.run_pending()
        time.sleep(1)
        if cnt > 0:
            cnt -= 1
            _log.info("moyu handler running")
    thread_name.exit()


_log = logging.get_logger()


def check_reply_sendable(reply: MessageReply):
    if reply.content is not None:
        return True
    elif reply.image is not None:
        return True
    else:
        return False


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

        reply = MessageReply()
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
        elif "/moyu" in message.content:
            _log.info(f"Recognized command moyu")
            reply = self.handler.moyu_handler(message=message)
        elif "/help" in message.content:
            _log.info(f"Recognized command help")
            reply = self.handler.help_handler(message=message)
        if check_reply_sendable(reply):
            await self.api.post_message(channel_id=message.channel_id,
                                        content=reply.content,
                                        image=reply.image,
                                        message_reference=reply.reference,
                                        msg_id=message.id)
            _log.info("Reply SUCCESS")
            reply.reset()
        else:
            _log.info("Undefined command")
            reply.reset()


def start_general_event_handler():
    _log.info("Start general event handler")
    intents = botpy.Intents(public_guild_messages=True)
    client = AyakiClient(intents=intents)
    client.run(appid=appid, token=access_token)
    while True:
        pass


class AyakiThread(Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        start_general_event_handler()


class AyakiMoyuThread(Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        _moyu_handler(self.name)


if __name__ == '__main__':
    userApi = qqbot.UserAPI(token, False)
    user = userApi.me()
    # 打印机器人名字
    qqbot.logger.info("Starting %s(Ver.%s)..." % (user.username, robot_version))
    qqbot.logger.info("Platform: %s" % platform.platform())
    qqbot.logger.info("Python version: %s" % platform.python_version())

    try:
        # _thread.start_new_thread(start_general_event_handler(), ())
        # _thread.start_new_thread(_moyu_handler(), ())
        # general_thread = AyakiThread(1, "general_thread", 1)
        moyu_thread = AyakiMoyuThread(2, "moyu_thread", 1)
        # general_thread.start()
        moyu_thread.start()
        # general_thread.join()
        start_general_event_handler()
        moyu_thread.join()
    except Exception as err:
        _log.error(err)

    while 1:
        pass

    # ayaki_at_message_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _at_message_handler)
    # ayaki_direct_message_handler = qqbot.Handler(qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _direct_message_handler)
    # qqbot.listen_events(token, False, ayaki_at_message_handler)
    # qqbot.listen_events(token, False, ayaki_direct_message_handler)
