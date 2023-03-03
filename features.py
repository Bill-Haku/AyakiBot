import botpy
import random
import datetime
import os
import requests
import platform
from botpy import *
from botpy.message import *
from botpy.types.message import *
from botpy.ext.cog_yaml import read

private_config = read(os.path.join(os.path.dirname(__file__), "private_config.yaml"))
config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()


class MessageReply:
    def __init__(self, content=None, image=None, reference=None, ark=None):
        self.content = content
        self.image = image
        self.reference = reference
        self.ark = ark

    def reset(self):
        self.content = None
        self.image = None
        self.reference = None
        self.ark = None


class AyakiFeaturesHandler:
    robot_version = config["robot_version"]
    reply_message = MessageReply()
    admin_list = private_config["admin_list"]
    ayaki_logo_url = config["ayaki_logo_url"]
    unsei_list = config["unsei_list"]
    liuhantangtang_url = config["liuhantangtang_url"]
    liuhantutu_url = config["liuhantutu_url"]
    baochaoaoao_url = config["baochaoaoao_url"]
    online = True
    # 模式目前有两种模式：普通的默认模式(default)和聊天模式(chat)。聊天模式下会将未识别的指令作为聊天信息输入。
    chat_mode = True

    def hello_handler(self, message: Message):
        self.reply_message.content = f"你好{message.author.username}! " \
                                     f"我是Ayaki，请多指教了哦!\n当前版本：{self.robot_version}\n"
        remain = self._get_seremain()
        if remain >= 0:
            remain_info = "%d" % remain
            _log.info("Get remain success, remain %d" % remain)
        else:
            remain_info = "获取失败"
            _log.warning("Get sese image database remain fail")
        self.reply_message.content += "运行平台：%s\n图库图片剩余%s" % (platform.platform(), remain_info)
        self.reply_message.image = self.ayaki_logo_url
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
                self.reply_message.content = "<@%s>，你今天已经签到了哦QAQ！" % message.author.id
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

    def sese_handler(self, message: Message):
        # self.reply_message.content = "该功能暂时下线。详见频道全局公告。"
        # return self.reply_message
        try:
            newlines = []
            havesent = False
            with open("pixiv_src.csv", "r") as img_src_file:
                for line in img_src_file.readlines():
                    if line == "":
                        continue
                    if not havesent:
                        values = line.split(',')
                        try:
                            img_id = values[0]
                            img_origin_url = values[1]
                            img_url = values[2]
                            have_used = int(values[3])
                            if have_used == 1:
                                newlines.append(line)
                                continue
                        except Exception as err:
                            _log.error("read line value error: " + str(err))
                            continue
                        try:
                            title = values[4]
                        except Exception:
                            title = "暂无标题信息"
                            _log.info("Title of %s found nil" % img_id)
                        try:
                            author = values[5]
                        except Exception:
                            author = "暂无画师信息\n"
                            _log.info("Author of %s found nil" % img_id)
                        self.reply_message.content = "PID: " + img_id + ", " + title + ", 画师：" + author
                        if img_url != img_origin_url:
                            self.reply_message.content += "(原图由于过大已被压缩过)"
                        self.reply_message.image = img_url
                        new_csv_info = img_id + "," + img_origin_url + "," + img_url + ",1," + title + "," + author
                        newlines.append(new_csv_info)
                        havesent = True
                        _log.info("Found available image %s" % img_id)
                    else:
                        newlines.append(line)

                if not havesent:
                    _log.warning("Sese image database found empty")
                    self.reply_message.content = "图库已用尽，请联系<@14862092315735810791>"

            # 写回新的资源表
            with open("pixiv_src.csv", "w") as write_src_file:
                for newline in newlines:
                    write_src_file.write(newline)
            return self.reply_message

        except Exception as err:
            self.reply_message.content = "获取图片失败, " + err
            _log.error("Get sese image fail: %s" % str(err))
            return self.reply_message

    def moyu_handler(self, message: Message):
        image_api = "https://api.vvhan.com/api/moyu?type=json"
        res = requests.get(image_api)
        res_json = res.json()
        image_url = res_json['url']
        self.reply_message.image = image_url
        today = datetime.date.today()
        self.reply_message.content = "今天是%s，今天也要努力摸鱼鸭！" % today
        return self.reply_message

    def help_handler(self, message: Message):
        self.reply_message.content = "欢迎使用Ayaki，以下是我的使用说明：\n" + \
                                     "我的主要功能是运势签到和发送一张涩涩图片。图片来自Pixiv日榜前30，图片每日更新通过转存到Bill的图库发送。" + \
                                     "图库在更新时，会自动筛选剔除已经发送过的和未被作者标记为插画类型的图片。以下是命令介绍：\n" + \
                                     "/hello：来跟我打个招呼吧。我会把我的一切都交给你的！\n " + \
                                     "/signin：别忘了每天在我这里打卡，同时会自动抽签，记得每天都来看看你的运势吧！\n " + \
                                     "/sese：涩涩！涩涩是人类进步的阶梯！要涩涩的话就来让我发一张涩图吧！（我自己才不给你看，哼！）\n" + \
                                     "/moyu：再次发送今天的摸鱼日历。人活着就是为了摸鱼。\n "
        return self.reply_message

    def waifu_handler(self, message: Message):
        # 读取今日老婆签到列表
        today = datetime.date.today()
        waifu_sign_in_list_name = "waifu_sign_in_list_%s" % today
        waifu_sign_in_list = []
        if os.path.exists(waifu_sign_in_list_name):
            with open(waifu_sign_in_list_name, mode='r') as list:
                for line in list.readlines():
                    waifu_sign_in_list.append(line.replace('\n', ''))
            if message.author.id in waifu_sign_in_list:
                # 用户ID已签到
                self.reply_message.content = "<@%s>，你今天已经有老婆了！" % message.author.id
            else:
                # 获取今日老婆
                self.waifu_sign_in_op_handler(message)
                # 将ID添加到老婆今日签到列表中
                with open(waifu_sign_in_list_name, mode="a") as list_file:
                    list_file.write(message.author.id + '\n')
        else:
            with open(waifu_sign_in_list_name, mode='w') as ff:
                _log.info("Create today's waifu sign in list success")
            # 获取今日老婆
            self.waifu_sign_in_op_handler(message)
            # 将ID添加到今日老婆签到列表中
            with open(waifu_sign_in_list_name, mode="a") as list_file:
                list_file.write(message.author.id + '\n')
        return self.reply_message

    def chat_handler(self, message: Message):
        texts = message.content.split(' ')
        text = texts[-1]
        if "你" in text:
            if "谁" in text or "名字" in text:
                self.reply_message.content = "我是Ayaki，Ayaki是我。"
                return self.reply_message
        url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + text
        tuling = requests.get(url)
        content = tuling.json()
        _log.info(f"get reply: {content['content']}")
        self.reply_message.content = content['content'].replace('{br}', '\n')
        return self.reply_message

    def openai_handler(self, message: Message):
        texts = message.content.split(' ')
        text = texts[-1]
        body = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}]
        }

        url = "https://api.openai.com/v1/chat/completions"
        openaiRequest = requests.post(url=url,
                                      headers={"Authorization": "Bearer " + private_config["openai_key"],
                                               "Content-Type": "application/json"},
                                      json=body)
        content = openaiRequest.json()
        # _log.info(content)
        result = content['choices'][0]['message']['content']
        _log.info(f"Got reply: {result}")
        self.reply_message.content = result.replace('\n\n', '')
        return self.reply_message

    # 签到请求处理，返回签到结果
    def sign_in_op_handler(self, message: Message):
        # 随机获得吉等级
        unsei_index = random.randint(0, 6)
        unsei = self.unsei_list[unsei_index]
        _log.info("Get unsei_index success: %s" % unsei_index)
        # 读取并获得宜忌事件列表
        events_list = config["event_list"]
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

        message = "<@%s> 签到成功!\n" % message.author.id
        today = datetime.date.today()
        message += "今天是%s\n" % today
        message += "今日运势: %s\n" % unsei
        message += good + "\n"
        message += bad
        _log.info("Get all luck success")
        return message

    def waifu_sign_in_op_handler(self, message: Message):
        if message.author.id == private_config["tutu_id"].replace('\n', ''):
            _log.info("Get tutu's waifu request")
            rdnum = random.randint(0, 100)
            if rdnum < 20:
                self.reply_message.content = f"<@{message.author.id}> 喂！你的老婆永远是🍬🍬！"
                self.reply_message.image = config["liuhantangtang_url"]
            else:
                waifu_list = config["waifu_list"]
                waifu_index = random.randint(0, len(waifu_list) - 1)
                self.reply_message.content = f"<@{message.author.id}> 你今天的老婆是：{waifu_list[waifu_index]['name']}\n"
                self.reply_message.content += f"她从{waifu_list[waifu_index]['origin']}来找你啦！"
                self.reply_message.image = waifu_list[waifu_index]['url']
        else:
            waifu_list = config["waifu_list"]
            waifu_index = random.randint(0, len(waifu_list) - 1)
            self.reply_message.content = f"<@{message.author.id}> 你今天的老婆是：{waifu_list[waifu_index]['name']}\n"
            self.reply_message.content += f"她从{waifu_list[waifu_index]['origin']}来找你啦！"
            self.reply_message.image = waifu_list[waifu_index]['url']
            # self.reply_message.ark = Ark(
            #     template_id=37,
            #     kv=[
            #         ArkKv(key="#METATITLE#", value=f"你今天的老婆是{waifu_list[waifu_index]['name']}!"),
            #         ArkKv(key="#PROMPT#", value="今日老婆"),
            #         ArkKv(key="METASUBTITLE#", value=f"她从{waifu_list[waifu_index]['origin']}来找你啦！"),
            #         ArkKv(key="METACOVER#", value=waifu_list[waifu_index]['url']),
            #     ]
            # )
        _log.info("Get today' waifu success")

    def _get_seremain(self):
        cnt = 0
        try:
            with open("pixiv_src.csv", "r") as src:
                for line in src.readlines():
                    values = line.split(',')
                    try:
                        have_used = int(values[3])
                        if have_used == 0:
                            cnt += 1
                    except Exception as e:
                        _log.error(e)
                        continue
        except Exception as err:
            cnt = -1
            _log.error("Get seremain fail, " + str(err))
        return cnt
