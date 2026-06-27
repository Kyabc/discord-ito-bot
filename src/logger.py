import logging
import logging.handlers
import os
from datetime import datetime

from src.settings import settings


def set_logger():
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    logger = logging.getLogger()

    now = datetime.now()

    streamHandler = logging.StreamHandler()
    fileHandler = logging.handlers.RotatingFileHandler(
        f"./{settings.LOG_DIR}/{now.strftime('%Y-%m-%d')}.log",
        maxBytes=1000000,
        backupCount=5,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        '%(asctime)s| %(levelname)-5s | %(name)s.%(funcName)s.%(lineno)d | %(message)s'
    )

    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.INFO)
    fileHandler.setLevel(logging.DEBUG)

    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)

    return logger
