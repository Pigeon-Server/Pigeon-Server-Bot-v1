# 数据库相关
import pymysql
from module.config import config
from module.logger import log

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
log.debug("数据库版本 : %s " % data)

async def sql_run(sql=None):
    try:
        # 执行sql语句
        if sql is not None:
            cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        log.info("[数据库]命令执行成功~")
    except:
        # 如果发生错误则回滚
        db.rollback()
        log.error("[数据库]数据库发生错误，执行失败")

# 创建数据表
if cursor.execute("show tables") != 3:
    log.info("数据表不存在，正在尝试创建1/3")
    create_table_whitelist = """create table whitelist (
    id float(5) PRIMARY KEY AUTO_INCREMENT,
    QQ char(16) UNIQUE not null,
    player_name char(16) UNIQUE not null
    )"""
    log.info("数据表不存在，正在尝试创建2/3")
    create_table_wait = """create table wait(
    id float(5) PRIMARY KEY AUTO_INCREMENT,
    QQ char(16) UNIQUE not null,
    player_name char(16) UNIQUE not null,
    pass boolean,
    pass_info char(50) 
    )"""
    log.info("数据表不存在，正在尝试创建3/3")
    create_table_banlist = """create table banlist(
    player_name char(16) UNIQUE not null,
    reason char(30)
    )"""
    cursor.execute(create_table_whitelist)
    cursor.execute(create_table_wait)
    cursor.execute(create_table_banlist)
    log.debug("数据表创建完成")
