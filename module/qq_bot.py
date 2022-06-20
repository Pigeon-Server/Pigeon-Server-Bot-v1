# by Pigeon Server Team
# QQ机器人部分

# 校验
import re
# 任务模块
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
# 机器人用UserProfile
from mirai_extensions.trigger import InterruptControl
from mirai.models import *
from mirai_extensions.trigger import Filter
# 自写模块
from module.mainmethod import *
from module.Check_Minecraft_update import Check_Verson
# from module.kaiheila_bot import kaiheila_bot


def QQ_bot():
    # 自动化部分

    Check_Update_Task = AsyncIOScheduler(timezone="Asia/Shanghai")

    # 启动时执行
    @bot.on(Startup)
    async def start(_):
        Check_Update_Task.start()
        # await say_group(config["admin_qun"],"你的小可爱上线了~")
        # kaiheila_bot()

    # 关闭时执行
    @bot.on(Shutdown)
    async def shutdown(_):
        Check_Update_Task.shutdown(True)

    # 任务-检测Minecraft版本更新
    @Check_Update_Task.scheduled_job(CronTrigger(second=10))
    async def Check_Update():
        tempdata = Check_Verson()
        if tempdata:
            await send_compound_message(tempdata)

    # 群消息记录
    @bot.on(GroupMessage)
    async def group_msg(event: GroupMessage):
        msg = str(event.message_chain)
        QQ = event.sender.id
        qun = event.sender.group.id
        # 消息输出
        logger.info("[消息]<-群{qun}:{QQ}:{msg}".format(msg=msg, QQ=QQ, qun=qun))

    # 退群后自动取消白名单
    @bot.on(MemberLeaveEventQuit)
    async def quit_del_whitelist(GroupEvent: MemberLeaveEventQuit):
        QQ_ID = GroupEvent.member.id
        Group_ID = GroupEvent.member.group.id
        await auto_del_whitelist(QQ_ID, Group_ID, "退出本群")

    # 踢出后自动取消白名单
    @bot.on(MemberLeaveEventQuit)
    async def kick_del_whitelist(GroupEvent: MemberLeaveEventKick):
        QQ_ID = GroupEvent.member.id
        Group_ID = GroupEvent.member.group.id
        await auto_del_whitelist(QQ_ID, Group_ID, "被踢出本群")

    # 自动审核
    @bot.on(MemberJoinRequestEvent)
    async def Join_Group(event: MemberJoinRequestEvent):
        QQ_ID = event.from_id
        Group_ID = GroupEvent.member.group.id
        User_Nick = event.nick
        User_Info = await bot.user_profile.get(QQ_ID)
        # 用户年龄须大于16并小于60 用户等级不小于20
        if (16 >= User_Info.age >= 60) and User_Info.level >= 20 and Group_ID != config["admin_qun"]:
            await bot.allow(event)
            await say_group(config["admin_qun"],
                            "[Bot-自动化]\n申请者[{User}:{QQ}]已满足入群条件，已自动同意".format(User=User_Nick, QQ=QQ_ID))
        # 用户等级低于10自动拒绝请求并拉黑
        elif User_Info.level <= 10:
            await bot.decline(event, "[Bot-自动化]远未达到入群标准，已自动拒绝并拉入黑名单", ban=True)
            await say_group(config["admin_qun"],
                            "[Bot-自动化]\n申请者[{User}:{QQ}]远低于入群条件，已自动拒绝并拉黑".format(User=User_Nick, QQ=QQ_ID))
        # 未达成以上条件须人工审核
        else:
            await say_group(config["admin_qun"],
                            "[Bot-自动化]\n申请者[{User}:{QQ}]未达到入群条件，请人工审核".format(User=User_Nick, QQ=QQ_ID))

    # 管理员部分

    # 模块开关
    @bot.on(GroupMessage)
    async def module_switch(event: GroupMessage):
        global whitelist, testop, botmanager, banlist
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        msg = str(event.message_chain)
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        if qun == config["admin_qun"] and msg[:1] in "!":
            if msg_split[0] == "!模块":
                pass

    # 重载配置文件
    @bot.on(GroupMessage)
    async def reload_config(event: GroupMessage):
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        msg = str(event.message_chain)
        qun = event.sender.group.id
        if qun == config["admin_qun"] and msg[:1] in "!":
            if msg_split[0] == "!reload":
                reloadConfig()

    # 查询审核列表
    @bot.on(GroupMessage)
    async def Inquire_whitelist(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        if qun == config["admin_qun"] and msg[:1] in "!":
            if msg_split[0] == "!查询":
                db.ping(reconnect=True)
                if len(msg_split) == 1:
                    await send_compound_message(await get_wait_list())
                elif len(msg_split) == 2:
                    if msg_split[1] == "通过":
                        await send_compound_message(await get_pass())
                    elif msg_split[1] == "拒绝":
                        await send_compound_message(await get_notpass())
                    elif msg_split[1] == "清空":
                        await send_compound_message(await del_wait_list_all())

    # 审核
    @bot.on(GroupMessage)
    async def whitelist_pass(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        if qun == config["admin_qun"] and msg[:1] in "!":
            if msg_split[0] == "!白名单":
                db.ping(reconnect=True)
                if len(msg_split) == 2 and msg_split[1] == "全部通过":
                    await send_compound_message(await pass_all())
                elif len(msg_split) >= 3:
                    if msg_split[1] == "通过" and len(msg_split) == 3:
                        await send_compound_message(await pass_one(msg_split[2]))
                    elif msg_split[1] == "拒绝":
                        if len(msg_split) == 3:
                            # 默认值None
                            await send_compound_message(await refuse_one(msg_split[2]))
                        elif len(msg_split) == 4:
                            await send_compound_message(await refuse_one(msg_split[2], msg_split[3]))
                        else:
                            await say_group_warning(qun, "参数错误！")

    # 黑名单
    @bot.on(GroupMessage)
    async def banlist(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        if qun == config["admin_qun"] and msg[:1] in "!":
            if msg_split[0] == "!ban":
                if len(msg_split) == 4 and msg_split[1] == "添加":
                    await send_compound_message(await banlist_add(msg_split[2], msg_split[3]))
                elif len(msg_split) == 3 and msg_split[1] == "移除":
                    await send_compound_message(await banlist_del(msg_split[2]))

    # 玩家部分

    # 白名单-申请
    @bot.on(GroupMessage)
    async def player_Whitelist(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        if qun == config["player_qun"] and msg[:1] in "!":
            if msg_split[0] == "!白名单":
                logger.debug("[消息]<-群{qun}:{QQ}:{msg}".format(msg=msg, QQ=QQ, qun=qun))
                if len(msg_split) == 2:
                    matchobj = re.match('^[a-zA-Z0-9_]+$', msg_split[1])
                    if matchobj is None:
                        await say_group_warning(qun, "参数:{player}含有非法字符！".format(player=msg_split[1]))
                    else:
                        await send_compound_message(await get_whitelist(msg_split[1], QQ))

    # 白名单-解绑
    @bot.on(GroupMessage)
    async def player_unbind_Whitelist(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        if qun == config["player_qun"] and msg[:1] in "!":
            if msg_split[0] == "!解绑":
                await send_compound_message(await unbundling(msg_split[1], QQ))

    # 白名单-改名
    @bot.on(GroupMessage)
    async def player_rename(event: GroupMessage):
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = event.sender.id
        qun = event.sender.group.id
        if qun == config["player_qun"] and msg[:1] in "!":
            if msg_split[0] == "!改名":
                matchobj = re.match('^[a-zA-Z0-9_]+$', msg_split[1])
                if matchobj is None:
                    await say_group_warning(qun, "参数:{player}含有非法字符！".format(player=msg_split[1]))
                else:
                    await send_compound_message(await rename(QQ, msg_split[1]))

    # 黑名单-查询
    @bot.on(GroupMessage)
    async def player_blacklist(event: GroupMessage):
        qun = event.sender.group.id
        QQ = str(event.sender.id)
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        if qun == config["player_qun"] and msg[:1] in "!":
            if msg_split[0] == "!黑名单":
                await send_compound_message(await get_banlist())

    # 服务器状态查询
    @bot.on(GroupMessage)
    async def get_server_status(event: GroupMessage):
        msg = str(event.message_chain)
        qun = event.sender.group.id
        if "!服务器" in msg or "!在线" in msg or "!人数" in msg or "!server" in msg:
            await say_group(qun, await Server_Status())

    # 全局部分

    # 问答
    @bot.on(GroupMessage)
    async def help(event: GroupMessage):
        msg = str(event.message_chain)
        # 屏蔽!开头的
        if msg[:1] != "!":
            qun = event.sender.group.id
            answer = await findAnswer(qun, msg)
            if answer is not None:
                await say_group(qun, answer)

    # 测试用代码
    inc = InterruptControl(bot)

    @bot.on(GroupMessage)
    async def on_friend_message(event: GroupMessage):
        # 触发
        if str(event.message_chain).strip() == '你是谁？':
            await bot.send(event, '我是气人姬。你呢？')

            # 等待回复
            @Filter(GroupMessage)
            def waiter(event_new: GroupMessage):
                if event.sender.id == event_new.sender.id:
                    msg = str(event_new.message_chain)
                    if msg.startswith('我是'):
                        return msg[2:].rstrip('。')

            # 最终执行
            name = await inc.wait(waiter)
            await bot.send(event, f'你好，{name}。')

    # 启动机器人
    bot.run()
