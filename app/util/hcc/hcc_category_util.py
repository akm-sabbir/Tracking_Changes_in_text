import json
import os

from hccpy.hcc import HCCEngine

from app.util.config_manager import ConfigManager
from data import data_base_path


class HCCCategoryUtil:
    data = None
    hcc_engine = None

    def __init__(self):
        HCCCategoryUtil.data = None
        __hcc_version = ConfigManager.get_specific_config(section="hcc", key="version")
        HCCCategoryUtil.hcc_engine = HCCEngine(version=__hcc_version)

    @classmethod
    def get_hcc_category(cls, hcc: str) -> str:
        if cls.data is None:
            hcc_categories_filename = ConfigManager.get_specific_config(section="hcc", key="category_filename")
            file_path = os.path.join(os.path.join(data_base_path, hcc_categories_filename))
            json_file = open(file_path)
            cls.data = json.load(json_file)
        if hcc in cls.data:
            return cls.data[hcc]
        else:
            return cls.hcc_engine.describe_hcc(hcc)['description']
