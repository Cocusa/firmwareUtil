import os
from models.models import CommonException, File
from services.bitrix_api import download_folder
from services.device_registry import is_url_location
from services.win_helper import win_shell_copy
from urllib.parse import urlparse, parse_qs

def parse_bitrix_folder_id(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    query_params = parse_qs(parsed_url.query)

    if 'bitrix24' in domain and 'folderId' in query_params:
        return query_params['folderId'][0]
    else:
        raise CommonException('Неверный путь к файлам установки в реестре')

def copy_setup_files(src_location: str, dst_path: str):    
    if is_url_location(src_location):
        
        dir_id = parse_bitrix_folder_id(src_location)

        download_folder(dir_id, dst_path)
    else:
        dirs = []
        for x in os.listdir(src_location):
            dirs.append(os.path.join(src_location, x))

        if not win_shell_copy(dirs, dst_path):
           raise CommonException(f'Ошибка копирования файлов установки. Отсюда - {dirs}. Сюда - {dst_path}.') 


def save_file(file: File, dst_path: str):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path, exist_ok=True)
        
    with open(os.path.join(dst_path, file.file_name), "wb" if isinstance(file.file_content, bytes) else "w") as f:
        if isinstance(file.file_content, bytes):
            f.write(file.file_content)
        else:
            f.write(file.file_content)
