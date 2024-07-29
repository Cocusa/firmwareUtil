import os
import ctypes
from ctypes import wintypes
import win32api
import win32file
from win32api import *

#stackoverflow code
class _SHFILEOPSTRUCTW(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("wFunc", wintypes.UINT),
        ("pFrom", wintypes.LPCWSTR),
        ("pTo", wintypes.LPCWSTR),
        ("fFlags", ctypes.c_uint),
        ("fAnyOperationsAborted", wintypes.BOOL),
        ("hNameMappings", ctypes.c_uint),
        ("lpszProgressTitle", wintypes.LPCWSTR),
    ]

#stackoverflow code
def win_shell_copy(soursec: list[str], dst: str):
    """
    :param str src: Source path to copy from. Must exist!
    :param str dst: Destination path to copy to. Will be created on demand.
    :return: Success of the operation. False means is was aborted!
    :rtype: bool
    """
    for src in soursec:
        if not os.path.exists(src):
            print('No such source "%s"' % src)
            return False

    sources_string = "\0".join(path for path in soursec)

    dst = dst.replace("/", "\\")

    if not os.path.exists(dst):
        print('No such source "%s"' % dst)
        return False

    src_buffer = ctypes.create_unicode_buffer(sources_string, len(sources_string) + 2)
    dst_buffer = ctypes.create_unicode_buffer(dst, len(dst) + 2)

    fileop = _SHFILEOPSTRUCTW()
    fileop.hwnd = 0
    fileop.wFunc = 2  # FO_COPY
    fileop.pFrom = wintypes.LPCWSTR(ctypes.addressof(src_buffer))
    fileop.pTo = wintypes.LPCWSTR(ctypes.addressof(dst_buffer))
    fileop.fFlags = 512  # FOF_NOCONFIRMMKDIR
    fileop.fAnyOperationsAborted = 0
    fileop.hNameMappings = 0
    fileop.lpszProgressTitle = None

    result = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(fileop))
    return not result


def get_flash_drives_path() -> str:
    drives = win32api.GetLogicalDriveStrings().split("\x00")[:-1]

    flash_drives = []

    for device in drives:
        if win32file.GetDriveType(device) == win32file.DRIVE_REMOVABLE:
            flash_drives.insert(-1, device)

    return flash_drives


def has_hidden_attribute(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    return result


def get_version_number(file_path):  
    File_information = GetFileVersionInfo(file_path, "\\")
  
    ms_file_version = File_information['FileVersionMS']
    ls_file_version = File_information['FileVersionLS']
  
    return [str(HIWORD(ms_file_version)), str(LOWORD(ms_file_version)),
            str(HIWORD(ls_file_version)), str(LOWORD(ls_file_version))]

