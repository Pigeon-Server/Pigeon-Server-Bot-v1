# by Pigeon Server Team
# QQ机器人部分

# 校验
import re
# 任务模块
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
# 机器人用
from mirai_extensions.trigger import InterruptControl, Filter
from mirai.models import *
# 自写模块
from module.mainmethod import *
from module.Check_Minecraft_update import CheckVersion
from module.basicModule.botsendmsg import *


def QQ_bot():
    # 自动化部分

    Check_Update_Task = AsyncIOScheduler(timezone="Asia/Shanghai")

    # 启动时执行
    @bot.on(Startup)
    async def start(_):
        Check_Update_Task.start()
        # await bot.member_info(856572659, 1811741096).set((await bot.member_info(856572659, 1811741096).get()).modify(member_name='test'))
        # await say_group(config["QQ_Config"]["Group_Config"]["admin_qun"],"你的小可爱上线了~")

    # 关闭时执行
    @bot.on(Shutdown)
    async def shutdown(_):
        Check_Update_Task.shutdown(True)

    # 任务-检测Minecraft版本更新
    @Check_Update_Task.scheduled_job(CronTrigger(second=10))
    async def Check_Update():
        tempData = CheckVersion()
        if tempData:
            await send_compound_message(tempData)

    # 群消息记录
    @bot.on(GroupMessage)
    async def group_msg(event: GroupMessage):
        msg = str(event.message_chain)
        QQ = event.sender.id
        qun = event.sender.group.id
        # 消息输出
        logger.info(f"[消息]<-群{qun}:{QQ}:{msg}")

    # 退群后自动取消白名单
    @bot.on(MemberLeaveEventQuit)
    async def quit_del_whitelist(groupEvent: MemberLeaveEventQuit):
        QQ_ID = groupEvent.member.id
        Group_ID = groupEvent.member.group.id
        await send_compound_message(await autoDelWhitelist(QQ_ID, Group_ID, "退出本群"))

    # 踢出后自动取消白名单
    @bot.on(MemberLeaveEventKick)
    async def kick_del_whitelist(groupEvent: MemberLeaveEventKick):
        QQ_ID = groupEvent.member.id
        Group_ID = groupEvent.member.group.id
        await send_compound_message(await autoDelWhitelist(QQ_ID, Group_ID, "被踢出本群"))

    # 自动审核
    @bot.on(MemberJoinRequestEvent)
    async def Join_Group(event: MemberJoinRequestEvent):
        QQ_ID = event.from_id
        Group_ID = event.group_id
        User_Nick = event.nick
        User_Info = await bot.user_profile.get(QQ_ID)
        # 用户年龄须大于16并小于60 用户等级不小于20
        if (16 <= User_Info.age <= 60) and User_Info.level >= 20 and Group_ID != config["QQ_Config"]["Group_Config"]["admin_qun"]:
            await bot.allow(event)
            await say_group(config["QQ_Config"]["Group_Config"]["admin_qun"],
                            f"[Bot-自动化]\n申请者[{User_Nick}:{QQ_ID}]已满足入群条件，已自动同意")
        # 用户等级低于10自动拒绝请求并拉黑
        elif User_Info.level <= 10:
            await bot.decline(event, "[Bot-自动化]远未达到入群标准，已自动拒绝并拉入黑名单", ban=True)
            await say_group(config["QQ_Config"]["Group_Config"]["admin_qun"],
                            f"[Bot-自动化]\n申请者[{User_Nick}:{QQ_ID}]远低于入群条件，已自动拒绝并拉黑")
        # 未达成以上条件须人工审核
        else:
            await say_group(config["QQ_Config"]["Group_Config"]["admin_qun"],
                            f"[Bot-自动化]\n申请者[{User_Nick}:{QQ_ID}]未达到入群条件，请人工审核")

    # 入群欢迎
    @bot.on(MemberJoinEvent)
    async def welcome(event: MemberJoinEvent):
        group = event.member.group.id
        name = event.member.member_name
        groupName = event.member.group.name
        QQ = event.member.id
        await welcome_msg(group, " " + config["Welcome_Message"].format(groupName=groupName), QQ)
        if group == config["QQ_Config"]["Group_Config"]["player_qun"]:
            await say_group(group, await findAnswer(group, "白名单"))
            await say_group(group, await findAnswer(group, "ip"))

    # 管理员部分

    # 重载配置文件
    @bot.on(GroupMessage)
    async def reload_config(event: GroupMessage):
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        msg = str(event.message_chain)
        qun = event.sender.group.id
        if qun == config["QQ_Config"]["Group_Config"]["admin_qun"] and msg[:1] in "!":
            if msg_split[0] == "!reload":
                configClass.reloadConfig()

    # 查询审核列表
    @bot.on(GroupMessage)
    async def Inquire_whitelist(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        qun = event.sender.group.id
        if qun == config["QQ_Config"]["Group_Config"]["admin_qun"] and msg[:1] in "!":
            if msg_split[0] == "!查询":
                connected.ping(reconnect=True)
                if len(msg_split) == 1:
                    await send_compound_message(await whitelist.getWaitList())
                elif len(msg_split) == 2:
                    if msg_split[1] == "通过":
                        await send_compound_message(await whitelist.getPass())
                    elif msg_split[1] == "拒绝":
                        await send_compound_message(await whitelist.getNotPass())
                    elif msg_split[1] == "清空":
                        await send_compound_message(await whitelist.delWaitListAll())

    # 审核
    @bot.on(GroupMessage)
    async def whitelist_pass(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        qun = event.sender.group.id
        if qun == config["QQ_Config"]["Group_Config"]["admin_qun"] and msg[:1] in "!":
            if msg_split[0] == "!白名单":
                connected.ping(reconnect=True)
                if len(msg_split) == 2 and msg_split[1] == "全部通过":
                    await send_compound_message(await whitelist.passAll())
                elif len(msg_split) >= 3:
                    if msg_split[1] == "通过" and len(msg_split) == 3:
                        await send_compound_message(await whitelist.passOne(msg_split[2]))
                    elif msg_split[1] == "拒绝":
                        if len(msg_split) == 3:
                            # 默认值None
                            await send_compound_message(await whitelist.refuseOne(msg_split[2]))
                        elif len(msg_split) == 4:
                            await send_compound_message(await whitelist.refuseOne(msg_split[2], msg_split[3]))
                        else:
                            await say_group_warning(qun, "参数错误！")

    # 黑名单
    @bot.on(GroupMessage)
    async def banLite(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        qun = event.sender.group.id
        if qun == config["QQ_Config"]["Group_Config"]["admin_qun"] and msg[:1] in "!":
            if msg_split[0] == "!ban":
                connected.ping(reconnect=True)
                if len(msg_split) == 4 and msg_split[1] == "添加":
                    await send_compound_message(await banlist.banlistAdd(msg_split[2], msg_split[3]))
                elif len(msg_split) == 3 and msg_split[1] == "移除":
                    await send_compound_message(await banlist.banlistDel(msg_split[2]))

    # 玩家部分

    # 白名单-申请
    inc = InterruptControl(bot)

    @bot.on(GroupMessage)
    async def player_Whitelist(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        if qun == config["QQ_Config"]["Group_Config"]["player_qun"] and msg[:1] in "!":
            if msg_split[0] == "!白名单":
                if len(msg_split) == 2:
                    matchObj = re.match('^\\w+$', msg_split[1])
                    if matchObj is None:
                        await say_group_warning(qun, f"参数:{msg_split[1]}含有非法字符！")
                    else:
                        logger.debug(f"[消息]<-群{qun}:{QQ}:{msg}")
                        if msg_split[1] not in (await bot.member_info(qun, QQ).get()).get_name():
                            await at_say_group(qun, "请将群名片改为游戏ID", QQ)
                            await sendImage(qun, image["Server_Rule_Image"])
                        else:
                            await sendImage(qun, image["Server_Rule_Image"], QQ)

                        # 等待回复
                        @Filter(GroupMessage)
                        def applyForWhitelist(event_new: GroupMessage):
                            if event.sender.id == event_new.sender.id:
                                Msg = str(event_new.message_chain)
                                if Msg.startswith('同意'):
                                    return True
                                elif Msg.startswith('不同意'):
                                    return False
                        # 判断并运行
                        Data = await inc.wait(applyForWhitelist, timeout=180)
                        if Data is True:
                            await send_compound_message(await whitelist.getWhitelist(msg_split[1], QQ, ))
                        elif Data is False:
                            await say_group(qun, '未同意，操作已取消')
                        else:
                            await at_say_group(qun, '操作超时', QQ)

    # 白名单-解绑
    @bot.on(GroupMessage)
    async def player_unbind_Whitelist(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        if qun == config["QQ_Config"]["Group_Config"]["player_qun"] and msg[:1] in "!":
            if msg_split[0] == "!解绑":
                await say_group(qun, '警告：该操作将会取消之前绑定的用户白名单\n\n是否继续（是/否）')

                # 等待回复
                @Filter(GroupMessage)
                def unbindWaiter(event_new: GroupMessage):
                    if event.sender.id == event_new.sender.id:
                        Msg = str(event_new.message_chain)
                        if Msg.startswith('是'):
                            return True
                        elif Msg.startswith('否'):
                            return False
                # 判断并运行
                Data = await inc.wait(unbindWaiter, timeout=25)
                if Data is True:
                    await send_compound_message(await whitelist.unBundling(msg_split[1], QQ))
                elif Data is False:
                    await say_group(qun, '未同意，操作已取消')
                else:
                    await at_say_group(qun, '操作超时', QQ)

    # 白名单-改名
    @bot.on(GroupMessage)
    async def player_rename(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = event.sender.id
        qun = event.sender.group.id
        if qun == config["QQ_Config"]["Group_Config"]["player_qun"] and msg[:1] in "!":
            if msg_split[0] == "!改名":
                matchObj = re.match('^\\w+$', msg_split[1])
                if matchObj is None:
                    await say_group_warning(qun, f"参数:{msg_split[1]}含有非法字符！")
                else:
                    await say_group(qun, '警告：该操作将会取消此前绑定用户的白名单并换绑新用户\n\n是否继续（是/否）')

                    # 等待回复
                    @Filter(GroupMessage)
                    def renameWaiter(event_new: GroupMessage):
                        if event.sender.id == event_new.sender.id:
                            Msg = str(event_new.message_chain)
                            if Msg.startswith('是'):
                                return True
                            elif Msg.startswith('否'):
                                return False
                    # 判断并运行
                    Data = await inc.wait(renameWaiter, timeout=25)
                    if Data is True:
                        await send_compound_message(await whitelist.rename(QQ, msg_split[1]))
                    elif Data is False:
                        await say_group(qun, '未同意，操作已取消')
                    else:
                        await at_say_group(qun, '操作超时', QQ)

    # 黑名单-查询
    @bot.on(GroupMessage)
    async def player_blacklist(event: GroupMessage):
        qun = event.sender.group.id
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        if qun == config["QQ_Config"]["Group_Config"]["player_qun"] and msg[:1] in "!":
            if msg_split[0] == "!黑名单":
                await send_compound_message(await banlist.getBanlist())

    # 服务器状态查询
    @bot.on(GroupMessage)
    async def get_server_status(event: GroupMessage):
        msg = str(event.message_chain)
        qun = event.sender.group.id
        if "!服务器" in msg or "!在线" in msg or "!人数" in msg or "!server" in msg:
            await say_group(qun, await server.GetServerStatus())

    # 全局部分

    # 问答
    @bot.on(GroupMessage)
    async def sendHelp(event: GroupMessage):
        msg = str(event.message_chain)
        # 屏蔽!开头的
        if msg[:1] != "!":
            qun = event.sender.group.id
            answer = await findAnswer(qun, msg)
            if answer is not None:
                await reply_group(qun, answer, event.message_chain.message_id)
    # 启动机器人
    bot.run()
