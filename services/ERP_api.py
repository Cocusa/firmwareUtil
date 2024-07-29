from datetime import date
import requests
import json
from base64 import b64encode
from models.models import (
    CommonException,
    Nomenclature,
    OrderInfo,
    LicenseInfo,
    FirmwareVersion,
)


class ERPApi:
    def __init__(self):
        self.url = "url"
        self.__session = requests.Session()
        self.__session.trust_env = False

    def connect(self, user_name, password):
        try:
            self.user_name = user_name
            self.password = password
            login_header = {
                "Authorization": f'Basic {self.encode_to_base64(self.user_name+":"+self.password)}'
            }
            self.__session.headers.update(login_header)
            result = self.__session.get(f"{self.url}api/login")

            if result.status_code == 401:
                raise AuthException("Неверный логин или пароль")

            if result.status_code != 200:
                raise Exception("Неизвестаня ошибка")
        except UnicodeEncodeError:
            raise AuthException("Неверный логин или пароль")

    def is_connect(self):
        result = self.__session.get(f"{self.url}api/login")
        return result.status_code == 200

    def encode_to_base64(self, str: str) -> str:
        message_bytes = str.encode("ascii")
        base64_bytes = b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        return base64_message

    def get_nomenclature(self, serialNumber: str) -> Nomenclature:
        r = self.__session.get(f"utl/{serialNumber}")
        if r.status_code == 200:
            response_dict = json.loads(r.content)
            if len(response_dict) < 1 or response_dict[0]["ID"] is None:
                return None

            return Nomenclature(response_dict[0]["ID"], response_dict[0]["NAME"])
        else:
            return None


    def get_bom_id(self, nom_id: int) -> int:
        r = self.__session.get(f"{self.url}/{nom_id}")
        if r.status_code != 200:
            raise CommonException("Не найдена номенклатура")
        
        return json.loads(r.content)['bomId']
    

    def get_bom_tree(self, bom_id: int):
        r = self.__session.get(f"{self.url}/{bom_id}")
        if r.status_code == 200:
            response_dict = json.loads(r.content)
            if len(response_dict) < 1 or response_dict[0]["id"] is None:
                raise CommonException("Не найдена номенклатура")

            return response_dict
        else:
            raise CommonException("Не найдена номенклатура")


    def get_order_info(self, serial_number: str) -> list[OrderInfo]:
        r = self.__session.get(
            f"{self.url}", params={"serial_number": serial_number}
        )
        if r.status_code == 200:
            response_dict = json.loads(r.content)
            if len(response_dict) < 1 or response_dict[0]["NOM_ID"] is None:
                return None

            orders_info = []
            for response in response_dict:
                orders_info.insert(
                    -1,
                    OrderInfo(
                        response["DOC_NUMBER"],
                        date.fromisoformat(response["ORDER_DATE"]),
                        Nomenclature(response["NOM_ID"], response["NOM_NAME"]),
                        LicenseInfo(response["IS_LICENSE"]),
                        FirmwareVersion(response["SOFTWARE_VERSION"]),
                    ),
                )

            return orders_info
        else:
            return None

    def get_vnapt_file_name(self, serial_number: str) -> str:
        r = self.__session.get(
            f"{self.url}", params={"number": serial_number}
        )
        if r.status_code == 200:
            response_dict = json.loads(r.content)
            if len(response_dict) < 1 or response_dict[0]["name"] is None:
                return None

            for response in response_dict:
                if ".prf" in str(response["name"]) and serial_number in str(response["name"]):
                    return response["name"]

            return None
        elif r.status_code == 404:
            return None
        else:
            raise CommonException("Ошибка получения данных ERP")

    def get_current_user_name(self) -> str:
        r = self.__session.get(f"{self.url}")
        if r.status_code == 200:
            response_dict = json.loads(r.content)
            if len(response_dict) < 1:
                return None

            return response_dict["user_name"]
        elif r.status_code == 404:
            return False
        else:
            raise CommonException("Ошибка получения данных ERP")
        

    def download_file(self, file_id):
        url = f"{self.url}/{file_id}"
        r = self.__session.get(url)
        if r.status_code == 200:
            return r.content
        elif r.status_code == 404:
            return None
        else:
            raise CommonException("Ошибка получения данныx ERP")
    
    def download_registry(self):
        registry_file_id = 111
        return self.download_file(registry_file_id)
    
    def download_config(self):
        config_file_id = 111
        return self.download_file(config_file_id)


class AuthException(Exception):
    pass
