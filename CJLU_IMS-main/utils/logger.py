import logging
import os
import sys
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 全局 logger 单例
logger = logging.getLogger("app")
if logger.handlers:  # 防止重复
    pass
else:
    logger.setLevel(logging.DEBUG)  # 默认全开

    # 控制台 + 文件 两个 handler
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
    )

    console = logging.StreamHandler(sys.stdout)
    file_hdl = logging.FileHandler(
        os.path.join(LOG_DIR, f"{datetime.now():%Y-%m-%d}.log"), encoding="utf-8"
    )
    for h in (console, file_hdl):
        h.setFormatter(fmt)
        logger.addHandler(h)


# 动态开关 API
def set_log_level(level: str | int):
    """
    立即全局生效
    level: "DEBUG"/"INFO"/"WARNING"/"ERROR"/"CRITICAL" 或其对应 int
    """
    logger.setLevel(level)


raw = os.getenv("LOG_LEVEL", "DEBUG").upper()
level = int(raw) if raw.isdigit() else getattr(logging, raw, logging.INFO)
set_log_level(level)

if __name__ == "__main__":
    logger.debug("test")
    logger.info("info")
