import logging
from typing import Tuple
from services import device_registry
from services.config_service import get_config
from stages.stageing_functions import get_failed_info
from models.technical_control_model import (
    ControlContext,
    Status,
    StatusError,
)


def check_context_stage(context: ControlContext) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None

    if context.db_context.serial_number != context.device_context.serialNumber:
        return get_failed_info(
            "Серийный номер на этикетке не совпадает с серийным номером зашитым в прибор.",
            "123.",
        )

    context.register_context = device_registry.get_register_context(
        context.db_context.nomenclature, context.device_context.model
    )
    logging.info(f"Информация из реестра- {context.register_context}")

    if context.register_context is None:
        return get_failed_info(
            "Подключенный прибор НЕ соответствует номенклатуре в заказе.",
            "123.",
        )
    
    logging.info(f"Информация в ERP совпадает с информацией в приборе.")

    context.config = get_config()

    return status, error
