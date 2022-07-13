# 模块-配置文件
import asyncio
import base64
import collections
import os
import json5
from typing import Any
from pathlib import Path
from module.basicModule.logger import logger

# 判断config文件夹是否存在
config = os.path.join('config')
if not os.path.exists(config):
    os.makedirs(config)

class Config:
    Main_Config = {
        "Config_Version": 2.1,
        "Check-Minecraft-Version": {
            "release": "",
            "snapshot": ""
        },
        "QQ_Config": {
            "QQ": 10000,
            "HTTP-Host": "127.0.0.1",
            "HTTP-Port": 8080,
            "HTTP_Key": "",
            "Msg_MAX_Rows": 20,
            "Group_Config": {
                "admin_qun": 100000000,
                "player_qun": 100000000
            }
        },
        "RCON_Config": {
            "Server1": {
                "RCON_Host": "127.0.0.1",
                "RCON_Port": 1337,
                "RCON_Password": "password"
            },
            "Server2": {
                "RCON_Host": "127.0.0.1",
                "RCON_Port": 1537,
                "RCON_Password": "password"
            }
        },
        "Run_Command": {
            "whitelist_add": "whitelist add",
            "whitelist_del": "whitelist remove",
            "ban_add": "ban",
            "ban_del": "pardon"
        },
        "Module_Run_Server": {
            "blacklist": ["Server1", "Server2"],
            "whitelist": ["Server1"],
            "test_op": ["Server2"]
        },
        "DB_Config": {
            "DB_Host": "127.0.0.1",
            "DB_Password": "root",
            "DB_User": "root",
            "database": "Bot_DB"
        },
        "Server_List": {
            "原版服": "127.0.0.1:25565",
            "模组服": "127.0.0.1:25566"
        },
        "Welcome_Message": "welcome",
        "HideNum": 10
    }
    FAQ_Config = {
        "FAQ": [
            {
                "qun": 10000000,
                "问题": "回答"
            },
            {
                "qun": "global",
                "问题": "回答"
            }
        ]
    }
    Module_Config = {
        "enable_whitelist": "true",
        "enable_banlist": "true",
        "enable_botManager": "true",
        "enable_testOp": "true"
    }
    Image_Config = {
        "Server_Rule_Image": "Path"
    }

    def CreateConfig(self, filename: str) -> None:

        """
        创建配置文件\n
        :param filename: 创建的配置文件名(str)
        :return: None
        """

        tempConfig = {}
        if filename == "config.json5":
            tempConfig = self.Main_Config
        elif filename == "FAQ.json5":
            tempConfig = self.FAQ_Config
        elif filename == "modules.json5":
            tempConfig = self.Module_Config
        elif filename == "image.json5":
            tempConfig = self.Image_Config
        logger.debug("[Bot]正在尝试创建配置文件")
        try:
            with open(f"config/{filename}", "w", encoding="UTF-8") as write_file:
                json5.dump(tempConfig, write_file, indent="\t", sort_keys=False, ensure_ascii=False)
        except:
            logger.error("[Bot]配置文件创建失败")
        else:
            logger.debug("[Bot]配置文件创建成功")

    def updateConfig(self, key: str, value: str, configName: dict, filename: str) -> None:

        """
        修改config\n
        :param key: 要修改的键(str)
        :param value: 要修改成的值(str)
        :param configName: 配置名称(str)
        :param filename: 配置文件名称(str)
        :return: None
        """

        File = open(f"config/{filename}", "r+", encoding="UTF-8", errors="ignore")  # 打开文件
        data = configName  # 存储原始文件
        File.truncate()
        data[key] = value  # 添加/修改
        File.write(  # 写入
            json5.dumps(data, indent="\t", sort_keys=False, ensure_ascii=False)
        )
        File.close()
        self.reloadConfig()

    def loadConfig(self, filename: str) -> dict:

        """
        加载config\n
        :param filename: 要加载的配置文件名(str)
        :return: dict
        """

        if not Path("config/" + filename).is_file():
            self.CreateConfig(filename)
        else:
            try:
                return json5.load(open(f"config/{filename}", "r", encoding="UTF-8", errors="ignore"),
                                  object_hook=collections.OrderedDict)
            except:
                logger.error("[Bot]Json文件已损坏，正在尝试重新创建")
                self.CreateConfig(filename)

    def reloadConfig(self) -> None:

        """
        重载配置\n
        :return: None
        """

        global config, FAQ, module
        logger.debug("正在重载配置文件...")
        try:
            config = self.loadConfig("config.json5")
            FAQ = self.loadConfig("FAQ.json5")
            module = self.modules()

        except:
            logger.error("配置文件重载失败")

    def modules(self) -> dict[str, Any]:

        """
        读取模块配置\n
        :return: dict
        """
        boolToStr = {"true": "启用", "false": "禁用"}
        Module = self.loadConfig("modules.json5")
        return {"whitelist": boolToStr[Module["enable_whitelist"]],
                "banlist": boolToStr[Module["enable_banlist"]],
                "testOp": boolToStr[Module["enable_testOp"]],
                "botManager": boolToStr[Module["enable_botManager"]]}

    async def loadImage(self) -> dict:
        pathConfig = self.loadConfig("image.json5")
        tempDict = {}
        for raw in pathConfig:
            with open(pathConfig[raw], 'rb') as i:
                tempDict.update({raw: str(base64.b64encode(i.read()), 'utf-8')})
        return tempDict


configClass = Config()
logger.debug("正在加载配置")
config = configClass.loadConfig("config.json5")
FAQ = configClass.loadConfig("FAQ.json5")
module = configClass.modules()
logger.debug("配置文件加载完成")
logger.debug("正在加载图片文件")
image = asyncio.run(configClass.loadImage())
logger.debug("图片加载完成")

