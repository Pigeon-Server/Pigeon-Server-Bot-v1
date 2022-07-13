from module.basicModule.logger import *
from mcstatus import JavaServer
import socket

class ServerStatus:

    __server_list = {}
    __server_player_list = ""
    __max_online = 0
    __online = 0
    __hideNum = 0

    def __init__(self, Server_List: dict, hideNum: int):
        if Server_List != {}:
            self.__server_list = Server_List
        self.__hideNum = hideNum

    # 玩家列表
    def __getServerPlayerList(self):
        self.__server_player_list = ""
        for server_name, host in self.__server_list.items():
            self.__server_player_list += "{server}".format(server=server_name)
            self.__server_player_list += "({count})："
            try:
                server = JavaServer.lookup(host)  # 连接服务器
                status = server.status()  # 启动连接
                # Forge无玩家时会返回一个None，解决这个问题
                if status.players.sample is not None:
                    count = 0
                    for player in status.players.sample:
                        count += 1
                        if count == (self.__hideNum + 1):
                            self.__server_player_list += "..."
                            break
                        self.__server_player_list += "[{name}] ".format(name=str(player.name))
                    self.__server_player_list = self.__server_player_list.format(count=len(status.players.sample))
            # 连接错误
            except socket.timeout:
                logger.error("连接超时")
                self.__server_player_list += "服务器连接超时"
            except:
                logger.error("连接错误")
                self.__server_player_list += "服务器连接失败"
            self.__server_player_list += "\n"

    # 检查服务器状态
    async def GetServerStatus(self):
        self.__max_online = 0
        self.__online = 0
        for host in self.__server_list.values():
            try:
                server = JavaServer.lookup(host)  # 连接服务器
                status = server.status()  # 启动连接
                self.__online += status.players.online
                self.__max_online += status.players.max
            except:
                logger.error("连接错误", host)
        self.__getServerPlayerList()
        return f"[Bot-服务器状态]\n在线人数：{self.__online}/{self.__max_online}\n在线玩家列表：\n{self.__server_player_list}"
