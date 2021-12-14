from unittest import TestCase
from app.settings import Settings


class test_Settings(TestCase):

    def test_configuration_values_should_return_correct_output(self):
        Settings.set_settings_dx_threshold(0.9)
        Settings.set_settings_icd10_threshold(0.67)
        Settings.set_settings_use_cache(True)
        Settings.set_settings_parent_threshold(0.8)
        assert Settings.get_settings_dx_threshold() == 0.9
        assert Settings.get_settings_icd10_threshold() == 0.67
        assert Settings.get_settings_use_cache() == True
        assert Settings.get_settings_parent_threshold() == 0.8
