# Bot 主体
# by Pigeon Server Team
from module.basicModule.config import config
from module.basicModule.logger import *
# 判断配置文件版本，如果版本不正确报错并退出
if "Config_Version" in config.keys() and config["Config_Version"] == 2.1:
    from module.qq_bot import QQ_bot
    # 启动
    QQ_bot()
else:
    logger.error("配置文件版本错误，请删除后重新生成")
