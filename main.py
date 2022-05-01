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

token = qqbot.Token(appid, access_token)


# 爬取一张图片并上传到我的图床并返回我的图床上的URL
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


# 群中被at的回复
def _at_message_handler(event, message: Message):
    hello_message = MessageSendRequest()
    # 打印返回信息
    qqbot.logger.info(
        "event %s" % event + ", receive at message %s" % message.content + ", came from %s" % message.author.username)

    if message.content.find("爱你") != -1 or message.content.find("love you") != -1:
        if message.author.username == "水里的碳酸钙":
            hello_message.content = "我也爱你哦"
        else:
            hello_message.content = "对不起，你是个好人。"
    elif message.content.find("sese") != -1:
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
                    else:
                        newlines.append(line)

                if not havesent:
                    hello_message.content = "图库已用尽，请联系@水里的碳酸钙"

            # 写回新的资源表
            with open("pixiv_src.csv", "w") as write_src_file:
                for newline in newlines:
                    # print(newline)
                    write_src_file.write(newline)

        except Exception as err:
            hello_message.content = "获取图片失败" + err
            qqbot.logger.info("get image fail")
            qqbot.logger.info(err)

    else:
        hello_message.content = "你好%s! 我是Ayaki，请多指教了哦!" % (message.author.username)
        hello_message.image = "http://billdc.synology.me:1234/images/2022/02/27/Ayaki-Watermark.png"
    hello_message.msg_id = message.id
    msg_api = qqbot.MessageAPI(token, False)
    msg_api.post_message(message.channel_id, hello_message)


# 私信回复
def _direct_message_handler(event, message: Message):
    hello_message = MessageSendRequest()
    # 打印返回信息
    qqbot.logger.info(
        "event %s" % event + ", receive direct message %s" % message.content + ", came from %s" % message.author.username)
    hello_message.content = "你好%s! 我是Ayaki，请多指教!" % (message.author.username)
    hello_message.image = "http://billdc.synology.me:1234/images/2022/02/27/Ayaki-Watermark.png"
    hello_message.msg_id = message.id
    dms_api = qqbot.DmsAPI(token, False)
    dms_api.post_direct_message(message.guild_id, hello_message)


if __name__ == '__main__':
    userApi = qqbot.UserAPI(token, False)
    user = userApi.me()
    # 打印机器人名字
    print(user.username)
    guilds = userApi.me_guilds()
    for guild in guilds:
        print(guild.id + " " + guild.name)

    channelApi = qqbot.ChannelAPI(token, False)
    channels = channelApi.get_channels(guildid)
    for channel in channels:
        print(channel.id + " " + channel.name)

    ayaki_at_message_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _at_message_handler)
    ayaki_direct_message_handler = qqbot.Handler(qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _direct_message_handler)
    qqbot.listen_events(token, False, ayaki_at_message_handler)
    qqbot.listen_events(token, False, ayaki_direct_message_handler)
