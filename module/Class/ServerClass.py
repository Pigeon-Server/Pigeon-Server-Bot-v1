from module.basicModule.logger import *
from rcon.source import rcon

class MinecraftServer:

    """
    服务器类
    """

    __RconPort = 0
    __RconHost = ""
    __RconPasswd = ""
    __ServerName = ""
    WhitelistAddCommandPrefix = ""
    WhitelistDelCommandPrefix = ""
    BanAddCommandPrefix = ""
    BanDelCommandPrefix = ""
    OpCommandPrefix = ""
    DelOpCommandPrefix = ""
    BotCommandPrefix = ""

    def __init__(self, Port: int, Host: str, Passwd: str, Name: str, whitelistAdd: str = "whitelist add",
                 whitelistDel: str = "whitelist remove", banAdd: str = "ban", banDel: str = "pardon",
                 op: str = "op", deop: str = "deop", bot: str = "player") -> None:

        """
        构造函数\n
        :param Port: Rcon端口(int)
        :param Host: Rcon主机(str)
        :param Passwd: Rcon密码(str)
        :param Name: 服务器名称(str)
        :param whitelistAdd: 添加白名单命令前缀(str)
        :param whitelistDel: 移除白名单命令前缀(str)
        :param banAdd: 封禁命令前缀(str)
        :param banDel: 解封命令前缀(str)
        :param op: 授予管理员命令前缀(str)
        :param deop: 移除管理员命令前缀(str)
        :param bot: 假人管理命令前缀(str)
        :return: None
        """

        self.__RconPort = Port
        self.__ServerName = Name
        self.__RconPasswd = Passwd
        self.__RconHost = Host
        self.WhitelistAddCommandPrefix = whitelistAdd
        self.WhitelistDelCommandPrefix = whitelistDel
        self.BanAddCommandPrefix = banAdd
        self.BanDelCommandPrefix = banDel
        self.OpCommandPrefix = op
        self.DelOpCommandPrefix = deop
        self.BotCommandPrefix = bot

    def ChangeInfo(self, Port: int, Host: str, Passwd: str, Name: str) -> None:

        """
        修改服务器信息\n
        :param Port: Rcon端口(int)
        :param Host: Rcon主机(str)
        :param Passwd: Rcon密码(str)
        :param Name: 服务器名称(str)
        :return: None
        """

        self.__RconPort = Port
        self.__ServerName = Name
        self.__RconPasswd = Passwd
        self.__RconHost = Host

    def GetServerInfo(self) -> dict:

        """
        获取服务器信息\n
        :return: {"ServerName": str,"RconPort": int,"RconHost": str,"RconPasswd": str,"whitelist":{"Add":str,"Del":str}
                  "Ban":{"Add":str,"Del":str},"Op":{"Add":str,"Del":str},"Bot":str}
        """

        return {
            "ServerName": self.__ServerName,
            "RconPort": self.__RconPort,
            "RconHost": self.__RconHost,
            "RconPasswd": self.__RconPasswd,
            "whitelist": {
                "Add": self.WhitelistAddCommandPrefix,
                "Del": self.WhitelistDelCommandPrefix
            },
            "Ban": {
                "Add": self.BanAddCommandPrefix,
                "Del": self.BanDelCommandPrefix
            },
            "Op": {
                "Add": self.OpCommandPrefix,
                "Del": self.DelOpCommandPrefix
            },
            "Bot": self.BotCommandPrefix
        }

    def GetServerName(self) -> str:

        """
        获取服务器名称\n
        :return: str
        """

        return self.__ServerName

    async def ServerRunCommand(self, Command: str) -> str:
        """
            服务器执行指定命令\n
            :param Command: 要运行的命令（str）
            :return: str
            """

        try:
            logger.debug(f"[RCON]:[{self.__ServerName}]执行命令：{Command}")
            output = await rcon(
                Command,
                host=self.__RconHost,
                port=self.__RconPort,
                passwd=self.__RconPasswd
            )
            return output
        except:
            logger.error("[RCON]发生错误,请检查配置是否出错")

    async def whitelistAdd(self, player: str) -> bool:

        """
        为指定玩家添加白名单\n
        :param player: 玩家名（str）
        :return: True(成功授予) False(已有白名单)
        """

        output = await self.ServerRunCommand(self.WhitelistAddCommandPrefix + " " + player)
        if "Player is already whitelisted" in output:
            return False
        elif "Added" in output:
            logger.info(f"[白名单-add]:已成功给予{player}白名单")
            return True

    async def whitelistDel(self, player: str) -> bool:

        """
        移除白名单\n
        :param player: 玩家名（str）
        :return: True(成功移除) False(未有白名单)
        """

        output = await self.ServerRunCommand(self.WhitelistDelCommandPrefix + " " + player)
        if "Player is not whitelisted" in output:
            logger.info("[白名单-del]:该玩家未拥有白名单")
            return False
        elif "Removed" in output:
            logger.info(f"[白名单-del]:已成功移除{player}白名单")
            return True

    async def banAdd(self, player: str, reason: str = None) -> bool:

        """
        ban 添加\n
        :param player: 玩家名（str）
        :param reason: 封禁理由(str)
        :return: True(成功封禁) False(玩家已经封禁)
        """

        await self.whitelistDel(player)
        output = await self.ServerRunCommand(self.BanDelCommandPrefix + " " + player + " " + reason)
        if "Nothing changed. The player is already banned" in output:
            logger.info("[黑名单-add]:该玩家已在黑名单列表")
            return False
        elif "Banned by" in output:
            logger.info(f"[黑名单-add]:已成功将{player}移入黑名单")
            return True

    async def banDel(self, player: str) -> bool:

        """
        ban 删除\n
        :param player: 玩家名（str）
        :return: True(成功解禁) False(玩家未被封禁)
        """

        output = await self.ServerRunCommand(self.BanDelCommandPrefix + " " + player)
        if "Nothing changed. The player isn't banned" in output:
            logger.info("[白名单-del]:该玩家未在黑名单内")
            return False
        elif "Unbanned" in output:
            logger.info(f"[黑名单-del]:已成功移出{player}黑名单")
            return True

    def __del__(self):
        del self.__RconPort, self.__RconHost, self.__RconPasswd, self.__ServerName, self.WhitelistAddCommandPrefix, \
            self.WhitelistDelCommandPrefix, self.BanAddCommandPrefix, self.BanDelCommandPrefix, self.OpCommandPrefix, \
            self.DelOpCommandPrefix, self.BotCommandPrefix
