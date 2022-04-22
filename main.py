import qqbot
from qqbot import MessageSendRequest, Message

appid = "102005740"
sandboxid = 4294837189
guildid = "5440859059313954953" # 之外语文
test_channel_id = "5463311"
hphoto_channel_id = "3613561"
access_token = "jIhM72IaFkMZmi8X8KIgxCzr6HbIiEgi"
access_secret = "QSGtIVUIsITWKxLX"

token = qqbot.Token(appid, access_token)

# 群中被at的回复
def _at_message_handler(event, message: Message):
    hello_message = MessageSendRequest()
    # 打印返回信息
    qqbot.logger.info("event %s" % event + ",receive at message %s" % message.content)
    hello_message.content = "Hello %s! My name is Ayaki!" % (message.author.username)
    hello_message.msg_id = message.id
    msg_api = qqbot.MessageAPI(token, False)
    msg_api.post_message(message.channel_id, hello_message)

# 私信回复
def _direct_message_handler(event, message: Message):
    hello_message = MessageSendRequest()
    # 打印返回信息
    qqbot.logger.info("event %s" % event + ",receive direct message %s" % message.content)
    hello_message.content = "Hello %s! My name is Ayaki!" % (message.author.username)
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
