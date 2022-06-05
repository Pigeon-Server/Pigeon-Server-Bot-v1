# 配置文件
import collections
import json
from pathlib import Path
from module.logger import log


# 新建config
def New_config():
    # 默认配置
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
        "RCON_post": "1337",  # RCON端口
        "RCON_host_test": "127.0.0.1",  # RCON密码
        "RCON_password_test": "password",  # RCON地址
        "RCON_post_test": "1337",  # RCON端口
        # config(模块)
        "enable_whitelist": "true",
        "enable_banlist": "true",
        "enable_botmanager": "true",
        "enable_testop": "true",
        # config(服务器列表)
        "serverlist": ["127.0.0.1", "127.0.0.1:25566"],
        "servername": ["Server1", "Server2"],
        # config(开黑啦)
        "kaiheila-key": "",
        # 问答
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
    log.debug("[Bot]正在尝试创建配置文件")
    try:
        with open("config.json", "w") as write_file:
            json.dump(config, write_file, indent="\t", sort_keys=True, ensure_ascii=False)
    except:
        log.error("[Bot]配置文件创建失败")
    else:
        log.debug("[Bot]配置文件创建成功")


# 修改config
def updata_config(key, value):
    File = open("config.json", "r+", encoding='utf-8')  # 打开文件
    data = config  # 存储原始文件
    File.truncate()
    data[key] = value  # 添加/修改
    File.write(  # 写入
        json.dumps(data, indent="\t", sort_keys=True, ensure_ascii=False)
    )
    # load_config()


def load_config(Path_file="config.json"):
    if not Path(Path_file).is_file():
        New_config()
    else:
        while True:
            try:
                config = json.load(open("config.json", "r", encoding="UTF-8"),object_hook=collections.OrderedDict)
                return config
            except:
                log.error("[Bot]Json文件已损坏，正在尝试重新创建")
                New_config()


config = load_config()
