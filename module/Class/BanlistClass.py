import module.Class.DataBaseClass

class Banlist:

    """
    黑名单模块\n
    父类：DataBase MinecraftServer
    """

    __DataBaseClass = None
    __ServerClass = None

    def __init__(self, Database: module.Class.DataBaseClass.DataBase, Server: module.Class.ServerClass.MinecraftServer) -> None:

        """
        构造函数\n
        :param Database: 数据库连接
        :param Server: MinecraftServer类
        """

        self.__DataBaseClass = Database
        self.__ServerClass = Server

    async def banlistAdd(self, playerName: str, reason: str) -> dict:

        """
        黑名单-添加/n
        :param playerName: 玩家名(str)
        :param reason: 封禁理由(str)
        :return: {"admin_msg": str, "player_msg": str} {"admin_msg": str} {"player_msg": str}
        """

        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        existBanlist = cursor.execute(f"SELECT * from banlist where player_name = '{playerName}'")
        if existBanlist == 0:
            await self.__ServerClass.banAdd(playerName, reason)
            await self.__DataBaseClass.DataBaseRunCommand(f"INSERT INTO banlist(player_name, reason) VALUES ('{playerName}', '{reason}')")
            executionStatus = await self.__DataBaseClass.DataBaseRunCommand()
            if executionStatus != -1:
                return {
                    "admin_msg": f"[黑名单-添加]成功添加玩家{playerName}\n原因:{reason}",
                    "player_msg": f"玩家:{playerName}\n原因:{reason}\n已被移入黑名单,请各位引以为戒"
                }
            else:
                return {
                    "admin_msg": "数据库执行错误"
                }
        else:
            return {
                "admin_msg": "该玩家已在黑名单内"
            }

    async def banlistDel(self, playerName: str) -> dict:

        """
        黑名单-删除/n
        :param playerName: 玩家名(str)
        :return: {"admin_msg": str, "player_msg": str} {"admin_msg": str} {"player_msg": str}
        """

        success = await self.__ServerClass.banDel(playerName)
        if success == 0:
            executionStatus = await self.__DataBaseClass.DataBaseRunCommand(f"DELETE from banlist where player_name = '{playerName}'")
            if executionStatus != -1:
                return {
                    "player_msg": f"{playerName}已被移出黑名单",
                    "admin_msg": f"[黑名单-移除]成功移除玩家{playerName}"
                }
            else:
                return {
                    "admin_msg": "数据库执行错误"
                }
        else:
            return {
                "admin_msg": "该玩家未被服务器封禁"
            }

    async def getBanlist(self) -> dict:

        """
        输出黑名单列表\n
        :return: {"player_msg": str}
        """

        self.__DataBaseClass.GetConnectionInfo().ping(reconnect=True)
        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        cursor.execute("SELECT * from banlist")
        output = cursor.fetchall()
        tempStr = ""
        if len(output) != 0:
            i = 1
            for row in output:
                player_name = row[0]
                reason = row[1]
                tempStr += f"[{i}]玩家ID：{player_name}\n原因:{reason}\n"
                # 打印结果
                i += 1
            return {
                "player_msg": tempStr
            }
        else:
            return {
                "player_msg": "[黑名单-查询]无玩家"
            }
