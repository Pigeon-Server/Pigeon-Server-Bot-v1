import module.Class.DataBaseClass
from module.Class.DataBaseClass import *

class Whitelist:

    """
    白名单类\n
    父类：Database MinecraftServer\n
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

    async def getPass(self) -> dict:

        """
        获取已通过玩家\n
        :return: {"admin_msg": str}
        """

        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        success = cursor.execute("SELECT id,QQ,player_name from wait where pass is True")
        output = cursor.fetchall()
        tempStr = ""
        if success >= 1:
            for row in output:
                id = row[0]
                QQ = row[1]
                player_name = row[2]
                tempStr += f"[{int(id)}]玩家ID：{player_name}\nQQ：{QQ}\n"
        del output
        return {
            "admin_msg": tempStr
        }

    async def getNotPass(self) -> dict:

        """
        获取未通过玩家\n
        :return: {"admin_msg": str}
        """

        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        success = cursor.execute("SELECT id,QQ,player_name,pass_info from wait where pass is False")
        output = cursor.fetchall()
        tempStr = ""
        if success >= 1:
            for row in output:
                id = row[0]
                QQ = row[1]
                player_name = row[2]
                pass_info = row[3]
                # 打印结果
                tempStr += f"[{int(id)}]玩家ID：{player_name}\nQQ：{QQ}\n退回原因：{pass_info}\n"
        del output
        return {
            "admin_msg": tempStr
        }

    async def getWaitList(self) -> dict:

        """
        获取待审核玩家\n
        :return: {"admin_msg": str}
        """

        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        success = cursor.execute("SELECT id,QQ,player_name from wait where pass is NULL")
        output = cursor.fetchall()
        tempStr = ""
        if success >= 1:
            for row in output:
                id = row[0]
                QQ = row[1]
                player_name = row[2]
                # 打印结果
                tempStr = tempStr + f"[{int(id)}]玩家ID：{player_name}\nQQ：{QQ}\n"
        del output
        return {
            "admin_msg": tempStr
        }

    async def passAll(self) -> dict:

        """
        通过所有待审核玩家\n
        :returns: {"admin_msg": str}（fail）  {"admin_msg": str, "player_msg": str} (success)
        """

        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        success = cursor.execute("SELECT id from wait where pass is not True and pass is not False")
        outputList = cursor.fetchall()
        if success != 0:
            for row in outputList:
                id = row[0]
                judgeExist = cursor.execute(f"SELECT id,QQ,player_name from wait where pass is NULL and `id` = '{id}'")
                output = cursor.fetchall()
                if judgeExist != 0:
                    QQ = output[0][1]
                    Player_Name = output[0][2]
                    # 执行
                    cursor.execute(f"UPDATE wait SET pass = true WHERE (`id` = '{id}')")
                    cursor.execute(f"INSERT INTO whitelist(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')")
                    executionStatus = await self.__DataBaseClass.DataBaseRunCommand()
                    if executionStatus != -1:
                        addStatus = await self.__ServerClass.whitelistAdd(Player_Name)
                        if addStatus is True:
                            return {
                                "QQ": f"{QQ}",
                                "admin_msg": f"ID：{id}添加白名单成功",
                                "player_msg": "白名单审核通过"
                            }
                        elif addStatus is False:
                            return {
                                "admin_msg": f"该玩家在{self.__ServerClass.GetServerName()}已拥有白名单"
                            }
                        else:
                            return {
                                "admin_msg": "发生未知错误，请检查"
                            }
                    else:
                        return {
                            "admin_msg": "数据库执行错误，请检查"
                        }
                else:
                    return {
                        "admin_msg": f"ID：{id}不存在，请重新查询"
                    }
        else:
            return {
                "admin_msg": "没有待审核的白名单申请"
            }
        del outputList

    async def delWaitListAll(self) -> dict:

        """
        清空所有未审核玩家\n
        :return: {"admin_msg": str}
        """

        executionStatus = await self.__DataBaseClass.DataBaseRunCommand("""DELETE from wait where pass is NULL""")
        if executionStatus != -1:
            return {
                "admin_msg": "[Bot-查询]:白名单未审核序列已清空"
            }
        else:
            return {
                "admin_msg": "[Bot-查询]:数据库出现错误，请检查"
            }

    async def passOne(self, id: str) -> dict:

        """
        通过指定ID的玩家\n
        :param id: 审核序号(str)
        :return: {"admin_msg": str}（fail）  {"admin_msg": str, "player_msg": str} (success)
        """

        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        targetExist = cursor.execute(
            f"SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'")
        output = cursor.fetchall()
        if targetExist == 1:
            QQ = output[0][1]
            Player_Name = output[0][2]
            cursor.execute(f"UPDATE wait SET pass = true WHERE (`id` = '{id}')")
            cursor.execute(f"INSERT INTO whitelist(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')")
            executionStatus = await self.__DataBaseClass.DataBaseRunCommand()
            if executionStatus != -1:
                addStatus = await self.__ServerClass.whitelistAdd(Player_Name)
                if addStatus is True:
                    return {
                        "QQ": f"{QQ}",
                        "admin_msg": f"ID：{id}添加白名单成功",
                        "player_msg": "白名单审核通过"
                    }
                elif addStatus is False:
                    return {
                        "admin_msg": f"该玩家在{self.__ServerClass.GetServerName()}上已拥有白名单"
                    }
                else:
                    return {
                        "admin_msg": "发生未知错误，请检查"
                    }
            else:
                return {
                    "admin_msg": "数据库执行错误，请检查"
                }
        else:
            return {
                "admin_msg": f"ID：{id}不存在，请重新查询"
            }

    async def refuseOne(self, id: str, reason: str = None) -> dict:

        """
        拒绝白名单\n
        :param id: 审核序号(str)
        :param reason: 拒绝原因(str),默认值None
        :return: {"admin_msg": str}（fail）  {"admin_msg": str, "player_msg": str} (success)
        """

        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        targetExist = cursor.execute(
            f"SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'")
        output = cursor.fetchall()
        if targetExist == 1:
            QQ = output[0][1]
            Player_Name = output[0][2]
            cursor.execute(f"UPDATE wait SET pass = false WHERE (`id` = '{id}')")
            cursor.execute(f"UPDATE wait SET pass_info = '{reason}' WHERE (`id` = '{id}')")
            executionStatus = await self.__DataBaseClass.DataBaseRunCommand()
            if executionStatus != -1:
                return {
                    "QQ": f"{QQ}",
                    "admin_msg": f"玩家：{Player_Name}白名单未通过\n退回原因：{reason}",
                    "player": f"白名单审核未通过\n原因：{reason}"
                }
            else:
                return {
                    "admin_msg": "数据库执行错误，请检查"
                }
        else:
            return {
                "admin_msg": f"ID：{id}不存在，请重新查询"
            }

    async def getWhitelist(self, playerName: str, qq: str) -> dict:

        """
        申请白名单\n
        :param playerName: 玩家名(str)
        :param qq: 玩家QQ(str)
        :return: {"admin_msg": str, "player_msg": str} {"admin_msg": str} {"player_msg": str}
        """

        self.__DataBaseClass.GetConnectionInfo().ping(reconnect=True)
        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()

        if len(playerName) > 16:
            playerName = playerName[:16]
            return {
                "player_msg": f"申请玩家名过长\n已自动截取为：{playerName}"
            }
        existWait = cursor.execute(f"SELECT * from wait where QQ = '{qq}'")
        existWhitelist = cursor.execute(f"SELECT * from whitelist where QQ = '{qq}'")
        existRefused = cursor.execute(f"SELECT * from wait where QQ = '{qq}' and pass = 0")
        existPassed = cursor.execute(f"SELECT * from wait where QQ = '{qq}' and pass = 1")
        logger.debug(f"是否已在wait表内：{existWait};是否已在whitelist表内：{existWhitelist};"
                     f"是否已被拒绝：{existRefused};是否已获得白名单：{existPassed}")
        if existWait != 1 and existWhitelist != 1:
            logger.info(f"[审核]已收到玩家{playerName}的白名单请求")
            cursor.execute(f"INSERT INTO wait(`QQ`, `player_name`) VALUES ('{qq}', '{playerName}')")
            executionStatus = await self.__DataBaseClass.DataBaseRunCommand()
            if executionStatus == -1:
                return {
                    "admin_msg": "数据库执行错误，请检查"
                }
            else:
                success = cursor.execute(f"SELECT id,player_name from wait where QQ = '{qq}'")
                tempData = cursor.fetchall()
                if success == 1:
                    id = tempData[0][0]
                    playerName = tempData[0][1]
                    return {
                        "QQ": f"{qq}",
                        "player_msg": '\n您的白名单申请已提交给服务器管理组~',
                        "admin_msg": f"[Bot-审核]收到一条新的白名单申请\n审核序号：{int(id)}\n玩家名：{playerName}\n使用!白名单 通过/不通过 [审核序号]"
                    }
                else:
                    return {
                        "QQ": f"{qq}",
                        "player_msg": '\n发生错误，请联系管理员'
                    }
        elif existRefused == 1:
            success = cursor.execute(f"SELECT pass_info from wait where QQ = '{qq}'")
            tempData = cursor.fetchall()
            if success == 1:
                reason = tempData[0][0]
                return {
                    "QQ": f"{qq}",
                    "player_msg": f'\n您的白名单申请权限已锁定\n原因：申请被管理组拒绝\n拒绝原因：{reason}'
                }
            else:
                return {
                    "QQ": f"{qq}",
                    "player_msg": '\n发生错误，请联系管理员'
                }
        elif existWhitelist == 1 and existPassed == 1:
            return {
                "QQ": f"{qq}",
                "player_msg": '\n您已经获取过白名单'
            }
        elif existWait == 1 and existWhitelist != 1:
            return {
                "QQ": f"{qq}",
                "player_msg": '\n您的白名单申请正在处理中,请耐心等待'
            }

    async def unBundling(self, playerName: str, qq: str) -> dict:

        """
        取消绑定\n
        :param playerName: 玩家名(str)
        :param qq: 玩家QQ(str)
        :return: {"admin_msg": str, "player_msg": str} {"admin_msg": str} {"player_msg": str}
        """

        self.__DataBaseClass.GetConnectionInfo().ping(reconnect=True)
        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        existWait = cursor.execute(f"SELECT * from wait where QQ = '{qq}' and player_name = '{playerName}'")
        existWhitelist = cursor.execute(
            f"SELECT * from whitelist where QQ = '{qq}' and player_name = '{playerName}'")
        existBanlist = cursor.execute(f"SELECT * from banlist where player_name = '{playerName}'")
        existRefused = cursor.execute(
            f"SELECT * from wait where QQ = '{qq}' and player_name = '{playerName}' and pass = 0")
        logger.debug(f"是否已在wait表内：{existWait};是否已在whitelist表内：{existWhitelist};"
                     f"是否已被拒绝：{existRefused};是否在黑名单：{existBanlist}")
        if existBanlist == 1:
            return {
                "QQ": f"{qq}",
                "player_msg": "\n你已被列入黑名单，无法解绑"
            }
        elif existRefused == 1:
            return {
                "QQ": f"{qq}",
                "player_msg": "\n你的白名单申请已被拒绝，无法解绑"
            }
        elif existWait == 1 or existWhitelist == 1:
            if existWait == 1:
                executionStatus = await self.__DataBaseClass.DataBaseRunCommand(
                    f"DELETE from wait where QQ = '{qq}' and player_name = '{playerName}'")
                if executionStatus == -1:
                    return {
                        "admin_msg": "数据库执行错误"
                    }
            if existWhitelist == 1:
                executionStatus = await self.__DataBaseClass.DataBaseRunCommand(
                    f"DELETE from whitelist where QQ = '{qq}' and player_name = '{playerName}'")
                if executionStatus == -1:
                    return {
                        "admin_msg": "数据库执行错误"
                    }
            addStatus = await self.__ServerClass.whitelistDel(playerName)
            if addStatus is True:
                return {
                    "QQ": f"{qq}",
                    "player_msg": '\n解绑成功~',
                    "admin_msg": f"[Bot-白名单]玩家{playerName}已解绑"
                }
            elif addStatus is False:
                return {
                    "QQ": f"{qq}",
                    "player_msg": '\n解绑失败，请联系管理员',
                    "admin_msg": f"该玩家在{self.__ServerClass.GetServerName()}上未拥有白名单"
                }
            else:
                return {
                    "QQ": f"{qq}",
                    "player_msg": '\n解绑失败，请联系管理员',
                    "admin_msg": "发生未知错误，请检查"
                }
        else:
            return {
                "QQ": f"{qq}",
                "player_msg": '\n该QQ名下未绑定该玩家，请检查ID是否正确'
            }

    async def rename(self, QQ: int, reName: str) -> dict:

        """
        改名\n
        :param QQ: 玩家QQ(int)
        :param reName: 要修改的名称(str)
        :return: {"admin_msg": str, "player_msg": str} {"admin_msg": str} {"player_msg": str}
        """

        # 数据库连接
        self.__DataBaseClass.GetConnectionInfo().ping(reconnect=True)
        cursor = self.__DataBaseClass.GetConnectionInfo().cursor()
        # 查询玩家原先名字
        InquireOriginalName = cursor.execute(f"SELECT * from whitelist where QQ = '{QQ}'")
        InquireOriginalNameArray = cursor.fetchone()

        # 查询是否已有这个名字的玩家
        InquireCollision = cursor.execute(f"SELECT * from whitelist where player_name = '{reName}'")

        # 查询要修改的玩家是否在黑名单内
        InquireBlacklist = cursor.execute(f"SELECT * from banlist where player_name = '{reName}'")

        # 功能实现

        # 是否在黑名单中
        if InquireBlacklist == 0:
            if InquireOriginalName == 1 and InquireCollision == 0:
                # 移除该玩家白名单
                await self.__ServerClass.whitelistDel(InquireOriginalNameArray[2])
                # 踢出该玩家
                await self.__ServerClass.ServerRunCommand("kick" + " " + InquireOriginalNameArray[2])
                # 更新数据库内数据
                await self.__DataBaseClass.DataBaseRunCommand(
                    f"update whitelist set player_name = '{reName}' where QQ = '{QQ}' and player_name = '{InquireOriginalNameArray[2]}'")
                await self.__DataBaseClass.DataBaseRunCommand(
                    f"update wait set player_name = '{reName}' where QQ = '{QQ}' and player_name = '{InquireOriginalNameArray[2]}'")
                # 添加白名单给新ID
                await self.__ServerClass.whitelistAdd(reName)
                return {
                    "QQ": f"{QQ}",
                    "player_msg": "\n成功~",
                    "admin_msg": f"[Bot-改名]\n玩家{InquireOriginalNameArray[2]}已改名，新名字{reName}"
                }
            # 查不到账户绑定玩家时
            elif InquireOriginalName == 0:
                return {
                    "QQ": f"{QQ}",
                    "player_msg": "\n你名下未绑定玩家！"
                }
            # 比对相同时
            elif InquireOriginalNameArray[2] == reName:
                return {
                    "QQ": f"{QQ}",
                    "player_msg": "\n要修改的名字与原名字相同"
                }
            # 数据库查询到该名字时
            elif InquireCollision != 0:
                return {
                    "QQ": f"{QQ}",
                    "player_msg": "\n该名字已有人使用过啦~"
                }
        elif InquireBlacklist != 0:
            return {
                "QQ": f"{QQ}",
                "player_msg": "\n禁止改名为黑名单用户"
            }
        else:
            return{
                "admin_msg": "发生未知错误，请查看日志"
            }
