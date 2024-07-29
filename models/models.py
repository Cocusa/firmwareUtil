from dataclasses import dataclass
from datetime import date
from enum import Enum


class Software(Enum):
    SOFT1 = "SOFT1"


class RegisterVersion(Enum):
    VER1 = "VER1"


class RegisterLicense(Enum):
    LICENSED = "123"
    NOT_LICENSED = "123"


class FirmwareVersion(Enum):
    VER1 = 1


class LicenseInfo(Enum):
    NO = 1
    YES = 2


class LocalizationMode(Enum):
    NO_CHECK_NO_WRITE = "123"
    CHECK = "123"
    WRITE = "123"


class VID(Enum):
    VID1 = "123"


class DeviceVID(Enum):
    DeviceVid1 = "123"


class PID(Enum):
    PID1 = "123" 


class IsCheckVnapt(Enum):
    Check = "123"
    NoCheck = "123"


@dataclass
class Localization:
    mode: LocalizationMode
    vid: VID
    pid: PID


@dataclass
class RegisterContext:
    license_info: RegisterLicense
    device_name: str
    location_setup_files: str
    firmware_version: RegisterVersion
    localization: Localization
    is_check_vnapt: IsCheckVnapt


@dataclass
class Nomenclature:
    id: int
    name: str


@dataclass
class OrderInfo:
    number: str
    date: date
    nomenclature: Nomenclature
    is_need_license: LicenseInfo
    virmware_version: FirmwareVersion


@dataclass
class ERPContext:
    order_info: OrderInfo = None
    nomenclature: Nomenclature = None
    software: Software = None
    is_vnapt: bool = False
    serial_number: str = ""
    user_name: str = ""


@dataclass
class DeviceContext:
    manufacturer: str
    model: str
    serialNumber: str
    version: str


class CommonException(Exception):
    pass