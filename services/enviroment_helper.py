import json
import os
from typing import Tuple


user_config_path = os.path.join(os.environ["LOCALAPPDATA"], "123/123.json")


def get_remote_or_local_path(dictionary_name: str) -> str:
    remote_path = os.path.join("path", dictionary_name)
    if os.path.exists(remote_path):
        return remote_path
    else:
        return os.path.join(".\\", dictionary_name)


def save_users_auth(login: str, password: str):
    os.makedirs(os.path.dirname(user_config_path), exist_ok=True)

    with open(user_config_path, "w") as f:
        f.write(json.dumps({"login": login, "password": password}))


def get_user_auth() -> Tuple[str, str]:
    if os.path.exists(user_config_path):
        data = {}
        with open(user_config_path, "r") as f:
            data = f.read()

        deserialized = dict(json.loads(data))

        return deserialized["login"], deserialized["password"]
    return "", ""


def get_backup_path() -> str:
    return get_remote_or_local_path("backups")


def get_backup_before_firmware_path() -> str:
    return get_remote_or_local_path("backups-before-firmware")


def get_log_path() -> str:
    return get_remote_or_local_path("logs")
    

def get_executable_path():
    return '.\\soft.exe'
