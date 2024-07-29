import logging
from typing import Tuple
from models.models import IsCheckVnapt
from stages.stageing_functions import get_failed_info
from models.technical_control_model import (
    ControlContext,
    Status,
    StatusError,
)


def check_vnapt_stage(context: ControlContext) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None

    if context.register_context.is_check_vnapt is IsCheckVnapt.NoCheck:
        logging.info("Проверка файла VNAPT не требуется согласно реестру.")
        return status, error

    logging.info("Проверка наличия привязанного файла VNAPT.")

    vnapt_file = context.erp_api.get_vnapt_file_name(context.db_context.serial_number)
    if vnapt_file is None:
        status, error = get_failed_info(
            "Отсутствует протокол VNAPT на подключенный прибор.", "123"
        )

    logging.info(f"Найден файл VNAPT - {vnapt_file}.")

    return status, error
