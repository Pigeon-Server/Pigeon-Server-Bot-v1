from khl import *
from module.config import *

# 创建开黑啦机器人
kaiheila = Bot(token=config["kaiheila-key"])


def kaiheila_bot():
    print(1)
    @kaiheila.command(regex=r'[\s\S]*')
    async def main(msg: Message):
        global isbot
        id = msg.author.id
        if msg.author.bot:
            isbot = 1
        else:
            isbot = 0
        print("[Bot-开黑啦]收到消息{group}<-{id}:{msg}".format(id=id, msg=msg.content, group=msg.target_id))
        if isbot == 0:
            await msg.reply("收到消息，回复成功")
            await msg.ctx.channel.send('world only for you too!', channel=msg.target_id)

    kaiheila.run()
