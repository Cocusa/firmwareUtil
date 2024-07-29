from dataclasses import dataclass


@dataclass
class Feature:
    id: int
    name: str
    bitrix_load_path: str
    flash_save_path: str


@dataclass
class Config:
    license_features: list[Feature]