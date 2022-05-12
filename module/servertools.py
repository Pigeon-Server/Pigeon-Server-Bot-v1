# 模块
from rcon.source import *
from modes.config import *
# 发送群消息

# 服务器执行
async def server_run(command):
    try:
        print("[RCON]执行命令：{comm}".format(comm=command))
        return await rcon(
            command,
            host=config["RCON_host"], port=config["RCON_post"], passwd=config["RCON_password"]
        )
    except:
        print("[RCON]发生错误,请检查配置是否出错")


# 添加白名单
async def whtielist_add(player):
    output = await server_run("whitelist add {player}".format(player=player))
    if "Player is already whitelisted" in output:
        print("[白名单-add]:该玩家已拥有白名单")
    elif "Added" in output:
        print("[白名单-add]:已成功给予{player}白名单".format(player=player))


# 移除白名单
async def whtielist_del(player):
    output = await server_run("whitelist remove {player}".format(player=player))
    if "Player is not whitelisted" in output:
        print("[白名单-del]:该玩家未拥有白名单")
    elif "Removed" in output:
        print("[白名单-del]:已成功移除{player}白名单".format(player=player))


# ban 添加
async def ban_add(player, reason=None):
    await whtielist_del(player)
    output = await server_run("ban {player} {reason}".format(player=player, reason=reason))
    if "Nothing changed. The player is already banned" in output:
        print("[黑名单-add]:该玩家已在黑名单列表")
    elif "Banned by" in output:
        print("[黑名单-add]:已成功将{player}移入黑名单".format(player=player))


# 删除
async def ban_del(player):
    await whtielist_add(player)
    output = await server_run("pardon {player}".format(player=player))
    if "Nothing changed. The player isn't banned" in output:
        print("[白名单-del]:该玩家未在黑名单内")
    elif "Unbanned" in output:
        print("[黑名单-del]:已成功移出{player}黑名单".format(player=player))
