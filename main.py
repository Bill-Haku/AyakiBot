import qqbot
import requests
import urllib3
import base64
from qqbot import *
from pixivpy3 import *

appid = "102005740"
sandboxid = 4294837189
guildid = "5440859059313954953"  # 之外语文
test_channel_id = "5463311"
hphoto_channel_id = "3613561"
access_token = "jIhM72IaFkMZmi8X8KIgxCzr6HbIiEgi"
access_secret = "QSGtIVUIsITWKxLX"
pixiv_access_token = "2xohFPRY2kf16FOuUok9gD16abM2DXQWFXwcOcaB6qI"
pixiv_refresh_token = "XlkWbEVUqVkS_zjpNb64LSD5wl7E-0CTaxmcziKp5rg"
robot_version = "3.1.4"

token = qqbot.Token(appid, access_token)


# 爬取一张图片并上传到我的图床并返回我的图床上的URL(已废弃）
def _get_pixiv_image(index: int):
    pixiv_api = AppPixivAPI()
    pixiv_api.auth(refresh_token=pixiv_refresh_token)

    pixiv_json_result = pixiv_api.illust_ranking('day')
    # for illust in pixiv_json_result.illusts:
    #     print(" p1 [%s] %s" % (illust.title, illust.image_urls.large))
    cur_Illust = pixiv_json_result.illusts[index]

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {'Referer': 'https://www.pixiv.net/'}
    print(cur_Illust)

    top_json_result = pixiv_api.illust_detail(cur_Illust.id)
    illustorigin = top_json_result.illust
    url = illustorigin.meta_single_page['original_image_url']
    # return url
    res = requests.get(url, headers=headers, verify=False)
    with open("pixiv_%s.jpg" % cur_Illust.id, 'wb') as f:
        file_name = "pixiv_%s.jpg" % cur_Illust.id
        f.write(res.content)
        encoded_str = base64.b64encode(res.content)
        # files = {"file": res.content}
        data = {
            "source": encoded_str,
            "action": "upload",
            "key": "26c556d135a0f1c18048fbac0d9b85c8",
            "format": "txt"
        }
        post_url = "http://billdc.synology.me:1234/api/1/upload"
        chevereto_req = requests.post(post_url, verify=False, data=data)
        print(chevereto_req.content)
        img_url = str(chevereto_req.content, 'utf-8')
        print(img_url)
        return img_url


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
        "event %s" % event + ", receive at message %s" % message.content + ", came from %s-%s" % (message.author.id, message.author.username))

    if message.content.find("爱你") != -1 or message.content.find("love you") != -1:
        qqbot.logger.info("Recognized command love you")
        if message.author.username == "水里的碳酸钙":
            hello_message.content = "我也爱你哦"
        else:
            hello_message.content = "对不起，你是个好人。"

    # 发送一张图库的图片
    elif message.content.find("sese") != -1:
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
                        img_id = values[0]
                        img_origin_url = values[1]
                        img_url = values[2]
                        have_used = int(values[3])
                        if have_used == 1:
                            newlines.append(line)
                            continue
                        hello_message.content = "PID: " + img_id
                        if img_url != img_origin_url:
                            hello_message.content += "(原图由于过大已被压缩过)"
                        hello_message.image = img_url
                        print("sent image %s" % img_id)
                        new_csv_info = img_id + "," + img_origin_url + "," + img_url + ",1\n"
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
    elif message.content.find("seremain") != -1:
        qqbot.logger.info("Recognized command seremain")
        remain = _get_seremain()
        if remain >= 0:
            hello_message.content = "图库还剩余%d张" % remain
            qqbot.logger.info("Get seremain success, remain %d" % remain)
        else:
            hello_message.content = "获取图库剩余图片失败"
            qqbot.logger.warning("Get sese image database remain fail")
    else:
        qqbot.logger.info("Recognized command default")
        hello_message.content = "你好%s! 我是Ayaki，请多指教了哦! 当前版本：%s" % (message.author.username, robot_version)
        hello_message.image = "http://billdc.synology.me:1234/images/2022/02/27/Ayaki-Watermark.png"

    hello_message.msg_id = message.id
    msg_api = qqbot.MessageAPI(token, False).with_timeout(10)
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



# 私信回复
def _direct_message_handler(event, message: Message):
    hello_message = MessageSendRequest()
    # 打印返回信息
    qqbot.logger.info(
        "event %s" % event + ", receive direct message %s" % message.content + ", came from %s-%s" % (message.author.id, message.author.username))
    qqbot.logger.info("Recognized command default")
    hello_message.content = "你好%s! 我是Ayaki，请多指教! 当前版本：%s" % (message.author.username, robot_version)
    hello_message.image = "http://billdc.synology.me:1234/images/2022/02/27/Ayaki-Watermark.png"
    hello_message.msg_id = message.id
    dms_api = qqbot.DmsAPI(token, False).with_timeout(10)
    dms_api.post_direct_message(message.guild_id, hello_message)


if __name__ == '__main__':
    userApi = qqbot.UserAPI(token, False)
    user = userApi.me()
    # 打印机器人名字
    qqbot.logger.info("Starting %s..." % user.username)

    ayaki_at_message_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _at_message_handler)
    ayaki_direct_message_handler = qqbot.Handler(qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _direct_message_handler)
    qqbot.listen_events(token, False, ayaki_at_message_handler)
    qqbot.listen_events(token, False, ayaki_direct_message_handler)
    qqbot.logger.info("%s start complete, current version %s" % (user.username, robot_version))
