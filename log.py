import logging
from logging.handlers import SysLogHandler


def log(msg: str, lvl: str, extra=None):
    file_name = "[Main.py]"
    print(f"{file_name}: [{lvl}]\t{msg}")
    return True
    logger = logging.getLogger()
    logger.addHandler(SysLogHandler("/dev/log"))
    logger.addHandler(logging.FileHandler("nginx-main.log"))

    lvl = lvl.upper()

    if lvl == "NOTSET":
        pass
        # logger.info(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "DEBUG":
        logger.debug(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "INFO":
        logger.info(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "WARNING":
        logger.warning(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "ERROR":
        logger.error(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "CRITICAL":
        logger.critical(f"{file_name}: [{lvl}]\t {msg}")

    else:
        logger.error("Not Working")
