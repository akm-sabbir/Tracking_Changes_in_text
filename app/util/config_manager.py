import os
from configparser import ConfigParser

from app import app_base_path


class ConfigManager:
    __config_file_path: str = os.path.join(os.path.dirname(app_base_path), 'config.ini')
    __config_sections: dict = {}
    __config_parser: ConfigParser = ConfigParser()

    @classmethod
    def initiate_config(cls):
        cls.__config_parser.read(filenames=cls.__config_file_path)
        cls.__config_sections = {section: dict(cls.__config_parser.items(section))
                                 for section in cls.__config_parser.sections()}

    @classmethod
    def get_specific_config(cls, section: str, key: str) -> str:
        if cls.__config_sections == {}:
            raise KeyError("Initiate ConfigManager using ConfigManager.initiate_config() before using.")
        return cls.__config_sections[section][key]

    @classmethod
    def get_config_section(cls, section: str) -> dict:
        if cls.__config_sections == {}:
            raise KeyError("Initiate ConfigManager using ConfigManager.initiate_config() before using.")
        return cls.__config_sections[section]
