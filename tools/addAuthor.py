import json

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
from PIL import Image
from pixivpy3 import *
from botpy.ext.cog_yaml import read

config = read(os.path.join(os.path.dirname(__file__), "../config.yaml"))


def addAuthor():
    havesent = False
    newlines = []
    pixiv_api = AppPixivAPI()
    pixiv_api.auth(refresh_token=config["pixiv_refresh_token"])
    with open("../pixiv_src.csv", "r") as img_src_file:
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
                    print("read line value error: " + str(err))
                    continue
                try:
                    title = values[4]
                except Exception:
                    title = "暂无标题信息\n"
                    print("Title of %s found nil" % img_id)
                try:
                    author = values[5]
                    haveAuthor = True
                except Exception:
                    haveAuthor = False
                if not haveAuthor:
                    author = "暂无画师信息\n"
                    print("Author of %s found nil" % img_id)
                    # 获取画师信息
                    result = pixiv_api.illust_detail(img_id)
                    illustOrigin = result.illust
                    # illustOrigin = str(illustOrigin)
                    print(illustOrigin)
                    author = illustOrigin["type"]
                    print(author)

                new_csv_info = img_id + "," + img_origin_url + "," + img_url + ",1," + title + "," + author
                newlines.append(new_csv_info)
                print("Set image %s" % img_id)
            else:
                newlines.append(line)

        if not havesent:
            print("Sese image database found empty")

    # 写回新的资源表
    # with open("../pixiv_src.csv", "w") as write_src_file:
    #     for newline in newlines:
    #         write_src_file.write(newline)


if __name__ == '__main__':
    addAuthor()
