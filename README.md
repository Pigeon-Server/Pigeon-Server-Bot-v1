# Pigeon Server Bot
A mirai plugin for remotely executing minecraft commands.

Pigeon Server · 气人姬部分功能实现，Minecraft服务器执行部分使用RCON


## 已实现功能
- 白名单申请
- 多服务器状态查询
- 分群问答
- 版本更新提示
## 待实现功能
- 多账户
- 多服务器
- 开黑啦同步
- 群文件自动分类
- 测试服权限申请
- 假人登记/自动踢出未登记假人

## 配置文件详解

### 机器人本体
|  Key   | Value  |
|  :----:  | :----:  |
| QQ  | 机器人的QQ号（int） |
| admin_qun  | 管理员群群号（int） |
| player_qun  | 玩家群群号（int） |
| post  | mirai-api-http HTTP端口（int） |
| hostname  | mirai-api-http HTTP地址（str） |

### 数据库（DB）
|  Key   | Value  |
|  :----:  | :----:  |
| db_host  | 数据库地址（str） |
| db_user  | 数据库用户（str） |
| db_password  | 数据库密码（str） |
| database  | 数据库库名（str） |

### 问答模块（FAQ）
|  Key   | Value  |
|  :----:  | :----:  |
| qun  | 启用的群号（global代表所有群生效） |
| F  | 问题 |
| Q  | 答案 |

### 版本检查（Check-Minecraft-Version）
|  Key   | Value  |
|  :----:  | :----:  |
| release  | 发行版本存储 |
| snapshot  | 快照版本存储 |

## 使用的SDK
[YiriMirai](https://github.com/YiriMiraiProject/YiriMirai)
