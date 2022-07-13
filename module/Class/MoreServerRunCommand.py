from module.Class.ServerClass import MinecraftServer

async def MoreServerRunCommand(ServerRCONList: dict, Command: str) -> dict:

    """
    多服执行\n
    :param ServerRCONList: 服务器RCON配置（dict）
    :param Command: 要执行的命令(str）
    :return: {ServerName: Result}
    """

    tempList = []
    respond = {}
    for raw in ServerRCONList:
        tempList.append(MinecraftServer(ServerRCONList[raw]["RCON_port"], ServerRCONList[raw]["RCON_host"], ServerRCONList[raw]["RCON_password"], raw))
    for Server in tempList:
        respond.update({Server.GetServerName(): await Server.ServerRunCommand(Command)})
        del Server
    return respond
