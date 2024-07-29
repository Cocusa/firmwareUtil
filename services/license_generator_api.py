import requests
from hashlib import sha256
import json
from models.config_models import Feature


class FileLicenseApi:
    def __init__(self):
        USER_NAME = "123"
        PASSWORD = "123"
        LOGIN_DATA = {
            "userName": USER_NAME,
            "password": sha256(PASSWORD.encode("utf-8")).hexdigest(),
        }
        self.url = "utl"
        self.__session = requests.Session()
        self.__session.post(f"{self.url}", json=LOGIN_DATA)

    def _get_device_info(self, serialNumber):
        r = self.__session.get(
            f"{self.url}", params={"serialNumber": serialNumber}
        )
        if r.status_code == 200:
            response_dict = json.loads(r.content)
            if len(response_dict) < 1:
                return None

            if len(response_dict) > 1:
                raise LicenseError(
                    "Ошибка загрузки файла лицензий. По серийному номеру было найдено несколько приборов."
                )

            return response_dict[0]
        else:
            raise LicenseError("Ошибка получения данный с сервера лицензий")
    
    def get_device_id(self, serialNumber) -> int:
        device_info = self._get_device_info(serialNumber)
        if device_info is None:
            return None
        return device_info["id"]

    def get_license_file(self, device_id: int) -> File:
        if device_id is None:
            return None

        r = self.__session.post(
            f"{self.url}", json={"devices": [device_id]}
        )
        if r.status_code == 200:
            response_dict = json.loads(r.content)

            if len(response_dict) < 1:
                return None

            license: File = File(response_dict["fileName"], response_dict["fileText"].encode("utf-8"))
            if license.file_name == None:
                return None

            return license
        else:
            raise LicenseError("Ошибка получения данный с сервера лицензий")
    
    
    def _is_feature(self, license_info, feature: Feature):
        for item in license_info['features']:
            if (
                item['id'] == feature.id and 
                item['activated'] and 
                item['licenseType'] == 1
            ):
                return True
            
        return False

    
    def is_include_feature(self, serialNumber, feature):
        device_info = self._get_device_info(serialNumber)
        if device_info is None:
            return None

        return self._is_feature(device_info, feature)


class LicenseError(Exception):
    pass
