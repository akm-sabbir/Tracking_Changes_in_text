from unittest import TestCase
from unittest.mock import patch

from app.util.config_manager import ConfigManager


class MockConfigParser:
    config_sections = {'section': {'key': 'value'}}

    def read(self, filenames: str):
        return

    def sections(self):
        return self.config_sections

    def items(self, section: str):
        return self.config_sections[section]


class TestConfigManager(TestCase):

    @patch.object(ConfigManager, '_ConfigManager__config_parser', MockConfigParser())
    def test_initiate_config(self):
        ConfigManager.initiate_config()

    @patch.object(ConfigManager, '_ConfigManager__config_parser', MockConfigParser())
    def test_get_specific_config(self):
        ConfigManager.initiate_config()
        assert ConfigManager.get_config_section('section') == {'key': 'value'}

    @patch.object(ConfigManager, '_ConfigManager__config_parser', MockConfigParser())
    def test_get_config_section(self):
        ConfigManager.initiate_config()
        assert ConfigManager.get_specific_config('section', 'key') == 'value'
