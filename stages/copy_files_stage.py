import logging
import os
from typing import Tuple
from models.models import File
from services.device_registry import FILES_NOT_AVAILABLE
from services.enviroment_helper import add_afr_dictionary
from services.load_files import copy_setup_files, save_file
from services.win_helper import get_flash_drives_path, has_hidden_attribute
from stages.stageing_functions import get_failed_info
from models.technical_control_model import (
    ControlContext,
    Status,
    StatusError,
)


def __is_dir_empty(dst_path: str):
    dirs = os.listdir(dst_path)
    not_hidden_dirs = list(
        filter(lambda x: not has_hidden_attribute(os.path.join(dst_path, x)), dirs)
    )
    return len(not_hidden_dirs) == 0


def __is_files_not_available(context: ControlContext) -> bool:
    return context.register_context.location_setup_files == FILES_NOT_AVAILABLE       


def copy_files_stage(context: ControlContext) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None

    if(__is_files_not_available(context)):
       logging.info(f"Файлы не были с копированы так как временно не поддерживаются")
       return status, error

    flash_drives_path = get_flash_drives_path()

    logging.info(f"Полученные пути до flash-дисков: {flash_drives_path}")

    if len(flash_drives_path) > 1:
        return get_failed_info("Подключено более одного flash-диска.")
    elif len(flash_drives_path) < 1:
        return get_failed_info("Не обнаружен flash-диск.")

    dst_path = flash_drives_path[0]

    if not __is_dir_empty(dst_path):
        return get_failed_info(
            "Flash-диск не пустой.", f"Необходимо очистить {dst_path}"
        )

    copy_setup_files(context.register_context.location_setup_files, dst_path)
    logging.info(f"Файлы установки и документации, находящися по пути - '{context.register_context.location_setup_files}', загружены по пути - '{dst_path}'")

    if context.license:
        save_file(context.license, dst_path)
        logging.info(f"Файл лицензий загружен по пути - {dst_path}")

    return status, error
