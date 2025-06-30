import logging
import os
from logging.handlers import TimedRotatingFileHandler
import time

# 日志保存路径
path_base = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(path_base, "testlog")
if not os.path.exists(path):
    os.makedirs(path)
def log():
    logger = logging.getLogger("test")

    # 避免重复添加 handler（否则会重复写入 + 锁死文件）
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)
    format1 = logging.Formatter("日志:%(asctime)s - 级别:%(levelname)s - %(message)s")

    # 控制台输出
    sh = logging.StreamHandler()
    sh.setFormatter(format1)
    logger.addHandler(sh)

    # 文件日志处理器（加 delay 避免文件锁，轮转安全）
    log_file = os.path.join(path, "log.log")
    fh = TimedRotatingFileHandler(
        filename=log_file,
        when='S',
        interval=5,              # 每 5 秒轮转一次（建议别用1秒，太频繁）
        backupCount=5,
        encoding='utf-8',
        delay=True               # ✅ 延迟打开文件，避免 WinError 32
    )
    fh.suffix = "%Y-%m-%d-%H-%M-%S"
    fh.setFormatter(format1)
    logger.addHandler(fh)
    return logger

# 单例 logger
logger = log()

if __name__ == '__main__':
    logger.info("我是info")
    logger.debug("debug")
    logger.error("error")
    logger.warning("warning")
    logger.critical("critical")
    # for i in range(6):
    #     logger.debug("我是 %d", i)
    #     time.sleep(1)
