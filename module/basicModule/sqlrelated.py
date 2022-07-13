from module.Class.DataBaseClass import *
from module.basicModule.config import *


database = DataBase(config["DB_Config"]["database"], config["DB_Config"]["DB_Host"],
                    config["DB_Config"]["DB_User"], config["DB_Config"]["DB_Password"])
database.Connect()
connected = database.GetConnectionInfo()
cursor = connected.cursor()

# 创建数据表
if cursor.execute("show tables") != 6:
    logger.error("数据表丢失，正在修复")
    create_tables = """CREATE TABLE IF NOT EXISTS whitelist (
        id float(5) PRIMARY KEY AUTO_INCREMENT,
        QQ char(16) UNIQUE not null,
        player_name char(16) UNIQUE not null
    );
    CREATE TABLE IF NOT EXISTS wait(
        id float(5) PRIMARY KEY AUTO_INCREMENT,
        QQ char(16) UNIQUE not null,
        player_name char(20) UNIQUE not null,
        pass boolean,
        pass_info char(50) 
    );
    CREATE TABLE IF NOT EXISTS banlist(
        player_name char(16) UNIQUE not null,
        reason char(30)
    );"""
    cursor.execute(create_tables)
    connected.commit()
    logger.debug("数据表创建完成")

