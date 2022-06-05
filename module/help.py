# 帮助导航
from module.botsendmsg import *


async def help_start(qun):
    await say_group(qun, "[Pigeon Server · 帮助]\n"
                         "可用子命令：\n"
                         "!帮助 白名单\n"
                         "!帮助 假人\n"
                         "!帮助 黑名单\n"
                         "!帮助 测试服OP(开发中)\n")
