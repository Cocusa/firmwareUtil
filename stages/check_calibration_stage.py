import logging
from typing import Tuple
from stages.stageing_functions import get_failed_info
from models.technical_control_model import (
    ControlContext,
    Status,
    StatusError,
)


def check_calibration_stage(context: ControlContext) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None

    logging.info("Проверка калибровки прибора")
    test_message = context.device.get_test_device_result()

    test_message = bytes(test_message, encoding="latin_1").decode("cp1251")

    if test_message != "No failures":
        status, error = get_failed_info(
            f"Прибор не прошёл заводскую калибровку. {test_message}",
            "123.",
        )
    else:
        logging.info("Прибор прошел заводскую калибровку")

    return status, error
