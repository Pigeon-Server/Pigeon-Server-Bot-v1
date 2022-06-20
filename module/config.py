# 配置文件
import collections
import json
from pathlib import Path
from module.logger import *
import os
config = os.path.join('config')
if not os.path.exists(config):
    os.makedirs(config)

def Creat_config(filename: str):
    config = {}
    if filename == "config.json":
        config = {
            # config（QQ）
            "QQ": 10000,  # QQ账户
            "hostname": "127.0.0.1",  # Http-API
            "key": "Key",  # Http-Key
            "post": 8080,  # Http-Post
            "admin_qun": 23333,  # 管理员群
            "player_qun": 23333,  # 玩家群
            # config(database)
            "db_host": "127.0.0.1",  # 数据库地址
            "db_user": "root",  # 数据库账户
            "db_password": "root",  # 数据库密码
            "database": "Bot",  # 表名
            # config(RCON)
            "RCON_password": "password",  # RCON密码
            "RCON_host": "127.0.0.1",  # RCON地址
            "RCON_port": "1337",  # RCON端口
            "RCONHost": "127.0.0.1",  # RCON地址
            "RCONPassword": "password",  # RCON密码
            "RCONPort": "1537",  # RCON端口
            # config(服务器列表)
            "serverlist": ["127.0.0.1", "127.0.0.1:25566"],
            "servername": ["Server1", "Server2"],
            # config(开黑啦)
            "kaiheila-key": "",
            # 版本检查
            "Check-Minecraft-Version": {
                "release": "None",
                "snapshot": "None"
            }
        }
    elif filename == "FAQ.json":
        config = {
            "FAQ": [
                {
                    "qun": 856572659,
                    "F": "Q"
                },
                {
                    "qun": 540689198,
                    "F": "Q"
                },
                {
                    "qun": "global",
                    "F": "Q"
                }
            ]
        }
    elif filename == "modules.json":
        config = {
            "enable_whitelist": "true",
            "enable_banlist": "true",
            "enable_botmanager": "true",
            "enable_testop": "true",
        }
    logger.debug("[Bot]正在尝试创建配置文件")
    try:
        with open(f"config/{filename}", "w") as write_file:
            json.dump(config, write_file, indent="\t", sort_keys=True, ensure_ascii=False)
    except:
        logger.error("[Bot]配置文件创建失败")
    else:
        logger.debug("[Bot]配置文件创建成功")

# 修改config
def updata_config(key, value, configname, filename):
    File = open(f"config/{filename}", "r+", encoding='utf-8')  # 打开文件
    data = configname  # 存储原始文件
    File.truncate()
    data[key] = value  # 添加/修改
    File.write(  # 写入
        json.dumps(data, indent="\t", sort_keys=True, ensure_ascii=False)
    )
    File.close()
    reloadConfig()

# 加载config
def load_config(filename):
    if not Path("config/" + filename).is_file():
        Creat_config(filename)
    else:
        try:
            return json.load(open(f"config/{filename}", "r", encoding="UTF-8"), object_hook=collections.OrderedDict)
        except:
            logger.error("[Bot]Json文件已损坏，正在尝试重新创建")
            Creat_config(filename)


# 重载配置
def reloadConfig():
    global config, FAQ, module
    logger.debug("正在重载配置文件...")
    try:
        config = load_config(".config.json")
        FAQ = load_config("FAQ.json")
        module = load_config("modules.json")
        logger.info("配置文件重载成功")
    except:
        logger.error("配置文件重载失败")


config = load_config("config.json")
FAQ = load_config("FAQ.json")
module = load_config("modules.json")


