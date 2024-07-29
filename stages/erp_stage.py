import logging
from typing import Tuple
from models.models import CommonException, ERPContext, Nomenclature
from services import check_functions, device_registry
from stages.stageing_functions import get_failed_info
from services.device_registry import get_nomenclature_names
from services.ERP_api import ERPApi
from ui.select_table_ui import TableWindow
import ttkbootstrap as ttk
# from ui.app import MainWindow
from models.technical_control_model import (
    ControlContext,
    Status,
    StatusError,
)

def select_nomenclature(parent, nomenclatures: list[Nomenclature]) -> Nomenclature:
    if(not nomenclatures or len(nomenclatures) == 0):
        raise CommonException("Не найдена номенклатура")
    
    if(len(nomenclatures) > 1):
        objects = nomenclatures
        fields = ["name"]
        table_window = TableWindow(parent, objects, fields, ['Номенклатура'], 'Выберите номенклатуру')
        table_window.grab_set()
        table_window.wait_window()
        selected_obj = table_window.selected_obj
        if(selected_obj == None):
            raise CommonException("Не выбрана номенклатура")
        return selected_obj
    else:
        return nomenclatures[0]

def _find_nomenclature(erp_api: ERPApi, nomenclature: Nomenclature):        
        register_nomenclature_names = get_nomenclature_names()
        nomenclatures = []

        if(nomenclature.name.strip() not in register_nomenclature_names):
            logging.info("Номенклатура в заказе отсутсвует в реестре. Поиск по дереву номенклатуры.")
            bom_id = erp_api.get_bom_id(nomenclature.id)
            bom_tree = erp_api.get_bom_tree(bom_id)

            for bom in bom_tree:
                if bom['nomName'].strip() in register_nomenclature_names:
                    nomenclatures.append(Nomenclature(bom['nomId'], bom['nomName'].strip()))
        else:
            logging.info("")
            nomenclatures.append(nomenclature)

        return nomenclatures


def _set_erp_context(
    context: ControlContext, serial_number: str
) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None

    orders_info = context.erp_api.get_order_info(serial_number)

    if orders_info is not None and len(orders_info) > 1:
        return get_failed_info(
            "Для данного серийного номера существует несколько заказов.",
            "",
        )

    if orders_info is None or not check_functions.is_serial_number_exists(
        orders_info[0]
    ):
        return get_failed_info("Не найдена информация по серийному номеру")

    db_context = ERPContext(
        order_info=orders_info[0],
        is_vnapt=context.erp_api.get_vnapt_file_name(serial_number),
        serial_number=serial_number,
        user_name=context.erp_api.get_current_user(),
    )

    context.db_context = db_context

    return status, error


def erp_order_stage(
    context: ControlContext, serial_number: str
) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None

    logging.info(
        f""
    )
    status, error = _set_erp_context(context, serial_number)
    if status == Status.Failed:
        return status, error

    logging.info(f"Полученная информация - {context.db_context}")

    if (
        context.db_context is not None
        and context.db_context.order_info is not None
        and context.db_context.order_info.nomenclature is not None
    ):
        nomenclatures = _find_nomenclature(context.erp_api, context.db_context.order_info.nomenclature)
        logging.info(f"Найденные номенклатуры в реестре - {nomenclatures}")
        
        nomenclature = select_nomenclature(context.main_window, nomenclatures)
        logging.info(f"Полученная номенклатура - {nomenclature}")
                
        context.db_context.nomenclature = nomenclature        
        context.db_context.software = device_registry.get_software_type(
            nomenclature
        )

    if not check_functions.is_software_exists(context.db_context):
        status, error = get_failed_info(
            "Отсутствует программное обеспечение работающее с данным устройством"
        )

    return status, error


def erp_sn_stage(
    context: ControlContext, serial_number: str
) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None

    nomenclature = context.erp_api.get_nomenclature(serial_number)
    logging.info(f"Полученная номенклатура - {nomenclature}")

    if nomenclature is None:
        status, error = get_failed_info(
            "", ""
        )

    return status, error
