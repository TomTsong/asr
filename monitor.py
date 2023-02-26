import logging.config
import psutil
import time

from collection import MonitorCollection

import log_config

logging.config.dictConfig(log_config.logging_dict_config)
logger = logging.getLogger()


def check():
    mem = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disk = psutil.disk_usage("/").percent
    info = {
        "mem": mem,
        "cpu": cpu,
        "disk": disk,
    }
    logger.info(f"{info}")
    MonitorCollection.insert_one(info)


def run():
    while True:
        check()
        time.sleep(5)


if __name__ == "__main__":
    run()
