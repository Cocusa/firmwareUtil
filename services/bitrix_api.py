import json
import os
import re
import requests
from models.config_models import Feature


_features_foler = {
    'ID': 111,
    'NAME': 'Программное обеспечение'
}


def _make_load_subfolder_link(folder_id):
    return f'url?id={folder_id}'


def _load_subfolders(folder):
    url = _make_load_subfolder_link(folder['ID'])

    response = requests.get(url)
    response.raise_for_status()
    content = json.loads(response.content)
    return content['result']


def _is_file(file):
    return file['TYPE'] == 'file'


def download_file(url, dst_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        content_disposition = r.headers.get('Content-Disposition')
        file_name = re.findall("filename=\"(.+)\"", content_disposition)[0]
        file_path = os.path.join(dst_path, file_name)

        if not os.path.exists(dst_path):
            os.makedirs(dst_path, exist_ok=True)

        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_path


def download_folder(dir_id: int, dst_path):
    for file in _load_subfolders({'ID': dir_id}):
        if (_is_file(file)):
            download_file(file['DOWNLOAD_URL'], dst_path)
        else:
            download_folder(file["ID"], os.path.join(dst_path,file['NAME']))


def download_feature(feature: Feature, dst_path: str):
    responses_files = _load_subfolders(_features_foler)
    for file in responses_files:
        if (file["NAME"] == feature.bitrix_load_path):
            download_folder(file["ID"], os.path.join(dst_path, feature.flash_save_path))
