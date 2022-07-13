# 主要方法实现
from module.basicModule.servertools import *
from module.Class.WhitelistClass import Whitelist
from module.Class.BanlistClass import Banlist
from module.Class.ServerStatusClass import ServerStatus

whitelist = Whitelist(database, vanillaServer)
banlist = Banlist(database, vanillaServer)
server = ServerStatus(config["Server_List"], config["HideNum"])

async def findAnswer(qun: int, msg: str) -> str:

    """
    FAQ\n
    :param qun: 群号(int)
    :param msg: 查询消息(str)
    :return: str
    """

    for row in FAQ["FAQ"]:
        if ("global" == row["qun"] and qun != config["QQ_Config"]["Group_Config"]["admin_qun"]) or qun == row["qun"]:
            tempData = row["qun"]
            row.pop("qun")
            for key in row:
                if key in msg:
                    row["qun"] = qun
                    return row.get(key)
            row["qun"] = tempData

