# 配置文件
import json
from pathlib import Path


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
    }
    print("[Bot]正在尝试创建配置文件")
    try:
        with open("config.json", "w") as write_file:
            json.dump(config, write_file, indent="\t", sort_keys=True)
    except:
        print("[Bot]配置文件创建失败")
    else:
        print("[Bot]配置文件创建成功")


config = Path("config.json")
if not config.is_file():
    New_config()
else:
    while True:
        try:
            config = json.load(open("config.json", "r"))
        except:
            print("[Bot]Json文件已损坏，正在尝试重新创建")
            New_config()
        else:
            break
    print(config["QQ"])
