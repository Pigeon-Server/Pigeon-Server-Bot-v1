# by Pigeon Server
# Bot 主体
import re
from module.servertools import *
from module.botsendmsg import *
from module.sqlrelated import *

num = 0

if __name__ == '__main__':
    @bot.on(GroupMessage)
    async def main(event: GroupMessage):
        # 群消息
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        # 消息输出
        print("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
        # 管理员-白名单-查询
        if msg_split[0] == "!查询" and qun == config["admin_qun"]:
            db.ping(reconnect=True)
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            msg_split.append(" ")
            if msg_split[1] == "已通过":
                log.debug("[查询]:正在查询白名单审核序列")
                success = cursor.execute("SELECT id,QQ,player_name from wait where pass is True")
                # db.commit()
                output = cursor.fetchall()
                tempstr = ""
                for row in output:
                    id = row[0]
                    QQ = row[1]
                    player_name = row[2]
                    tempstr += "[{sum}]玩家ID：{ID}\nQQ：{QQ}\n".format(sum=int(id), ID=player_name, QQ=QQ)
                    # 打印结果
                del output
                if success == 0:
                    await say_group_warning(config["admin_qun"], "未查询到通过玩家")
                else:
                    await say_group(config["admin_qun"], tempstr)
            elif msg_split[1] == "未通过":
                log.debug("[查询]:正在查询白名单审核序列")
                success = cursor.execute("SELECT id,QQ,player_name,pass_info from wait where pass is False")
                output = cursor.fetchall()
                tempstr = ""
                for row in output:
                    id = row[0]
                    QQ = row[1]
                    player_name = row[2]
                    pass_info = row[3]
                    # 打印结果
                    tempstr += "[{sum}]玩家ID：{ID}\nQQ：{QQ}\n退回原因：{msg}\n".format(sum=int(id), ID=player_name, QQ=QQ, msg=pass_info)
                del output
                if success == 0:
                    await say_group_warning(config["admin_qun"], "未查询到不通过玩家")
                else:
                    await say_group(config["admin_qun"], tempstr)
            elif msg_split[1] == "清空":
                cursor.execute("DELETE from wait where pass is NULL")
                await say_group_info(config["admin_qun"], "[Bot-查询]:白名单未审核序列已清空")
            else:
                log.debug("[查询]:正在查询白名单审核序列")
                success = cursor.execute("SELECT id,QQ,player_name from wait where pass is NULL")
                # db.commit()
                output = cursor.fetchall()
                if success == 0:
                    await say_group_info(config["admin_qun"], "[Bot-查询]:没有待审核的白名单")
                else:
                    for row in output:
                        id = row[0]
                        QQ = row[1]
                        player_name = row[2]
                        # 打印结果
                        await say_group(config["admin_qun"], "【{sum}】玩家ID：{ID}\nQQ：{QQ}".format(sum=int(id), ID=player_name, QQ=QQ))
                    del output
        # 管理员-白名单-操作
        if msg_split[0] == "!白名单" and qun == config["admin_qun"]:
            global num
            db.ping(reconnect=True)
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            try:
                if msg_split[1] == "拒绝" and len(msg_split) == 3:
                    Inquire_1 = cursor.execute("SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'".format(id=msg_split[2]))
                    if Inquire_1 == 1:
                        output = cursor.fetchall()
                        Player_Name = output[0][2]
                        # 执行
                        db.ping(reconnect=True)
                        cursor.execute("UPDATE wait SET pass = false WHERE (`id` = '{id}')".format(id=msg_split[2]))
                        await sql_run()
                        await say_group(config["admin_qun"], "玩家：{player}白名单未通过".format(player=Player_Name))
                        await say_group_info(config["player_qun"], "玩家：{player}白名单未审核通过".format(player=Player_Name))
                    else:
                        await say_group_warning(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=msg_split[2]))
                elif msg_split[1] == "拒绝" and len(msg_split) == 4:
                    Inquire_1 = cursor.execute("SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'".format(id=msg_split[2]))
                    if Inquire_1 == 1:
                        output = cursor.fetchall()
                        Player_Name = output[0][2]
                        # 执行
                        cursor.execute("UPDATE wait SET pass = false WHERE (`id` = '{id}')".format(id=msg_split[2]))
                        cursor.execute("UPDATE wait SET pass_info = '{info}' WHERE (`id` = '{id}')".format(id=msg_split[2], info=msg_split[3]))
                        await sql_run()
                        await say_group(config["admin_qun"], "玩家：{player}白名单未通过\n退回原因：{info}".format(player=Player_Name, info=msg_split[3]))
                        await say_group_info(config["player_qun"], "玩家：{player}白名单未审核通过\n原因：{info}".format(player=Player_Name, info=msg_split[3]))
                    else:
                        await say_group_warning(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=msg_split[2]))
                elif msg_split[1] == "全部通过":
                    cursor.execute("SELECT id from wait where pass is not True and pass is not False")
                    output_list = cursor.fetchall()
                    for row in output_list:
                        id = row[0]
                        Inquire_1 = cursor.execute("SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'".format(id=id))
                        if Inquire_1 == 1:
                            output = cursor.fetchall()
                            QQ = output[0][1]
                            Player_Name = output[0][2]
                            # 执行
                            cursor.execute("UPDATE wait SET pass = true WHERE (`id` = '{id}')".format(id=id))
                            cursor.execute("INSERT INTO whitelist(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(QQ=QQ, Player_Name=Player_Name))
                            await sql_run()
                            await say_group(config["admin_qun"], "ID：{id}添加白名单成功".format(id=id))
                            await say_group_info(config["player_qun"], "玩家：{player}白名单审核通过".format(player=Player_Name))
                            await whitelist_add(Player_Name)
                        else:
                            await say_group_warning(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=id))
                elif msg_split[1] == "通过" and len(msg_split) == 3:
                    Inquire_1 = cursor.execute("SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'".format(id=msg_split[2]))
                    if Inquire_1 == 1:
                        output = cursor.fetchall()
                        QQ = output[0][1]
                        Player_Name = output[0][2]
                        # 执行
                        cursor.execute("UPDATE wait SET pass = true WHERE (`id` = '{id}')".format(id=msg_split[2]))
                        cursor.execute("INSERT INTO whitelist(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(QQ=QQ, Player_Name=Player_Name))
                        await sql_run()
                        await say_group(config["admin_qun"], "ID：{id}添加白名单成功".format(id=msg_split[2]))
                        await say_group_info(config["player_qun"], "玩家：{player}白名单审核通过".format(player=Player_Name))
                        await whitelist_add(Player_Name)
                    else:
                        await say_group_warning(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=msg_split[2]))
                elif msg_split[1] == "移除" and len(msg_split) == 3:
                    if msg_split[2] == "重置":
                        num = 0
                        await say_group_info(config["admin_qun"], "[Bot-白名单审核]ID重置成功")
                    elif num == 0:
                        num = msg_split[2]
                        success = cursor.execute("SELECT id,QQ,player_name from whitelist where `id` = '{id}'".format(id=msg_split[2]))
                        if success == 1:
                            output = cursor.fetchall()
                            Player_Name = output[0][2]
                            await say_group(config["admin_qun"], "[Bot-白名单审核]是否移除玩家{player}的白名单？".format(player=Player_Name))
                            del output
                        else:
                            num = 0
                            await say_group_warning(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=msg_split[2]))
                    else:
                        await say_group_warning(config["admin_qun"], "上一次对ID为{id}玩家的操作还未完成".format(id=num))
                elif msg_split[1] == "移除" and len(msg_split) == 4:
                    if msg_split[3] == "确认" and num == msg_split[2]:
                        num = 0
                        cursor.execute("SELECT id,QQ,player_name from whitelist where `id` = '{id}'".format(id=msg_split[2]))
                        output = cursor.fetchall()
                        Player_Name = output[0][2]
                        await whitelist_del(Player_Name)
                        await sql_run("DELETE from whitelist where id = '{id}'".format(id=msg_split[2]))
                        await sql_run("DELETE from wait where player_name = '{name}'".format(name=Player_Name))
                        success = cursor.execute("SELECT id,QQ,player_name from whitelist where `id` = '{id}'".format(id=msg_split[2]))
                        del output
                        if success == 0:
                            await say_group_info(config["admin_qun"], "[Bot-白名单审核]移除白名单成功")
                        else:
                            await say_group_warning(config["admin_qun"], "[Bot-白名单审核]移除白名单失败")
                    elif msg_split[3] == "取消" and num == msg_split[2]:
                        num = 0
                        await say_group_info(config["admin_qun"], "[Bot-白名单审核]操作已取消")
            except:
                await say_group_warning(config["admin_qun"], "[Bot-白名单审核]发生错误，请检查参数是否错误")
                await say_group(config["admin_qun"], "[Bot-白名单审核]\n"
                                            '通过白名单申请：!白名单 通过 [ID]\n'
                                            '拒绝白名单申请：!白名单 拒绝 [ID]\n'
                                            '清空白名单待审核列表：!查询 清空\n'
                                            '手动删除白名单：!白名单 移除 [ID]\n'
                                            '确认删除白名单：!白名单 移除 [ID] 确认\n'
                                            '取消删除白名单：!白名单 移除 [ID] 取消\n'
                                            '取消待确认操作：!白名单 移除 重置\n'
                                            '注意：可使用!白名单 全部通过 通过所有玩家的请求\n'
                                            '注意：ID非玩家昵称，请使用!查询')
        # 白名单-审核add
        if msg_split[0] == "!白名单" and len(msg_split) == 2 and qun == config["player_qun"]:
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            db.ping(reconnect=True)
            Inquire_1 = cursor.execute("SELECT * from wait where QQ like '%{QQ}%'".format(QQ=QQ))
            Inquire_2 = cursor.execute("SELECT * from whitelist where QQ like '%{QQ}%'".format(QQ=QQ))
            Inquire_3 = cursor.execute("SELECT * from wait where QQ like '%{QQ}%' and pass like 0".format(QQ=QQ))
            Inquire_4 = cursor.execute("SELECT * from wait where QQ like '%{QQ}%' and pass like 1".format(QQ=QQ))
            print(Inquire_1, Inquire_2, Inquire_3, Inquire_4)
            # 判断
            matchobj = re.match('^[a-zA-Z1-9_]+$', msg_split[1])
            if matchobj is None:
                await say_group_warning(config["player_qun"], "参数:{player}格式错误".format(player=msg_split[1]))
            elif Inquire_1 != 1 and Inquire_2 != 1 and qun == config["player_qun"]:
                log.info("[审核]已收到玩家{player}的白名单请求".format(player=msg_split[1]))
                sql = """INSERT INTO wait(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')""".format(database=config["database"], QQ=QQ, Player_Name=msg_split[1])
                await sql_run(sql)
                cursor.execute("SELECT id,player_name,pass_info from wait where QQ like '%{QQ}%'".format(QQ=QQ))
                data = cursor.fetchall()
                for row in data:
                    id = row[0]
                    playername = row[1]
                await say_group(config["admin_qun"],
                                "[Bot-审核]收到一条新的白名单申请\n"
                                "玩家序号：{ID}\n"
                                "玩家名：{player}\n"
                                "使用!白名单 通过/不通过 [玩家序号]".format(player=playername, ID=int(id)))
                del data
                await say_group(config["player_qun"], '您的白名单申请已提交给服务器管理组~')
            elif Inquire_3 == 1:
                cursor.execute("SELECT pass_info from wait where QQ like '%{QQ}%'".format(QQ=QQ))
                data = cursor.fetchall()
                for row in data:
                    reason = row[0]
                await say_group(config["player_qun"], '您的白名单申请已锁定\n'
                                                      '原因：白名单申请被管理组拒绝\n'
                                                      '拒绝原因：{res}'.format(res=reason))
                del data
            elif Inquire_2 == 1 and Inquire_4 == 1:
                await say_group(config["player_qun"], '您已经获取过白名单')
            elif Inquire_1 == 1 and Inquire_2 != 1:
                await say_group(config["player_qun"], '您的白名单申请正在处理中哦')
        elif "白名单" in msg and qun == config["player_qun"]:
            await say_group(config["player_qun"], '[Bot-白名单帮助]\n'
                                        '使用 "!白名单 [ID]" 申请白名单\n'
                                        '使用 "!解绑 [ID]" 解除QQ与白名单的绑定（该操作会取消之前绑定ID的白名单）\n'
                                        '注意：一个QQ账号只能绑定一个ID\n'
                                        '注意：如果为BE玩家，需要在ID前加上"BE_"\n'
                                        '警告：请进入一次服务器（聊天栏提示：你未被此服务器列入白名单）后再申请白名单，否则大概率无法生效！！！')
        # 解绑用户
        elif msg_split[0] == "!解绑" and len(msg_split) == 2 and qun == config["player_qun"]:
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            db.ping(reconnect=True)
            Inquire_1 = cursor.execute("SELECT * from wait where QQ = '{QQ}' and player_name = '{player}'".format(QQ=QQ, player=msg_split[1]))
            Inquire_2 = cursor.execute("SELECT * from whitelist where QQ = '{QQ}' and player_name = '{player}'".format(QQ=QQ, player=msg_split[1]))
            Inquire_3 = cursor.execute("SELECT * from banlist where player_name = '{player}'".format(player=msg_split[1]))
            Inquire_4 = cursor.execute("SELECT * from wait where QQ = '{QQ}' and player_name = '{player}' and pass = 0".format(QQ=QQ, player=msg_split[1]))
            print(Inquire_1, Inquire_2, Inquire_3, Inquire_4)
            if Inquire_3 == 1:
                await say_group_info(config["player_qun"], "你已被列入黑名单，无法解绑")
            elif Inquire_4 == 1:
                await say_group_info(config["player_qun"], "你的白名单申请已被拒绝，无法解绑")
            elif Inquire_1 >= 1 or Inquire_2 >= 1:
                try:
                    if Inquire_1 == 1:
                        await sql_run("DELETE from wait where QQ = '{QQ}' and player_name = '{player}'".format(QQ=QQ, player=msg_split[1]))
                    if Inquire_2 == 1:
                        await sql_run("DELETE from whitelist where QQ = '{QQ}' and player_name = '{player}'".format(QQ=QQ,player=msg_split[1]))
                    await whitelist_del(msg_split[1])
                    await say_group_info(config["admin_qun"], "[Bot-白名单]玩家{player}已解绑".format(player=msg_split[1]))
                    await say_group(config["player_qun"], '解绑成功~')
                except:
                    await say_group_warning(config["player_qun"], '解绑失败')
            else:
                await say_group_warning(config["player_qun"], '该QQ名下未绑定该玩家，请检查ID是否正确')
        # ban
        if msg_split[0] == "!ban" and qun == config["admin_qun"]:
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            db.ping(reconnect=True)
            Inquire_1 = cursor.execute("SELECT * from banlist where player_name like '%{Player}%'".format(Player=msg_split[2]))
            if msg_split[1] == "添加" and Inquire_1 != 1 and len(msg_split) == 4:
                await ban_add(msg_split[2], msg_split[3])
                sql = """INSERT INTO banlist(player_name, reason) VALUES ('{player}', '{reason}')""".format(player=msg_split[2], reason=msg_split[3])
                await sql_run(sql)
                await say_group_info(config["player_qun"], "玩家:{player} 原因:{reason} 已被移入黑名单,请各位引以为戒".format(player=msg_split[2],reason=msg_split[3]))
                await say_group(config["admin_qun"], "[黑名单-添加]成功")
            elif msg_split[1] == "移除" and Inquire_1 == 1 and len(msg_split) == 3:
                await ban_del(msg_split[2])
                sql = """DELETE from banlist where player_name like '{player}'""".format(player=msg_split[2])
                await sql_run(sql)
                await say_group_info(config["player_qun"], "玩家:{player}已被移出黑名单".format(player=msg_split[2]))
                await say_group(config["admin_qun"], "[黑名单-移除]成功")
        elif ("ban" in msg or "黑名单" in msg) and qun == config["admin_qun"]:
            await say_group(config["admin_qun"], "[Bot-黑名单]\n"
                                       "将玩家列入黑名单：!ban 添加 [ID] [原因]\n"
                                       "将玩家移出黑名单：!ban 移除 [ID]")
        elif msg_split[0] == "!黑名单" and qun == config["player_qun"]:
            log.debug("[消息]<-群:{QQ}:{msg}".format(msg=msg, QQ=QQ))
            log.debug("[bot-查询]:正在查询黑名单列表")
            db.ping(reconnect=True)
            cursor.execute("SELECT * from banlist")
            output = cursor.fetchall()
            tempstr = ""
            if len(output) != 0:
                i = 1
                for row in output:
                    player_name = row[0]
                    reason = row[1]
                    tempstr += "[{i}]玩家ID：{ID}\n原因:{reason}\n".format(i=i, ID=player_name, reason=reason)
                    # 打印结果
                    i += 1
                await say_group(config["player_qun"], tempstr)
            else:
                await say_group_warning(config["player_qun"], "[黑名单-查询]无玩家")
        elif "黑名单" in msg and qun == config["player_qun"]:
            await say_group(config["player_qun"], "[Bot-黑名单]\n""查询黑名单列表：!黑名单")


    bot.run()
