# 工具模块
from module.basicModule.sqlrelated import *
from module.Class.ServerClass import *

vanillaServer = MinecraftServer(config["RCON_Config"]["Server1"]["RCON_port"],
                                config["RCON_Config"]["Server1"]["RCON_host"],
                                config["RCON_Config"]["Server1"]["RCON_password"], "VanillaServer",
                                config["Run_Command"]["whitelist_add"],
                                config["Run_Command"]["whitelist_del"])
# testServer =

async def autoDelWhitelist(QQ_ID: int, Group_ID: int, Cause: str):

    """
    取消玩家白名单\n
    :param QQ_ID: 玩家QQ(int)
    :param Group_ID: 群号(int)
    :param Cause: 原因(str)
    :return: {"admin_msg": str, "player_msg": str}
    """

    Inquire = cursor.execute(f"SELECT player_name from whitelist where QQ = '{QQ_ID}'")
    if Inquire and Group_ID == config["QQ_Config"]["Group_Config"]["player_qun"]:
        picklData = cursor.fetchall()
        player = picklData[0][0]
        await vanillaServer.whitelistDel(player)
        await vanillaServer.ServerRunCommand("kick" + " " + player)
        await database.DataBaseRunCommand(f"DELETE from whitelist as wait where QQ = '{QQ_ID}'")
        return {
            "player_msg": f"[Bot-自动化]\n{QQ_ID}{Cause}，已自动取消{player}的白名单！",
            "admin_msg": f"[Bot-自动化]已自动取消玩家：{player}白名单！"
        }
    else:
        logger.info("该QQ名下未绑定玩家")

