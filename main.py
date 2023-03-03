import qqbot
import botpy
import time
import threading
import schedule as sch
from qqbot import *
from botpy import logging
from botpy.ext.cog_yaml import read
from features import *
from threading import Thread

private_config = read(os.path.join(os.path.dirname(__file__), "private_config.yaml"))
config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
appid = private_config["appid"]
access_token = private_config["access_token"]
token = qqbot.Token(appid, access_token)
_log = logging.get_logger()


class AyakiMoyuThread(Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        _moyu_handler(self.name)


def send_moyu_cal():
    _log.info("Send today's moyu calendar")
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
        msg_api.post_message(private_config["nichijou_channel_id"], send_message)
        _log.info("Send message success")
    except Exception as err:
        _log.error("Send message error: %s, now try again" % str(err))


def _moyu_handler(thread_name):
    _log.info("Start moyu handler")
    sch.every().day.at("09:00").do(send_moyu_cal)
    while True:
        sch.run_pending()
        time.sleep(1)


def check_reply_sendable(reply: MessageReply):
    if reply.content is not None:
        return True
    elif reply.image is not None:
        return True
    elif reply.ark is not None:
        return True
    else:
        return False


class AyakiClient(botpy.Client):
    handler = AyakiFeaturesHandler()
    reply = MessageReply()

    async def on_ready(self):
        _log.info(f"{self.robot.name} is ready!")

    async def on_at_message_create(self, message: Message):
        _log.info(f"At message {message.content} came from {message.author.username} - {message.author.id}")
        if not self.handler.online:
            _log.info("Bot is offline, ignore at message")
            if "turnon" in message.content:
                _log.info("Recognized command turnon")
                if message.author.id in self.handler.admin_list:
                    self.reply = self.handler.turnon_handler(message)
                    await self.api.post_message(channel_id=message.channel_id, content=self.reply.content, msg_id=message.id)
                    return
                else:
                    return
            else:
                return

        if "/hello" in message.content:
            _log.info(f"Recognized command hello")
            self.reply = self.handler.hello_handler(message=message)
        elif "/signin" in message.content:
            _log.info(f"Recognized command signin")
            self.reply = self.handler.signin_handler(message=message)
        elif "shutdown" in message.content:
            _log.info(f"Recognized command shutdown")
            self.reply = self.handler.shutdown_handler(message=message)
        elif "/sese" in message.content:
            _log.info(f"Recognized command sese")
            self.reply = self.handler.sese_handler(message=message)
        elif "/moyu" in message.content:
            _log.info(f"Recognized command moyu")
            self.reply = self.handler.moyu_handler(message=message)
        elif "/waifu" in message.content:
            _log.info(f"Recognized command waifu")
            self.reply = self.handler.waifu_handler(message=message)
        elif "/help" in message.content:
            _log.info(f"Recognized command help")
            self.reply = self.handler.help_handler(message=message)
        elif "/chat" in message.content:
            _log.info(f"Recognized command chat")
            if not self.handler.chat_mode:
                _log.info(f"Start chat mode")
                self.handler.chat_mode = True
                self.reply.content = "Ayaki来陪你聊天了！"
            else:
                _log.info(f"Stop chat mode")
                self.handler.chat_mode = False
                self.reply.content = "聊天就到这吧。"
        else:
            # openai bot
            _log.info(f"No command found, message = {message.content}")
            self.reply = self.handler.openai_handler(message=message)
        if check_reply_sendable(self.reply):
            await self.post_message(message=message)
        else:
            if self.handler.chat_mode:
                self.reply = self.handler.chat_handler(message=message)
                await self.post_message(message=message)
            else:
                _log.info("Undefined command")
                self.reply.reset()

    async def post_message(self, message: Message):
        try:
            await self.api.post_message(channel_id=message.channel_id,
                                        content=self.reply.content,
                                        image=self.reply.image,
                                        message_reference=self.reply.reference,
                                        ark=self.reply.ark,
                                        msg_id=message.id)
            _log.info("Reply SUCCESS")
        except Exception as err:
            _log.error("Reply FAIL")
            self.reply.reset()
            self.reply.content = f"嘤嘤，由于{str(err)}，消息被狗吃了，再试一下吧。"
            await self.api.post_message(channel_id=message.channel_id,
                                        content=self.reply.content,
                                        msg_id=message.id)
        self.reply.reset()


def start_general_event_handler():
    _log.info("Start general event handler")
    intents = botpy.Intents(public_guild_messages=True)
    client = AyakiClient(intents=intents)
    client.run(appid=appid, token=access_token)
    while True:
        pass


if __name__ == '__main__':
    # 打印机器人名字
    _log.info("Starting Ayaki(Ver.%s)..." % config["robot_version"])
    _log.info("Platform: %s" % platform.platform())
    _log.info("Python version: %s" % platform.python_version())

    try:
        moyu_thread = AyakiMoyuThread(2, "moyu_thread", 1)
        moyu_thread.start()
        start_general_event_handler()
        moyu_thread.join()
    except Exception as err:
        _log.error(err)

    while 1:
        pass
