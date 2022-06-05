
import sys
import logging
from logging import handlers
import datetime
import os

# 日志级别关系映射
level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}


logs = os.path.join('logs')
if not os.path.exists(logs):
    os.makedirs(logs)


def outputlog(filename, level="info"):
    # 创建日志对象
    log = logging.getLogger(filename)
    # 设置日志级别
    log.setLevel(level_relations.get(level))
    # 日志输出格式
    fmt = logging.Formatter('[{time}] - %(levelname)s: %(message)s'.format(time=datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')))
    # 输出到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(fmt)
    # 输出到文件
    file_handler = handlers.TimedRotatingFileHandler(filename=filename, when='D', encoding='utf-8')
    file_handler.setFormatter(fmt)
    log.addHandler(console_handler)
    log.addHandler(file_handler)
    return log


# 明确指定日志输出的文件路径和日志级别
log = outputlog('./logs/output.log', 'debug')