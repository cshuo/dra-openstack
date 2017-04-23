# -*- coding:utf8 -*-

import logging

loggers = {}

def draLogger(name):
    global loggers
    if loggers.get(name):
        return loggers.get(name)
    else:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        ch =logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        fmt = "%(asctime)-15s %(levelname)s %(name)s [%(filename)s:%(lineno)d] - %(message)s"
        datefmt = "%a %d %b %Y %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        loggers.update(dict(name=logger))
        return logger


def init_logger():
    # 创建一个logger
    logger = logging.getLogger('DRA')
    logger.setLevel(logging.DEBUG)
    
    # 创建一个handler，用于写入日志文件
    # fh = logging.FileHandler('test.log')
    # fh.setLevel(logging.DEBUG)
    
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    # 定义handler的输出格式
    # fh.setFormatter(formatter)
    fmt = "%(asctime)-15s %(levelname)s %(name)s [%(filename)s:%(lineno)d] - %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)
    ch.setFormatter(formatter)
    
    # 给logger添加handler
    logger.addHandler(ch)
