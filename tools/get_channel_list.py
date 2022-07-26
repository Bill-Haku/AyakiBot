import os
import qqbot
from botpy.ext.cog_yaml import read

config = read(os.path.join(os.path.dirname(__file__), "../private_config.yaml"))
token = qqbot.Token(config["appid"], config["access_token"])
guildid = config["guildid"]

# 获取子频道的ID列表
api = qqbot.ChannelAPI(token, False)
channels = api.get_channels(guildid)
for channel in channels:
    print(channel.id + channel.name)
