import logging
from typing import Tuple
from models.config_models import Feature
from services.bitrix_api import download_feature
from services.license_generator_api import FileLicenseApi
from services.win_helper import get_flash_drives_path
from models.technical_control_model import ControlContext, Status, StatusError


def license_features_stage(context: ControlContext) -> Tuple[Status, StatusError]:
    status = Status.Success
    error = None    

    if(not context.license):
        logging.info("")
        return status, error
    
    flash_path = get_flash_drives_path()[0]

    for feature in context.config.license_features:
        if(not __is_feature_licensed(context.db_context.serial_number, feature)):
            logging.info(f"")
            continue
        
        download_feature(feature, flash_path)
        logging.info(f"")

    return status, error

def __is_feature_licensed(serial_number: str, feature: Feature):
    api = FileLicenseApi()
    return api.is_include_feature(serial_number, feature)