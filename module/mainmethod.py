# 主要方法实现
from module.servertools import *

# 获取已通过玩家
async def get_pass():
    db.ping(reconnect=True)
    success = cursor.execute("SELECT id,QQ,player_name from wait where pass is True")
    output = cursor.fetchall()
    tempstr = " "
    if success == 1:
        for row in output:
            id = row[0]
            QQ = row[1]
            player_name = row[2]
            tempstr += "[{sum}]玩家ID：{ID}\nQQ：{QQ}\n".format(sum=int(id), ID=player_name, QQ=QQ)
    del output
    return {
        "admin_msg": tempstr
    }


# 获取未通过玩家
async def get_notpass():
    db.ping(reconnect=True)
    success = cursor.execute("SELECT id,QQ,player_name,pass_info from wait where pass is False")
    output = cursor.fetchall()
    tempstr = " "
    if success == 1:
        for row in output:
            id = row[0]
            QQ = row[1]
            player_name = row[2]
            pass_info = row[3]
            # 打印结果
            tempstr += "[{sum}]玩家ID：{ID}\nQQ：{QQ}\n退回原因：{msg}\n".format(sum=int(id), ID=player_name, QQ=QQ,
                                                                        msg=pass_info)
    del output
    return {
        "admin_msg": tempstr
    }


# 获取待审核玩家
async def get_wait_list():
    db.ping(reconnect=True)
    success = cursor.execute("SELECT id,QQ,player_name from wait where pass is NULL")
    output = cursor.fetchall()
    tempstr = " "
    if success == 1:
        for row in output:
            id = row[0]
            QQ = row[1]
            player_name = row[2]
            # 打印结果
            tempstr = tempstr + "[{sum}]玩家ID：{ID}\nQQ：{QQ}".format(sum=int(id), ID=player_name, QQ=QQ) + "\n"
    del output
    return {
        "admin_msg": tempstr
    }


# 通过所有待审核玩家
async def pass_all():
    db.ping(reconnect=True)
    success = cursor.execute("SELECT id from wait where pass is not True and pass is not False")
    output_list = cursor.fetchall()
    if success == 1:
        for row in output_list:
            id = row[0]
            judge1 = cursor.execute(
                "SELECT id,QQ,player_name from wait where pass is NULL and `id` = '{id}'".format(id=id))
            output = cursor.fetchall()
            if judge1 == 1:
                QQ = output[0][1]
                Player_Name = output[0][2]
                # 执行
                cursor.execute("UPDATE wait SET pass = true WHERE (`id` = '{id}')".format(id=id))
                cursor.execute(
                    "INSERT INTO whitelist(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(QQ=QQ,
                                                                                                         Player_Name=Player_Name))
                statu = await sql_run()
                if statu != -1:
                    statu1 = await whitelist_add(Player_Name)
                    if statu1 == 0:
                        return {
                            "admin_msg": "ID：{id}添加白名单成功".format(id=id),
                            "player_msg": "玩家：{player}白名单审核通过".format(player=Player_Name)
                        }
                    elif statu1 == 1:
                        return {
                            "admin_msg": "该玩家已拥有白名单"
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
                    "admin_msg": "ID：{id}不存在，请重新查询".format(id=id)
                }
    else:
        return {
            "admin_msg": "没有待审核的白名单申请"
        }
    del output_list


# 清空所有未审核玩家
async def del_wait_list_all():
    success = await sql_run("""DELETE from wait where pass is NULL""")
    if success != -1:
        return {
            "admin_msg": "[Bot-查询]:白名单未审核序列已清空"
        }
    else:
        return {
            "admin_msg": "[Bot-查询]:数据库出现错误，请检查"
        }


# 通过指定ID的玩家
async def pass_one(id: str):
    db.ping(reconnect=True)
    Inquire_1 = cursor.execute(
        "SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'".format(
            id=id))
    output = cursor.fetchall()
    if Inquire_1 == 1:
        QQ = output[0][1]
        Player_Name = output[0][2]
        cursor.execute("UPDATE wait SET pass = true WHERE (`id` = '{id}')".format(id=id))
        cursor.execute("INSERT INTO whitelist(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(QQ=QQ,
                                                                                                            Player_Name=Player_Name))
        statu = await sql_run()
        if statu != -1:
            statu1 = await whitelist_add(Player_Name)
            if statu1 == 0:
                return {
                    "admin_msg": "ID：{id}添加白名单成功".format(id=id),
                    "player_msg": "玩家：{player}白名单审核通过".format(player=Player_Name)
                }
            elif statu1 == 1:
                return {
                    "admin_msg": "该玩家已拥有白名单"
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
            "admin_msg": "ID：{id}不存在，请重新查询".format(id=id)
        }


# 拒绝白名单
async def refuse_one(id: str, reason=None):
    db.ping(reconnect=True)
    Inquire_1 = cursor.execute(
        "SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'".format(
            id=id))
    output = cursor.fetchall()
    if Inquire_1 == 1:
        Player_Name = output[0][2]
        cursor.execute("UPDATE wait SET pass = false WHERE (`id` = '{id}')".format(id=id))
        cursor.execute("UPDATE wait SET pass_info = '{info}' WHERE (`id` = '{id}')".format(id=id, info=reason))
        statu = await sql_run()
        if statu != -1:
            return {
                "admin_msg": "玩家：{player}白名单未通过\n退回原因：{info}".format(player=Player_Name, info=reason),
                "player": "玩家：{player}白名单未审核通过\n原因：{info}".format(player=Player_Name, info=reason)
            }
        else:
            return {
                "admin_msg": "数据库执行错误，请检查"
            }
    else:
        return {
            "admin_msg": "ID：{id}不存在，请重新查询".format(id=id)
        }


# 申请白名单
async def get_whitelist(playername: str, qq: str):
    db.ping(reconnect=True)
    if len(playername) > 16:
        playername = playername[:16]
        return {
            "player_msg": "申请玩家名过长\n已自动截取为：{playerfix}".format(playerfix=playername)
        }
    Inquire_1 = cursor.execute("SELECT * from wait where QQ = '{QQ}'".format(QQ=qq))
    Inquire_2 = cursor.execute("SELECT * from whitelist where QQ = '{QQ}'".format(QQ=qq))
    Inquire_3 = cursor.execute("SELECT * from wait where QQ = '{QQ}' and pass = 0".format(QQ=qq))
    Inquire_4 = cursor.execute("SELECT * from wait where QQ = '{QQ}' and pass = 1".format(QQ=qq))
    print(Inquire_1, Inquire_2, Inquire_3, Inquire_4)
    if Inquire_1 != 1 and Inquire_2 != 1:
        logger.info("[审核]已收到玩家{player}的白名单请求".format(player=playername))
        cursor.execute(
            "INSERT INTO wait(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(database=config["database"],
                                                                                            QQ=qq,
                                                                                            Player_Name=playername))
        statu = await sql_run()
        if statu == -1:
            return {
                "admin_msg": "数据库执行错误，请检查"
            }
        else:
            success = cursor.execute("SELECT id,player_name from wait where QQ = '{QQ}'".format(QQ=qq))
            data = cursor.fetchall()
            if success == 1:
                id = data[0][0]
                playername = data[0][1]
                return {
                    "player_msg": '您的白名单申请已提交给服务器管理组~',
                    "admin_msg": "[Bot-审核]收到一条新的白名单申请\n审核序号：{ID}\n玩家名：{player}\n使用!白名单 通过/不通过 [审核序号]".format(
                        player=playername, ID=int(id))
                }
            else:
                return {
                    "player_msg": '发生错误，请联系管理员'
                }
    elif Inquire_3 == 1:
        success = cursor.execute("SELECT pass_info from wait where QQ = '{QQ}'".format(QQ=qq))
        data = cursor.fetchall()
        if success == 1:
            reason = data[0][0]
            return {
                "player_msg": '您的白名单申请权限已锁定\n原因：申请被管理组拒绝\n拒绝原因：{res}'.format(res=reason)
            }
        else:
            return {
                "player_msg": '发生错误，请联系管理员'
            }
    elif Inquire_2 == 1 and Inquire_4 == 1:
        return {
            "player_msg": '您已经获取过白名单'
        }
    elif Inquire_1 == 1 and Inquire_2 != 1:
        return {
            "player_msg": '您的白名单申请正在处理中~ 请耐心等待'
        }


# 取消绑定
async def unbundling(playername: str, qq: str):
    db.ping(reconnect=True)
    Inquire_1 = cursor.execute(
        "SELECT * from wait where QQ = '{QQ}' and player_name = '{player}'".format(QQ=qq, player=playername))
    Inquire_2 = cursor.execute(
        "SELECT * from whitelist where QQ = '{QQ}' and player_name = '{player}'".format(QQ=qq, player=playername))
    Inquire_3 = cursor.execute("SELECT * from banlist where player_name = '{player}'".format(player=playername))
    Inquire_4 = cursor.execute(
        "SELECT * from wait where QQ = '{QQ}' and player_name = '{player}' and pass = 0".format(QQ=qq,
                                                                                                player=playername))
    print(Inquire_1, Inquire_2, Inquire_3, Inquire_4)
    if Inquire_3 == 1:
        return {
            "player_msg": "你已被列入黑名单，无法解绑"
        }
    elif Inquire_4 == 1:
        return {
            "player_msg": "你的白名单申请已被拒绝，无法解绑"
        }
    elif Inquire_1 == 1 or Inquire_2 == 1:
        if Inquire_1 == 1:
            statu1 = await sql_run(
                "DELETE from wait where QQ = '{QQ}' and player_name = '{player}'".format(QQ=qq, player=playername))
            if statu1 == -1:
                return {
                    "admin_msg": "数据库执行错误"
                }
        if Inquire_2 == 1:
            statu2 = await sql_run(
                "DELETE from whitelist where QQ = '{QQ}' and player_name = '{player}'".format(QQ=qq, player=playername))
            if statu2 == -1:
                return {
                    "admin_msg": "数据库执行错误"
                }
        await whitelist_del(playername)
        return {
            "player_msg": '解绑成功~',
            "admin_msg": "[Bot-白名单]玩家{player}已解绑".format(player=playername)
        }
    else:
        return {
            "player_msg": '该QQ名下未绑定该玩家，请检查ID是否正确'
        }


# 改名
async def rename(QQ: int, rename: str):
    # 数据库查询
    db.ping(reconnect=True)
    # 查询玩家原先名字
    Inquire_original_name = cursor.execute("SELECT * from whitelist where QQ = '{QQ}'".format(QQ=QQ))
    Inquire_original_name_arry = cursor.fetchone()

    # 查询是否已有这个名字的玩家
    Inquire_collision = cursor.execute("SELECT * from whitelist where player_name = '{player}'".format(player=rename))

    # 查询要修改的玩家是否在黑名单内
    Inquire_blacklist = cursor.execute("SELECT * from banlist where player_name = '{player}'".format(player=rename))

    # 功能实现

    # 是否在黑名单中
    if Inquire_blacklist == 0:
        if Inquire_original_name and Inquire_collision == 0:
            # 移除该玩家白名单
            await whitelist_del(Inquire_original_name_arry[2])
            # 踢出该玩家
            await server_run("kick " + Inquire_original_name_arry[2])
            # 更新数据库内数据
            await sql_run(
                "update whitelist set player_name = '{rename}' where QQ = '{QQ}' and player_name = '{original_name}'".format(
                    rename=rename, QQ=QQ, original_name=Inquire_original_name_arry[2]))
            await sql_run(
                "update wait set player_name = '{rename}' where QQ = '{QQ}' and player_name = '{original_name}'".format(
                    rename=rename, QQ=QQ, original_name=Inquire_original_name_arry[2]))
            # 添加白名单给新ID
            await whitelist_add(rename)
            return {
                "player_msg": "成功~",
                "admin_msg": "[Bot-改名]\n玩家{original_name}已改名，新名字{rename}".format(
                    original_name=Inquire_original_name_arry[2], rename=rename)
            }
        # 查不到账户绑定玩家时
        elif Inquire_original_name == 0:
            return {
                "player_msg": "你名下未绑定玩家！"
            }
        # 比对相同时
        elif Inquire_original_name_arry[2] == rename:
            return {
                "player_msg": "要修改的名字与原名字相同"
            }
        # 数据库查询到该名字时
        elif Inquire_collision != 0:
            return {
                "player_msg": "该名字已有人使用过啦~"
            }
    elif Inquire_blacklist != 0:
        return {
            "player_msg": "黑名单用户禁止改名"
        }


# 黑名单-添加
async def banlist_add(playername: str, reason: str):
    db.ping(reconnect=True)
    exist = cursor.execute("SELECT * from banlist where player_name = 'player'".format(player=playername))
    if exist != 1:
        await ban_add(playername, reason)
        cursor.execute(
            "INSERT INTO banlist(player_name, reason) VALUES ('{player}', '{reason}')".format(player=playername,
                                                                                              reason=reason))
        statu = await sql_run()
        if statu != -1:
            return {
                "admin_msg": "[黑名单-添加]成功",
                "player_msg": "玩家:{player} 原因:{reason} 已被移入黑名单,请各位引以为戒".format(player=playername, reason=reason)
            }
        else:
            return {
                "admin_msg": "数据库执行错误"
            }
    else:
        return {
            "admin_msg": "该玩家已在黑名单内"
        }


# 黑名单-删除
async def banlist_del(playername: str):
    db.ping(reconnect=True)
    success = await ban_del(playername)
    if success == 0:
        statu = await sql_run("DELETE from banlist where player_name = '{player}'".format(player=playername))
        if statu != -1:
            return {
                "player_msg": "{player}已被移出黑名单".format(player=playername),
                "admin_msg": "[黑名单-移除]成功"
            }
        else:
            return {
                "admin_msg": "数据库执行错误"
            }
    else:
        return {
            "admin_msg": "该玩家未被服务器封禁"
        }


# 输出黑名单列表
async def get_banlist():
    db.ping(reconnect=True)
    cursor.execute("SELECT * from banlist")
    output = cursor.fetchall()
    tempstr = " "
    if len(output) != 0:
        i = 1
        for row in output:
            player_name = row[0]
            reason = row[1]
            tempstr += "[{i}]玩家ID：{ID}\n原因:{reason}\n".format(i=i, ID=player_name, reason=reason)
            # 打印结果
            i += 1
        return {
            "player_msg": tempstr
        }
    else:
        return {
            "player_msg": "[黑名单-查询]无玩家"
        }


# 剥夺玩家白名单
async def del_whitelist(playerid):
    global num
    if num == 0:
        num = playerid
        success = cursor.execute("SELECT id,QQ,player_name from whitelist where `id` = '{id}'".format(id=playerid))
        if success == 1:
            output = cursor.fetchall()
            Player_Name = output[0][2]
            await say_group(config["admin_qun"], "[Bot-白名单审核]是否移除玩家{player}的白名单？".format(player=Player_Name))
            del output
        else:
            num = 0
            await say_group_warning(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=playerid))
    else:
        await say_group_warning(config["admin_qun"], "上一次对ID为{id}玩家的操作还未完成".format(id=num))


# 确定剥夺
async def confirm_del(playerid):
    global num
    num = 0
    cursor.execute("SELECT id,QQ,player_name from whitelist where `id` = '{id}'".format(id=playerid))
    output = cursor.fetchall()
    Player_Name = output[0][2]
    await whitelist_del(Player_Name)
    await sql_run("DELETE from whitelist where id = '{id}'".format(id=playerid))
    await sql_run("DELETE from wait where player_name = '{name}'".format(name=Player_Name))
    success = cursor.execute("SELECT id,QQ,player_name from whitelist where `id` = '{id}'".format(id=playerid))
    del output
    if success == 0:
        await say_group(config["admin_qun"], "[Bot-白名单审核]移除白名单成功")
    else:
        await say_group_warning(config["admin_qun"], "[Bot-白名单审核]移除白名单失败")


# FAQ
async def findAnswer(qun, msg):
    for row in FAQ["FAQ"]:
        if qun == row["qun"] or "global" == row["qun"]:
            temp = row["qun"]
            row.pop("qun")
            for key in row:
                if key in msg:
                    row["qun"] = qun
                    return row.get(key)
            row["qun"] = temp


# 退回白名单
async def refuse_one_op(id, reason=None):
    db.ping(reconnect=True)
    Inquire_1 = cursor.execute(
        "SELECT id,QQ,player_name from opwait where pass is not True and pass is not False and `id` = '{id}'".format(
            id=id))
    output = cursor.fetchall()
    if Inquire_1 == 1:
        Player_Name = output[0][2]
        cursor.execute("UPDATE opwait SET pass = false WHERE (`id` = '{id}')".format(id=id))
        cursor.execute("UPDATE opwait SET reason = '{info}' WHERE (`id` = '{id}')".format(id=id, info=reason))
        statu = await sql_run()
        if statu != -1:
            await say_group(config["admin_qun"],
                            "玩家：{player}OP申请未通过\n退回原因：{info}".format(player=Player_Name, info=reason))
            await say_group(config["player_qun"],
                                 "玩家：{player}OP申请未审核通过\n原因：{info}".format(player=Player_Name, info=reason))
        else:
            return {"admin_msg": "数据库执行错误，请检查"}
    else:
        return {"admin_msg": "ID：{id}不存在，请重新查询".format(id=id)}

# # 假人 添加
# async def bot_add(bot_name, qq, purpose, open=0):
#     if open == 1:
#         cursor.execute(
#             "INSERT INTO usedbot(QQ,bot_name,isused,purpose) VALUES ('{QQ}','{bot_name}',true,'{purpose}')".format(
#                 QQ=qq, bot_name="bot_" + bot_name, purpose=purpose))
#     else:
#         cursor.execute(
#             "INSERT INTO usedbot(QQ,bot_name,isused,purpose) VALUES ('{QQ}','{bot_name}',false,'{purpose}')".format(
#                 QQ=qq, bot_name="bot_" + bot_name, purpose=purpose))
#     success = await sql_run()
#     if success != -1:
#         if open == 0:
#             return {
#                 "player_msg": "[Bot-假人管理] 登记成功,假人未启用"
#             }
#         else:
#             return {
#                 "player_msg": "[Bot-假人管理] 登记成功,假人已启用"
#             }
#     else:
#         return {
#             "player_msg": "[Bot-假人管理] 数据库执行错误，请联系管理员"
#         }
#
#
# # 假人 删除
# async def bot_del(botname, qq, admin=0):
#     success = cursor.execute("SELECT QQ from usedbot where bot_name = '{bot}'".format(bot="bot_" + botname))
#     if success == 1:
#         output = cursor.fetchall()
#         Q = output[0][0]
#         if Q == qq or admin == 1:
#             await sql_run(
#                 "DELETE from usedbot where QQ = '{QQ}' and bot_name = '{bot}'".format(QQ=qq, bot="bot_" + botname))
#             success = cursor.execute("SELECT * from usedbot where bot_name = '{bot}'".format(bot="bot_" + botname))
#             if success != 1:
#                 await say_group(config["player_qun"], "[Bot-假人管理] 删除成功")
#             else:
#                 await say_group_warning(config["player_qun"], "[Bot-假人管理] 删除失败，请重试或联系管理员")
#         else:
#             await say_group_warning(config["player_qun"], "[Bot-假人管理] 你不是该假人的添加者，无法删除")
#         del output
#     else:
#         await say_group_warning(config["player_qun"], "[Bot-假人管理] 不存在该假人，请登记或检查ID是否正确")
#
#
# # 获取假人信息
# async def get_bot(botname):
#     success = cursor.execute(
#         "SELECT QQ,bot_name,isused,purpose,time from usedbot where bot_name = '{bot}'".format(bot="bot_" + botname))
#     if success == 1:
#         output = cursor.fetchall()
#         QQ = output[0][0]
#         bot_name = output[0][1]
#         isused = output[0][2]
#         purpose = output[0][3]
#         time = output[0][4]
#         if isused == 1:
#             use = "是"
#         else:
#             use = "否"
#         await say_group(config["player_qun"], "[Bot-假人管理]\n"
#                                               "假人信息:\n"
#                                               "名称: {bot_name}\n"
#                                               "添加者QQ: {QQ}\n"
#                                               "添加时间：{time}"
#                                               "正在使用: {isused}\n"
#                                               "用途: {purpose}".format(bot_name=bot_name, QQ=QQ, isused=use,
#                                                                      purpose=purpose, time=time))
#         del output
#     else:
#         await say_group(config["player_qun"], "[Bot-假人管理]查询的假人不存在")
#
#
# # 获取假人列表
# async def get_bot_all():
#     success = cursor.execute("SELECT id,bot_name,isused,purpose,time from usedbot")
#     if success == 0:
#         await say_group_warning(config["player_qun"], "未查询到假人信息")
#     else:
#         output = cursor.fetchall()
#         tempstr = "[Bot-假人管理]\n已登记的所有假人:\n"
#         for row in output:
#             id = row[0]
#             bot_name = row[1]
#             isused = row[2]
#             purpose = row[3]
#             time = row[4]
#             if isused == 1:
#                 use = "是"
#             else:
#                 use = "否"
#             tempstr += "\n[{sum}]假人名称：{bot_name}\n是否使用：{use}\n用途：{purpose}\n创建时间：{time}\n".format(sum=int(id),
#                                                                                                   bot_name=bot_name,
#                                                                                                   use=use,
#                                                                                                   purpose=purpose,
#                                                                                                   time=time)
#             # 打印结果
#         del output
#         await say_group(config["player_qun"], tempstr)
#
#
# # 获取假人（字符串）
# async def bot_get():
#     finded = await server_run("list")
#     tempstr = "服务器内假人:\n"
#     i = 0
#     find1 = finded.find(": ")
#     finded = finded[find1 + 2:]
#     temp = finded.split(", ")
#     while i != len(temp):
#         find = temp[i]
#         if find.find('bot_') != -1:
#             tempstr = tempstr + find[find.find('bot_') + 4:] + "\n"
#         i += 1
#     return tempstr
#
#
# # 获取假人列表（列表）
# async def bot_get_list():
#     finded = await server_run("list")
#     templist = []
#     i = 0
#     find1 = finded.find(": ")
#     finded = finded[find1 + 2:]
#     temp = finded.split(", ")
#     while i != len(temp):
#         find = temp[i]
#         if find.find('bot_') != -1:
#             templist.append(find[find.find('bot_') + 4:])
#         i += 1
#     return templist
#
#
# # 获取未登记假人（字符串）
# async def check_bot():
#     botlist = await bot_get_list()
#     nopass = "服务器内以下假人未登记：\n"
#     i = 0
#     while i != len(botlist):
#         success = cursor.execute("SELECT isused from usedbot WHERE bot_name = '{bot}'".format(bot="bot_" + botlist[i]))
#         if success == 1:
#             output = cursor.fetchall()
#             isused = output[0][0]
#             if isused != 1:
#                 nopass = nopass + botlist[i] + "\n"
#             del output
#         else:
#             nopass = nopass + botlist[i] + "\n"
#         i += 1
#     return nopass
#
#
# # 获取未登记假人（列表）
# async def check_bot_list():
#     botlist = await bot_get_list()
#     nopass = []
#     i = 0
#     while i != len(botlist):
#         success = cursor.execute("SELECT isused from usedbot WHERE bot_name = '{bot}'".format(bot="bot_" + botlist[i]))
#         if success == 1:
#             output = cursor.fetchall()
#             isused = output[0][0]
#             if isused != 1:
#                 nopass.append(botlist[i])
#             del output
#         else:
#             nopass.append(botlist[i])
#         i += 1
#     return nopass
#
#
# # 切换Bot是否开启
# async def switch_bot(lenth, qq, botname, purpose=None):
#     success = cursor.execute(
#         "SELECT QQ,bot_name,isused from usedbot where bot_name = '{bot}'".format(bot="bot_" + botname))
#     if success:
#         output = cursor.fetchall()
#         dataQQ = output[0][0]
#         bot_name = output[0][1]
#         isused = output[0][2]
#         # 切换是否使用
#         if lenth == 3:
#             if qq == dataQQ:
#                 if isused == 1:
#                     cursor.execute(
#                         "UPDATE usedbot SET isused = false WHERE (`bot_name` = '{bot}')".format(bot=bot_name))
#                     success = await sql_run()
#                     if success != -1:
#                         await server_run("player {bot} kill".format(bot=bot_name))
#                         await say_group(config["player_qun"], "[Bot-假人管理] 现在假人不再使用了")
#                     else:
#                         await say_group_warning(config["player_qun"], "[Bot-假人管理] 数据库执行错误，请联系管理员")
#                 else:
#                     cursor.execute("UPDATE usedbot SET isused = true WHERE (`bot_name` = '{bot}')".format(bot=bot_name))
#                     success = await sql_run()
#                     if success != -1:
#                         await server_run("player {bot} kill".format(bot=bot_name))
#                         await say_group(config["player_qun"], "[Bot-假人管理] 现在假人可以使用了")
#                     else:
#                         await say_group_warning(config["player_qun"], "[Bot-假人管理] 数据库执行错误，请联系管理员")
#             else:
#                 await say_group_warning(config["player_qun"], "[Bot-假人管理] 你不是该假人的添加者，无法切换")
#         # 更改用途
#         elif lenth == 4:
#             if qq == dataQQ:
#                 cursor.execute(
#                     "UPDATE usedbot SET purpose = '{purpose}' WHERE (`bot_name` = '{bot}')".format(bot=bot_name,
#                                                                                                    purpose=purpose))
#                 success = await sql_run()
#                 if success != -1:
#                     await server_run("player {bot} kill".format(bot=bot_name))
#                     await say_group(config["player_qun"], "[Bot-假人管理] 用途修改成功")
#                 else:
#                     await say_group_warning(config["player_qun"], "[Bot-假人管理] 数据库执行错误，请联系管理员")
#     else:
#         await say_group_warning(config["player_qun"], "[Bot-假人管理] 此假人未登记")
#
#
# # 删除假人
# async def del_bot(botname):
#     nopass = await check_bot_list()
#     if botname in nopass:
#         await server_run("player {bot} kill".format(bot="bot_" + botname))
#         await say_group(config["admin_qun"], "[Bot-假人管理] 删除服务器内假人成功")
#     else:
#         await say_group_warning(config["admin_qun"], "[Bot-假人管理] 此假人不存在或已登记")
#
#
# # 删除所有假人
# async def del_bot_all():
#     nopass = await check_bot_list()
#     i = 0
#     while i != len(nopass):
#         await server_run("player {bot} kill".format(bot="bot_" + nopass[i]))
#         await say_group(config["admin_qun"], "[Bot-假人管理] 删除服务器内假人{bot}成功".format(bot=nopass[i]))
#         i += 1
#     await say_group(config["admin_qun"], "[Bot-假人管理] 删除服务器内未登记假人完成")


# 获取op
# async def get_op(qq, playername):
#     db.ping(reconnect=True)
#     if len(playername) > 16:
#         await say_group_warning(config["player_qun"], "玩家名：{player}过长（{len}/16个字符）\n"
#                                                       "自动截取为：{playerfix}\n"
#                                                       "服务器会自动截取16个字符".format(player=playername, len=len(playername), playerfix=playername[:16]))
#         playername = playername[:16]
#     Inquire_1 = cursor.execute("SELECT * from opwait where QQ = '{QQ}'".format(QQ=qq))
#     Inquire_2 = cursor.execute("SELECT * from existop where QQ = '{QQ}'".format(QQ=qq))
#     Inquire_3 = cursor.execute("SELECT * from opwait where QQ = '{QQ}' and pass = 0".format(QQ=qq))
#     Inquire_4 = cursor.execute("SELECT * from opwait where QQ = '{QQ}' and pass = 1".format(QQ=qq))
#     print(Inquire_1, Inquire_2, Inquire_3, Inquire_4)
#     if Inquire_1 != 1 and Inquire_2 != 1:
#         logger.info("[审核]已收到玩家{player}的OP请求".format(player=playername))
#         cursor.execute("INSERT INTO opwait(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(database=config["database"], QQ=qq, Player_Name=playername))
#         statu = await sql_run()
#         if statu == -1:
#             await say_group_warning(config["admin_qun"], "数据库执行错误")
#         else:
#             success = cursor.execute("SELECT id,player_name from opwait where QQ = '{QQ}'".format(QQ=qq))
#             data = cursor.fetchall()
#             if success == 1:
#                 id = data[0][0]
#                 playername = data[0][1]
#                 await say_group(config["admin_qun"],
#                                 "[Bot-审核]收到一条新的OP申请\n"
#                                 "玩家序号：{ID}\n"
#                                 "玩家名：{player}\n"
#                                 "使用!OP 通过/不通过 [玩家序号]".format(player=playername, ID=int(id)))
#                 await say_group(config["player_qun"], '您的OP申请已提交给服务器管理组~')
#             else:
#                 await say_group_warning(config["player_qun"], '发生错误，请联系管理员')
#             del data
#     elif Inquire_3 == 1:
#         success = cursor.execute("SELECT pass_info from opwait where QQ = '{QQ}'".format(QQ=qq))
#         data = cursor.fetchall()
#         if success == 1:
#             reason = data[0][0]
#             await say_group(config["player_qun"], '您的OP申请权限已锁定\n'
#                                                   '原因：OP申请被管理组拒绝\n'
#                                                   '拒绝原因：{res}'.format(res=reason))
#         else:
#             await say_group_warning(config["player_qun"], '发生错误，请联系管理员')
#         del data
#     elif Inquire_2 == 1 and Inquire_4 == 1:
#         await say_group(config["player_qun"], '您已经申请过OP')
#     elif Inquire_1 == 1 and Inquire_2 != 1:
#         await say_group(config["player_qun"], '您的OP申请正在处理中哦')

# async def pass_all_op():
#     db.ping(reconnect=True)
#     success = cursor.execute("SELECT id from opwait where pass is not True and pass is not False")
#     output_list = cursor.fetchall()
#     if success == 1:
#         for row in output_list:
#             id = row[0]
#             judge1 = cursor.execute("SELECT id,QQ,player_name from opwait where pass is NULL and `id` = '{id}'".format(id=id))
#             output = cursor.fetchall()
#             if judge1 == 1:
#                 QQ = output[0][1]
#                 Player_Name = output[0][2]
#                 # 执行
#                 cursor.execute("UPDATE opwait SET pass = true WHERE (`id` = '{id}')".format(id=id))
#                 cursor.execute("INSERT INTO existop(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(QQ=QQ, Player_Name=Player_Name))
#                 statu = await sql_run()
#                 if statu != -1:
#                     statu1 = await op_add(Player_Name)
#                     if statu1 == 0:
#                         await say_group(config["admin_qun"], "ID：{id}添加OP成功".format(id=id))
#                         await say_group_info(config["player_qun"], "玩家：{player}OP审核通过".format(player=Player_Name))
#                     elif statu1 == 1:
#                         await say_group(config["admin_qun"], "该玩家已有OP")
#                     else:
#                         await say_group(config["admin_qun"], "发生未知错误，请检查")
#                 else:
#                     await say_group(config["admin_qun"], "数据库执行错误，请检查")
#             else:
#                 await say_group_warning(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=id))
#     else:
#         await say_group(config["admin_qun"], "没有待审核的OP申请")
#     del output_list

# async def pass_one_op(id):
#     db.ping(reconnect=True)
#     Inquire_1 = cursor.execute("SELECT id,QQ,player_name from opwait where pass is not True and pass is not False and `id` = '{id}'".format(id=id))
#     output = cursor.fetchall()
#     if Inquire_1 == 1:
#         QQ = output[0][1]
#         Player_Name = output[0][2]
#         cursor.execute("UPDATE opwait SET pass = true WHERE (`id` = '{id}')".format(id=id))
#         cursor.execute("INSERT INTO existop(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(QQ=QQ,Player_Name=Player_Name))
#         statu = await sql_run()
#         if statu != -1:
#             statu1 = await op_add(Player_Name)
#             if statu1 == 0:
#                 await say_group(config["admin_qun"], "ID：{id}获取OP成功".format(id=id))
#                 await say_group_info(config["player_qun"], "玩家：{player}OP审核通过".format(player=Player_Name))
#             elif statu1 == 1:
#                 await say_group(config["admin_qun"], "该玩家已是OP")
#             else:
#                 await say_group(config["admin_qun"], "发生未知错误，请检查")
#         else:
#             await say_group(config["admin_qun"], "数据库执行错误，请检查")
#     else:
#         await say_group_warning(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=id))
#     del output

# 解绑 op
# async def unbundling_op(playername, qq):
#     db.ping(reconnect=True)
#     Inquire_1 = cursor.execute("SELECT * from opwait where QQ = '{QQ}' and player_name = '{player}'".format(QQ=qq, player=playername))
#     Inquire_2 = cursor.execute("SELECT * from existop where QQ = '{QQ}' and player_name = '{player}'".format(QQ=qq, player=playername))
#     Inquire_3 = cursor.execute("SELECT * from banlist where player_name = '{player}'".format(player=playername))
#     Inquire_4 = cursor.execute("SELECT * from opwait where QQ = '{QQ}' and player_name = '{player}' and pass = 0".format(QQ=qq, player=playername))
#     print(Inquire_1, Inquire_2, Inquire_3, Inquire_4)
#     if Inquire_3 == 1:
#         await say_group_info(config["player_qun"], "你已被列入黑名单，无法解绑")
#     elif Inquire_4 == 1:
#         await say_group_info(config["player_qun"], "你的OP申请已被拒绝，无法解绑")
#     elif Inquire_1 == 1 or Inquire_2 == 1:
#         if Inquire_1 == 1:
#             statu1 = await sql_run(
#                 "DELETE from opwait where QQ = '{QQ}' and player_name = '{player}'".format(QQ=qq, player=playername))
#             if statu1 == -1:
#                 await say_group_warning(config["admin_qun"], "数据库执行错误")
#         if Inquire_2 == 1:
#             statu2 = await sql_run("DELETE from existop where QQ = '{QQ}' and player_name = '{player}'".format(QQ=qq, player=playername))
#             if statu2 == -1:
#                 await say_group_warning(config["admin_qun"], "数据库执行错误")
#         await whitelist_del(playername)
#         await say_group_info(config["admin_qun"], "[Bot-白名单]玩家{player}OP已解绑".format(player=playername))
#         await say_group(config["player_qun"], '解绑成功~')
#     else:
#         await say_group_warning(config["player_qun"], '该QQ名下未绑定该玩家，请检查ID是否正确')
