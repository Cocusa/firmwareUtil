import json

from models.config_models import Config, Feature


CONFIG_PATH = "config\\config.json"


def _load_config():
    with open(CONFIG_PATH, "r") as json_file:
        return json.load(json_file)
    
    
def get_config():
    data = _load_config()
    return Config(license_features=[Feature(**feature) for feature in data['license_features']])
