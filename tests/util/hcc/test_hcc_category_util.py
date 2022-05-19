from unittest import TestCase
from unittest.mock import patch, Mock

from app.util.hcc.hcc_category_util import HCCCategoryUtil


class TestHCCCategoryUtil(TestCase):
    data = None
    hcc_engine = None

    @patch("app.util.hcc.hcc_category_util.ConfigManager.get_specific_config")
    @patch("builtins.open")
    def test__get_hcc_category__should_retrun_correct_category__given_hcc_code(self, mock_file_open: Mock,
                                                                               mock_config: Mock):
        mock_config.side_effect = ["23", "file_name"]
        hcc_util = HCCCategoryUtil()
        hcc_util.get_hcc_category("HCC1")
