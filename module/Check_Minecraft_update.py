# 检查Minecraft更新
import time
import urllib.request
from module.basicModule.config import *
from module.basicModule.logger import *

def getRecord(url: str) -> dict:
    resp = urllib.request.urlopen(url, data=None, timeout=10)
    ele_json = json5.loads(resp.read())
    return ele_json

def CheckVersion() -> dict:
    try:
        get_version = getRecord('https://launchermeta.mojang.com/mc/game/version_manifest.json')
    except:
        logger.error("查询失败，发生错误")
    else:
        if get_version is not None:
            for version_type in get_version["latest"]:
                if get_version["latest"].get(version_type) != config["Check-Minecraft-Version"][version_type]:
                    # 写入文件
                    File = open("config/config.json5", "r+", encoding="UTF-8", errors="ignore")  # 打开文件
                    data = config  # 存储原始文件
                    File.truncate()
                    data["Check-Minecraft-Version"][version_type] = get_version["latest"].get(version_type)  # 添加/修改
                    File.write(  # 写入
                        json5.dumps(data, indent="\t", sort_keys=True, ensure_ascii=False)
                    )
                    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    logger.info(f"检测到新版本[{version_type}:{get_version['latest'].get(version_type)}]，已更新配置文件")
                    return {
                        "player_msg": f"[Bot-Minecraft版本更新检测]\n检测到新版本[{version_type}:{get_version['latest'].get(version_type)}]\n查询时间：{time_now}"
                    }
        else:
            logger.error("查询失败，发生错误")

