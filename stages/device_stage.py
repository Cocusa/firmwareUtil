import logging
from typing import Tuple
from stages.stageing_functions import get_failed_info
from models.technical_control_model import (
    ControlContext,
    Status,
    StatusError,
)
from services.device_software import (
    DeviceCommunicator,
    DeviceCommunicator,
    soft_names,
)


def device_stage(context: ControlContext) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None
    logging.info(
        f"Запуск приложения - { soft_names[context.db_context.software] }"
    )
    try:
        device = DeviceCommunicator(context.db_context.software)
    except Exception as ex:
        logging.error(ex)
        return get_failed_info(
            "",
            "",
        )

    logging.info("Получение данных с прибора.")
    device_context = device.get_device_context()

    logging.info(f"Полученные данные с прибора - {str(device_context)}")

    context.device = device
    context.device_context = device_context

    return status, error
