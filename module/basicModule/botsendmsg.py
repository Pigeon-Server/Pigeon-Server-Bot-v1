# QQ机器人发送消息
import random
from module.basicModule.config import *
from mirai import *
from module.basicModule.logger import *

adapter = HTTPAdapter(verify_key=config["QQ_Config"]["Key"], host=config["QQ_Config"]["Host"],
                      port=config["QQ_Config"]["Post"])
bot = Mirai(qq=config["QQ_Config"]["QQ"], adapter=adapter)


# 发送复合信息
async def send_compound_message(message: dict) -> None:
    # 校验是否存在
    if "QQ" in message.keys():
        if "admin_msg" in message.keys():
            await say_group(config["QQ_Config"]["Group_Config"]["admin_qun"], message["admin_msg"])
        if "player_msg" in message.keys():
            await at_say_group(config["QQ_Config"]["Group_Config"]["player_qun"], message["player_msg"], message["QQ"])
    else:
        if "admin_msg" in message.keys():
            # 校验数据类型
            if isinstance(message["admin_msg"], list):
                # 多句输出
                for msg in message["admin_msg"]:
                    await say_group(config["QQ_Config"]["Group_Config"]["admin_qun"], msg)
            else:
                # 单句输出
                await segmentation(config["QQ_Config"]["Group_Config"]["admin_qun"], message["admin_msg"])
        if "player_msg" in message.keys():
            if isinstance(message["player_msg"], list):
                for msg in message["player_msg"]:
                    await say_group(config["QQ_Config"]["Group_Config"]["player_qun"], msg)
            else:
                await segmentation(config["QQ_Config"]["Group_Config"]["player_qun"], message["player_msg"])


async def segmentation(qun: int, message: str) -> None:
    """
    切分输出\n
    :param qun: 群号(int)
    :param message: 发送的消息(str)
    :return: None
    """

    msg = "".join(map(str, message)).split("\n")  # 按换行符切分
    lineCount = 0  # 定义计数器变量
    sendCount = 0
    tempStr = ""  # 定义临时存储变量
    for raw in msg:
        lineCount += 1  # 每次循环计数器加1
        tempStr = tempStr + raw + "\n"
        if lineCount == config["QQ_Config"]["Msg_len_MAX"]:
            lineCount = 0  # 重置循环计数器
            sendCount += 1  # 发送计数器加1
            tempStr.strip()  # 删除末尾换行符
            logger.info(f"切分发送:{tempStr}")
            if sendCount == 6:  # 第六次发送时
                sendCount = 0  # 重置发送计数器
                await asyncio.sleep(2)  # 延时两秒
                await say_group(qun, tempStr)
            else:
                await say_group(qun, tempStr)
            tempStr = ""  # 重置字符串
    tempStr.strip()  # 删除末尾换行符
    print(lineCount)
    if lineCount > 1:
        await say_group(qun, tempStr)  # 循环结束发送一次，防止行数无法触发输出


# 普通消息
async def say_group(group, msg) -> None:
    logger.info(f"[消息]->群:{group}:{msg}")
    await asyncio.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain([
        Plain(msg)
    ]))


# 艾特消息
async def at_say_group(group, msg, qq) -> None:
    logger.info(f"[消息]->群:{group}:{msg}")
    await asyncio.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain(
        [At(qq),
         Plain(msg)]
    ))


# 警告消息
async def say_group_warning(group, msg) -> None:
    logger.warning(f"[消息]->群:{group}:{msg}")
    await asyncio.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain([
        Plain(msg)
    ]))


# 发送图片
async def sendImage(group, base, QQ=None) -> None:
    logger.info(f"[图片]->群:{group}")
    await asyncio.sleep(random.uniform(1.0, 0.3))
    if QQ is not None:
        await bot.send_group_message(group, MessageChain([
            At(QQ)
        ]))
    await bot.send_group_message(group, MessageChain([
        Image(base64=base)
    ]))

# 回复消息
async def reply_group(group, msg, targetMsg) -> None:
    logger.info(f"[图片]->群:{group}")
    await asyncio.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain([
        Plain(msg)
    ]), targetMsg)

# 欢迎消息
async def welcome_msg(group, msg, QQ) -> None:
    logger.info(f"[图片]->群:{group}")
    await asyncio.sleep(random.uniform(1.0, 0.3))
    await bot.send_group_message(group, MessageChain([
        At(QQ),
        Plain(msg)
    ]))
