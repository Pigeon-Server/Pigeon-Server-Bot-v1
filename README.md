# Pigeon Server Bot V1
A [mirai-api-http](https://github.com/project-mirai/mirai-api-http) plugin for remotely executing minecraft commands.

# 当前版本已停止开发

Pigeon Server · 气人姬部分功能实现，Minecraft服务器执行部分使用RCON

## 已实现功能
- 白名单申请
- 多服务器状态查询
- 分群问答
- 版本更新提示
- 热重载配置
## 待实现功能
- 多账户
- 多服务器
- 开黑啦同步
- 群文件自动分类
- 测试服权限申请
- 假人登记/自动踢出未登记假人

## 配置文件详解

### [config.json](config/config.json)主配置文件

#### 机器人本体
|  Key   | Value  |
|  :----:  | :----:  |
| QQ  | 机器人的QQ号（int） |
| admin_qun  | 管理员群群号（int） |
| player_qun  | 玩家群群号（int） |
| post  | mirai-api-http HTTP端口（int） |
| hostname  | mirai-api-http HTTP地址（str） |

#### 数据库（DB）
|  Key   | Value  |
|  :----:  | :----:  |
| db_host  | 数据库地址（str） |
| db_user  | 数据库用户（str） |
| db_password  | 数据库密码（str） |
| database  | 数据库库名（str） |

#### RCON服务器部分（服务器执行命令）
|  Key   | Value  |
|  :----:  | :----:  |
| RCON_host  | RCON地址（str） |
| RCON_post  | RCON端口（int） |
| RCON_password  | RCON密码（str） |

#### 多服务器人数查询
```json
"serverlist": [
	"服务器1IP",
	"服务器2IP"
],
"servername": [
	"服务器1",
	"服务器2"
]
```

#### 版本检查（Check-Minecraft-Version）
|  Key   | Value  |
|  :----:  | :----:  |
| release  | 发行版本存储 |
| snapshot  | 快照版本存储 |

### [FAQ.json](config/FAQ.json)问答模块配置（此模块将会忽略所有!开头的问题）

```json
{
	"FAQ": [
		{
			"qun": "群号（global代表所有群生效）",
			"问题关键字":"解答"
		},
        {
			"qun": "群号（global代表所有群生效）",
			"问题关键字":"解答"
		}
    ]
}    
```

### [modules.json](config/modules.json)模块开关

```json
{
	"enable_banlist": "true",
	"enable_botmanager": "true",
	"enable_testop": "true",
	"enable_whitelist": "true"
}
```

|  Key   | Value  |
|  :----:  | :----:  |
| enableBanlist | 黑名单开关 |
| enableBotmanager | 假人管理开关 |
| enableTestop | 测试服权限开关 |
| enableWhitelist | 白名单开关 |

## 机器人指令详解

### 玩家群部分


#### 白名单

|  命令   | 解释  |
|  :----:  | :----:  |
| !白名单 玩家名 | 申请白名单（该操作需要管理组同意后生效） |
| !解绑 玩家名 | 解除与该玩家的绑定 |
| !改名 玩家名 | 更改绑定的玩家名（同时删除之前名字的白名单并尝试踢出服务器） |

#### 多服务器玩家查询

|  命令   | 解释  |
|  :----:  | :----:  |
| !服务器 或 !在线 或 !人数 或 !server | 查询在线玩家 |

#### 黑名单查询

|  命令   | 解释  |
|  :----:  | :----:  |
| !黑名单 | 查询被封禁的玩家 |

### 管理组部分


#### 白名单审核（这里的审核ID不是玩家ID）

|  命令   | 解释  |
|  :----:  | :----:  |
| !白名单 通过 审核ID | 通过该审核ID的白名单申请 |
| !白名单 拒绝 审核ID [可选：原因] | 拒绝该审核ID的白名单申请（该操作会导致无法重新申请白名单） |
| !白名单 全部通过 | 通过所有待审核玩家 |

#### 审核查询

|  命令   | 解释  |
|  :----:  | :----:  |
| !查询 | 查询所有待审核ID |
| !查询 通过 | 查询所有已通过ID |
| !查询 拒绝 | 清空所有已拒绝ID |
| !查询 清空 | 清空所有待审核ID |

#### 黑名单

|  命令   | 解释  |
|  :----:  | :----:  |
| !ban 添加 玩家ID | 将该玩家加入黑名单 |
| !ban 移除 | 将该玩家移出黑名单 |

## 使用的SDK
[YiriMirai](https://github.com/YiriMiraiProject/YiriMirai)
