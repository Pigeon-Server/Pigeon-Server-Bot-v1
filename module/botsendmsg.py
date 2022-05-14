import time
import random
from module.config import config
from mirai import *
from module.logger import log

adapter = HTTPAdapter(verify_key=config["key"], host=config["hostname"], port=config["post"])
bot = Mirai(qq=config["QQ"], adapter=adapter)


async def say_group(group, msg):
    print("[消息]->群:{group}:{msg}".format(group=group, msg=msg))
    time.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain([
        Plain(msg)
    ]))


async def say_group_info(group, msg):
    log.info("[消息]->群:{group}:{msg}".format(group=group, msg=msg))
    time.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain([
        Plain(msg)
    ]))


async def say_group_warning(group, msg):
    log.warning("[消息]->群:{group}:{msg}".format(group=group, msg=msg))
    time.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain([
        Plain(msg)
    ]))
