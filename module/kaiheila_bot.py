from khl import *
from module.basicModule.config import *

# 创建开黑啦机器人
kaiHeiLa = Bot(token=config["kaiHeiLaKey"])


def kaiHeiLaBot():
    @kaiHeiLa.command(regex=r'[\s\S]*')
    async def main(msg: Message):
        id = msg.author.id
        if msg.author.bot:
            isBot = 1
        else:
            isBot = 0
        print("[Bot-开黑啦]收到消息{group}<-{id}:{msg}".format(id=id, msg=msg.content, group=msg.target_id))
        if isBot == 0:
            await msg.reply("收到消息，回复成功")
            await msg.ctx.channel.send('world only for you too!', channel=msg.target_id)
    kaiHeiLa.run()
