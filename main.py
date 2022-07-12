import random

import qqbot
import requests
import urllib3
import base64
import datetime
import time
import os
import _thread
import platform
import schedule as sch
from qqbot import *
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
robot_version = "3.5.6"

liuhantangtang_url = "http://image.hakubill.tech:1234/images/2022/07/04/IMG_2641.jpg"
liuhantutu_url = "http://image.hakubill.tech:1234/images/2022/07/04/IMG_2642.jpg"
baochaoaoao_url = "http://image.hakubill.tech:1234/images/2022/07/04/IMG_2643.jpg"

token = qqbot.Token(appid, access_token)

unsei_list = ["★★★大吉★★★", "★★中吉★★", "★小吉★", "吉", "末吉", "凶", "大凶"]


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)


def get_file_modified_time(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)

# 签到请求处理，返回签到结果
def sign_in_handler(message: Message):
    # 随机获得吉等级
    unsei_index = random.randint(0,6)
    unsei = unsei_list[unsei_index]
    qqbot.logger.info("Get unsei_index success: %s" % unsei_index)
    # 读取并获得宜忌事件列表
    events_list = []
    with open("events.txt", mode='r') as events_file:
        events_list = events_file.readlines()
    # 根据等级返回宜忌事件
    good = "宜："
    bad = "忌："
    threshold = 90
    threshold2 = 20
    manshi_rand = random.randint(0,100)
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
            good_num = random.randint(4,5)
            bad_num = random.randint(1,2)
        elif unsei_index == 1:
            good_num = random.randint(3,4)
            bad_num = random.randint(2,3)
        elif unsei_index == 2:
            good_num = random.randint(3,4)
            bad_num = random.randint(2,3)
        elif unsei_index == 3:
            good_num = random.randint(2,4)
            bad_num = random.randint(2,4)
        elif unsei_index == 4:
            good_num = random.randint(2,4)
            bad_num = random.randint(2,4)
        elif unsei_index == 5:
            good_num = random.randint(2,3)
            bad_num = random.randint(3,4)
        elif unsei_index == 6:
            good_num = random.randint(1,2)
            bad_num = random.randint(3,5)
        index_dict = {}
        # 获得宜事件
        for i in range(good_num):
            while True:
                index = random.randint(0,len(events_list)-1)
                if index not in index_dict:
                    index_dict[index] = True
                    break
            good += events_list[index].replace('\n', '')
            good += "  "
        # 获得忌事件
        for i in range(bad_num):
            while True:
                index = random.randint(0,len(events_list)-1)
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
    qqbot.logger.info("Get all luck success")
    return message


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

    # 发送一张图库的图片
    elif message.content.find("/sese") != -1:
        qqbot.logger.info("Recognized command sese")
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
                            qqbot.logger.error("read line value error: " + str(err))
                            continue
                        try:
                            title = values[4]
                        except Exception:
                            title = "暂无标题信息\n"
                            qqbot.logger.info("Title of %s found nil" % img_id)
                        try:
                            author = values[5]
                        except Exception:
                            author = "暂无画师信息\n"
                            qqbot.logger.info("Author of %s found nil" % img_id)
                        hello_message.content = "PID: " + img_id + ", " + title + ", 画师：" + author
                        if img_url != img_origin_url:
                            hello_message.content += "(原图由于过大已被压缩过)"
                        hello_message.image = img_url
                        new_csv_info = img_id + "," + img_origin_url + "," + img_url + ",1," + title + "," + author
                        newlines.append(new_csv_info)
                        havesent = True
                        qqbot.logger.info("Found available image %s" % img_id)
                    else:
                        newlines.append(line)

                if not havesent:
                    qqbot.logger.warning("Sese image database found empty")
                    hello_message.content = "图库已用尽，请联系@水里的碳酸钙"

            # 写回新的资源表
            with open("pixiv_src.csv", "w") as write_src_file:
                for newline in newlines:
                    write_src_file.write(newline)

        except Exception as err:
            hello_message.content = "获取图片失败, " + err
            qqbot.logger.error("Get sese image fail: %s" % str(err))

    # 获取图库剩余图片
    # elif message.content.find("/seremain") != -1:
    #     qqbot.logger.info("Recognized command seremain")
    #     remain = _get_seremain()
    #     if remain >= 0:
    #         hello_message.content = "图库还剩余%d张" % remain
    #         qqbot.logger.info("Get seremain success, remain %d" % remain)
    #     else:
    #         hello_message.content = "获取图库剩余图片失败"
    #         qqbot.logger.warning("Get sese image database remain fail")

    # 打招呼
    elif message.content.find("/hello") != -1:
        qqbot.logger.info("Recognized command hello")
        hello_message.content = "你好%s! 我是Ayaki，请多指教了哦! 当前版本：%s" % (message.author.username, robot_version)
        hello_message.image = "http://nas.hakubill.tech:1234/images/2022/02/27/Ayaki-Watermark.png"

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

    # 签到与运势功能
    elif message.content.find("/signin") != -1:
        qqbot.logger.info("Recognized command signin")
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
                hello_message.content = "%s，你今天已经签到了哦QAQ！" % message.author.username
            else:
                # 签到
                hello_message.content = sign_in_handler(message)
                # 将ID添加到今日签到列表中
                with open(sign_in_list_name, mode="a") as list_file:
                    list_file.write(message.author.id + '\n')
        else:
            with open(sign_in_list_name, mode='w') as ff:
                qqbot.logger.info("Create today's sign in list success")
            # 签到
            hello_message.content = sign_in_handler(message)
            # 将ID添加到今日签到列表中
            with open(sign_in_list_name, mode="a") as list_file:
                list_file.write(message.author.id + '\n')
        if hello_message.content.find("流汗糖豆") != -1:
            hello_message.image = liuhantangtang_url
        elif hello_message.content.find("爆炒🍬🍬") != -1:
            hello_message.image = liuhantangtang_url
        elif hello_message.content.find("流汗土豆") != -1:
            hello_message.image = liuhantutu_url
        elif hello_message.content.find("爆炒土土") != -1:
            hello_message.image = liuhantutu_url
        elif hello_message.content.find("爆炒奥奥") != -1:
            hello_message.image = baochaoaoao_url
        msg_reference = MessageReference(message_id=message.id)
        hello_message.message_reference = msg_reference

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


if __name__ == '__main__':
    userApi = qqbot.UserAPI(token, False)
    user = userApi.me()
    # 打印机器人名字
    qqbot.logger.info("Starting %s..." % user.username)
    qqbot.logger.info("Platform: %s" % platform.platform())
    qqbot.logger.info("Python version: %s" % platform.python_version())

    ayaki_at_message_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _at_message_handler)
    ayaki_direct_message_handler = qqbot.Handler(qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _direct_message_handler)
    # ayaki_moyu_handler = qqbot.Handler(qqbot.HandlerType.PLAIN_EVENT_HANDLER, _moyu_handler)
    qqbot.listen_events(token, False, ayaki_at_message_handler)
    qqbot.listen_events(token, False, ayaki_direct_message_handler)
    # qqbot.listen_events(token, False, ayaki_moyu_handler)
    qqbot.logger.info("%s start complete, current version %s" % (user.username, robot_version))
    _thread.start_new_thread(_moyu_handler())
