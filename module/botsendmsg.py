# QQ机器人发送消息
import time
import random
from module.config import *
from mirai import *
from module.logger import *

adapter = HTTPAdapter(verify_key=config["key"], host=config["hostname"], port=config["post"])
bot = Mirai(qq=config["QQ"], adapter=adapter)

# 发送复合信息
async def send_compound_message(message: dict):
    # 校验是否存在
    if "admin_msg" in message.keys():
        # 校验数据类型
        if isinstance(message["admin_msg"], list):
            # 多句输出
            for msg in message["admin_msg"]:
                await say_group(config["admin_qun"], msg)
        else:
            # 单句输出
            await say_group(config["admin_qun"], message["admin_msg"])
    if "player_msg" in message.keys():
        if isinstance(message["player_msg"], list):
            for msg in message["player_msg"]:
                await say_group(config["player_qun"], msg)
        else:
            await say_group(config["player_qun"], message["player_msg"])

# 普通消息
async def say_group(group, msg):
    logger.info("[消息]->群:{group}:{msg}".format(group=group, msg=msg))
    time.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain([
        Plain(msg)
    ]))

# 警告消息
async def say_group_warning(group, msg):
    logger.warning("[消息]->群:{group}:{msg}".format(group=group, msg=msg))
    time.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain([
        Plain(msg)
    ]))
