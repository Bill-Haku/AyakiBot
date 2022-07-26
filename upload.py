import os.path

import urllib3
import requests
import base64
import os
from pixivpy3 import *
from PIL import Image
from botpy.ext.cog_yaml import read

sent_image_list = []
private_config = read(os.path.join(os.path.dirname(__file__), "private_config.yaml"))


def get_sent_image_list():
    with open("pixiv_src.csv", "r") as img_src_file:
        for line in img_src_file.readlines():
            if line == "":
                continue
            values = line.split(',')
            img_id = str(values[0])
            if img_id == "update":
                continue
            if img_id in sent_image_list:
                continue
            else:
                sent_image_list.append(img_id)


# 压缩图片并保存
def compression(srcFile, distFile):
    size_ratio = 0.9
    quality = 80
    try:
        # 读取原图
        srcImg = Image.open(srcFile)
        w, h = srcImg.size
        # 重新设置图片尺寸和选项，Image.ANTIALIAS：平滑抗锯齿
        distImg = srcImg.resize((int(w * size_ratio), int(h * size_ratio)), Image.ANTIALIAS)
        # 保存为新图
        distImg.save(distFile, quality=quality)
        print(distFile + " 压缩成功！")
    except Exception as e:
        print(distFile + " 压缩失败！异常信息：", e)


# 爬取一张图片并上传到我的图床并返回我的图床上的URL
def _upload_pixiv_image():
    get_sent_image_list()
    # print(sent_image_list)
    pixiv_api = AppPixivAPI()
    pixiv_api.auth(refresh_token=private_config["pixiv_refresh_token"])

    pixiv_json_result = pixiv_api.illust_ranking('day')
    illusts = pixiv_json_result.illusts

    for cur_Illust in illusts:
        # print(cur_Illust)
        if str(cur_Illust.id) in sent_image_list:
            print("have added this image")
            continue
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        headers = {'Referer': 'https://www.pixiv.net/'}

        top_json_result = pixiv_api.illust_detail(cur_Illust.id)
        illustorigin = top_json_result.illust
        # print(illustorigin)
        author = cur_Illust.user['name']
        # print(author)

        if illustorigin["type"] != 'illust':
            print("Get %s, skip" % illustorigin["type"])
            continue


        if str(illustorigin.meta_single_page) != '{}':
            url = illustorigin.meta_single_page['original_image_url']
        else:
            url = illustorigin.meta_pages[0].image_urls['original']
        try:
            res = requests.get(url, headers=headers, verify=False)
        except Exception as err:
            print("occured error " + str(err))
            continue

        with open("pixiv_%s.jpg" % cur_Illust.id, 'wb') as f:
            file_name = "pixiv_%s.jpg" % cur_Illust.id
            f.write(res.content)
            encoded_str = base64.b64encode(res.content)
            data = {
                "source": encoded_str,
                "action": "upload",
                "key": "26c556d135a0f1c18048fbac0d9b85c8",
                "format": "txt"
            }
            post_url = "http://nas.hakubill.tech:1234/api/1/upload"
            chevereto_req = requests.post(post_url, verify=False, data=data)
            img_url = str(chevereto_req.content, 'utf-8')
            print(img_url)

            # 检查图片大小
            size = os.path.getsize(file_name)
            size /= 1024  # 单位化为kB
            print(size)
            img_compressed_url = img_url
            if size > 4000:
                # 文件过大，额外保存一个压缩版
                file_name_compressed = "pixiv_%s_compressed.png" % cur_Illust.id
                try:
                    compression(file_name, file_name_compressed)
                    try:
                        with open(file_name_compressed, "rb") as f_compressed:
                            encoded_str = base64.b64encode(f_compressed.read())
                        data = {
                            "source": encoded_str,
                            "action": "upload",
                            "key": "26c556d135a0f1c18048fbac0d9b85c8",
                            "format": "txt"
                        }
                        post_url = "http://nas.hakubill.tech:1234/api/1/upload"
                        chevereto_req = requests.post(post_url, verify=False, data=data)
                        img_compressed_url = str(chevereto_req.content, 'utf-8')
                        print("compressed " + img_compressed_url)
                    except Exception as err:
                        print("save compress fail " + str(err))
                except Exception as err:
                    print("compress fail: " + str(err))
                    continue

            # 写入csv文件
            # csv文件格式: "id", "img_url", "img_compressed_url", "have_used?", "title"
            with open("pixiv_src.csv", "a+") as w:
                csv_line = str(cur_Illust.id) + "," + img_url + "," + img_compressed_url + ",0," + \
                           str(cur_Illust.title) + "," + author + "\n"
                w.write(csv_line)



if __name__ == '__main__':
    _upload_pixiv_image()
