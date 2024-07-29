from pathlib import Path
import csv
from urllib.parse import urlparse
from models.models import (
    PID,
    VID,
    CommonException,
    IsCheckVnapt,
    Localization,
    LocalizationMode,
    Nomenclature,
    RegisterContext,
    RegisterLicense,
    RegisterVersion,
    Software,
)

FILE = ".\\config\\vna_registry.csv"
NOMENCLATURE_NAME = "Номенклатура"
COPY_FILES_NAME = "папка для записи на флешку"
SOFTWARE = "Совместимое ПО"
DEVICE_NAME = "Наименование модели в SCPI"
FIRMWARE_VERSION = 'значение бита "вариант исполнения"'
LICENSE_INFO = "предусмотрена ли генерация лицензий"
LOCALIZATION_MODE = "локализация"
VID_ROW = "VID"
PID_ROW = "PID[15]"
VNAPT_ROW = "VNAPT"

FILES_NOT_AVAILABLE = "N/A"
GENERAL_FILE_PATH = "url"


def is_url(path):
    return urlparse(path).scheme in ['http', 'https']

def __handle_url(url):
    return url

def __handle_file_name(file_name):
    if(file_name == FILES_NOT_AVAILABLE):
        return file_name
    
    paths = list(Path(GENERAL_FILE_PATH).glob(f"{file_name}*"))

    if len(paths) < 1:
        raise CommonException(f"Не найдена директория {GENERAL_FILE_PATH + file_name}")

    if len(paths) > 1:
        raise CommonException(f"Найдено несколько директорий {GENERAL_FILE_PATH + file_name}")

    return str(paths[0])

def get_file_location(file_location) -> str:
    if is_url(file_location):
        return __handle_url(file_location)
    else:
        return __handle_file_name(file_location)


def get_software_type(nomenclature: Nomenclature) -> Software:
    with open(FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        nomenclature_name = nomenclature.name.strip()
        for row in reader:
            if row[NOMENCLATURE_NAME].strip() == nomenclature_name:
                return Software(row[SOFTWARE])

    return None


def get_register_context(
    nomenclature: Nomenclature, device_name: str
) -> RegisterContext:
    with open(FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        nomenclature_name = nomenclature.name.strip()
        for row in reader:
            if (
                row[NOMENCLATURE_NAME].strip() == nomenclature_name
                and row[DEVICE_NAME] == device_name
            ):
                return RegisterContext(
                    license_info=RegisterLicense(row[LICENSE_INFO]),
                    device_name=str(row[DEVICE_NAME]),
                    location_setup_files=get_file_location(row[COPY_FILES_NAME]),
                    firmware_version=RegisterVersion(row[FIRMWARE_VERSION]),
                    localization=Localization(LocalizationMode(row[LOCALIZATION_MODE]), VID(row[VID_ROW]), PID(row[PID_ROW])),
                    is_check_vnapt=IsCheckVnapt(row[VNAPT_ROW])
                )
    return None


def get_nomenclature_names() -> list[str]:
    nomanclature_names = []
    with open(FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        
        for row in reader:
            nomanclature_names.append(row[NOMENCLATURE_NAME].strip())

    return nomanclature_names
