# 检查Minecraft更新
import urllib.request
import json
from module.config import *
from module.logger import *

def get_record(url):
    resp = urllib.request.urlopen(url)
    ele_json = json.loads(resp.read())
    return ele_json

def Check_Verson():
    try:
        get_version = get_record('https://launchermeta.mojang.com/mc/game/version_manifest.json')
    except:
        log.error("查询失败，网络错误")
    else:
        for row in get_version["latest"]:
            print(config["Check-Minecraft-Version"][row])
            if get_version["latest"].get(row) == config["Check-Minecraft-Version"][row]:
                print("检测到新版本",get_version["latest"].get(row))
                print(row)
                File = open("config.json", "r+", encoding='utf-8')  # 打开文件
                data = config  # 存储原始文件
                File.truncate()
                data["Check-Minecraft-Version"][row] = get_version["latest"].get(row)  # 添加/修改
                print(data["Check-Minecraft-Version"][row])
                File.write(  # 写入
                    json.dumps(data, indent="\t", sort_keys=True, ensure_ascii=False)
                )