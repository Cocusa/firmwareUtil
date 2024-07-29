import datetime
import logging
import os
from services.enviroment_helper import get_executable_path, get_log_path
from services.win_helper import get_version_number


def configure_proccess_log(serial_number: str, user: str):    
    log_path = get_log_path()
    
    filename = os.path.join(
        log_path,
        f"{serial_number},{datetime.datetime.now().strftime('%d-%m-%Y %I-%M-%S')},{user}.log",
    )
    
    logging.basicConfig(
        level=logging.DEBUG,
        filename=filename,
        format="%(asctime)s %(levelname)s:%(message)s",
        force=True,
    )   


def configure_init_log():
    log_path = get_log_path()
    logging.basicConfig(
        level=logging.DEBUG,
        filename=os.path.join(log_path, "app_init.log"),
        format="%(asctime)s %(levelname)s:%(message)s",
    )