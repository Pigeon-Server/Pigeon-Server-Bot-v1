# 检查Minecraft更新
import time
import urllib.request
from module.config import *
from module.logger import *

def get_record(url):
    resp = urllib.request.urlopen(url)
    ele_json = json.loads(resp.read())
    return ele_json

def Check_Verson():
    try:
        get_version = get_record('https://launchermeta.mojang.com/mc/game/version_manifest.json')
    except :
        logger.error("查询失败，发生错误")
    else:
        for version_type in get_version["latest"]:
            if get_version["latest"].get(version_type) != config["Check-Minecraft-Version"][version_type]:
                # 写入文件
                File = open("config/config.json", "r+", encoding='utf-8')  # 打开文件
                data = config  # 存储原始文件
                File.truncate()
                data["Check-Minecraft-Version"][version_type] = get_version["latest"].get(version_type)  # 添加/修改
                File.write(  # 写入
                    json.dumps(data, indent="\t", sort_keys=True, ensure_ascii=False)
                )
                time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                logger.info("检测到新版本[{version_type}:{Version}]，已更新配置文件".format(version_type=version_type, Version=get_version["latest"].get(version_type)))
                return {
                    "player_msg": "[Bot-Minecraft版本更新检测]\n检测到新版本[{version_type}:{Version}]\n查询时间：{time}".format(version_type=version_type, Version=get_version["latest"].get(version_type), time=time_now)
                }

