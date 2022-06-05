# by Pigeon Server Team
# Bot 主体
import re
from mirai.models import *
from module.mainmethod import *
from module.help import *

num = 0
# 读取配置
enable_banlist = config["enable_banlist"]
enable_botmanager = config["enable_botmanager"]
enable_testop = config["enable_testop"]
enable_whitelist = config["enable_whitelist"]
if enable_banlist:
    banlist = "启用"
else:
    banlist = "未启用"
if enable_botmanager:
    botmanager = "启用"
else:
    botmanager = "未启用"
if enable_testop:
    testop = "启用"
else:
    testop = "未启用"
if enable_whitelist:
    whitelist = "启用"
else:
    whitelist = "未启用"
# runtimer = 0

if __name__ == '__main__':

    @bot.on(BotOnlineEvent)
    async def start(event: BotOnlineEvent):
        await say_group(admin_group,"你的小可爱上线了~")

    # 群消息记录
    @bot.on(GroupMessage)
    async def group_msg(event: GroupMessage):
        msg = str(event.message_chain)
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        # 消息输出
        print("[消息]<-群{qun}:{QQ}:{msg}".format(msg=msg, QQ=QQ, qun=qun))

    # 退群后自动取消白名单
    @bot.on(MemberLeaveEventQuit)
    async def auto_del_whitelist(GroupEvent: MemberLeaveEventQuit):
        Info = GroupEvent.member
        Inquire = cursor.execute("SELECT player_name from whitelist where QQ = '{QQ}'".format(QQ=Info.id))
        if Inquire and Info.group.id == config["player_qun"]:
            data = cursor.fetchall()
            player = data[0][0]
            await whitelist_del(player)
            await server_run("kick "+player)
            await sql_run("DELETE from whitelist as wait where QQ = '{QQ}'".format(QQ=Info.id))
            await say_group(config["player_qun"],"[Bot-自动化]\n{QQ}已退出本群，已自动取消玩家：{player}白名单！".format(QQ = Info.id,player = player))
            await say_group(config["admin_qun"],"[Bot-自动化]已自动取消玩家：{player}白名单！".format(QQ=Info.id, player=player))

    # 模块开关
    @bot.on(GroupMessage)
    async def module_switch(event: GroupMessage):
        # 前置操作
        global whitelist, testop, botmanager, banlist, num
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        msg = str(event.message_chain)
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        # 模块
        if msg_split[0] == "!模块" and qun == config["admin_qun"]:
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            # TODO 模块切换帮助
            if len(msg_split) == 2 and msg_split[1] == "状态":
                await say_group_info(qun, "当前模块状态：\n"
                                          "白名单申请：{whitelist}\n"
                                          "黑名单：{banlist}\n"
                                          "假人管理：{bot}\n"
                                          "测试服OP：{op}".format(whitelist=whitelist, op=testop, bot=botmanager, banlist=banlist))
            elif len(msg_split) >= 2 and msg_split[1] == "设置":
                if len(msg_split) == 2:
                    await say_group(qun, "可选参数为：白名单/黑名单/假人/测试服")
                elif msg_split[2] == "白名单":
                    if msg_split[3] == "开启":
                        whitelist = "启用"
                        await say_group_warning(qun, "白名单模块已启用")
                    elif msg_split[3] == "关闭":
                        whitelist = "关闭"
                        await say_group_warning(qun, "白名单模块已关闭")
                    else:
                        await say_group_warning(qun, "参数错误！可选参数为：开启/关闭")
                elif msg_split[2] == "黑名单":
                    if msg_split[3] == "开启":
                        banlist = "启用"
                        await say_group_warning(qun, "黑名单模块已启用")
                    elif msg_split[3] == "关闭":
                        banlist = "关闭"
                        await say_group_warning(qun, "黑名单模块已关闭")
                    else:
                        await say_group_warning(qun, "参数错误！可选参数为：开启/关闭")
                elif msg_split[2] == "假人":
                    if msg_split[3] == "开启":
                        botmanager = "启用"
                        await say_group_warning(qun, "假人管理模块已启用")
                    elif msg_split[3] == "关闭":
                        botmanager = "关闭"
                        await say_group_warning(qun, "假人管理模块已关闭")
                    else:
                        await say_group_warning(qun, "参数错误！可选参数为：开启/关闭")
                elif msg_split[2] == "测试服":
                    if msg_split[3] == "开启":
                        testop = "启用"
                        await say_group_warning(qun, "测试服OP申请模块已启用")
                    elif msg_split[3] == "关闭":
                        testop = "关闭"
                        await say_group_warning(qun, "测试服OP申请模块已关闭")
                    else:
                        await say_group_warning(qun, "参数错误！可选参数为：开启/关闭")
                else:
                    await say_group_warning(qun, "参数错误！可选参数为：白名单/黑名单/假人/测试服")
            else:
                await say_group_warning(qun, "未知命令！可用的子命令为：状态/设置")

    # 管理组
    @bot.on(GroupMessage)
    async def admin_group(event: GroupMessage):
        global whitelist, testop, botmanager, banlist, num
        # 群消息
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        # 管理员群部分
        if qun == config["admin_qun"] and "!" in msg_split[0]:
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            if (msg_split[0] == "!查询" or msg_split[0] == "!白名单") and whitelist == "启用":
                if msg_split[0] == "!查询":
                    if len(msg_split) == 1:
                        tempstr = await get_wait_list()
                        if tempstr is not None:
                            await say_group(qun, tempstr)
                        else:
                            await say_group_warning(qun, "未查询待审核玩家")
                    elif len(msg_split) == 2:
                        # TODO 通过的长度可能太长，需要限制和切分输出
                        if msg_split[1] == "已通过":
                            tempstr = await get_pass()
                            if tempstr is not None:
                                await say_group(qun, tempstr)
                            else:
                                await say_group_warning(qun, "未查询到通过玩家")
                        elif msg_split[1] == "未通过":
                            tempstr = await get_notpass()
                            if tempstr is not None:
                                if tempstr is not None:
                                    await say_group(qun, tempstr)
                                else:
                                    await say_group_warning(qun, "未查询到未通过玩家")
                        elif msg_split[1] == "清空":
                            success = await sql_run("""DELETE from wait where pass is NULL""")
                            if success != -1:
                                await say_group_info(qun, "[Bot-查询]:白名单未审核序列已清空")
                            else:
                                await say_group_info(qun, "[Bot-查询]:数据库出现错误，请检查")
                elif msg_split[0] == "!白名单":
                    if len(msg_split) == 2 and msg_split[1] == "全部通过":
                        await pass_all()
                    elif len(msg_split) >= 3:
                        if msg_split[1] == "通过" and len(msg_split) == 3:
                            await pass_one(msg_split[2])
                        elif msg_split[1] == "拒绝":
                            if len(msg_split) == 3:
                                await refuse_one(msg_split[2])
                            elif len(msg_split) == 4:
                                await refuse_one(msg_split[2], msg_split[3])
                            else:
                                await say_group_warning(qun, "过多的参数！")
                        elif msg_split[1] == "移除":
                            if len(msg_split) == 3:
                                if msg_split[2] == "重置":
                                    num = 0
                                    await say_group_info(qun, "[Bot-白名单审核]ID重置成功")
                                elif type(msg_split[2]) == int:
                                    await del_whitelist(msg_split[2])
                            elif len(msg_split) == 4 and type(msg_split[2]) == int:
                                if msg_split[3] == "确认" and num == msg_split[2]:
                                    await confirm_del(msg_split[2])
                                elif msg_split[3] == "取消" and num == msg_split[2]:
                                    num = 0
                                    await say_group_info(qun, "[Bot-白名单审核]操作已取消")
                                else:
                                    await say_group(qun, "未知命令！可用子命令为：确认/取消")
            elif (msg_split[0] == "!查询" or msg_split[0] == "!白名单") and whitelist == "关闭":
                await say_group(qun, "白名单申请未启用")
            elif msg_split[0] == "!ban" and banlist == "启用":
                if len(msg_split) == 4 and msg_split[1] == "添加":
                    await banlist_add(msg_split[2], msg_split[3])
                elif len(msg_split) == 3 and msg_split[1] == "移除":
                    await banlist_del(msg_split[2])
            elif msg_split[0] == "!ban" and banlist == "关闭":
                await say_group(qun, "黑名单未启用")
            elif msg_split[0] == "!假人" and botmanager == "启用":
                if len(msg_split) == 3 and msg_split[1] == "删除":
                    await bot_del(msg_split[2], QQ, 1)
                elif len(msg_split) == 4 and msg_split[1] == "服务器" and msg_split[2] == "删除":
                    await del_bot(msg_split[3])
                elif len(msg_split) == 3 and msg_split[1] == "服务器" and msg_split[2] == "删除":
                    await del_bot_all()
            elif msg_split[0] == "!假人" and botmanager == "关闭":
                await say_group(qun, "假人管理未启用")
            elif msg_split[0] == "!OP" and testop == "启用":
                if len(msg_split) == 2 and msg_split[1] == "全部通过":
                    await pass_all_op()
                elif len(msg_split) >= 3:
                    if msg_split[1] == "通过" and len(msg_split) == 3:
                        await pass_one_op(msg_split[2])
                    elif msg_split[1] == "不通过":
                        if len(msg_split) == 3:
                            await refuse_one_op(msg_split[2])
                        elif len(msg_split) == 4:
                            await refuse_one_op(msg_split[2], msg_split[3])
                        else:
                            await say_group_warning(qun, "过多的参数！")
            elif msg_split[0] == "!OP" and testop == "关闭":
                await say_group(qun, "测试服OP申请未启用")
            else:
                await say_group_warning(qun, "未知命令")

    # 玩家
    @bot.on(GroupMessage)
    async def player_group(event: GroupMessage):
        global whitelist, testop, botmanager, banlist
        # 群消息
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        # 玩家群部分
        if qun == config["player_qun"] and "!" in msg_split[0]:
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            if (msg_split[0] == "!白名单" or msg_split[0] == "!解绑") and whitelist == "启用":
                if msg_split[0] == "!白名单":
                    if len(msg_split) == 2:
                        matchobj = re.match('^[a-zA-Z0-9_]+$', msg_split[1])
                        if matchobj is None:
                            await say_group_warning(qun, "参数:{player}含有非法字符！".format(player=msg_split[1]))
                        else:
                            await get_whitelist(msg_split[1], QQ)
                elif msg_split[0] == "!解绑":
                    await unbundling(msg_split[1], QQ)
            elif (msg_split[0] == "!白名单" or msg_split[0] == "!解绑") and whitelist == "关闭":
                await say_group(qun, "白名单申请未启用，请联系管理员")
            elif msg_split[0] == "!黑名单" and banlist == "启用":
                await get_banlist()
            elif msg_split[0] == "!黑名单" and banlist == "关闭":
                await say_group(qun, "黑名单未启用，请联系管理员")
            elif msg_split[0] == "!假人" and botmanager == "启用":
                if len(msg_split) >= 4 and msg_split[1] == "添加":
                    nameexisted = cursor.execute("SELECT * from usedbot where bot_name = '{bot}'".format(bot="bot_" + msg_split[2]))
                    if nameexisted == 0:
                        if len(msg_split) == 4:
                            await bot_add(msg_split[2], QQ, msg_split[3])
                        elif len(msg_split) == 5 and msg_split[4] == "启用":
                            await bot_add(msg_split[2], QQ, msg_split[3], 1)
                    else:
                        await say_group_warning(qun, "[Bot-假人管理]已有重名假人\n")
                elif len(msg_split) == 3 and msg_split[1] == "删除":
                    await bot_del(msg_split[2], QQ)
                elif len(msg_split) == 3 and msg_split[1] == "查询":
                    await get_bot(msg_split[2])
                elif len(msg_split) == 2 and msg_split[1] == "查询":
                    await get_bot_all()
                elif len(msg_split) == 2 and msg_split[1] == "服务器":
                    string = await bot_get()
                    if qun == config["player_qun"]:
                        await say_group(qun, "[Bot-假人管理]\n{bot}".format(bot=string))
                    else:
                        await say_group(config["admin_qun"], "[Bot-假人管理]\n {bot}".format(bot=string))
                elif len(msg_split) == 2 and msg_split[1] == "检查":
                    nopass = await check_bot()
                    if len(nopass) != 1:
                        await say_group(qun, "[Bot-假人管理]\n{check}".format(check=nopass))
                    else:
                        await say_group(qun, "[Bot-假人管理] 服务器内假人均已登记\n")
                elif len(msg_split) > 2 and msg_split[1] == "设置":
                    if len(msg_split) == 3:
                        await switch_bot(len(msg_split), QQ, msg_split[2])
                    elif len(msg_split) == 4:
                        await switch_bot(len(msg_split), QQ, msg_split[2], msg_split[3])
            elif msg_split[0] == "!假人" and botmanager == "关闭":
                await say_group(qun, "假人管理未启用，请联系管理员")
            elif msg_split[0] == "!OP" and testop == "启用":
                if len(msg_split) == 2:
                    matchobj = re.match('^[a-zA-Z0-9_]+$', msg_split[1])
                    if matchobj is None:
                        await say_group_warning(qun, "参数:{player}含有非法字符！".format(player=msg_split[1]))
                    else:
                        await get_op(QQ, msg_split[1])
                elif len(msg_split) == 3 and msg_split[1] == "解绑":
                    await unbundling_op(msg_split[2], QQ)
            elif msg_split[0] == "!OP" and testop == "关闭":
                await say_group(qun, "测试服OP申请未启用，请联系管理员")

    # 服务器状态查询
    @bot.on(GroupMessage)
    async def get_server_status(event: GroupMessage):
        msg = str(event.message_chain)
        qun = event.sender.group.id
        QQ = str(event.sender.id)
        if "!服务器" in msg or "!在线" in msg or "!人数" in msg or "!server" in msg:
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            await say_group(qun, await Server_Status())

    # 问答
    @bot.on(GroupMessage)
    async def help(event: GroupMessage):
        msg = str(event.message_chain)
        qun = event.sender.group.id
        if msg[:1] is not "!":
            answer = await FAQ(qun, msg)
            QQ = str(event.sender.id)
            if answer is not None:
                log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
                await say_group(qun, answer)
    # 启动机器人
    bot.run()
