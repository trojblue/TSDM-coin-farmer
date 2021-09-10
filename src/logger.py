import logging
from logging.handlers import RotatingFileHandler


# 最大存储30m的log, 先试着以后改
FILE_SIZE = 10*1024*1024
FILE_COUNT = 3


def set_logger():
    """设置log格式
    """
    logger = logging.getLogger('farmer')
    logger.setLevel(logging.INFO)

    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    logHandler = RotatingFileHandler('farmer.log', maxBytes=FILE_SIZE, backupCount=FILE_COUNT, encoding='UTF-8')

    logHandler.setFormatter(log_formatter)
    logHandler.setLevel(logging.INFO)
    logger.addHandler(logHandler)
    logger.info("farmer.py: 开始运行")



def heartbeat():
    """定时心跳来确认进程存活
    """
    logger = logging.getLogger('farmer')
    logger.debug("heartbeat")


def display_info(info_str:str):
    """同时打印和输出到log一行信息
    """
    logger = logging.getLogger('farmer')
    print(info_str)
    logger.info(info_str)

def add_debug(debug_str:str):
    """同时输出到log一行debug
    """
    logger = logging.getLogger('farmer')
    logger.debug(debug_str)

def display_warning(warn_str:str):
    """同时打印和输出到log一行警告
    """
    logger = logging.getLogger('farmer')
    print(warn_str)
    logger.warning(warn_str)

def display_error(error_str:str):
    """同时打印和输出到log一行错误
    """
    logger = logging.getLogger('farmer')
    print(error_str)
    logger.error(error_str)