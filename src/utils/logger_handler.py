import datetime
import logging
import os
from unittest.mock import DEFAULT
from venv import logger
from utils.path_tool import get_abs_path

#日志保存根目录
LOG_ROOT = get_abs_path('logs')

#确保日志目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

#日志的格式配置
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

def get_logger(
        name: str = "agent",
        console_level=logging.INFO, #控制台日志级别，默认为INFO
        file_level=logging.DEBUG,   #文件日志级别，默认为DEBUG
        log_file: str = None,
) -> logging.Logger:
    logger = logging.getLogger(name)    #实例化一个logger对象，参数name指定了logger的名称，通常使用模块名或功能名来区分不同的logger
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别为DEBUG，确保所有日志都被处理

    if logger.hasHandlers():
        return logger  # 清除已有的处理器，避免重复日志
    #控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    #文件处理器
    if log_file is None:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.datetime.now().strftime('%Y-%m-%d')}.log")  #配置默认日志文件路径，格式为logs/agent_2025-04-17.log
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)

    return logger

#快捷获取
logger = get_logger()


if __name__ == "__main__":
    logger.info("这是一个测试日志")
    logger.debug("这是一个调试日志")
    logger.error("这是一个错误日志")