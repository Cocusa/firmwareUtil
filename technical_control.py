import traceback
from typing import Callable

from requests import RequestException
from models.models import CommonException
from services.enviroment_helper import get_executable_path
from services.device_software import SoftwareError
from services.ERP_api import ERPApi
from services.license_generator_api import LicenseError
from services.logger_configurations import configure_proccess_log
from services.win_helper import get_version_number
from stages.license_feature_stage import license_features_stage
from stages.check_calibration_stage import check_calibration_stage
from stages.check_context_stage import check_context_stage
from stages.check_vnapt_stage import check_vnapt_stage
from stages.copy_files_stage import copy_files_stage
from stages.device_stage import device_stage
from stages.firmware_stage import firmware_stage
from stages.erp_stage import erp_order_stage, erp_sn_stage
from stages.license_stage import license_stage
from stages.save_dump_stage import save_dump_stage
import logging
from models.technical_control_model import (
    ControlContext,
    ControlInfo,
    Stage,
    Status,
    StatusError,
)


def start_technical_control(
    serial_number: str, ui_react: Callable[[ControlInfo], None], erp_api: ERPApi, main_window
):
    try:
        control = ControlInfo()
        context = ControlContext()
        context.main_window = main_window
        context.erp_api = erp_api
        util_version = get_version_number(get_executable_path())
        user = context.erp_api.get_current_user()

        configure_proccess_log(serial_number, user, util_version)

        logging.info(
            f"Старт ОТК, пользователь - {user}, серийный номер - {serial_number}, версия утилиты - {util_version}"
        )

        done = False
        while not done:
            ui_react(control)

            match control.stage:
                case Stage.ERPSn:
                    control.status, control.error = erp_sn_stage(
                        context, serial_number
                    )
                case Stage.ERPOrder:
                    control.status, control.error = erp_order_stage(
                        context, serial_number
                    )
                case Stage.Device:
                    control.status, control.error = device_stage(context)
                case Stage.CheckContext:
                    control.status, control.error = check_context_stage(context)
                case Stage.CheckCalibration:
                    control.status, control.error = check_calibration_stage(context)
                case Stage.CheckVnapn:
                    control.status, control.error = check_vnapt_stage(context)
                case Stage.Firmware:
                    control.status, control.error = firmware_stage(context)
                case Stage.LoadLicense:
                    control.status, control.error = license_stage(context)
                case Stage.LoadFeature:
                    control.status, control.error = license_features_stage(context)
                case Stage.CopyFiles:
                    control.status, control.error = copy_files_stage(context)
                case Stage.SaveDump:
                    control.status, control.error = save_dump_stage(context)
                case Stage.SaveReport:
                    control.status, control.error = Status.Success, None
                    ui_react(control)
                    done = True
                    break

            ui_react(control)
            if control.status == Status.Failed:
                logging.error(f"Стадия - {control}")
                break
            next_stage(control)

    except (SoftwareError, LicenseError) as ex:
        control.status = Status.Failed
        control.error = StatusError(str(ex))
        ui_react(control)
        logging.error(f"Стадия - {control}, Ошибка - {str(ex)} \n {traceback.format_exc()}")
    except (RequestException, ConnectionError) as ex:
        control.status = Status.Failed
        control.error = StatusError("Ошибка сети.")
        ui_react(control)
        logging.error(f"Стадия - {control}, Ошибка - {str(ex)} \n {traceback.format_exc()}")
    except CommonException as ex:
        control.status = Status.Failed
        control.error = StatusError(f"Ошибка. {str(ex)}")
        ui_react(control)
        logging.error(f"Стадия - {control}, Ошибка - {str(ex)} \n {traceback.format_exc()}")
    except Exception as ex:
        control.status = Status.Failed
        control.error = StatusError(
            "Критическая ошибка приложения.",
            "Обратитесь в отдел разработчиков ERP.",
        )
        ui_react(control)
        logging.critical(f"Стадия - {control}, Ошибка - {str(ex)} \n {traceback.format_exc()}")

    finally:
        context = None


def next_stage(control_info: ControlInfo):
    control_info.error = None
    control_info.stage = Stage(control_info.stage.value + 1)
    control_info.status = Status.InProgress