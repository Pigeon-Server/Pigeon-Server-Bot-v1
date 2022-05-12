# by Pigeon Server
# Bot 主体
import pymysql
import re
from mirai import *
from module.servertools import *
from module.config import *
if __name__ == '__main__':

    # 连接数据库
    db = pymysql.connect(
        host=config["db_host"],
        user=config["db_user"],
        password=config["db_password"],
        database=config["database"]
    )
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("数据库版本 : %s " % data)

    async def sql_run(sql=None):
        try:
            # 执行sql语句
            if sql != None:
                cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print("[数据库]命令执行成功~")
        except:
            # 如果发生错误则回滚
            db.rollback()
            print("[数据库]数据库发生错误，执行失败")


    async def say_group(group, msg):
        print("[bot-消息]发送群消息:{group}:{msg}".format(group=group, msg=msg))
        time.sleep(random.uniform(1.0, 0.3))
        await bot.send_group_message(group, MessageChain([
            Plain(msg)
        ]))

    # # 创建数据表
    if cursor.execute("show tables") != 3:
        print("数据表不存在，正在尝试创建1/3")
        create_table_whitelist = """create table whitelist (
        id float(5) PRIMARY KEY AUTO_INCREMENT,
        QQ char(16) UNIQUE not null,
        player_name char(16) UNIQUE not null
        )"""
        print("数据表不存在，正在尝试创建2/3")
        create_table_wait = """create table wait(
        id float(5) PRIMARY KEY AUTO_INCREMENT,
        QQ char(16) UNIQUE not null,
        player_name char(16) UNIQUE not null,
        pass boolean,
        pass_info char(50) 
        )"""
        print("数据表不存在，正在尝试创建3/3")
        create_table_banlist = """create table banlist(
        player_name char(16) UNIQUE not null,
        reason char(30)
        )"""
        cursor.execute(create_table_whitelist)
        cursor.execute(create_table_wait)
        cursor.execute(create_table_banlist)
        print("数据表创建完成")


    # 连接QQ机器人（HTTP）
    adapter = HTTPAdapter(verify_key=config["key"], host=config["hostname"], port=config["post"])
    bot = Mirai(qq=config["QQ"], adapter=adapter)


    @bot.on(GroupMessage)
    async def main(event: GroupMessage):
        # 群消息
        msg = str(event.message_chain)
        msg_split = "".join(map(str, event.message_chain[Plain])).split(" ")
        QQ = str(event.sender.id)
        qun = event.sender.group.id
        # 消息输出
        print("[Bot-消息]收到群消息:{QQ}:{msg}".format(msg=msg, QQ=QQ))
        # 管理员-白名单-查询
        if msg_split[0] == "!查询" and qun == config["admin_qun"]:
            msg_split.append(" ")
            if msg_split[1] == "已通过":
                print("[bot-查询]:正在查询白名单审核序列")
                cursor.execute("SELECT id,QQ,player_name from wait where pass is True")
                # db.commit()
                output = cursor.fetchall()
                for row in output:
                    id = row[0]
                    QQ = row[1]
                    player_name = row[2]
                    # 打印结果
                    await say_group(config["admin_qun"], "【{sum}】玩家ID：{ID}\nQQ：{QQ}".format(sum=int(id), ID=player_name, QQ=QQ))
                del output
            elif msg_split[1] == "未通过":
                print("[bot-查询]:正在查询白名单审核序列")
                cursor.execute("SELECT id,QQ,player_name,pass_info from wait where pass is False")
                output = cursor.fetchall()
                for row in output:
                    id = row[0]
                    QQ = row[1]
                    player_name = row[2]
                    pass_info = row[3]
                    # 打印结果
                    await say_group(config["admin_qun"],"【{sum}】玩家ID：{ID}\nQQ：{QQ}\n退回原因：{msg}".format(sum=int(id), ID=player_name, QQ=QQ,msg=pass_info))
                del output
            elif msg_split[1] == "清空":
                print("[bot-查询]:正在清空白名单审核序列")
                cursor.execute("DELETE from wait where pass is NULL")
                await say_group(config["admin_qun"], "白名单未审核序列已清空")
            else:
                print("[bot-查询]:正在查询白名单审核序列")
                success = cursor.execute("SELECT id,QQ,player_name from wait where pass is NULL")
                # db.commit()
                output = cursor.fetchall()
                if success == 0:
                    await say_group(config["admin_qun"], "[bot-查询]:没有待审核的白名单")
                else:
                    for row in output:
                        id = row[0]
                        QQ = row[1]
                        player_name = row[2]
                        # 打印结果
                        await say_group(config["admin_qun"], "【{sum}】玩家ID：{ID}\nQQ：{QQ}".format(sum=int(id), ID=player_name, QQ=QQ))
                    del output
        # 管理员-白名单-通过
        if msg_split[0] == "!白名单" and qun == config["admin_qun"]:
            try:
                if msg_split[1] == "拒绝":
                    Inquire_1 = cursor.execute(
                        "SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'".format(id=msg_split[2]))
                    if Inquire_1 == 1:
                        output = cursor.fetchall()
                        Player_Name = output[0][2]
                        # 执行
                        cursor.execute("UPDATE wait SET pass = false WHERE (`id` = '{id}')".format(id=msg_split[2]))
                        await sql_run()
                        await say_group(config["admin_qun"], "ID：{id}白名单未通过".format(id=msg_split[2]))
                        await say_group(config["player_qun"], "玩家：{player}白名单未审核通过".format(player=Player_Name))
                    else:
                        await say_group(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=msg_split[2]))
                elif msg_split[1] == "全部通过":
                    cursor.execute("SELECT id from wait where pass is not True and pass is not False")
                    output_list = cursor.fetchall()
                    for row in output_list:
                        id = row[0]
                        Inquire_1 = cursor.execute(
                            "SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'".format(id=id))
                        if Inquire_1 == 1:
                            output = cursor.fetchall()
                            QQ = output[0][1]
                            Player_Name = output[0][2]
                            # 执行
                            cursor.execute("UPDATE wait SET pass = true WHERE (`id` = '{id}')".format(id=id))
                            cursor.execute(
                                "INSERT INTO whitelist(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(QQ=QQ, Player_Name=Player_Name))
                            await sql_run()
                            await say_group(config["admin_qun"], "ID：{id}添加白名单成功".format(id=id))
                            await say_group(config["player_qun"], "玩家：{player}白名单审核通过".format(player=Player_Name))
                            await whtielist_add(Player_Name)
                        else:
                            await say_group(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=id))
                elif msg_split[1] == "通过":
                    Inquire_1 = cursor.execute(
                        "SELECT id,QQ,player_name from wait where pass is not True and pass is not False and `id` = '{id}'".format(id=msg_split[2]))
                    if Inquire_1 == 1:
                        output = cursor.fetchall()
                        QQ = output[0][1]
                        Player_Name = output[0][2]
                        # 执行
                        cursor.execute("UPDATE wait SET pass = true WHERE (`id` = '{id}')".format(id=msg_split[2]))
                        cursor.execute(
                            "INSERT INTO whitelist(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')".format(QQ=QQ,Player_Name=Player_Name))
                        await sql_run()
                        await say_group(config["admin_qun"], "ID：{id}添加白名单成功".format(id=msg_split[2]))
                        await say_group(config["player_qun"], "玩家：{player}白名单审核通过".format(player=Player_Name))
                        await whtielist_add(Player_Name)
                    else:
                        await say_group(config["admin_qun"], "ID：{id}不存在，请重新查询".format(id=msg_split[2]))
            except:
                await say_group(config["admin_qun"], "[Bot-白名单审核]发生错误，请检查参数是否错误")
                await say_group(config["admin_qun"], "[Bot-白名单审核]\n"
                                           '通过白名单申请：!白名单 通过 [ID]\n'
                                           '拒绝白名单申请：!白名单 拒绝 [ID]\n'
                                           '清空白名单待审核列表：!查询 清空\n'
                                           '注意：可使用!白名单 全部通过 通过所有玩家的请求\n'
                                           '注意：ID非玩家昵称，请使用!查询')
        # 白名单-审核add
        if msg_split[0] == "!白名单" and len(msg_split) == 2 and qun == config["player_qun"]:
            Inquire_1 = cursor.execute("SELECT * from wait where QQ like '%{QQ}%'".format(QQ=QQ))
            Inquire_2 = cursor.execute("SELECT * from whitelist where QQ like '%{QQ}%'".format(QQ=QQ))
            Inquire_3 = cursor.execute("SELECT * from wait where QQ like '%{QQ}%' and pass like 0".format(QQ=QQ))
            Inquire_4 = cursor.execute("SELECT * from wait where QQ like '%{QQ}%' and pass like 1".format(QQ=QQ))
            print(Inquire_1, Inquire_2, Inquire_3, Inquire_4)
            # 判断
            matchobj = re.match('^[a-zA-Z1-9_]+$', msg_split[1])
            if matchobj is None:
                await say_group(config["player_qun"], "参数:{player}格式错误".format(player=msg_split[1]))
            elif Inquire_1 != 1 and Inquire_2 != 1 and qun == config["player_qun"]:
                print("[Bot-审核]已收到玩家{player}的白名单请求".format(player=msg_split[1]))
                sql = """INSERT INTO wait(`QQ`, `player_name`) VALUES ('{QQ}', '{Player_Name}')""".format(database=database, QQ=QQ, Player_Name=msg_split[1])
                await sql_run(sql)
                cursor.execute("SELECT id,player_name from wait where QQ like '%{QQ}%'".format(QQ=QQ))
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
                await say_group(config["player_qun"], '您的白名单申请已被管理组拒绝')
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
            Inquire_1 = cursor.execute("SELECT * from wait where QQ = '{QQ}' and player_name = '{player}'".format(QQ=QQ, player=msg_split[1]))
            Inquire_2 = cursor.execute("SELECT * from whitelist where QQ = '{QQ}' and player_name = '{player}'".format(QQ=QQ, player=msg_split[1]))
            print(Inquire_1, Inquire_2)
            if Inquire_1 >= 1 or Inquire_2 >= 1:
                try:
                    if Inquire_1 == 1:
                        await sql_run("DELETE from wait where QQ = '{QQ}' and player_name = '{player}'".format(QQ=QQ, player=msg_split[1]))
                    if Inquire_2 == 1:
                        await sql_run("DELETE from whitelist where QQ = '{QQ}' and player_name = '{player}'".format(QQ=QQ,player=msg_split[1]))
                    await whtielist_del(msg_split[1])
                    await say_group(config["admin_qun"], "[Bot-白名单]玩家{player}已解绑".format(player=msg_split[1]))
                    await say_group(config["player_qun"], '解绑成功~')
                except:
                    await say_group(config["player_qun"], '解绑失败')
            else:
                await say_group(config["player_qun"], '该QQ名下未绑定该玩家，请检查ID是否正确')
        # ban
        if msg_split[0] == "!ban" and qun == config["admin_qun"]:
            Inquire_1 = cursor.execute(
                "SELECT * from banlist where player_name like '%{Player}%'".format(Player=msg_split[2]))
            if msg_split[1] == "添加" and Inquire_1 != 1 and len(msg_split) == 4:
                await ban_add(msg_split[2], msg_split[3])
                sql = """INSERT INTO banlist(player_name, reason) VALUES ('{player}', '{reason}')""".format(player=msg_split[2], reason=msg_split[3])
                await sql_run(sql)
                await say_group(config["player_qun"], "玩家:{player} 原因:{reason} 已被移入黑名单,请各位引以为戒".format(player=msg_split[2],reason=msg_split[3]))
                await say_group(config["admin_qun"], "[黑名单-添加]成功")
            elif msg_split[1] == "移除" and Inquire_1 == 1 and len(msg_split) == 3:
                await ban_del(msg_split[2])
                sql = """DELETE from banlist where player_name like '{player}'""".format(player=msg_split[2])
                await sql_run(sql)
                await say_group(config["player_qun"], "玩家:{player}已被移出黑名单".format(player=msg_split[2]))
                await say_group(config["admin_qun"], "[黑名单-移除]成功")
        elif ("ban" in msg or "黑名单" in msg) and qun == config["admin_qun"]:
            await say_group(config["admin_qun"], "[Bot-黑名单]\n"
                                       "将玩家列入黑名单：!ban 添加 [ID] [原因]\n"
                                       "将玩家移出黑名单：!ban 移除 [ID]")
        elif msg_split[0] == "!黑名单" and qun == config["player_qun"]:
            print("[bot-查询]:正在查询黑名单列表")
            cursor.execute("SELECT player_name,reason from banlist")
            output = cursor.fetchall()
            if len(output) != 0:
                i = 1
                for row in output:
                    player_name = row[0]
                    reason = row[1]
                    # 打印结果
                    await say_group(config["player_qun"],
                                    "【{i}】玩家ID:{ID}\n原因:{reason}".format(i=i, ID=player_name, reason=reason))
                    i += 1
            else:
                await say_group(config["player_qun"], "[黑名单-查询]无玩家")
        elif "黑名单" in msg and qun == config["player_qun"]:
            await say_group(config["player_qun"], "[Bot-黑名单]\n""查询黑名单列表：!黑名单")
        # 测试服管理申请


    bot.run()
