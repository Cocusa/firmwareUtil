from dataclasses import dataclass, field
from enum import Enum
from models.config_models import Config
from models.models import DeviceContext, ERPContext, File, RegisterContext
from services.device_software import DeviceCommunicator
from services.ERP_api import ERPApi
from services.license_generator_api import FileLicenseApi
import tkinter as tk

class Stage(Enum):
    ERPSn = 0
    ERPOrder = 1
    Device = 2
    CheckContext = 3
    CheckCalibration = 4
    CheckVnapn = 5
    Firmware = 6
    LoadLicense = 7
    CopyFiles = 8
    LoadFeature = 9
    SaveDump = 10
    SaveReport = 11


class Status(Enum):
    Success = 0
    InProgress = 1
    Failed = 2


@dataclass
class StatusError:
    text: str = ""
    hint: str = ""


@dataclass
class ControlInfo:
    stage: Stage = Stage(0)
    status: Status = Status.InProgress
    error: StatusError = None


@dataclass
class ControlContext:
    db_context: ERPContext = None
    device_context: DeviceContext = None
    license: File = None
    afr_files: list[File] = None
    register_context: RegisterContext = None
    device: DeviceCommunicator = None
    erp_api: ERPApi = None
    license_generator_api: FileLicenseApi = None
    config: Config = None
    main_window: tk.Tk = None
