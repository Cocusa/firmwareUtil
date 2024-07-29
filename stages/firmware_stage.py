import datetime
import logging
import os
from typing import Tuple
from models.models import (
    FirmwareVersion,
    ERPContext,
    RegisterContext,
    RegisterVersion,
)
from services.enviroment_helper import get_backup_before_firmware_path
from stages.localization_vid_pid import localize_vid_pid
from stages.stageing_functions import get_failed_info
from models.technical_control_model import (
    ControlContext,
    Status,
    StatusError,
)
from services.device_software import (
    DeviceCommunicator,
)


def firmware_stage(context: ControlContext) -> Tuple[Status, StatusError]:
    path = get_backup_before_firmware_path()
    path = os.path.join(path, 
                        f"backup_{context.db_context.serial_number}_{context.db_context.user_name}_{datetime.datetime.now().strftime('%d-%m-%Y %I-%M%S')}")    

    logging.info(f"Сохранение дампа '{path}'")
    context.device.save_backup(path)

    device_error = context.device.get_error()
    if context.device.get_no_error_text() not in device_error:
        logging.error(f"Ошибка сохранения дампа - {device_error}")
        return get_failed_info(
            f"",
            "",
        )
    else:
        logging.info(f"Дамп сохранен")

    status, error = configure_device_version(
        context.db_context, context.device, context.register_context
    )

    if(status == Status.Failed):
        return status, error

    status, error = localize_vid_pid(context)

    return status, error


def configure_device_version(
    db_context: ERPContext, device: DeviceCommunicator, register: RegisterContext
) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None    

    return status, error
